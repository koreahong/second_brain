"""
Document Curator Agent

문서를 종합적으로 분석하고 정리하는 메인 에이전트
"""

from pathlib import Path
from typing import Dict, List
from datetime import datetime
from ..core.document_scorer import DocumentQualityScorer
from ..core.note_classifier import NoteClassifier
from ..core.link_suggester import LinkSuggester
from ..utils.markdown_utils import MarkdownNote


class DocumentCurator:
    """문서 큐레이션 에이전트"""

    def __init__(self, vault_root: Path):
        self.vault_root = vault_root
        self.scorer = DocumentQualityScorer(vault_root)
        self.classifier = NoteClassifier(vault_root)
        self.link_suggester = LinkSuggester(vault_root)

    def curate_document(self, note_path: Path, auto_update: bool = False) -> Dict:
        """
        문서 종합 분석 및 큐레이션

        Args:
            note_path: 노트 경로
            auto_update: True면 frontmatter 자동 업데이트

        Returns:
            {
                'score': {...},
                'classification': {...},
                'link_suggestions': [...],
                'permanent_note_suggestions': [...],
                'actions': [...]
            }
        """
        print(f"📝 Curating: {note_path.name}")

        # 1. 품질 점수
        score_result = self.scorer.score_document(note_path)
        print(f"   Score: {score_result['total_score']}/100 ({score_result['grade']})")

        # 2. 노트 분류
        classification = self.classifier.classify(note_path)
        print(f"   Type: {classification['note_type']} (confidence: {classification['confidence']:.2f})")

        # 3. 링크 제안
        link_suggestions = self.link_suggester.suggest_links(note_path)
        print(f"   Link suggestions: {len(link_suggestions)}")

        # 4. Permanent Note 추출 제안
        permanent_note_suggestions = []
        if classification['note_type'] == 'project' and score_result['grade'] in ['A', 'S']:
            permanent_note_suggestions = self.classifier.suggest_permanent_notes(note_path)
            print(f"   Permanent note candidates: {len(permanent_note_suggestions)}")

        # 5. 액션 생성
        actions = self._generate_actions(
            note_path,
            score_result,
            classification,
            link_suggestions,
            permanent_note_suggestions
        )

        # 6. Frontmatter 업데이트 (선택)
        if auto_update:
            self._update_frontmatter(
                note_path,
                score_result,
                classification,
                link_suggestions
            )
            print(f"   ✓ Frontmatter updated")

        return {
            'score': score_result,
            'classification': classification,
            'link_suggestions': link_suggestions,
            'permanent_note_suggestions': permanent_note_suggestions,
            'actions': actions
        }

    def curate_folder(self, folder_path: Path, auto_update: bool = False) -> Dict:
        """
        폴더 내 모든 문서 큐레이션

        Returns:
            {
                'total_notes': 50,
                'processed': 48,
                'failed': 2,
                'results': {...}
            }
        """
        results = {}
        failed = []

        md_files = list(folder_path.rglob('*.md'))
        total = len(md_files)

        print(f"\n🗂️  Curating folder: {folder_path}")
        print(f"   Found {total} markdown files\n")

        for i, md_file in enumerate(md_files, 1):
            # automation 폴더 제외
            if 'automation' in md_file.parts:
                continue

            # 숨김 파일 제외
            if any(part.startswith('.') for part in md_file.parts):
                continue

            try:
                print(f"[{i}/{total}] ", end='')
                result = self.curate_document(md_file, auto_update)
                rel_path = str(md_file.relative_to(self.vault_root))
                results[rel_path] = result
            except Exception as e:
                print(f"   ✗ Error: {e}")
                failed.append(str(md_file))

        print(f"\n✓ Processed: {len(results)}")
        print(f"✗ Failed: {len(failed)}")

        return {
            'total_notes': total,
            'processed': len(results),
            'failed': len(failed),
            'failed_files': failed,
            'results': results
        }

    def _generate_actions(
        self,
        note_path: Path,
        score_result: Dict,
        classification: Dict,
        link_suggestions: List,
        permanent_suggestions: List
    ) -> List[Dict]:
        """액션 아이템 생성"""
        actions = []

        grade = score_result['grade']
        note_type = classification['note_type']

        # 1. 저품질 문서 → Inbox 이동
        if grade == 'D':
            actions.append({
                'type': 'move_to_inbox',
                'priority': 'high',
                'message': f'D등급 문서입니다. Inbox로 이동하여 재작성하세요',
                'target': '00-Inbox'
            })

        # 2. 위치 부적절 → 이동 제안
        if not classification['is_well_placed']:
            actions.append({
                'type': 'relocate',
                'priority': 'medium',
                'message': f"{note_type} 타입이므로 {classification['suggested_location']}로 이동 권장",
                'target': classification['suggested_location']
            })

        # 3. 링크 추가
        if link_suggestions:
            actions.append({
                'type': 'add_links',
                'priority': 'medium',
                'message': f'{len(link_suggestions)}개 관련 노트와 링크 추가 가능',
                'suggestions': link_suggestions[:3]  # 상위 3개만
            })

        # 4. Permanent Note 추출
        if permanent_suggestions:
            actions.append({
                'type': 'extract_permanent_notes',
                'priority': 'high',
                'message': f'{len(permanent_suggestions)}개 영구 지식 추출 가능',
                'suggestions': permanent_suggestions
            })

        # 5. 점수 향상 제안
        if score_result['suggestions']:
            actions.append({
                'type': 'improve_quality',
                'priority': 'low',
                'message': '품질 개선 제안',
                'suggestions': score_result['suggestions']
            })

        return actions

    def _update_frontmatter(
        self,
        note_path: Path,
        score_result: Dict,
        classification: Dict,
        link_suggestions: List
    ):
        """Frontmatter 자동 업데이트"""
        note = MarkdownNote(note_path)

        # 품질 점수
        note.update_frontmatter(
            quality_score=score_result['total_score'],
            quality_grade=score_result['grade'],
            quality_last_updated=datetime.now().strftime('%Y-%m-%d')
        )

        # 노트 타입
        note.update_frontmatter(
            note_type=classification['note_type'],
            note_type_confidence=round(classification['confidence'], 2)
        )

        # 연결성
        note.update_frontmatter(
            related_notes_count=len(link_suggestions),
            backlinks_count=len(self.link_suggester.find_backlinks(note_path)),
            orphaned=(len(link_suggestions) == 0)
        )

        # 큐레이션 메타데이터
        note.update_frontmatter(
            curator_last_run=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            curator_version='1.0.0'
        )

        # 저장
        note.save()

    def generate_summary_report(self, results: Dict) -> str:
        """큐레이션 결과 요약 리포트"""
        if 'results' not in results:
            return "No results to summarize"

        notes = results['results']
        total = len(notes)

        if total == 0:
            return "No notes processed"

        # 등급 분포
        grade_dist = {}
        for data in notes.values():
            grade = data['score']['grade']
            grade_dist[grade] = grade_dist.get(grade, 0) + 1

        # 타입 분포
        type_dist = {}
        for data in notes.values():
            note_type = data['classification']['note_type']
            type_dist[note_type] = type_dist.get(note_type, 0) + 1

        # 액션 통계
        total_actions = sum(len(data['actions']) for data in notes.values())

        report = f"""
📊 Curation Summary Report
{'='*50}

Total Notes: {total}
Processed: {results['processed']}
Failed: {results['failed']}

Grade Distribution:
"""
        for grade in ['S', 'A', 'B', 'C', 'D']:
            count = grade_dist.get(grade, 0)
            pct = (count / total * 100) if total > 0 else 0
            report += f"  {grade}: {count:3d} ({pct:5.1f}%)\n"

        report += "\nNote Type Distribution:\n"
        for note_type, count in sorted(type_dist.items()):
            pct = (count / total * 100) if total > 0 else 0
            report += f"  {note_type}: {count:3d} ({pct:5.1f}%)\n"

        report += f"\nTotal Actions Generated: {total_actions}\n"

        return report
