#!/usr/bin/env python3
"""
Life-Insights 노트 변환 스크립트

Frontmatter에 있는 실질적인 내용(깨달은 것, 본 것, 일기, 적용할 것)을
본문으로 옮기고, frontmatter를 간소화합니다.
"""

import os
import re
from pathlib import Path
from typing import Dict, Any
import frontmatter


def parse_frontmatter_content(fm: Dict[str, Any]) -> Dict[str, str]:
    """Frontmatter에서 본문으로 옮길 내용 추출"""
    content_fields = {
        '본 것': fm.get('본 것', ''),
        '깨달은 것': fm.get('깨달은 것', ''),
        '적용할 것': fm.get('적용할 것', ''),
        '일기': fm.get('일기', '')
    }

    # 빈 값 제거
    return {k: v for k, v in content_fields.items() if v and v.strip()}


def create_new_frontmatter(fm: Dict[str, Any]) -> Dict[str, Any]:
    """간소화된 frontmatter 생성"""
    new_fm = {
        'title': fm.get('title', fm.get('주제(API용)', 'Untitled')),
        'date': fm.get('날짜(생성날짜)', fm.get('날짜', '')),
        'week': fm.get('주차', ''),
        'type': fm.get('회고종류', ''),
    }

    # Tags 정리
    tags = fm.get('tags', [])
    if isinstance(tags, list):
        # notion-import, 본깨적 등 불필요한 태그 제거
        cleaned_tags = [
            tag for tag in tags
            if tag not in ['notion-import', '본깨적', 'database']
        ]
        if cleaned_tags:
            new_fm['tags'] = cleaned_tags

    # 빈 값 제거
    return {k: v for k, v in new_fm.items() if v}


def create_markdown_content(
    title: str,
    date: str,
    week: int,
    type_: str,
    content_sections: Dict[str, str],
    related_links: str
) -> str:
    """새로운 마크다운 본문 생성"""
    lines = [f"# {title}", ""]

    # 메타데이터 블록
    meta_lines = []
    if date:
        # 날짜 포맷 정리 (ISO 8601 → YYYY-MM-DD)
        date_str = date.split('T')[0] if 'T' in date else date
        meta_lines.append(f"> **날짜**: {date_str}")
    if week:
        meta_lines.append(f"> **주차**: {week}주차")
    if type_:
        meta_lines.append(f"> **회고종류**: {type_}")

    if meta_lines:
        lines.extend(meta_lines)
        lines.append("")

    # 본문 섹션
    section_order = ['본 것', '깨달은 것', '적용할 것', '일기']
    for section in section_order:
        if section in content_sections:
            lines.extend([
                f"## {section}",
                "",
                content_sections[section],
                ""
            ])

    # Related 링크
    if related_links and related_links.strip():
        lines.extend([
            "---",
            "",
            related_links.strip()
        ])

    return '\n'.join(lines)


def extract_related_links(content: str) -> str:
    """기존 본문에서 Related 섹션 추출"""
    # ## Related 이후의 내용 추출
    match = re.search(r'## Related\s*\n(.*)', content, re.DOTALL)
    if match:
        return "## Related\n" + match.group(1).strip()
    return ""


def convert_note(file_path: Path, dry_run: bool = False) -> bool:
    """단일 노트 파일 변환"""
    try:
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # 이미 변환된 파일인지 체크 (frontmatter에 '본 것' 등이 없으면 스킵)
        fm = post.metadata
        if not any(key in fm for key in ['본 것', '깨달은 것', '일기', '적용할 것']):
            print(f"⏭️  Skip (already converted): {file_path.name}")
            return False

        # 내용 추출
        content_sections = parse_frontmatter_content(fm)
        if not content_sections:
            print(f"⚠️  Skip (no content): {file_path.name}")
            return False

        # 새 frontmatter 생성
        new_fm = create_new_frontmatter(fm)

        # Related 링크 추출
        related_links = extract_related_links(post.content)

        # 새 본문 생성
        new_content = create_markdown_content(
            title=new_fm.get('title', 'Untitled'),
            date=new_fm.get('date', ''),
            week=new_fm.get('week', ''),
            type_=new_fm.get('type', ''),
            content_sections=content_sections,
            related_links=related_links
        )

        if dry_run:
            print(f"✅ Would convert: {file_path.name}")
            return True

        # 파일 쓰기
        new_post = frontmatter.Post(new_content, **new_fm)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(new_post))

        print(f"✅ Converted: {file_path.name}")
        return True

    except Exception as e:
        print(f"❌ Error converting {file_path.name}: {e}")
        return False


def convert_directory(dir_path: Path, dry_run: bool = False) -> tuple[int, int]:
    """디렉토리 내 모든 마크다운 파일 변환"""
    converted = 0
    skipped = 0

    for file_path in dir_path.rglob('*.md'):
        # README 등 제외
        if file_path.name in ['README.md', '_INDEX.md']:
            continue

        if convert_note(file_path, dry_run):
            converted += 1
        else:
            skipped += 1

    return converted, skipped


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Life-Insights 노트 변환 (Frontmatter → Body)'
    )
    parser.add_argument(
        '--dir',
        type=str,
        default='30-Flow/Life-Insights',
        help='변환할 디렉토리 경로 (기본값: 30-Flow/Life-Insights)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='실제 변환 없이 미리보기만 (Dry run)'
    )

    args = parser.parse_args()

    # 경로 설정
    vault_root = Path(__file__).parent.parent
    target_dir = vault_root / args.dir

    if not target_dir.exists():
        print(f"❌ Directory not found: {target_dir}")
        return

    print(f"\n🔍 Target Directory: {target_dir}")
    print(f"{'🔄 DRY RUN MODE - No files will be changed' if args.dry_run else '✏️  WRITE MODE - Files will be modified'}\n")

    # 변환 실행
    converted, skipped = convert_directory(target_dir, args.dry_run)

    # 결과 출력
    print(f"\n{'─' * 50}")
    print(f"✅ Converted: {converted}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"📊 Total: {converted + skipped}")

    if args.dry_run:
        print(f"\n💡 Run without --dry-run to actually convert files")


if __name__ == '__main__':
    main()
