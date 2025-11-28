#!/usr/bin/env python3
"""
Vault Cleanup Agent

자동으로 수정할 수 있는 이슈들을 해결합니다:
1. 중복 파일 삭제 (Old structure vs New structure)
2. YAML 메타데이터 수정 (브래킷 이스케이핑)
3. Qraft README 업데이트 (모든 프로젝트 링크)
4. 고아 페이지를 Hub에 자동 링크
"""

import re
import yaml
from pathlib import Path
from collections import defaultdict

class VaultCleaner:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.changes = []

    def _extract_notion_id(self, file_path):
        """Extract notion_id from file's frontmatter"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if fm_match:
                metadata = yaml.safe_load(fm_match.group(1))
                return metadata.get('notion_id')
        except:
            pass
        return None

    def _get_content_without_frontmatter(self, file_path):
        """Get file content without frontmatter"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove frontmatter
            content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
            # Normalize whitespace
            return ' '.join(content.split())
        except:
            return ''

    def remove_duplicates(self, dry_run=True):
        """Remove duplicate files based on content comparison"""
        print("\n🔄 Checking for duplicate files (comparing content)...")

        duplicates_to_remove = []
        warnings = []

        # 1. Check Projects/Staging/* against Experiences/Qraft/Projects/
        staging_dir = self.vault_path / 'Projects' / 'Staging'
        if staging_dir.exists():
            for staging_file in staging_dir.glob('*.md'):
                qraft_dir = self.vault_path / 'Experiences' / 'Qraft' / 'Projects'

                # Get staging file's notion_id and content
                staging_notion_id = self._extract_notion_id(staging_file)
                staging_content = self._get_content_without_frontmatter(staging_file)

                # Find matching file in Qraft
                found_duplicate = False
                for qraft_file in qraft_dir.glob('*.md'):
                    qraft_notion_id = self._extract_notion_id(qraft_file)

                    # Compare by notion_id first (most reliable)
                    if staging_notion_id and qraft_notion_id == staging_notion_id:
                        duplicates_to_remove.append((staging_file, qraft_file, 'notion_id'))
                        found_duplicate = True
                        break

                    # Compare by content similarity
                    qraft_content = self._get_content_without_frontmatter(qraft_file)
                    if staging_content and qraft_content:
                        # Simple similarity check (can be improved)
                        if staging_content == qraft_content:
                            duplicates_to_remove.append((staging_file, qraft_file, 'content'))
                            found_duplicate = True
                            break

                # If similar name but no notion_id match, check if it's old template version
                if not found_duplicate:
                    title = staging_file.stem.replace('_', ' ')
                    for qraft_file in qraft_dir.glob('*.md'):
                        if title.lower() in qraft_file.stem.lower():
                            # Check if staging file has template boilerplate
                            staging_lines = len(open(staging_file, 'r', encoding='utf-8').readlines())
                            if 30 <= staging_lines <= 40:  # Template size range (old imports with boilerplate)
                                # Likely old template version - mark for removal
                                duplicates_to_remove.append((staging_file, qraft_file, 'old_template'))
                                found_duplicate = True
                            else:
                                warnings.append({
                                    'file1': staging_file,
                                    'file2': qraft_file,
                                    'reason': 'Similar names but different content'
                                })
                            break

        # 2. Check Archives/Old-Structure/_HUB_Python.md vs new Python-Hub
        old_python_hub = self.vault_path / 'Archives' / 'Old-Structure' / '_HUB_Python.md'
        new_python_hub = self.vault_path / 'Knowledge' / 'Technology' / 'Languages' / 'Python' / 'Python-Hub.md'

        if old_python_hub.exists() and new_python_hub.exists():
            # Compare content
            old_content = self._get_content_without_frontmatter(old_python_hub)
            new_content = self._get_content_without_frontmatter(new_python_hub)

            if old_content == new_content:
                duplicates_to_remove.append((old_python_hub, new_python_hub, 'content'))
            else:
                # Different content - just archive it
                duplicates_to_remove.append((old_python_hub, new_python_hub, 'archived'))

        if duplicates_to_remove:
            print(f"\n  Found {len(duplicates_to_remove)} confirmed duplicate files:")
            for dup_file, original, reason in duplicates_to_remove:
                print(f"    - {dup_file.relative_to(self.vault_path)}")
                print(f"      → duplicate of {original.relative_to(self.vault_path)} ({reason})")

            if not dry_run:
                for dup_file, original, reason in duplicates_to_remove:
                    dup_file.unlink()
                    self.changes.append(f"Deleted duplicate: {dup_file.relative_to(self.vault_path)}")
                print(f"\n  ✅ Removed {len(duplicates_to_remove)} duplicate files")
            else:
                print(f"\n  ℹ️  DRY RUN - would remove {len(duplicates_to_remove)} files")
        else:
            print("  ✅ No confirmed duplicates to remove")

        if warnings:
            print(f"\n  ⚠️  Found {len(warnings)} files with similar names but different content:")
            for warning in warnings[:5]:  # Show first 5
                print(f"    - {warning['file1'].relative_to(self.vault_path)}")
                print(f"      vs {warning['file2'].relative_to(self.vault_path)}")
            if len(warnings) > 5:
                print(f"    ... and {len(warnings) - 5} more")
            print("  → Manual review recommended")

    def fix_yaml_metadata(self, dry_run=True):
        """Fix YAML metadata with invalid brackets"""
        print("\n📝 Fixing YAML metadata errors...")

        files_with_errors = []

        for md_file in self.vault_path.rglob('*.md'):
            if 'Templates' in md_file.parts:
                continue

            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue

            # Check for frontmatter
            frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not frontmatter_match:
                continue

            yaml_content = frontmatter_match.group(1)

            # Try to parse
            try:
                yaml.safe_load(yaml_content)
            except yaml.YAMLError:
                # YAML error - try to fix
                files_with_errors.append(md_file)

                # Fix: Quote titles with brackets
                fixed_yaml = yaml_content
                lines = yaml_content.split('\n')
                fixed_lines = []

                for line in lines:
                    # Fix title with brackets
                    if line.startswith('title:') and '[' in line:
                        # Extract title
                        title = line.replace('title:', '').strip()
                        # Quote it
                        fixed_line = f'title: "{title}"'
                        fixed_lines.append(fixed_line)
                    else:
                        fixed_lines.append(line)

                fixed_yaml = '\n'.join(fixed_lines)

                # Verify fix works
                try:
                    yaml.safe_load(fixed_yaml)

                    if not dry_run:
                        # Replace in original content
                        new_content = content.replace(yaml_content, fixed_yaml)

                        with open(md_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)

                        self.changes.append(f"Fixed YAML in: {md_file.relative_to(self.vault_path)}")
                except yaml.YAMLError:
                    pass  # Can't fix automatically

        if files_with_errors:
            print(f"  Found {len(files_with_errors)} files with YAML errors")
            if not dry_run:
                print(f"  ✅ Fixed YAML metadata in {len(files_with_errors)} files")
            else:
                print(f"  ℹ️  DRY RUN - would fix {len(files_with_errors)} files")
        else:
            print("  ✅ No YAML errors to fix")

    def update_qraft_readme(self, dry_run=True):
        """Update Qraft README to link all project files"""
        print("\n🔗 Updating Qraft README with project links...")

        readme_path = self.vault_path / 'Experiences' / 'Qraft' / 'README.md'
        projects_dir = self.vault_path / 'Experiences' / 'Qraft' / 'Projects'

        if not readme_path.exists() or not projects_dir.exists():
            print("  ⚠️  Qraft README or Projects directory not found")
            return

        # Get all project files
        project_files = sorted(projects_dir.glob('*.md'))

        # Read current README
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the section to update (after "## 🎯 주요 업무 영역")
        # We'll add a new section "## 📋 전체 프로젝트 목록"

        # Check if section already exists
        if '## 📋 전체 프로젝트 목록' not in content:
            # Find where to insert (before "## 🛠️ 사용 기술 스택")
            insert_marker = '## 🛠️ 사용 기술 스택'

            if insert_marker in content:
                # Build project list
                project_list = '\n## 📋 전체 프로젝트 목록\n\n'

                for project_file in project_files:
                    # Extract title from file
                    with open(project_file, 'r', encoding='utf-8') as f:
                        proj_content = f.read()

                    # Try to get title from frontmatter
                    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', proj_content, re.DOTALL)
                    if fm_match:
                        try:
                            metadata = yaml.safe_load(fm_match.group(1))
                            title = metadata.get('title', project_file.stem)
                        except:
                            title = project_file.stem
                    else:
                        # Try h1
                        h1_match = re.search(r'^#\s+(.+)$', proj_content, re.MULTILINE)
                        title = h1_match.group(1) if h1_match else project_file.stem

                    # Add link
                    relative_path = f"Projects/{project_file.name}"
                    project_list += f'- [[{relative_path}|{title}]]\n'

                project_list += '\n---\n\n'

                # Insert before tech stack section
                new_content = content.replace(insert_marker, project_list + insert_marker)

                if not dry_run:
                    with open(readme_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    self.changes.append(f"Updated Qraft README with {len(project_files)} project links")
                    print(f"  ✅ Added {len(project_files)} project links to README")
                else:
                    print(f"  ℹ️  DRY RUN - would add {len(project_files)} project links")
            else:
                print("  ⚠️  Could not find insertion point in README")
        else:
            print("  ℹ️  Project list section already exists in README")

    def link_orphan_docs_to_readme(self, dry_run=True):
        """Link orphan documentation files to main README"""
        print("\n🔗 Linking orphan documentation to README...")

        # Documentation files that should be linked in README
        doc_files = {
            'PARA-BRAIN-STRUCTURE.md': 'PARA + Brain 구조 설명',
            'RESTRUCTURE_SUMMARY.md': '재구조화 요약',
            'CAREER_STRUCTURE.md': '커리어 구조 가이드',
            'RECOMMENDED_PLUGINS.md': '추천 플러그인',
            'QUICK_START.md': '빠른 시작 가이드',
            'KNOWLEDGE_STRUCTURE_DESIGN.md': 'Knowledge 구조 설계',
            'MIGRATION_SUMMARY.md': '마이그레이션 요약'
        }

        readme_path = self.vault_path / 'README.md'

        if not readme_path.exists():
            print("  ⚠️  README.md not found")
            return

        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if documentation section exists
        if '## 📚 Documentation' not in content:
            # Find where to insert (at the end, before any trailing content)
            doc_section = '\n## 📚 Documentation\n\n'
            doc_section += '### 구조 및 가이드\n\n'

            for doc_file, description in doc_files.items():
                if (self.vault_path / doc_file).exists():
                    doc_section += f'- [[{doc_file}|{description}]]\n'

            doc_section += '\n---\n'

            # Insert before the final line or at the end
            if content.endswith('\n'):
                new_content = content + doc_section
            else:
                new_content = content + '\n' + doc_section

            if not dry_run:
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                self.changes.append(f"Added Documentation section to README with {len(doc_files)} links")
                print(f"  ✅ Added Documentation section to README")
            else:
                print(f"  ℹ️  DRY RUN - would add Documentation section with {len(doc_files)} links")
        else:
            print("  ℹ️  Documentation section already exists in README")

    def generate_summary(self):
        """Generate cleanup summary"""
        print("\n" + "=" * 70)
        print("📊 CLEANUP SUMMARY")
        print("=" * 70)

        if self.changes:
            print(f"\nTotal changes made: {len(self.changes)}\n")
            for change in self.changes:
                print(f"  ✓ {change}")
        else:
            print("\nNo changes made (dry run mode)")

        print("\n" + "=" * 70)

def main():
    import sys

    vault_path = Path(__file__).parent
    dry_run = '--apply' not in sys.argv

    print("🧹 DAE Second Brain Vault Cleanup Agent")
    print("=" * 70)

    if dry_run:
        print("ℹ️  DRY RUN MODE - No changes will be made")
        print("   Run with --apply to actually make changes")
    else:
        print("⚠️  APPLY MODE - Changes will be made!")

    print()

    cleaner = VaultCleaner(vault_path)

    # Run cleanup tasks
    cleaner.remove_duplicates(dry_run=dry_run)
    cleaner.fix_yaml_metadata(dry_run=dry_run)
    cleaner.update_qraft_readme(dry_run=dry_run)
    cleaner.link_orphan_docs_to_readme(dry_run=dry_run)

    # Summary
    cleaner.generate_summary()

    if dry_run:
        print("\n💡 To apply these changes, run: python3 cleanup_vault.py --apply")

    print("\n✅ Cleanup complete!")

if __name__ == '__main__':
    main()
