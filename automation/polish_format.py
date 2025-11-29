#!/usr/bin/env python3
"""
Vault 포맷 최종 다듬기 스크립트

이미 정규화된 노트들의 세부 일관성을 개선합니다:
- 날짜 포맷 통일
- Type 값 정규화
- 본문 메타데이터 중복 제거
- 빈 태그 제거
- 섹션 구조 통일
"""

import os
import re
from pathlib import Path
import yaml
from datetime import datetime


class FormatPolisher:
    """포맷 다듬기"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.stats = {
            'processed': 0,
            'modified': 0,
            'errors': 0
        }

        # Type 정규화 매핑
        self.type_mapping = {
            '하루일기': 'daily-insight',
            '일일회고': 'daily-reflection',
            'insight': 'insight',
            'weekly-reflection': 'weekly-reflection',
            'project': 'project',
            'resource': 'resource'
        }

    def parse_frontmatter(self, content: str) -> tuple:
        """Frontmatter 파싱"""
        if not content.startswith('---'):
            return None, content

        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                return None, content

            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()

            return frontmatter, body
        except Exception as e:
            print(f"⚠️  Frontmatter 파싱 오류: {e}")
            return None, content

    def polish_frontmatter(self, fm: dict) -> dict:
        """Frontmatter 다듬기"""
        if not fm:
            return {}

        polished = {}

        # 1. Title (그대로 유지)
        if 'title' in fm:
            polished['title'] = fm['title']

        # 2. Date (따옴표 제거, YYYY-MM-DD 형식)
        if 'date' in fm:
            date_val = fm['date']
            if isinstance(date_val, str):
                # 따옴표가 있든 없든 통일
                date_clean = date_val.strip("'\"")
                # ISO 형식 → YYYY-MM-DD
                try:
                    if 'T' in date_clean:
                        dt = datetime.fromisoformat(date_clean.replace('Z', '+00:00'))
                        polished['date'] = dt.strftime('%Y-%m-%d')
                    else:
                        polished['date'] = date_clean
                except:
                    polished['date'] = date_clean
            else:
                polished['date'] = str(date_val)

        # 3. Type 정규화
        if 'type' in fm:
            old_type = fm['type']
            polished['type'] = self.type_mapping.get(old_type, old_type)

        # 4. Week (그대로 유지)
        if 'week' in fm and fm['week']:
            polished['week'] = fm['week']

        # 5. Status (프로젝트용)
        if 'status' in fm and fm['status']:
            polished['status'] = fm['status']

        # 6. Created/Updated (있으면 유지)
        for key in ['created', 'updated', 'completed']:
            if key in fm and fm[key]:
                polished[key] = fm[key]

        # 7. Tags (빈 배열 제거, 있으면 유지)
        if 'tags' in fm:
            tags = fm['tags']
            if tags and len(tags) > 0:
                polished['tags'] = sorted(list(set(tags)))
            # 빈 배열은 제거 (포함하지 않음)

        # 8. 기타 유용한 필드
        for key in ['summary', 'url', 'author', 'category', 'jira_key', 'related']:
            if key in fm and fm[key]:
                polished[key] = fm[key]

        return polished

    def polish_body(self, body: str, fm: dict) -> str:
        """본문 다듬기"""
        if not body:
            return ""

        # 1. 본문 메타데이터 블록 제거 (frontmatter와 중복)
        # > **날짜**: ... 형식 제거
        body = re.sub(r'>\s*\*\*날짜\*\*:.*?\n', '', body)
        body = re.sub(r'>\s*\*\*주차\*\*:.*?주차\n', '', body)
        body = re.sub(r'>\s*\*\*회고종류\*\*:.*?\n', '', body)

        # 빈 인용구 블록 제거
        body = re.sub(r'>\s*\n>\s*\n>\s*\n', '', body)
        body = re.sub(r'>\s*\n>\s*\n', '', body)

        # 2. 불필요한 빈 줄 정리 (3개 이상 → 2개)
        body = re.sub(r'\n{3,}', '\n\n', body)

        # 3. 마지막 공백 제거
        body = body.strip()

        return body

    def process_file(self, file_path: Path) -> bool:
        """파일 처리"""
        try:
            # 파일 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Frontmatter 파싱
            fm, body = self.parse_frontmatter(content)

            if not fm:
                self.stats['processed'] += 1
                return False

            # 다듬기
            polished_fm = self.polish_frontmatter(fm)
            polished_body = self.polish_body(body, polished_fm)

            # 새 콘텐츠 생성
            new_content = "---\n"
            new_content += yaml.dump(polished_fm, allow_unicode=True,
                                    sort_keys=False, default_flow_style=False)
            new_content += "---\n\n"
            new_content += polished_body

            # 변경 확인
            if content != new_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                self.stats['modified'] += 1
                print(f"✅ {file_path.relative_to(self.vault_path)}")
                return True

            self.stats['processed'] += 1
            return False

        except Exception as e:
            print(f"❌ {file_path.relative_to(self.vault_path)}: {e}")
            self.stats['errors'] += 1
            self.stats['processed'] += 1
            return False

    def run(self):
        """전체 실행"""
        print(f"\n{'='*60}")
        print(f"✨ Vault 포맷 다듬기 시작")
        print(f"{'='*60}\n")

        # 처리할 디렉토리
        directories = [
            self.vault_path / '30-Flow' / 'Life-Insights',
            self.vault_path / '02-Areas' / '크래프트테크놀로지스',
            self.vault_path / '03-Resources',
        ]

        for directory in directories:
            if not directory.exists():
                continue

            print(f"\n📁 {directory.relative_to(self.vault_path)} 처리 중...\n")

            for file_path in directory.rglob('*.md'):
                # 제외할 파일
                if any(skip in str(file_path) for skip in [
                    'README.md', 'automation/', '99-Assets/',
                    '.git/', '.obsidian/', '90-Meta/'
                ]):
                    continue

                self.process_file(file_path)

        # 결과
        print(f"\n{'='*60}")
        print(f"🎉 완료!")
        print(f"{'='*60}")
        print(f"  📊 전체 파일: {self.stats['processed']}")
        print(f"  ✅ 수정됨: {self.stats['modified']}")
        print(f"  ❌ 오류: {self.stats['errors']}")
        print(f"{'='*60}\n")


def main():
    """메인 함수"""
    polisher = FormatPolisher('/Users/qraft_hongjinyoung/DAE-Second-Brain')
    polisher.run()


if __name__ == '__main__':
    main()
