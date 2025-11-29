"""
Link Suggester

관련 노트를 찾아 자동으로 링크를 제안합니다.
"""

from pathlib import Path
from typing import Dict, List, Set
from collections import Counter
from ..utils.markdown_utils import (
    MarkdownNote,
    extract_keywords,
    extract_tags,
    get_note_relative_path
)
from .config import AUTO_LINK_CONFIG


class LinkSuggester:
    """자동 링크 제안기"""

    def __init__(self, vault_root: Path):
        self.vault_root = vault_root
        self._note_cache: Dict[str, MarkdownNote] = {}
        self._keyword_index: Dict[str, Set[str]] = {}
        self._tag_index: Dict[str, Set[str]] = {}

    def build_index(self):
        """
        전체 노트 인덱스 구축
        (초기 한 번 실행하면 빠르게 검색 가능)
        """
        print("Building note index...")
        self._note_cache.clear()
        self._keyword_index.clear()
        self._tag_index.clear()

        for md_file in self.vault_root.rglob('*.md'):
            # 제외 패턴
            if self._should_exclude(md_file):
                continue

            try:
                note = MarkdownNote(md_file)
                rel_path = get_note_relative_path(self.vault_root, md_file)

                # 캐시 저장
                self._note_cache[rel_path] = note

                # 키워드 인덱스
                keywords = extract_keywords(note.content, top_n=10)
                for kw in keywords:
                    if kw not in self._keyword_index:
                        self._keyword_index[kw] = set()
                    self._keyword_index[kw].add(rel_path)

                # 태그 인덱스
                tags = extract_tags(note.content, note.frontmatter)
                for tag in tags:
                    if tag not in self._tag_index:
                        self._tag_index[tag] = set()
                    self._tag_index[tag].add(rel_path)

            except Exception as e:
                print(f"Error indexing {md_file}: {e}")
                continue

        print(f"Indexed {len(self._note_cache)} notes")

    def suggest_links(self, note_path: Path, max_suggestions: int = None) -> List[Dict]:
        """
        관련 노트 링크 제안

        Args:
            note_path: 대상 노트 경로
            max_suggestions: 최대 제안 개수

        Returns:
            [
                {
                    'path': '01-Projects/Note.md',
                    'title': 'Related Note',
                    'similarity': 0.75,
                    'reasons': ['같은 태그: snowflake', ...]
                }
            ]
        """
        if max_suggestions is None:
            max_suggestions = AUTO_LINK_CONFIG['max_suggestions']

        # 인덱스 없으면 구축
        if not self._note_cache:
            self.build_index()

        note = MarkdownNote(note_path)
        current_path = get_note_relative_path(self.vault_root, note_path)

        # 현재 노트의 특징 추출
        keywords = extract_keywords(note.content, top_n=10)
        tags = extract_tags(note.content, note.frontmatter)
        existing_links = set(note.get_links())

        # 후보 노트들과 유사도 계산
        candidates = {}

        # 1. 태그 기반 후보
        for tag in tags:
            if tag in self._tag_index:
                for candidate_path in self._tag_index[tag]:
                    if candidate_path != current_path and candidate_path not in existing_links:
                        if candidate_path not in candidates:
                            candidates[candidate_path] = {'score': 0, 'reasons': []}
                        candidates[candidate_path]['score'] += 0.3
                        candidates[candidate_path]['reasons'].append(f'같은 태그: #{tag}')

        # 2. 키워드 기반 후보
        keyword_matches = Counter()
        for kw in keywords:
            if kw in self._keyword_index:
                for candidate_path in self._keyword_index[kw]:
                    if candidate_path != current_path and candidate_path not in existing_links:
                        keyword_matches[candidate_path] += 1

        for candidate_path, match_count in keyword_matches.items():
            if match_count >= AUTO_LINK_CONFIG['min_keyword_match']:
                if candidate_path not in candidates:
                    candidates[candidate_path] = {'score': 0, 'reasons': []}
                score_boost = min(match_count * 0.15, 0.5)
                candidates[candidate_path]['score'] += score_boost
                candidates[candidate_path]['reasons'].append(
                    f'{match_count}개 키워드 매칭'
                )

        # 3. 같은 폴더 보너스
        current_folder = Path(current_path).parent
        for candidate_path in candidates:
            candidate_folder = Path(candidate_path).parent
            if candidate_folder == current_folder:
                candidates[candidate_path]['score'] += 0.2
                candidates[candidate_path]['reasons'].append('같은 폴더')

        # 최소 점수 필터링
        min_score = AUTO_LINK_CONFIG['min_similarity_score']
        filtered_candidates = {
            path: data for path, data in candidates.items()
            if data['score'] >= min_score
        }

        # 점수순 정렬
        sorted_candidates = sorted(
            filtered_candidates.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )[:max_suggestions]

        # 결과 생성
        suggestions = []
        for candidate_path, data in sorted_candidates:
            candidate_note = self._note_cache.get(candidate_path)
            if candidate_note:
                title = candidate_note.frontmatter.get('title', Path(candidate_path).stem)
                suggestions.append({
                    'path': candidate_path,
                    'title': title,
                    'similarity': round(data['score'], 2),
                    'reasons': data['reasons']
                })

        return suggestions

    def find_backlinks(self, note_path: Path) -> List[Dict]:
        """
        이 노트를 링크하는 다른 노트들 찾기 (백링크)

        Returns:
            [
                {
                    'path': '01-Projects/Note.md',
                    'title': 'Note Title'
                }
            ]
        """
        if not self._note_cache:
            self.build_index()

        target_path = get_note_relative_path(self.vault_root, note_path)
        target_name = Path(target_path).stem

        backlinks = []

        for note_path_str, note in self._note_cache.items():
            links = note.get_links()
            # [[target]] 또는 [[target.md]] 형식 확인
            if any(target_name in link or target_path in link for link in links):
                title = note.frontmatter.get('title', Path(note_path_str).stem)
                backlinks.append({
                    'path': note_path_str,
                    'title': title
                })

        return backlinks

    def find_orphaned_notes(self) -> List[Dict]:
        """
        고아 노트 찾기 (링크가 없는 노트)

        Returns:
            [
                {
                    'path': '01-Projects/Orphan.md',
                    'title': 'Orphan Note'
                }
            ]
        """
        if not self._note_cache:
            self.build_index()

        orphans = []

        for note_path, note in self._note_cache.items():
            # 링크가 없는지 확인
            outgoing_links = len(note.get_links())
            incoming_links = len(self.find_backlinks(
                self.vault_root / note_path
            ))

            if outgoing_links == 0 and incoming_links == 0:
                title = note.frontmatter.get('title', Path(note_path).stem)
                orphans.append({
                    'path': note_path,
                    'title': title,
                    'outgoing': outgoing_links,
                    'incoming': incoming_links
                })

        return orphans

    def _should_exclude(self, file_path: Path) -> bool:
        """파일 제외 여부"""
        # automation 폴더
        if 'automation' in file_path.parts:
            return True

        # 숨김 파일/폴더
        if any(part.startswith('.') for part in file_path.parts):
            return True

        # 제외 패턴
        name = file_path.name
        for pattern in AUTO_LINK_CONFIG['exclude_patterns']:
            if pattern.lower() in name.lower():
                return True

        return False

    def generate_network_stats(self) -> Dict:
        """
        네트워크 통계 생성

        Returns:
            {
                'total_notes': 150,
                'total_links': 450,
                'avg_links_per_note': 3.0,
                'orphaned_notes': 10,
                'most_linked': [...]
            }
        """
        if not self._note_cache:
            self.build_index()

        total_notes = len(self._note_cache)
        total_links = 0
        link_counts = {}

        for note_path, note in self._note_cache.items():
            link_count = len(note.get_links())
            total_links += link_count
            link_counts[note_path] = link_count

        avg_links = total_links / total_notes if total_notes > 0 else 0

        # 가장 많이 링크된 노트 (상위 10개)
        most_linked = sorted(
            link_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        most_linked_formatted = [
            {
                'path': path,
                'title': self._note_cache[path].frontmatter.get('title', Path(path).stem),
                'link_count': count
            }
            for path, count in most_linked
        ]

        orphaned_count = len(self.find_orphaned_notes())

        return {
            'total_notes': total_notes,
            'total_links': total_links,
            'avg_links_per_note': round(avg_links, 2),
            'orphaned_notes': orphaned_count,
            'most_linked': most_linked_formatted
        }
