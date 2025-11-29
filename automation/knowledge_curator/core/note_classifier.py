"""
Note Type Classifier

노트를 자동으로 분류합니다:
- Fleeting Note: 빠른 메모
- Literature Note: 외부 출처 정리
- Permanent Note: 영구 지식
- Project Note: 프로젝트 관련
"""

from pathlib import Path
from typing import Dict, List, Optional
from ..utils.markdown_utils import MarkdownNote, extract_keywords
from .config import NOTE_TYPE_KEYWORDS, FOLDERS


class NoteClassifier:
    """노트 타입 자동 분류기"""

    def __init__(self, vault_root: Path):
        self.vault_root = vault_root

    def classify(self, note_path: Path) -> Dict:
        """
        노트 타입 분류

        Args:
            note_path: 노트 파일 경로

        Returns:
            {
                'note_type': 'permanent',
                'confidence': 0.85,
                'reasons': [...],
                'suggested_location': '10-Zettelkasten',
                'is_well_placed': True
            }
        """
        note = MarkdownNote(note_path)

        # 각 타입별 점수 계산
        scores = {
            'fleeting': self._score_fleeting(note),
            'literature': self._score_literature(note),
            'permanent': self._score_permanent(note),
            'project': self._score_project(note)
        }

        # 최고 점수 타입 선택
        note_type = max(scores, key=scores.get)
        confidence = scores[note_type]

        # 이유 생성
        reasons = self._generate_reasons(note_type, note)

        # 추천 위치
        suggested_location = self._suggest_location(note_type)

        # 현재 위치가 적절한지 확인
        current_location = self._get_current_location(note_path)
        is_well_placed = self._check_placement(current_location, suggested_location)

        return {
            'note_type': note_type,
            'confidence': confidence,
            'all_scores': scores,
            'reasons': reasons,
            'suggested_location': suggested_location,
            'current_location': current_location,
            'is_well_placed': is_well_placed
        }

    def _score_fleeting(self, note: MarkdownNote) -> float:
        """Fleeting Note 점수 (0-1)"""
        score = 0.0
        config = NOTE_TYPE_KEYWORDS['fleeting']

        # 1. 키워드 매칭 (0.3)
        content_lower = note.content.lower()
        keyword_matches = sum(1 for kw in config['indicators'] if kw in content_lower)
        score += (keyword_matches / len(config['indicators'])) * 0.3

        # 2. 짧은 길이 (0.4)
        char_count = note.char_count()
        if char_count < config['max_length']:
            score += 0.4 * (1 - char_count / config['max_length'])

        # 3. 링크 없음 (0.3)
        link_count = len(note.get_links())
        if link_count == 0:
            score += 0.3

        return score

    def _score_literature(self, note: MarkdownNote) -> float:
        """Literature Note 점수 (0-1)"""
        score = 0.0
        config = NOTE_TYPE_KEYWORDS['literature']

        # 1. 출처 필드 존재 (0.5)
        has_source_field = any(
            field in note.frontmatter
            for field in ['source', 'url', 'link', 'reference']
        )
        if has_source_field:
            score += 0.5

        # 2. 키워드 매칭 (0.3)
        content_lower = note.content.lower()
        keyword_matches = sum(1 for kw in config['indicators'] if kw in content_lower)
        score += (keyword_matches / len(config['indicators'])) * 0.3

        # 3. 구조화 (헤딩, 리스트) (0.2)
        headings = note.get_headings()
        if len(headings) >= 2:
            score += 0.2

        return score

    def _score_permanent(self, note: MarkdownNote) -> float:
        """Permanent Note 점수 (0-1)"""
        score = 0.0
        config = NOTE_TYPE_KEYWORDS['permanent']

        # 1. 충분한 길이 (0.3)
        char_count = note.char_count()
        if char_count >= config['min_length']:
            score += 0.3

        # 2. 링크 존재 (0.3)
        link_count = len(note.get_links())
        if link_count >= config['min_links']:
            score += 0.3

        # 3. 헤딩 구조 (0.2)
        headings = note.get_headings()
        if len(headings) >= 3:
            score += 0.2

        # 4. 독립적 개념 키워드 (0.2)
        content_lower = note.content.lower()
        keyword_matches = sum(1 for kw in config['indicators'] if kw in content_lower)
        score += (keyword_matches / len(config['indicators'])) * 0.2

        return score

    def _score_project(self, note: MarkdownNote) -> float:
        """Project Note 점수 (0-1)"""
        score = 0.0
        config = NOTE_TYPE_KEYWORDS['project']

        # 1. type 필드 확인 (0.4)
        note_type = note.frontmatter.get('type', '').lower()
        if note_type in ['project', 'projects']:
            score += 0.4

        # 2. 프로젝트 키워드 (0.3)
        content_lower = note.content.lower()
        keyword_matches = sum(1 for kw in config['indicators'] if kw in content_lower)
        score += (keyword_matches / len(config['indicators'])) * 0.3

        # 3. 프로젝트 필드들 (0.3)
        project_fields = ['deadline', 'status', 'goal', '목표', '완료']
        field_matches = sum(1 for field in project_fields if field in note.frontmatter)
        score += (field_matches / len(project_fields)) * 0.3

        return score

    def _generate_reasons(self, note_type: str, note: MarkdownNote) -> List[str]:
        """분류 이유 생성"""
        reasons = []

        if note_type == 'fleeting':
            if note.char_count() < 500:
                reasons.append(f"짧은 내용 ({note.char_count()}자)")
            if len(note.get_links()) == 0:
                reasons.append("내부 링크 없음")
            reasons.append("빠른 메모 형식")

        elif note_type == 'literature':
            if any(field in note.frontmatter for field in ['source', 'url']):
                reasons.append("출처 정보 존재")
            if '출처' in note.content or 'source' in note.content.lower():
                reasons.append("출처 관련 내용 포함")
            reasons.append("외부 자료 정리 형식")

        elif note_type == 'permanent':
            if note.char_count() >= 300:
                reasons.append(f"충분한 내용 ({note.char_count()}자)")
            if len(note.get_links()) >= 2:
                reasons.append(f"내부 링크 {len(note.get_links())}개")
            if len(note.get_headings()) >= 3:
                reasons.append("체계적인 구조")
            reasons.append("독립적 지식 형식")

        elif note_type == 'project':
            if note.frontmatter.get('type') == 'project':
                reasons.append("프로젝트 타입 명시")
            if 'deadline' in note.frontmatter:
                reasons.append("마감일 설정")
            reasons.append("프로젝트 관련 내용")

        return reasons

    def _suggest_location(self, note_type: str) -> str:
        """타입에 따른 추천 위치"""
        location_map = {
            'fleeting': FOLDERS['inbox'],
            'literature': FOLDERS['resources'],
            'permanent': FOLDERS['zettelkasten'],
            'project': FOLDERS['projects']
        }
        return location_map.get(note_type, '')

    def _get_current_location(self, note_path: Path) -> str:
        """현재 노트 위치"""
        try:
            rel_path = note_path.relative_to(self.vault_root)
            # 첫 번째 폴더 이름 반환
            if rel_path.parts:
                return rel_path.parts[0]
        except ValueError:
            pass
        return ''

    def _check_placement(self, current: str, suggested: str) -> bool:
        """위치 적절성 확인"""
        if not current or not suggested:
            return False

        # 정확히 일치하거나, 같은 그룹이면 OK
        if current == suggested:
            return True

        # Resources 그룹 (03-Resources, Resources, 자료 등)
        if suggested == FOLDERS['resources']:
            if 'resource' in current.lower() or '자료' in current:
                return True

        # Projects 그룹
        if suggested == FOLDERS['projects']:
            if 'project' in current.lower() or '프로젝트' in current:
                return True

        return False

    def suggest_permanent_notes(self, note_path: Path) -> List[Dict]:
        """
        프로젝트 노트에서 Permanent Note로 추출할 만한 내용 제안

        Returns:
            [
                {
                    'title': 'Snowflake RBAC 패턴',
                    'content_snippet': '...',
                    'keywords': ['snowflake', 'rbac', 'security']
                }
            ]
        """
        note = MarkdownNote(note_path)
        suggestions = []

        # 코드 블록이 많으면 추출 후보
        code_blocks = note.get_code_blocks()
        if len(code_blocks) >= 2:
            keywords = extract_keywords(note.content, top_n=5)
            suggestions.append({
                'title': f"{keywords[0].title() if keywords else '개념'} 패턴",
                'content_snippet': note.content[:200] + '...',
                'keywords': keywords,
                'reason': f'{len(code_blocks)}개 코드 블록 포함'
            })

        # 헤딩이 많으면 섹션별로 추출 가능
        headings = note.get_headings()
        for heading in headings:
            if heading['level'] == 2:  # H2 헤딩
                # 개념/방법/패턴 관련 제목이면 제안
                title_lower = heading['text'].lower()
                if any(kw in title_lower for kw in ['개념', '방법', '패턴', 'concept', 'pattern']):
                    suggestions.append({
                        'title': heading['text'],
                        'content_snippet': '(헤딩 섹션 추출)',
                        'keywords': [heading['text']],
                        'reason': '독립적 개념 섹션'
                    })

        return suggestions[:3]  # 최대 3개
