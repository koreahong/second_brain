#!/usr/bin/env python3
"""
Vault 포맷 정규화 스크립트

Notion에서 마이그레이션된 노트들의 frontmatter, 태그, 본문 포맷을
Second Brain 구조에 맞게 일관성 있게 정리합니다.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml
from datetime import datetime


class VaultNormalizer:
    """Vault 노트 정규화"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.stats = {
            'processed': 0,
            'modified': 0,
            'errors': 0,
            'skipped': 0
        }

        # 카테고리별 frontmatter 스키마
        self.schemas = {
            'life-insights': {
                'required': ['title', 'date', 'type'],
                'optional': ['week', 'tags', 'related'],
                'remove': ['source', 'notion_id', 'imported', 'database',
                          '적용할 것', '회고종류', '날짜(생성날짜)', '주제(API용)',
                          '사진', '깨달은 것', '본 것', '주차', '일기', '날짜']
            },
            'weekly': {
                'required': ['title', 'date', 'type'],
                'optional': ['week', 'tags', 'summary', 'achievements', 'challenges',
                            'learnings', 'next_week', 'related_projects'],
                'remove': ['source', 'notion_id', 'imported', 'database',
                          '🔧 대처 방법', '🌟 한 줄 요약', '✨ 성과 / 개선점',
                          '🚩 문제 상황', '역량', '🙌 배운 점']
            },
            'projects': {
                'required': ['title', 'status', 'created'],
                'optional': ['tags', 'jira_key', 'related', 'updated', 'completed'],
                'remove': ['source', 'notion_id', 'imported', 'database', '태그',
                          'Git 커밋', 'Jira Key', '상태', '시행착오 (Trial & Error)',
                          '업무 구상 1', '작업 히스토리', '상위 항목', 'Jira 결과',
                          '업무 구상', '생성 일시', '하위 항목']
            },
            'resources': {
                'required': ['title', 'category'],
                'optional': ['tags', 'url', 'author', 'date', 'summary', 'related'],
                'remove': ['source', 'notion_id', 'imported', 'database', '하위 항목',
                          '구상기록', '구분', '링크', '최종편집시각', '제목',
                          '상위 항목', '날짜', 'PARA']
            }
        }

        # 태그 정규화 매핑
        self.tag_mapping = {
            # 제거할 임시 태그
            'notion-import': None,
            '본깨적': None,
            '회고록': None,
            '업무리스트': None,
            '레퍼런스': None,

            # 기술 태그 (소문자, 하이픈)
            'Airflow': 'airflow',
            'DBT': 'dbt',
            'DataHub': 'datahub',
            'PostgreSQL': 'postgresql',
            'Snowflake': 'snowflake',
            'AWS': 'aws',
            'Docker': 'docker',
            'Kubernetes': 'kubernetes',
            'Python': 'python',

            # 역량 태그 (한글 유지, 일관성)
            '의사소통': '의사소통',
            '문서화': '문서화',
            '문제해결': '문제해결',
            '구조화': '구조화',
            '데이터모델링': '데이터모델링',
            '거버넌스': '거버넌스',
        }

    def detect_category(self, file_path: Path) -> str:
        """파일 경로로 카테고리 감지"""
        path_str = str(file_path)

        if '30-Flow/Life-Insights' in path_str:
            return 'life-insights'
        elif 'Experience/Weekly' in path_str:
            return 'weekly'
        elif 'Projects/' in path_str:
            return 'projects'
        elif '03-Resources/' in path_str:
            return 'resources'

        return 'unknown'

    def parse_frontmatter(self, content: str) -> tuple[Optional[Dict], str]:
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

    def normalize_frontmatter(self, frontmatter: Dict, category: str) -> Dict:
        """Frontmatter 정규화"""
        if not frontmatter:
            return {}

        schema = self.schemas.get(category, self.schemas['resources'])
        normalized = {}

        # 1. 제거할 필드 제거
        for key in schema['remove']:
            frontmatter.pop(key, None)

        # 2. 날짜 필드 통일
        date_value = None
        for date_key in ['date', '날짜', '날짜(생성날짜)', '생성 일시', '최종편집시각']:
            if date_key in frontmatter:
                date_value = frontmatter.pop(date_key)
                break

        if date_value:
            # ISO 형식 → YYYY-MM-DD
            if isinstance(date_value, str):
                try:
                    dt = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                    normalized['date'] = dt.strftime('%Y-%m-%d')
                except:
                    normalized['date'] = date_value
            else:
                normalized['date'] = str(date_value)

        # 3. 제목
        if 'title' in frontmatter:
            normalized['title'] = frontmatter['title']

        # 4. 타입 (카테고리별)
        if category == 'life-insights':
            normalized['type'] = frontmatter.get('type', frontmatter.get('회고종류', 'insight'))
        elif category == 'weekly':
            normalized['type'] = 'weekly-reflection'
        elif category == 'projects':
            normalized['type'] = 'project'
            # 상태 매핑
            status_map = {
                '리스트업': 'planned',
                '진행중': 'active',
                '완료': 'completed',
                '보류': 'on-hold'
            }
            old_status = frontmatter.get('상태', frontmatter.get('status', 'planned'))
            normalized['status'] = status_map.get(old_status, old_status)
        elif category == 'resources':
            normalized['type'] = 'resource'
            # 구분 → category
            categories = frontmatter.get('구분', [])
            if categories:
                normalized['category'] = categories[0] if isinstance(categories, list) else categories

        # 5. 태그 정규화
        tags = frontmatter.get('tags', [])
        if not isinstance(tags, list):
            tags = [tags] if tags else []

        # 역량 태그 추가
        competencies = frontmatter.get('역량', [])
        if competencies and isinstance(competencies, list):
            tags.extend(competencies)

        normalized_tags = []
        for tag in tags:
            if tag in self.tag_mapping:
                new_tag = self.tag_mapping[tag]
                if new_tag:  # None이 아닌 경우만
                    normalized_tags.append(new_tag)
            else:
                normalized_tags.append(tag)

        # 중복 제거
        normalized['tags'] = sorted(list(set(normalized_tags)))

        # 6. 기타 유용한 필드 유지
        for key in ['week', 'summary', 'url', 'author', 'jira_key', 'related']:
            if key in frontmatter and frontmatter[key]:
                normalized[key] = frontmatter[key]

        # 7. created/updated
        if category == 'projects':
            if '생성 일시' in frontmatter:
                try:
                    dt = datetime.fromisoformat(frontmatter['생성 일시'].replace('Z', '+00:00'))
                    normalized['created'] = dt.strftime('%Y-%m-%d')
                except:
                    pass

        return normalized

    def normalize_body(self, body: str, category: str, frontmatter: Dict) -> str:
        """본문 포맷 정규화"""
        if not body or body.strip() == '':
            # 빈 본문인 경우 기본 구조 생성
            if category == 'life-insights':
                title = frontmatter.get('title', '제목 없음')
                date = frontmatter.get('date', '')
                week = frontmatter.get('week', '')

                body = f"""# {title}

> **날짜**: {date}
> **주차**: {week}주차

## 본 것

(내용 추가 필요)

## 깨달은 것

(내용 추가 필요)

## 적용할 것

(내용 추가 필요)
"""
            elif category == 'weekly':
                body = """## 🌟 한 줄 요약

(요약 추가)

## ✨ 성과 / 개선점

-

## 🚩 문제 상황

-

## 🙌 배운 점

-

## 🔧 대처 방법

-

## 📋 다음 주 계획

-

---

### Related Projects

-
"""
            return body

        # 링크 포맷 정규화 (🔖 제거)
        body = re.sub(r'🔖\s*\[', '[', body)

        # 불필요한 빈 줄 제거 (3개 이상 연속 → 2개)
        body = re.sub(r'\n{3,}', '\n\n', body)

        return body.strip()

    def process_file(self, file_path: Path) -> bool:
        """개별 파일 처리"""
        try:
            # 카테고리 감지
            category = self.detect_category(file_path)
            if category == 'unknown':
                self.stats['skipped'] += 1
                return False

            # 파일 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Frontmatter 파싱
            frontmatter, body = self.parse_frontmatter(content)

            if not frontmatter:
                self.stats['skipped'] += 1
                return False

            # 정규화
            normalized_fm = self.normalize_frontmatter(frontmatter, category)
            normalized_body = self.normalize_body(body, category, normalized_fm)

            # 새 콘텐츠 생성
            new_content = "---\n"
            new_content += yaml.dump(normalized_fm, allow_unicode=True, sort_keys=False)
            new_content += "---\n\n"
            new_content += normalized_body

            # 변경사항 확인
            if content != new_content:
                # 파일 쓰기
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                self.stats['modified'] += 1
                print(f"✅ {file_path.relative_to(self.vault_path)}")
                return True
            else:
                self.stats['skipped'] += 1
                return False

        except Exception as e:
            print(f"❌ {file_path.relative_to(self.vault_path)}: {e}")
            self.stats['errors'] += 1
            return False
        finally:
            self.stats['processed'] += 1

    def process_directory(self, directory: Path):
        """디렉토리 재귀 처리"""
        for file_path in directory.rglob('*.md'):
            # 특정 파일/폴더 제외
            if any(skip in str(file_path) for skip in [
                'README.md',
                'automation/',
                '99-Assets/',
                '.git/',
                '.obsidian/'
            ]):
                continue

            self.process_file(file_path)

    def run(self, dry_run: bool = False):
        """전체 처리 실행"""
        print(f"\n{'='*60}")
        print(f"🚀 Vault 포맷 정규화 시작")
        print(f"{'='*60}\n")

        if dry_run:
            print("⚠️  DRY RUN 모드 - 실제 파일은 수정하지 않습니다.\n")

        # 주요 디렉토리 처리
        directories = [
            self.vault_path / '30-Flow' / 'Life-Insights',
            self.vault_path / '02-Areas' / '크래프트테크놀로지스',
            self.vault_path / '03-Resources',
        ]

        for directory in directories:
            if directory.exists():
                print(f"\n📁 {directory.relative_to(self.vault_path)} 처리 중...\n")
                self.process_directory(directory)

        # 결과 출력
        print(f"\n{'='*60}")
        print(f"✨ 처리 완료")
        print(f"{'='*60}")
        print(f"  📊 전체 파일: {self.stats['processed']}")
        print(f"  ✅ 수정됨: {self.stats['modified']}")
        print(f"  ⏭️  건너뜀: {self.stats['skipped']}")
        print(f"  ❌ 오류: {self.stats['errors']}")
        print(f"{'='*60}\n")


def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(description='Vault 포맷 정규화')
    parser.add_argument('--vault', default='/Users/qraft_hongjinyoung/DAE-Second-Brain',
                       help='Vault 경로')
    parser.add_argument('--dry-run', action='store_true',
                       help='실제 수정하지 않고 미리보기만')

    args = parser.parse_args()

    normalizer = VaultNormalizer(args.vault)
    normalizer.run(dry_run=args.dry_run)


if __name__ == '__main__':
    main()
