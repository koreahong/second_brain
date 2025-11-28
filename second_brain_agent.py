#!/usr/bin/env python3
"""
Second Brain Curator Agent

목표: 문서들이 적절하게 발견되고 연결되어 Second Brain이 제 역할을 하도록 함

주요 기능:
1. 검증 (Validation) - 현재 상태 분석
2. 정리 (Cleanup) - 문제 자동 해결
3. 강화 (Enhancement) - 발견성과 연결성 향상
4. 모니터링 (Monitoring) - 지속적 품질 관리
"""

import re
import json
import yaml
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import difflib

class SecondBrainAgent:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.files = []
        self.links = defaultdict(set)
        self.backlinks = defaultdict(set)
        self.metadata = {}
        self.titles = {}
        self.content_cache = {}

        # Enhancement tracking
        self.suggestions = {
            'link_suggestions': [],
            'hub_suggestions': [],
            'tag_suggestions': [],
            'content_improvements': []
        }

    def scan_vault(self):
        """Scan all markdown files"""
        print("📂 Scanning vault...")

        for md_file in self.vault_path.rglob('*.md'):
            if 'Templates' in md_file.parts:
                continue

            rel_path = md_file.relative_to(self.vault_path)
            self.files.append(rel_path)
            self._parse_file(rel_path)

        print(f"✅ Scanned {len(self.files)} files\n")

    def _parse_file(self, rel_path):
        """Parse file and extract metadata, links, content"""
        full_path = self.vault_path / rel_path

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return

        # Store content for similarity analysis
        self.content_cache[rel_path] = content

        # Extract frontmatter
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if fm_match:
            try:
                metadata = yaml.safe_load(fm_match.group(1))
                self.metadata[rel_path] = metadata or {}

                if 'title' in metadata:
                    self.titles[rel_path] = metadata['title']
            except:
                pass

        # Extract title from h1 if not in metadata
        if rel_path not in self.titles:
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1_match:
                self.titles[rel_path] = h1_match.group(1)
            else:
                self.titles[rel_path] = rel_path.stem

        # Extract links
        wiki_links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
        for link in wiki_links:
            self.links[rel_path].add(link.strip())

    def build_graph(self):
        """Build knowledge graph with backlinks"""
        print("🕸️  Building knowledge graph...")

        for source, links in self.links.items():
            for link in links:
                target = self._resolve_link(link)
                if target:
                    self.backlinks[target].add(source)

        print(f"✅ Built graph with {len(self.backlinks)} connected nodes\n")

    def _resolve_link(self, link):
        """Resolve wiki link to file path"""
        # Try by title
        for file_path, title in self.titles.items():
            if title == link:
                return file_path

        # Try by filename
        for file_path in self.files:
            if file_path.stem == link:
                return file_path

        # Partial match
        link_lower = link.lower()
        for file_path in self.files:
            if link_lower in str(file_path).lower():
                return file_path

        return None

    def analyze_discoverability(self):
        """Analyze how discoverable each file is"""
        print("🔍 Analyzing discoverability...\n")

        scores = {}

        for file_path in self.files:
            score = 0
            issues = []

            # 1. Has backlinks (most important)
            backlink_count = len(self.backlinks.get(file_path, []))
            if backlink_count == 0:
                issues.append("No backlinks (orphan)")
                score -= 10
            else:
                score += min(backlink_count * 2, 20)  # Cap at 20

            # 2. Has outgoing links (connected)
            outlink_count = len(self.links.get(file_path, []))
            if outlink_count == 0:
                issues.append("No outgoing links (isolated)")
                score -= 5
            else:
                score += min(outlink_count, 10)  # Cap at 10

            # 3. Has metadata
            if file_path not in self.metadata:
                issues.append("Missing metadata")
                score -= 5
            else:
                metadata = self.metadata[file_path]

                # Has tags
                if 'tags' in metadata and metadata['tags']:
                    score += 5
                else:
                    issues.append("No tags")

                # Has type
                if 'type' not in metadata:
                    issues.append("No type")
                    score -= 3

            # 4. Content quality
            content = self.content_cache.get(file_path, '')
            content_no_fm = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
            content_length = len(content_no_fm.strip())

            if content_length < 100:
                issues.append("Very short content")
                score -= 5
            elif content_length > 1000:
                score += 5

            # 5. In a hub
            in_hub = self._is_in_hub(file_path)
            if not in_hub:
                issues.append("Not linked in any hub")
                score -= 8
            else:
                score += 10

            scores[file_path] = {
                'score': score,
                'backlinks': backlink_count,
                'outlinks': outlink_count,
                'issues': issues,
                'in_hub': in_hub
            }

        # Find files with low discoverability
        low_score_files = [(f, s) for f, s in scores.items() if s['score'] < 0]
        low_score_files.sort(key=lambda x: x[1]['score'])

        print(f"📊 Discoverability Analysis:")
        print(f"  Total files: {len(self.files)}")
        print(f"  Well-connected: {len([s for s in scores.values() if s['score'] >= 10])}")
        print(f"  Needs improvement: {len([s for s in scores.values() if 0 <= s['score'] < 10])}")
        print(f"  Poorly discoverable: {len(low_score_files)}")

        if low_score_files:
            print(f"\n  Top 10 least discoverable files:")
            for file_path, score_data in low_score_files[:10]:
                title = self.titles.get(file_path, file_path.stem)
                print(f"    • {title} (score: {score_data['score']})")
                for issue in score_data['issues'][:3]:
                    print(f"      - {issue}")

        print()
        return scores

    def _is_in_hub(self, file_path):
        """Check if file is linked in a hub page"""
        # Find hub pages
        hub_pages = [f for f in self.files if 'Hub' in str(f) or 'README' in str(f)]

        for hub in hub_pages:
            if file_path in [self._resolve_link(link) for link in self.links.get(hub, [])]:
                return True
        return False

    def suggest_links(self):
        """Suggest potential links between related documents"""
        print("🔗 Analyzing potential connections...\n")

        suggestions = []

        for file1 in self.files:
            content1 = self.content_cache.get(file1, '')
            title1 = self.titles.get(file1, file1.stem)

            # Skip very short files
            if len(content1) < 200:
                continue

            # Find files with similar content
            for file2 in self.files:
                if file1 == file2:
                    continue

                # Skip if already linked
                if self._resolve_link(self.titles.get(file2, '')) in self.links.get(file1, []):
                    continue

                content2 = self.content_cache.get(file2, '')
                title2 = self.titles.get(file2, file2.stem)

                # Check if title2 appears in content1
                if title2.lower() in content1.lower():
                    suggestions.append({
                        'from': file1,
                        'to': file2,
                        'reason': f'"{title2}" mentioned in content',
                        'confidence': 'high'
                    })

                # Check for keyword overlap
                keywords1 = self._extract_keywords(content1)
                keywords2 = self._extract_keywords(content2)

                overlap = keywords1 & keywords2
                if len(overlap) >= 3:  # At least 3 common keywords
                    suggestions.append({
                        'from': file1,
                        'to': file2,
                        'reason': f'Common keywords: {", ".join(list(overlap)[:3])}',
                        'confidence': 'medium'
                    })

        # Remove duplicates
        seen = set()
        unique_suggestions = []
        for s in suggestions:
            key = (s['from'], s['to'])
            if key not in seen:
                seen.add(key)
                unique_suggestions.append(s)

        self.suggestions['link_suggestions'] = unique_suggestions[:50]  # Top 50

        print(f"  Found {len(unique_suggestions)} potential connections")
        if unique_suggestions:
            print(f"\n  Top 10 suggestions:")
            for s in unique_suggestions[:10]:
                from_title = self.titles.get(s['from'], s['from'].stem)
                to_title = self.titles.get(s['to'], s['to'].stem)
                print(f"    • {from_title} → {to_title}")
                print(f"      Reason: {s['reason']} ({s['confidence']})")

        print()

    def _extract_keywords(self, content):
        """Extract important keywords from content"""
        # Remove frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

        # Common Korean/English stopwords
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     '은', '는', '이', '가', '을', '를', '에', '의', '와', '과', '도'}

        # Extract words (Korean + English)
        words = re.findall(r'[가-힣a-zA-Z]{2,}', content.lower())

        # Count frequency
        word_count = Counter(words)

        # Remove stopwords and get top keywords
        keywords = {word for word, count in word_count.most_common(20)
                   if word not in stopwords and count >= 2}

        return keywords

    def suggest_hubs(self):
        """Suggest creating hub pages for clusters of related documents"""
        print("🌟 Analyzing clusters for hub creation...\n")

        # Group files by directory
        clusters = defaultdict(list)

        for file_path in self.files:
            # Skip existing hubs
            if 'Hub' in str(file_path) or 'README' in str(file_path):
                continue

            # Group by parent directory
            parent = file_path.parent
            clusters[parent].append(file_path)

        # Find clusters without hubs
        suggestions = []

        for directory, files in clusters.items():
            if len(files) < 3:  # Skip small clusters
                continue

            # Check if hub exists
            hub_exists = any('Hub' in f.stem or 'README' in f.stem
                           for f in (self.vault_path / directory).glob('*.md'))

            if not hub_exists:
                suggestions.append({
                    'directory': directory,
                    'file_count': len(files),
                    'suggested_name': f"{directory.name}-Hub.md",
                    'files': files[:10]  # Sample
                })

        self.suggestions['hub_suggestions'] = suggestions

        print(f"  Found {len(suggestions)} clusters without hubs")
        if suggestions:
            print(f"\n  Suggestions:")
            for s in suggestions[:5]:
                print(f"    • Create {s['suggested_name']} for {s['file_count']} files")
                print(f"      Directory: {s['directory']}")

        print()

    def generate_report(self, output_file='second_brain_report.md'):
        """Generate comprehensive Second Brain report"""
        print(f"📝 Generating comprehensive report...\n")

        report = f"""# Second Brain Health Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 Overview

- **Total Documents**: {len(self.files)}
- **Total Links**: {sum(len(links) for links in self.links.values())}
- **Connected Nodes**: {len(self.backlinks)}
- **Orphan Pages**: {len([f for f in self.files if f not in self.backlinks])}

---

## 🔗 Link Suggestions ({len(self.suggestions['link_suggestions'])})

These connections would improve discoverability:

"""

        for s in self.suggestions['link_suggestions'][:20]:
            from_title = self.titles.get(s['from'], s['from'].stem)
            to_title = self.titles.get(s['to'], s['to'].stem)
            report += f"### {from_title} → {to_title}\n\n"
            report += f"- **Confidence**: {s['confidence']}\n"
            report += f"- **Reason**: {s['reason']}\n"
            report += f"- **Files**: `{s['from']}` → `{s['to']}`\n\n"

        report += "\n---\n\n"
        report += f"## 🌟 Hub Suggestions ({len(self.suggestions['hub_suggestions'])})\n\n"

        for s in self.suggestions['hub_suggestions'][:10]:
            report += f"### {s['suggested_name']}\n\n"
            report += f"- **Directory**: `{s['directory']}`\n"
            report += f"- **Files to link**: {s['file_count']}\n"
            report += f"- **Sample files**:\n"
            for f in s['files'][:5]:
                title = self.titles.get(f, f.stem)
                report += f"  - [[{f}|{title}]]\n"
            report += "\n"

        # Save report
        report_path = self.vault_path / output_file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✅ Report saved to: {report_path}\n")

    def auto_enhance(self, dry_run=True):
        """Automatically enhance Second Brain with high-confidence suggestions"""
        print("🚀 Auto-enhancing Second Brain...\n")

        enhancements = []

        # 1. Add high-confidence links
        high_conf_links = [s for s in self.suggestions['link_suggestions']
                          if s['confidence'] == 'high']

        print(f"  Found {len(high_conf_links)} high-confidence link suggestions")

        if not dry_run and high_conf_links:
            for link_suggestion in high_conf_links[:10]:  # Limit to 10
                self._add_link_to_file(
                    link_suggestion['from'],
                    link_suggestion['to']
                )
                enhancements.append(f"Added link: {link_suggestion['from']} → {link_suggestion['to']}")

        # 2. Create missing hubs for large clusters
        large_clusters = [s for s in self.suggestions['hub_suggestions']
                         if s['file_count'] >= 5]

        print(f"  Found {len(large_clusters)} large clusters without hubs")

        if not dry_run and large_clusters:
            for hub_suggestion in large_clusters[:3]:  # Limit to 3
                self._create_hub_page(hub_suggestion)
                enhancements.append(f"Created hub: {hub_suggestion['suggested_name']}")

        if dry_run:
            print(f"\n  ℹ️  DRY RUN - would make {len(high_conf_links[:10]) + len(large_clusters[:3])} enhancements")
        else:
            print(f"\n  ✅ Made {len(enhancements)} enhancements")

        return enhancements

    def _add_link_to_file(self, from_file, to_file):
        """Add a link from one file to another"""
        from_path = self.vault_path / from_file
        to_title = self.titles.get(to_file, to_file.stem)

        with open(from_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add link in a "Related" section at the end
        if '## 🔗 Related' not in content:
            content += f"\n\n## 🔗 Related\n\n- [[{to_file}|{to_title}]]\n"
        else:
            # Append to existing Related section
            content = content.replace(
                '## 🔗 Related\n\n',
                f'## 🔗 Related\n\n- [[{to_file}|{to_title}]]\n'
            )

        with open(from_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _create_hub_page(self, hub_suggestion):
        """Create a hub page for a cluster"""
        hub_path = self.vault_path / hub_suggestion['directory'] / hub_suggestion['suggested_name']

        hub_name = hub_suggestion['suggested_name'].replace('-Hub.md', '').replace('_', ' ')

        content = f"""---
type: hub
category: {hub_suggestion['directory'].name}
created: {datetime.now().strftime('%Y-%m-%d')}
---

# {hub_name} Hub

## 📚 Documents ({hub_suggestion['file_count']})

"""

        for file_path in hub_suggestion['files']:
            title = self.titles.get(file_path, file_path.stem)
            content += f"- [[{file_path}|{title}]]\n"

        content += "\n---\n\n*Auto-generated hub page*\n"

        with open(hub_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def run(self, auto_enhance=False, dry_run=True):
        """Run complete Second Brain curation"""
        print("=" * 70)
        print("🧠 Second Brain Curator Agent")
        print("=" * 70)
        print()

        # 1. Scan
        self.scan_vault()

        # 2. Build graph
        self.build_graph()

        # 3. Analyze discoverability
        scores = self.analyze_discoverability()

        # 4. Generate suggestions
        self.suggest_links()
        self.suggest_hubs()

        # 5. Generate report
        self.generate_report()

        # 6. Auto-enhance (if requested)
        if auto_enhance:
            enhancements = self.auto_enhance(dry_run=dry_run)

        print("=" * 70)
        print("✅ Second Brain curation complete!")
        print("=" * 70)
        print()
        print("📄 Check second_brain_report.md for detailed suggestions")
        print()

def main():
    import sys

    vault_path = Path(__file__).parent
    dry_run = '--apply' not in sys.argv
    auto_enhance = '--enhance' in sys.argv

    agent = SecondBrainAgent(vault_path)
    agent.run(auto_enhance=auto_enhance, dry_run=dry_run)

if __name__ == '__main__':
    main()
