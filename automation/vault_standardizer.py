#!/usr/bin/env python3
"""
Vault Standardization Script
============================

이 스크립트는 Obsidian vault의 frontmatter, 태그, 연결성을 표준화합니다.

Usage:
    python vault_standardizer.py --phase 1 --dry-run
    python vault_standardizer.py --phase 2 --area "30-Flow/Life-Insights/Personal"
    python vault_standardizer.py --all --apply

Phases:
    1. Type 표준화
    2. 태그 표준화
    3. 필수 필드 추가
    4. Related 섹션 생성
    5. 백링크 강화
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import argparse


@dataclass
class Note:
    """노트 정보를 담는 데이터 클래스"""
    path: Path
    frontmatter: Dict
    content: str
    has_frontmatter: bool = True


class VaultStandardizer:
    """Vault 표준화 클래스"""

    # Type 변환 매핑
    TYPE_MAPPING = {
        "주간회고": "weekly-reflection",
        "daily-insight": "insight",
        "daily-reflection": "reflection",
        "일일회고": "reflection",
        "하루일기": "insight",
    }

    # 태그 변환 매핑 (한글 → 영어)
    TAG_MAPPING = {
        "커리어": "career",
        "커리어-지원내역": "career-application",
        "문제해결": "problem-solving",
        "데이터거버넌스": "data-governance",
        "구조화": "structuring",
        "문서화": "documentation",
        "의사소통": "communication",
        "협업": "collaboration",
        "기술전파": "knowledge-sharing",
        "비용 최적화": "cost-optimization",
        "성능개선": "performance-optimization",
        "운영 체계화": "operation-systematization",
        "자동화": "automation",
        "주식투자": "stock-investment",
        "투자노트": "investment-note",
        "이직": "job-change",
        "현대오토에버": "hyundai-autoever",
        "성과질문": "achievement-question",
        "알고리즘": "algorithm",
        "인간관계": "relationship",
        "가족": "family",
        "친구": "friends",
        "연애": "love",
        "인생결정": "life-decision",
        "성찰": "reflection",
        "관찰": "observations",
        "개인": "personal",
        "일상": "daily",
        "업무": "work",
        "회사생활": "work-life",
        "사고방식": "mindset",
        "철학": "philosophy",
        "인간본성": "human-nature",
    }

    # 표준 타입 목록
    STANDARD_TYPES = {
        "resource", "project", "reflection", "insight", "map", "moc",
        "weekly-reflection", "permanent", "literature", "fleeting",
        "experience", "outcome", "knowledge", "guide", "documentation"
    }

    def __init__(self, vault_path: str, dry_run: bool = True):
        self.vault_path = Path(vault_path)
        self.dry_run = dry_run
        self.stats = {
            "total_files": 0,
            "processed": 0,
            "skipped": 0,
            "errors": 0,
            "changes": []
        }

    def find_markdown_files(self, area: Optional[str] = None) -> List[Path]:
        """마크다운 파일 찾기"""
        search_path = self.vault_path / area if area else self.vault_path

        # .git, automation 등 제외
        exclude_dirs = {".git", "automation", "node_modules", ".obsidian"}

        files = []
        for file_path in search_path.rglob("*.md"):
            # 제외 디렉토리 체크
            if any(ex in file_path.parts for ex in exclude_dirs):
                continue
            files.append(file_path)

        return files

    def parse_note(self, file_path: Path) -> Note:
        """노트 파싱"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Frontmatter 추출
            fm_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)

            if fm_match:
                fm_text = fm_match.group(1)
                body = fm_match.group(2)

                try:
                    frontmatter = yaml.safe_load(fm_text) or {}
                except yaml.YAMLError:
                    frontmatter = {}

                return Note(
                    path=file_path,
                    frontmatter=frontmatter,
                    content=body,
                    has_frontmatter=True
                )
            else:
                return Note(
                    path=file_path,
                    frontmatter={},
                    content=content,
                    has_frontmatter=False
                )

        except Exception as e:
            print(f"❌ 파일 읽기 오류: {file_path} - {e}")
            return None

    def standardize_type(self, note: Note) -> Dict:
        """Type 필드 표준화"""
        changes = []
        fm = note.frontmatter.copy()

        if "type" in fm:
            old_type = fm["type"]

            # 문자열 정리 (따옴표 제거 등)
            if isinstance(old_type, str):
                old_type = old_type.strip().strip('"').strip("'")

                # 매핑 적용
                if old_type in self.TYPE_MAPPING:
                    new_type = self.TYPE_MAPPING[old_type]
                    fm["type"] = new_type
                    changes.append(f"Type: '{old_type}' → '{new_type}'")

                # 비표준 타입 경고
                elif old_type not in self.STANDARD_TYPES:
                    changes.append(f"⚠️  비표준 타입: '{old_type}'")
        else:
            # Type 필드 없으면 자동 추정
            inferred_type = self._infer_type(note)
            if inferred_type:
                fm["type"] = inferred_type
                changes.append(f"Type 추가: '{inferred_type}'")

        return fm, changes

    def standardize_tags(self, note: Note) -> Dict:
        """태그 표준화"""
        changes = []
        fm = note.frontmatter.copy()

        if "tags" not in fm:
            fm["tags"] = []
            changes.append("Tags 필드 추가")

        tags = fm["tags"]

        # 문자열을 리스트로 변환
        if isinstance(tags, str):
            # 해시태그 형식 처리
            if tags.startswith("#"):
                tags = [t.strip() for t in tags.split() if t.startswith("#")]
                tags = [t[1:] for t in tags]  # # 제거
            else:
                tags = [tags]

        # 빈 리스트면 내용 기반 태그 추정
        if not tags or tags == []:
            inferred_tags = self._infer_tags(note)
            if inferred_tags:
                tags = inferred_tags
                changes.append(f"Tags 자동 추가: {inferred_tags}")

        # 태그 변환 (한글 → 영어)
        new_tags = []
        for tag in tags:
            if isinstance(tag, str):
                tag = tag.strip()

                # 한글 태그 변환
                if tag in self.TAG_MAPPING:
                    new_tag = self.TAG_MAPPING[tag]
                    new_tags.append(new_tag)
                    if tag != new_tag:
                        changes.append(f"Tag: '{tag}' → '{new_tag}'")
                else:
                    # 소문자화 및 정리
                    new_tag = tag.lower().replace("_", "-").replace(" ", "-")
                    new_tags.append(new_tag)
                    if tag != new_tag:
                        changes.append(f"Tag 정리: '{tag}' → '{new_tag}'")

        fm["tags"] = list(set(new_tags))  # 중복 제거

        return fm, changes

    def add_missing_fields(self, note: Note) -> Dict:
        """누락된 필드 추가"""
        changes = []
        fm = note.frontmatter.copy()

        # created 필드
        if "created" not in fm:
            # 파일 생성일 사용
            created = datetime.fromtimestamp(note.path.stat().st_ctime)
            fm["created"] = created.strftime("%Y-%m-%d")
            changes.append(f"Created 추가: {fm['created']}")

        # updated 필드
        if "updated" not in fm:
            # 파일 수정일 사용
            updated = datetime.fromtimestamp(note.path.stat().st_mtime)
            fm["updated"] = updated.strftime("%Y-%m-%d")
            changes.append(f"Updated 추가: {fm['updated']}")

        # title 필드 (없으면 파일명 사용)
        if "title" not in fm:
            title = note.path.stem.replace("-", " ")
            fm["title"] = title
            changes.append(f"Title 추가: '{title}'")

        # aliases 필드
        if "aliases" not in fm:
            fm["aliases"] = []

        return fm, changes

    def create_related_section(self, note: Note) -> str:
        """Related 섹션 생성"""
        # 기존 Related 섹션 확인
        if "## Related" in note.content or "## 📎 Related" in note.content:
            return note.content, []

        # 태그 기반 관련 노트 찾기 (간단한 버전)
        related_section = "\n---\n\n## 📎 Related\n\n"
        related_section += "<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->\n\n"
        related_section += "### Projects\n\n"
        related_section += "### Knowledge\n\n"
        related_section += "### Insights\n\n"

        new_content = note.content.rstrip() + "\n" + related_section

        return new_content, ["Related 섹션 추가"]

    def write_note(self, note: Note, new_fm: Dict, new_content: str):
        """노트 저장"""
        # Frontmatter를 YAML로 변환
        fm_yaml = yaml.dump(new_fm, allow_unicode=True, sort_keys=False)

        # 전체 내용 조합
        full_content = f"---\n{fm_yaml}---\n{new_content}"

        if self.dry_run:
            print(f"  [DRY RUN] 저장할 내용:")
            print(f"  {full_content[:200]}...")
        else:
            try:
                with open(note.path, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                print(f"  ✅ 저장 완료")
            except Exception as e:
                print(f"  ❌ 저장 실패: {e}")
                self.stats["errors"] += 1

    def _infer_type(self, note: Note) -> Optional[str]:
        """노트 타입 자동 추정"""
        path_str = str(note.path)

        if "Projects/" in path_str:
            return "project"
        elif "Weekly/" in path_str:
            return "weekly-reflection"
        elif "Life-Insights/" in path_str:
            return "insight"
        elif "Resources/" in path_str:
            return "resource"
        elif "Zettelkasten/Permanent" in path_str:
            return "permanent"
        elif "Zettelkasten/Literature" in path_str:
            return "literature"
        elif "Zettelkasten/Fleeting" in path_str:
            return "fleeting"

        return None

    def _infer_tags(self, note: Note) -> List[str]:
        """노트 태그 자동 추정 (향상된 버전)"""
        tags = []
        path_str = str(note.path)
        content = note.content
        content_lower = content.lower()

        # 1. 경로 기반 태그
        if "크래프트테크놀로지스" in path_str or "qraft" in content_lower:
            tags.append("qraft")
        if "Career/" in path_str:
            tags.append("career")
        if "Technology/" in path_str:
            tags.append("technology")
        if "Life-Insights/Work" in path_str:
            tags.append("work")
        if "Life-Insights/Personal" in path_str:
            tags.append("personal")
        if "Observations" in path_str:
            tags.append("observations")

        # 2. 기술 키워드 (확장)
        tech_keywords = {
            "airflow": "airflow",
            "dbt": "dbt",
            "python": "python",
            "sql": "sql",
            "aws": "aws",
            "docker": "docker",
            "kubernetes": "kubernetes",
            "jenkins": "jenkins",
            "kafka": "kafka",
            "snowflake": "snowflake",
            "postgres": "postgres",
            "datahub": "datahub",
            "데이터": "data",
            "파이프라인": "pipeline",
            "쿼리": "query",
        }

        for keyword, tag in tech_keywords.items():
            if keyword in content_lower:
                tags.append(tag)

        # 3. 감정/주제 키워드
        emotion_keywords = {
            "스트레스": "stress",
            "화": "anger",
            "분노": "anger",
            "억울": "frustration",
            "답답": "frustration",
            "행복": "happiness",
            "기쁨": "joy",
            "슬픔": "sadness",
            "우울": "depression",
            "불안": "anxiety",
            "걱정": "worry",
        }

        for keyword, tag in emotion_keywords.items():
            if keyword in content:
                tags.append(tag)

        # 4. 업무 관련 키워드
        work_keywords = {
            "회사": "company",
            "업무": "work",
            "프로젝트": "project",
            "팀": "team",
            "미팅": "meeting",
            "회의": "meeting",
            "상사": "boss",
            "동료": "colleague",
            "출근": "commute",
            "야근": "overtime",
            "성과": "achievement",
            "목표": "goal",
        }

        for keyword, tag in work_keywords.items():
            if keyword in content:
                tags.append(tag)

        # 5. 인간관계 키워드
        relationship_keywords = {
            "가족": "family",
            "부모": "family",
            "엄마": "family",
            "아빠": "family",
            "친구": "friends",
            "연애": "love",
            "애인": "love",
            "결혼": "marriage",
            "사람": "relationships",
        }

        for keyword, tag in relationship_keywords.items():
            if keyword in content:
                tags.append(tag)

        # 6. 자기계발 키워드
        growth_keywords = {
            "배움": "learning",
            "공부": "study",
            "성장": "growth",
            "발전": "development",
            "개선": "improvement",
            "목표": "goal",
            "계획": "planning",
            "시간관리": "time-management",
        }

        for keyword, tag in growth_keywords.items():
            if keyword in content:
                tags.append(tag)

        # 7. 인사이트 타입 추정
        if "## 본 것" in content or "## 깨달은 것" in content:
            tags.append("reflection")
        if "## 일기" in content:
            tags.append("journal")
        if "## 적용할 것" in content:
            tags.append("action-item")

        # 중복 제거 및 상위 8개만 반환
        return list(set(tags))[:8]

    def process_phase(self, phase: int, area: Optional[str] = None):
        """특정 Phase 실행"""
        files = self.find_markdown_files(area)
        self.stats["total_files"] = len(files)

        print(f"\n{'='*60}")
        print(f"Phase {phase} 실행: {len(files)}개 파일")
        print(f"영역: {area or '전체'}")
        print(f"모드: {'DRY RUN (테스트)' if self.dry_run else 'APPLY (실제 적용)'}")
        print(f"{'='*60}\n")

        for file_path in files:
            note = self.parse_note(file_path)
            if not note:
                self.stats["skipped"] += 1
                continue

            print(f"\n📄 {file_path.relative_to(self.vault_path)}")

            changes = []
            new_fm = note.frontmatter.copy()
            new_content = note.content

            # Phase별 처리
            if phase == 1:  # Type 표준화
                new_fm, type_changes = self.standardize_type(note)
                changes.extend(type_changes)

            elif phase == 2:  # 태그 표준화
                new_fm, tag_changes = self.standardize_tags(note)
                changes.extend(tag_changes)

            elif phase == 3:  # 필수 필드 추가
                new_fm, field_changes = self.add_missing_fields(note)
                changes.extend(field_changes)

            elif phase == 4:  # Related 섹션
                new_content, related_changes = self.create_related_section(note)
                changes.extend(related_changes)

            # 변경사항 출력
            if changes:
                for change in changes:
                    print(f"  • {change}")

                # 저장
                self.write_note(note, new_fm, new_content)
                self.stats["processed"] += 1
                self.stats["changes"].extend(changes)
            else:
                print(f"  ℹ️  변경사항 없음")
                self.stats["skipped"] += 1

        # 통계 출력
        print(f"\n{'='*60}")
        print(f"완료!")
        print(f"  총 파일: {self.stats['total_files']}")
        print(f"  처리됨: {self.stats['processed']}")
        print(f"  건너뜀: {self.stats['skipped']}")
        print(f"  오류: {self.stats['errors']}")
        print(f"  총 변경: {len(self.stats['changes'])}")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Vault 표준화 스크립트")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4, 5],
                       help="실행할 Phase (1=Type, 2=Tags, 3=Fields, 4=Related, 5=Backlinks)")
    parser.add_argument("--all", action="store_true",
                       help="모든 Phase 실행")
    parser.add_argument("--area", type=str,
                       help="특정 영역만 처리 (예: '30-Flow/Life-Insights/Personal')")
    parser.add_argument("--dry-run", action="store_true", default=True,
                       help="테스트 모드 (기본값)")
    parser.add_argument("--apply", action="store_true",
                       help="실제 적용 (--dry-run 비활성화)")

    args = parser.parse_args()

    # Vault 경로
    vault_path = Path(__file__).parent.parent

    # Dry run 설정
    dry_run = not args.apply

    # Standardizer 생성
    standardizer = VaultStandardizer(vault_path, dry_run=dry_run)

    # Phase 실행
    if args.all:
        for phase in [1, 2, 3, 4]:
            standardizer.process_phase(phase, args.area)
    elif args.phase:
        standardizer.process_phase(args.phase, args.area)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
