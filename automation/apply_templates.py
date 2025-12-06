#!/usr/bin/env python3
"""
Apply Templates to Notion Migrated Notes
Converts Notion-migrated notes to proper Obsidian template format
with Notion page URL preserved as comment
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


class TemplateApplier:
    """Notion 노트를 Obsidian 템플릿 형식으로 변환"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.templates_path = self.vault_path / "99-Assets/Templates"

        # Content type별 템플릿 매핑
        self.template_map = {
            "Article": "Article.md",
            "Reference": "Reference.md",
            "Insight": "Insight.md",
            "Experience": "Exprience.md",  # 템플릿 파일명 오타 유지
        }

    def get_notion_url(self, notion_id: str) -> str:
        """Notion ID로부터 페이지 URL 생성"""
        # Notion ID에서 하이픈 제거
        clean_id = notion_id.replace("-", "")
        return f"https://www.notion.so/{clean_id}"

    def load_template(self, content_type: str) -> Optional[str]:
        """템플릿 파일 로드"""
        template_file = self.template_map.get(content_type)
        if not template_file:
            print(f"⚠️  No template found for content type: {content_type}")
            return None

        template_path = self.templates_path / template_file
        if not template_path.exists():
            print(f"⚠️  Template file not found: {template_path}")
            return None

        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def parse_note(self, file_path: Path) -> tuple[Dict, str]:
        """노트 파일에서 frontmatter와 content 분리"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # frontmatter 추출
        fm_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if not fm_match:
            return {}, content

        frontmatter_text = fm_match.group(1)
        body = fm_match.group(2)

        # YAML 파싱
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter, body

    def apply_article_template(self, fm: Dict, content: str) -> str:
        """Article 템플릿 적용"""
        template = self.load_template("Article")
        if not template:
            return None

        # 제목 추출 (content에서 첫 번째 # 헤더)
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else fm.get('title', 'Untitled')

        # 본문에서 제목 제거
        content_without_title = re.sub(r'^# .+\n\n', '', content, count=1)

        # 템플릿 변수 치환
        filled_template = template.replace('{{title}}', title)
        filled_template = filled_template.replace('{{date}}', fm.get('created', datetime.now().isoformat()))

        # frontmatter 업데이트
        new_fm = {
            'tags': fm.get('tags', []) + ['article', 'reading'],
            'created': fm.get('created'),
            'updated': fm.get('updated'),
            'title': title,
            'type': 'article',
            'notion_id': fm.get('notion_id'),
            'company': fm.get('company'),
            'period': fm.get('period'),
        }

        # None 값 제거
        new_fm = {k: v for k, v in new_fm.items() if v is not None}

        # 중복 태그 제거
        if 'tags' in new_fm:
            new_fm['tags'] = list(set(new_fm['tags']))

        return self.build_note(new_fm, filled_template, content_without_title)

    def apply_reference_template(self, fm: Dict, content: str) -> str:
        """Reference 템플릿 적용"""
        template = self.load_template("Reference")
        if not template:
            return None

        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else fm.get('title', 'Untitled')

        content_without_title = re.sub(r'^# .+\n\n', '', content, count=1)

        filled_template = template.replace('{{title}}', title)
        filled_template = filled_template.replace('{{date}}', fm.get('created', datetime.now().isoformat()))

        new_fm = {
            'tags': list(set(fm.get('tags', []) + ['reference', 'knowledge'])),
            'created': fm.get('created'),
            'updated': fm.get('updated'),
            'title': title,
            'type': 'reference',
            'notion_id': fm.get('notion_id'),
        }

        new_fm = {k: v for k, v in new_fm.items() if v is not None}

        return self.build_note(new_fm, filled_template, content_without_title)

    def apply_insight_template(self, fm: Dict, content: str) -> str:
        """Insight 템플릿 적용"""
        template = self.load_template("Insight")
        if not template:
            return None

        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else fm.get('title', 'Untitled')

        content_without_title = re.sub(r'^# .+\n\n', '', content, count=1)

        filled_template = template.replace('{{title}}', title)
        filled_template = filled_template.replace('{{date}}', fm.get('created', datetime.now().isoformat()))

        new_fm = {
            'tags': list(set(fm.get('tags', []) + ['insight', 'life-learning'])),
            'created': fm.get('created'),
            'updated': fm.get('updated'),
            'title': title,
            'type': 'insight',
            'notion_id': fm.get('notion_id'),
            'company': fm.get('company'),
        }

        new_fm = {k: v for k, v in new_fm.items() if v is not None}

        return self.build_note(new_fm, filled_template, content_without_title)

    def build_note(self, frontmatter: Dict, template: str, original_content: str) -> str:
        """최종 노트 생성 (Notion URL 주석 포함)"""
        # frontmatter YAML 생성
        fm_lines = ["---"]
        for key, value in frontmatter.items():
            if isinstance(value, list):
                if value:  # 빈 리스트가 아닐 때만
                    fm_lines.append(f"{key}:")
                    for item in value:
                        fm_lines.append(f"  - {item}")
            elif value is not None:
                # 문자열에 콜론이 포함된 경우 따옴표로 감싸기
                if isinstance(value, str) and ':' in value:
                    fm_lines.append(f'{key}: "{value}"')
                else:
                    fm_lines.append(f"{key}: {value}")
        fm_lines.append("---")

        frontmatter_str = "\n".join(fm_lines)

        # Notion URL 주석 생성
        notion_comment = ""
        if 'notion_id' in frontmatter:
            notion_url = self.get_notion_url(frontmatter['notion_id'])
            notion_comment = f"\n<!--\nNotion 원본: {notion_url}\n마이그레이션 날짜: {datetime.now().strftime('%Y-%m-%d')}\n-->\n"

        # 최종 노트 구성
        # 1. Frontmatter
        # 2. Notion URL 주석
        # 3. 템플릿 구조
        # 4. 구분선
        # 5. 원본 콘텐츠
        return (
            f"{frontmatter_str}\n"
            f"{notion_comment}\n"
            f"{template}\n\n"
            f"---\n\n"
            f"## 📄 원본 콘텐츠 (Notion에서 마이그레이션)\n\n"
            f"{original_content}"
        )

    def process_note(self, file_path: Path, dry_run: bool = False) -> bool:
        """단일 노트 처리"""
        try:
            # 노트 파싱
            frontmatter, content = self.parse_note(file_path)

            # notion_id 확인 (Notion에서 마이그레이션된 노트만 처리)
            if 'notion_id' not in frontmatter:
                print(f"⏭️  Skipping (not from Notion): {file_path.name}")
                return False

            content_type = frontmatter.get('content_type')
            if not content_type:
                print(f"⚠️  No content_type in: {file_path.name}")
                return False

            # Content type별 템플릿 적용
            if content_type == "Article":
                new_content = self.apply_article_template(frontmatter, content)
            elif content_type == "Reference":
                new_content = self.apply_reference_template(frontmatter, content)
            elif content_type == "Insight":
                new_content = self.apply_insight_template(frontmatter, content)
            else:
                print(f"⚠️  Unsupported content type '{content_type}': {file_path.name}")
                return False

            if not new_content:
                return False

            # Dry run 모드
            if dry_run:
                print(f"✅ Would transform: {file_path.name} ({content_type})")
                return True

            # 파일 백업
            backup_path = file_path.with_suffix('.md.backup')
            file_path.rename(backup_path)

            # 새 파일 작성
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ Transformed: {file_path.name} ({content_type})")
            print(f"   Backup: {backup_path.name}")

            return True

        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
            return False

    def process_directory(self, directory: Path, dry_run: bool = False) -> Dict[str, int]:
        """디렉토리 내 모든 노트 처리"""
        stats = {
            'processed': 0,
            'skipped': 0,
            'errors': 0,
        }

        # .md 파일 찾기
        md_files = list(directory.rglob('*.md'))

        # 템플릿 파일 제외
        md_files = [f for f in md_files if not f.is_relative_to(self.templates_path)]

        print(f"\n📂 Processing directory: {directory}")
        print(f"   Found {len(md_files)} markdown files\n")

        for file_path in md_files:
            result = self.process_note(file_path, dry_run=dry_run)

            if result:
                stats['processed'] += 1
            else:
                stats['skipped'] += 1

        return stats


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Apply Obsidian templates to Notion-migrated notes'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to directory or file to process (default: current directory)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--vault',
        default='/Users/qraft_hongjinyoung/Second-Brain',
        help='Path to Obsidian vault'
    )

    args = parser.parse_args()

    applier = TemplateApplier(args.vault)
    target_path = Path(args.path).resolve()

    print("🔄 Template Applier")
    print("=" * 60)
    print(f"Vault: {applier.vault_path}")
    print(f"Target: {target_path}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)

    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No files will be modified\n")

    # 단일 파일 또는 디렉토리 처리
    if target_path.is_file():
        applier.process_note(target_path, dry_run=args.dry_run)
    elif target_path.is_dir():
        stats = applier.process_directory(target_path, dry_run=args.dry_run)

        print("\n" + "=" * 60)
        print("📊 Summary")
        print("=" * 60)
        print(f"✅ Processed: {stats['processed']}")
        print(f"⏭️  Skipped: {stats['skipped']}")
        print(f"❌ Errors: {stats['errors']}")
        print()

        if args.dry_run:
            print("💡 Run without --dry-run to apply changes")
    else:
        print(f"❌ Path not found: {target_path}")


if __name__ == '__main__':
    main()
