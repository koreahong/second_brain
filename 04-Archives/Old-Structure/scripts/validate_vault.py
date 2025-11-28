#!/usr/bin/env python3
"""
Obsidian Vault Validation Agent

검증 항목:
1. 네트워크 구조 (backlinks, forward links, orphan pages, hub pages)
2. 중복 체크 (제목, 내용, Notion ID)
3. 통합 여부 (Hub 연결 상태, 관련 문서 링크)
4. 발견 여부 (깨진 링크, 메타데이터 누락)
"""

import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import yaml

class VaultValidator:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.files = []
        self.links = defaultdict(set)  # file -> set of linked files
        self.backlinks = defaultdict(set)  # file -> set of files linking to it
        self.metadata = {}  # file -> metadata dict
        self.titles = {}  # file -> title
        self.notion_ids = {}  # notion_id -> file
        self.issues = {
            'orphans': [],
            'duplicates': [],
            'broken_links': [],
            'missing_metadata': [],
            'hub_issues': [],
            'similar_content': []
        }

    def scan_vault(self):
        """Scan all markdown files in vault"""
        print("📂 Scanning vault...")

        for md_file in self.vault_path.rglob('*.md'):
            # Skip template files
            if 'Templates' in md_file.parts:
                continue

            rel_path = md_file.relative_to(self.vault_path)
            self.files.append(rel_path)

            # Parse file
            self._parse_file(rel_path)

        print(f"✅ Found {len(self.files)} markdown files\n")

    def _parse_file(self, rel_path):
        """Parse single markdown file"""
        full_path = self.vault_path / rel_path

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Error reading {rel_path}: {e}")
            return

        # Extract frontmatter
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if frontmatter_match:
            try:
                metadata = yaml.safe_load(frontmatter_match.group(1))
                self.metadata[rel_path] = metadata or {}

                # Extract title
                if 'title' in metadata:
                    self.titles[rel_path] = metadata['title']

                # Extract notion_id
                if 'notion_id' in metadata:
                    notion_id = metadata['notion_id']
                    if notion_id in self.notion_ids:
                        # Duplicate Notion ID!
                        if 'duplicates' not in self.issues:
                            self.issues['duplicates'] = []
                        self.issues['duplicates'].append({
                            'type': 'notion_id',
                            'id': notion_id,
                            'files': [self.notion_ids[notion_id], rel_path]
                        })
                    else:
                        self.notion_ids[notion_id] = rel_path
            except yaml.YAMLError as e:
                self.issues['missing_metadata'].append({
                    'file': str(rel_path),
                    'issue': f'Invalid YAML: {e}'
                })
        else:
            self.issues['missing_metadata'].append({
                'file': str(rel_path),
                'issue': 'No frontmatter'
            })

        # Extract title from first h1 if not in metadata
        if rel_path not in self.titles:
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1_match:
                self.titles[rel_path] = h1_match.group(1)
            else:
                self.titles[rel_path] = rel_path.stem

        # Extract links [[...]]
        wiki_links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
        for link in wiki_links:
            # Clean link
            link = link.strip()
            self.links[rel_path].add(link)

    def build_backlinks(self):
        """Build backlink index"""
        print("🔗 Building backlink index...")

        for source_file, linked_files in self.links.items():
            for link in linked_files:
                # Find actual file for this link
                target_file = self._resolve_link(link)
                if target_file:
                    self.backlinks[target_file].add(source_file)
                else:
                    # Broken link
                    self.issues['broken_links'].append({
                        'source': str(source_file),
                        'broken_link': link
                    })

        print(f"✅ Built backlinks for {len(self.backlinks)} files\n")

    def _resolve_link(self, link):
        """Resolve wiki link to actual file path"""
        # Try exact match by title
        for file_path, title in self.titles.items():
            if title == link:
                return file_path

        # Try by filename (without extension)
        for file_path in self.files:
            if file_path.stem == link:
                return file_path

        # Try partial match
        link_lower = link.lower()
        for file_path in self.files:
            if link_lower in str(file_path).lower():
                return file_path

        return None

    def find_orphans(self):
        """Find orphan pages (no backlinks and not in hub)"""
        print("🔍 Finding orphan pages...")

        for file_path in self.files:
            # Skip README and index files
            if file_path.name in ['README.md', 'index.md']:
                continue

            # Check if has any backlinks
            if file_path not in self.backlinks or len(self.backlinks[file_path]) == 0:
                self.issues['orphans'].append(str(file_path))

        print(f"⚠️  Found {len(self.issues['orphans'])} orphan pages\n")

    def find_hubs(self):
        """Find hub pages (pages with many outgoing links)"""
        print("🌟 Analyzing hub pages...")

        hub_threshold = 5  # Pages linking to 5+ other pages
        hubs = {}

        for file_path, links in self.links.items():
            if len(links) >= hub_threshold:
                hubs[file_path] = len(links)

        print(f"✅ Found {len(hubs)} hub pages\n")
        return hubs

    def find_duplicate_titles(self):
        """Find duplicate titles"""
        print("🔍 Finding duplicate titles...")

        title_count = Counter(self.titles.values())
        duplicates = {title: count for title, count in title_count.items() if count > 1}

        for dup_title in duplicates:
            files_with_title = [str(f) for f, t in self.titles.items() if t == dup_title]
            self.issues['duplicates'].append({
                'type': 'title',
                'title': dup_title,
                'files': files_with_title
            })

        print(f"⚠️  Found {len(duplicates)} duplicate titles\n")

    def check_hub_coverage(self):
        """Check if files are properly linked in hub pages"""
        print("🔍 Checking hub coverage...")

        # Define expected hubs
        expected_hubs = {
            'Knowledge/Technology/Orchestration/Airflow-Hub.md',
            'Knowledge/Technology/Languages/Python/Python-Hub.md',
            'Experiences/Qraft/README.md'
        }

        for hub_name in expected_hubs:
            hub_path = Path(hub_name)

            # Check if hub exists
            if hub_path not in self.files:
                self.issues['hub_issues'].append({
                    'hub': str(hub_path),
                    'issue': 'Hub file does not exist'
                })
                continue

            # Find related files that should be linked in hub
            if 'Airflow' in str(hub_path):
                related_pattern = 'airflow'
            elif 'Python' in str(hub_path):
                related_pattern = 'python'
            elif 'Qraft' in str(hub_path):
                related_pattern = 'Qraft/Projects'
            else:
                continue

            # Find files matching pattern
            related_files = [f for f in self.files if related_pattern.lower() in str(f).lower()]

            # Check which ones are linked in hub
            hub_links = self.links.get(hub_path, set())

            # Find unlinked related files
            unlinked = []
            for rel_file in related_files:
                if rel_file == hub_path:  # Skip hub itself
                    continue

                # Check if file is linked in hub
                file_title = self.titles.get(rel_file, rel_file.stem)
                if file_title not in hub_links and rel_file.stem not in hub_links:
                    unlinked.append(str(rel_file))

            if unlinked:
                self.issues['hub_issues'].append({
                    'hub': str(hub_path),
                    'issue': f'{len(unlinked)} related files not linked in hub',
                    'files': unlinked[:5]  # Show first 5
                })

        print(f"✅ Hub coverage check complete\n")

    def generate_report(self):
        """Generate validation report"""
        print("\n" + "=" * 70)
        print("📊 VAULT VALIDATION REPORT")
        print("=" * 70)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Summary
        print("📈 Summary")
        print("-" * 70)
        print(f"Total files: {len(self.files)}")
        print(f"Total links: {sum(len(links) for links in self.links.values())}")
        print(f"Files with backlinks: {len(self.backlinks)}")
        print(f"Orphan pages: {len(self.issues['orphans'])}")
        print(f"Broken links: {len(self.issues['broken_links'])}")
        print(f"Duplicate titles: {len([d for d in self.issues['duplicates'] if d['type'] == 'title'])}")
        print(f"Missing metadata: {len(self.issues['missing_metadata'])}\n")

        # Network Analysis
        print("🕸️  Network Analysis")
        print("-" * 70)

        # Top connected pages (most backlinks)
        top_connected = sorted(
            [(f, len(bl)) for f, bl in self.backlinks.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]

        print("Top 10 most referenced pages:")
        for file_path, count in top_connected:
            title = self.titles.get(file_path, file_path.stem)
            print(f"  • {title}: {count} backlinks")
        print()

        # Hub pages
        hubs = self.find_hubs()
        if hubs:
            print("Hub pages (5+ outgoing links):")
            for hub_path, link_count in sorted(hubs.items(), key=lambda x: x[1], reverse=True)[:10]:
                title = self.titles.get(hub_path, hub_path.stem)
                print(f"  • {title}: {link_count} links")
        print()

        # Issues
        if self.issues['orphans']:
            print("⚠️  Orphan Pages (no backlinks)")
            print("-" * 70)
            for orphan in self.issues['orphans'][:20]:
                print(f"  • {orphan}")
            if len(self.issues['orphans']) > 20:
                print(f"  ... and {len(self.issues['orphans']) - 20} more")
            print()

        if self.issues['broken_links']:
            print("❌ Broken Links")
            print("-" * 70)
            for broken in self.issues['broken_links'][:20]:
                print(f"  • {broken['source']} → [[{broken['broken_link']}]]")
            if len(self.issues['broken_links']) > 20:
                print(f"  ... and {len(self.issues['broken_links']) - 20} more")
            print()

        if self.issues['duplicates']:
            print("🔄 Duplicates")
            print("-" * 70)
            for dup in self.issues['duplicates']:
                if dup['type'] == 'title':
                    print(f"  • Duplicate title: '{dup['title']}'")
                    for f in dup['files']:
                        print(f"    - {f}")
                elif dup['type'] == 'notion_id':
                    print(f"  • Duplicate Notion ID: {dup['id']}")
                    for f in dup['files']:
                        print(f"    - {f}")
            print()

        if self.issues['hub_issues']:
            print("🌟 Hub Coverage Issues")
            print("-" * 70)
            for issue in self.issues['hub_issues']:
                print(f"  • {issue['hub']}: {issue['issue']}")
                if 'files' in issue:
                    for f in issue['files']:
                        print(f"    - {f}")
            print()

        if self.issues['missing_metadata']:
            print("📝 Missing/Invalid Metadata")
            print("-" * 70)
            for issue in self.issues['missing_metadata'][:20]:
                print(f"  • {issue['file']}: {issue['issue']}")
            if len(self.issues['missing_metadata']) > 20:
                print(f"  ... and {len(self.issues['missing_metadata']) - 20} more")
            print()

        # Recommendations
        print("💡 Recommendations")
        print("-" * 70)

        if self.issues['orphans']:
            print(f"1. Link {len(self.issues['orphans'])} orphan pages to relevant hub pages")

        if self.issues['broken_links']:
            print(f"2. Fix {len(self.issues['broken_links'])} broken links")

        if self.issues['duplicates']:
            dup_titles = len([d for d in self.issues['duplicates'] if d['type'] == 'title'])
            if dup_titles:
                print(f"3. Resolve {dup_titles} duplicate titles by renaming or merging")

        if self.issues['missing_metadata']:
            print(f"4. Add metadata to {len(self.issues['missing_metadata'])} files")

        if not any([self.issues['orphans'], self.issues['broken_links'],
                   self.issues['duplicates'], self.issues['missing_metadata']]):
            print("✅ Vault is in excellent shape! No major issues found.")

        print("\n" + "=" * 70)

    def save_report_json(self, output_file='vault_validation_report.json'):
        """Save detailed report as JSON"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_files': len(self.files),
                'total_links': sum(len(links) for links in self.links.values()),
                'files_with_backlinks': len(self.backlinks),
                'orphan_count': len(self.issues['orphans']),
                'broken_link_count': len(self.issues['broken_links']),
                'duplicate_count': len(self.issues['duplicates']),
                'missing_metadata_count': len(self.issues['missing_metadata'])
            },
            'issues': self.issues,
            'network': {
                'backlinks': {str(k): [str(v) for v in vals] for k, vals in self.backlinks.items()},
                'forward_links': {str(k): list(v) for k, v in self.links.items()}
            }
        }

        output_path = self.vault_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Detailed report saved to: {output_path}")

def main():
    vault_path = Path(__file__).parent

    print("🔍 DAE Second Brain Vault Validator")
    print("=" * 70)
    print()

    validator = VaultValidator(vault_path)

    # Run validation
    validator.scan_vault()
    validator.build_backlinks()
    validator.find_orphans()
    validator.find_duplicate_titles()
    validator.check_hub_coverage()

    # Generate reports
    validator.generate_report()
    validator.save_report_json()

    print("\n✅ Validation complete!")

if __name__ == '__main__':
    main()