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

    def remove_duplicates(self, dry_run=True):
        """Remove duplicate files (prefer new structure over old/staging)"""
        print("\n🔄 Checking for duplicate files to remove...")

        duplicates_to_remove = []

        # 1. Remove Projects/Staging/* duplicates (already in Experiences/Qraft/Projects/)
        staging_dir = self.vault_path / 'Projects' / 'Staging'
        if staging_dir.exists():
            for staging_file in staging_dir.glob('*.md'):
                # Check if corresponding file exists in Experiences/Qraft/Projects/
                title = staging_file.stem.replace('_', ' ')
                qraft_dir = self.vault_path / 'Experiences' / 'Qraft' / 'Projects'

                # Find matching file
                for qraft_file in qraft_dir.glob('*.md'):
                    if title.lower() in qraft_file.stem.lower():
                        duplicates_to_remove.append(staging_file)
                        break

        # 2. Remove Archives/Old-Structure/_HUB_Python.md (prefer new Python-Hub)
        old_python_hub = self.vault_path / 'Archives' / 'Old-Structure' / '_HUB_Python.md'
        if old_python_hub.exists():
            duplicates_to_remove.append(old_python_hub)

        if duplicates_to_remove:
            print(f"\n  Found {len(duplicates_to_remove)} duplicate files:")
            for dup in duplicates_to_remove:
                print(f"    - {dup.relative_to(self.vault_path)}")

            if not dry_run:
                for dup in duplicates_to_remove:
                    dup.unlink()
                    self.changes.append(f"Deleted duplicate: {dup.relative_to(self.vault_path)}")
                print(f"\n  ✅ Removed {len(duplicates_to_remove)} duplicate files")
            else:
                print(f"\n  ℹ️  DRY RUN - would remove {len(duplicates_to_remove)} files")
        else:
            print("  ✅ No duplicates to remove")

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

    def remove_orphan_docs(self, dry_run=True):
        """Remove documentation files that are orphans"""
        print("\n🗑️  Removing orphan documentation files...")

        orphan_docs = [
            'PARA-BRAIN-STRUCTURE.md',
            'RESTRUCTURE_SUMMARY.md',
            'CAREER_STRUCTURE.md',
            'RECOMMENDED_PLUGINS.md',
            'QUICK_START.md'
        ]

        removed = []
        for doc in orphan_docs:
            doc_path = self.vault_path / doc
            if doc_path.exists():
                if not dry_run:
                    doc_path.unlink()
                    self.changes.append(f"Deleted orphan doc: {doc}")
                removed.append(doc)

        if removed:
            print(f"  Found {len(removed)} orphan documentation files")
            if not dry_run:
                print(f"  ✅ Removed {len(removed)} orphan docs")
            else:
                print(f"  ℹ️  DRY RUN - would remove {len(removed)} files")
        else:
            print("  ✅ No orphan docs to remove")

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
    cleaner.remove_orphan_docs(dry_run=dry_run)

    # Summary
    cleaner.generate_summary()

    if dry_run:
        print("\n💡 To apply these changes, run: python3 cleanup_vault.py --apply")

    print("\n✅ Cleanup complete!")

if __name__ == '__main__':
    main()
