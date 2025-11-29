"""
Document Quality Scorer

문서의 품질을 0-100점으로 자동 평가합니다.

점수 기준:
- Completeness (완성도): 0-25점
- Organization (구조화): 0-25점
- Connectivity (연결성): 0-25점
- Actionability (실행가능성): 0-25점
"""

from pathlib import Path
from typing import Dict, List
from ..utils.markdown_utils import (
    MarkdownNote,
    extract_tags,
    extract_keywords,
    has_todo_items,
    count_list_items,
    count_tables
)
from .config import SCORE_WEIGHTS, SCORE_THRESHOLDS


class DocumentQualityScorer:
    """문서 품질 점수 계산기"""

    def __init__(self, vault_root: Path):
        self.vault_root = vault_root

    def score_document(self, note_path: Path) -> Dict:
        """
        문서 점수 계산

        Args:
            note_path: 노트 파일 경로

        Returns:
            {
                'total_score': 85,
                'grade': 'A',
                'breakdown': {...},
                'suggestions': [...]
            }
        """
        note = MarkdownNote(note_path)

        scores = {
            'completeness': self._score_completeness(note),
            'organization': self._score_organization(note),
            'connectivity': self._score_connectivity(note),
            'actionability': self._score_actionability(note)
        }

        total_score = sum(scores.values())
        grade = self._get_grade(total_score)
        suggestions = self._generate_suggestions(scores, note)

        return {
            'total_score': total_score,
            'grade': grade,
            'breakdown': scores,
            'suggestions': suggestions,
            'metadata': {
                'word_count': note.word_count(),
                'char_count': note.char_count(),
                'link_count': len(note.get_links()),
                'heading_count': len(note.get_headings()),
                'code_block_count': len(note.get_code_blocks())
            }
        }

    def _score_completeness(self, note: MarkdownNote) -> float:
        """
        완성도 점수 (0-25점)

        기준:
        - Frontmatter 존재: 5점
        - 적절한 내용 길이 (>200자): 10점
        - 코드/예시 존재: 5점
        - 명확한 제목: 5점
        """
        score = 0.0

        # 1. Frontmatter 존재 (5점)
        if note.frontmatter:
            score += 5.0

        # 2. 내용 길이 (10점)
        char_count = note.char_count()
        if char_count > 1000:
            score += 10.0
        elif char_count > 500:
            score += 7.0
        elif char_count > 200:
            score += 5.0
        elif char_count > 100:
            score += 3.0

        # 3. 코드 블록/예시 (5점)
        code_blocks = note.get_code_blocks()
        if len(code_blocks) >= 3:
            score += 5.0
        elif len(code_blocks) >= 1:
            score += 3.0

        # 4. 명확한 제목 (5점)
        headings = note.get_headings()
        if headings:
            # H1 제목 존재
            if any(h['level'] == 1 for h in headings):
                score += 5.0
            else:
                score += 3.0

        return min(score, SCORE_WEIGHTS['completeness'])

    def _score_organization(self, note: MarkdownNote) -> float:
        """
        구조화 점수 (0-25점)

        기준:
        - 헤딩 구조: 10점
        - 리스트/테이블 활용: 5점
        - 태그: 5점
        - 날짜 정보: 5점
        """
        score = 0.0

        # 1. 헤딩 구조 (10점)
        headings = note.get_headings()
        if len(headings) >= 5:
            score += 10.0
        elif len(headings) >= 3:
            score += 7.0
        elif len(headings) >= 1:
            score += 5.0

        # 2. 리스트/테이블 (5점)
        list_count = count_list_items(note.content)
        table_count = count_tables(note.content)

        if list_count >= 5 or table_count >= 1:
            score += 5.0
        elif list_count >= 3:
            score += 3.0

        # 3. 태그 (5점)
        tags = extract_tags(note.content, note.frontmatter)
        if len(tags) >= 3:
            score += 5.0
        elif len(tags) >= 1:
            score += 3.0

        # 4. 날짜 정보 (5점)
        date_fields = ['created', 'updated', 'date', 'imported', '날짜']
        has_date = any(field in note.frontmatter for field in date_fields)
        if has_date:
            score += 5.0

        return min(score, SCORE_WEIGHTS['organization'])

    def _score_connectivity(self, note: MarkdownNote) -> float:
        """
        연결성 점수 (0-25점)

        기준:
        - 내부 링크 개수: 15점 (1개당 3점, 최대 15점)
        - 백링크 개수: 10점 (추후 구현)
        """
        score = 0.0

        # 1. 내부 링크 (15점)
        links = note.get_links()
        link_score = min(len(links) * 3, 15)
        score += link_score

        # 2. 백링크 (10점) - 추후 구현
        # 현재는 보너스로 frontmatter에 related_notes가 있으면 가산점
        if 'related_notes' in note.frontmatter:
            score += 5.0

        return min(score, SCORE_WEIGHTS['connectivity'])

    def _score_actionability(self, note: MarkdownNote) -> float:
        """
        실행가능성 점수 (0-25점)

        기준:
        - TODO 항목: 10점
        - Jira/Git 연동: 10점
        - 프로젝트 연결: 5점
        """
        score = 0.0

        # 1. TODO 항목 (10점)
        if has_todo_items(note.content):
            score += 10.0

        # 2. Jira/Git 연동 (10점)
        fm = note.frontmatter
        has_jira = 'jira' in fm or 'Jira Key' in fm or 'jira_key' in fm
        has_git = 'git' in fm or 'Git 커밋' in fm or 'git_commit' in fm

        if has_jira and has_git:
            score += 10.0
        elif has_jira or has_git:
            score += 5.0

        # 3. 프로젝트/영역 연결 (5점)
        note_type = fm.get('type', '')
        if note_type in ['project', 'projects', 'area']:
            score += 5.0

        return min(score, SCORE_WEIGHTS['actionability'])

    def _get_grade(self, score: float) -> str:
        """점수를 등급으로 변환"""
        for grade, threshold in sorted(SCORE_THRESHOLDS.items(), key=lambda x: -x[1]):
            if score >= threshold:
                return grade
        return 'D'

    def _generate_suggestions(self, scores: Dict[str, float], note: MarkdownNote) -> List[str]:
        """개선 제안 생성"""
        suggestions = []

        # Completeness
        if scores['completeness'] < 20:
            if note.char_count() < 200:
                suggestions.append("내용을 더 추가하세요 (현재 {}자)".format(note.char_count()))
            if not note.get_code_blocks():
                suggestions.append("코드 예시나 실습 예제를 추가하세요")
            if not note.frontmatter:
                suggestions.append("Frontmatter를 추가하세요")

        # Organization
        if scores['organization'] < 20:
            if len(note.get_headings()) < 3:
                suggestions.append("헤딩 구조를 추가하여 내용을 구조화하세요")
            tags = extract_tags(note.content, note.frontmatter)
            if len(tags) < 2:
                suggestions.append("태그를 2개 이상 추가하세요")

        # Connectivity
        if scores['connectivity'] < 15:
            link_count = len(note.get_links())
            needed = max(0, 3 - link_count)
            if needed > 0:
                suggestions.append(f"관련 노트와 내부 링크를 {needed}개 이상 추가하세요")

        # Actionability
        if scores['actionability'] < 15:
            if not has_todo_items(note.content):
                suggestions.append("실행 가능한 TODO 항목을 추가하세요")

        return suggestions

    def score_all_notes(self, folder: Path = None) -> Dict[str, Dict]:
        """
        폴더 내 모든 노트 점수화

        Args:
            folder: 대상 폴더 (None이면 vault 전체)

        Returns:
            {
                'note1.md': {...},
                'note2.md': {...}
            }
        """
        if folder is None:
            folder = self.vault_root

        results = {}

        for md_file in folder.rglob('*.md'):
            # automation 폴더 제외
            if 'automation' in md_file.parts:
                continue

            # 숨김 파일 제외
            if any(part.startswith('.') for part in md_file.parts):
                continue

            try:
                relative_path = str(md_file.relative_to(self.vault_root))
                score_result = self.score_document(md_file)
                results[relative_path] = score_result
            except Exception as e:
                print(f"Error scoring {md_file}: {e}")
                continue

        return results
