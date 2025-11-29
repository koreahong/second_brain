"""
Weekly Review Agent

주간 문서 분석 및 리포트 생성
"""

from pathlib import Path
from typing import Dict, List
from datetime import datetime, timedelta
from collections import Counter
from ..core.document_scorer import DocumentQualityScorer
from ..core.note_classifier import NoteClassifier
from ..core.link_suggester import LinkSuggester
from ..utils.markdown_utils import MarkdownNote
from ..core.config import WEEKLY_REVIEW_CONFIG, FOLDERS


class WeeklyReviewer:
    """주간 리뷰 에이전트"""

    def __init__(self, vault_root: Path):
        self.vault_root = vault_root
        self.scorer = DocumentQualityScorer(vault_root)
        self.classifier = NoteClassifier(vault_root)
        self.link_suggester = LinkSuggester(vault_root)

    def generate_weekly_report(self, week: str = None) -> Dict:
        """
        주간 리포트 생성

        Args:
            week: YYYY-WXX 형식 (예: 2025-W48)

        Returns:
            {
                'period': '2025-W48',
                'statistics': {...},
                'top_documents': [...],
                'needs_attention': {...},
                'network_insights': {...},
                'recommendations': [...]
            }
        """
        if week is None:
            week = self._get_current_week()

        print(f"\n📅 Generating Weekly Report for {week}")
        print("="*50)

        # 1. 통계
        print("\n1️⃣  Calculating statistics...")
        statistics = self._calculate_statistics()

        # 2. 우수 문서
        print("2️⃣  Finding top documents...")
        top_documents = self._get_top_documents()

        # 3. 주의 필요 문서
        print("3️⃣  Identifying documents needing attention...")
        needs_attention = self._find_documents_needing_attention()

        # 4. 네트워크 분석
        print("4️⃣  Analyzing knowledge network...")
        network_insights = self._analyze_network()

        # 5. 개선 제안
        print("5️⃣  Generating recommendations...")
        recommendations = self._generate_recommendations(
            statistics,
            needs_attention,
            network_insights
        )

        report = {
            'period': week,
            'generated_at': datetime.now().isoformat(),
            'statistics': statistics,
            'top_documents': top_documents,
            'needs_attention': needs_attention,
            'network_insights': network_insights,
            'recommendations': recommendations
        }

        print("\n✓ Weekly report generated successfully\n")
        return report

    def _calculate_statistics(self) -> Dict:
        """전체 통계 계산"""
        all_notes = {}
        new_this_week = []
        grade_dist = Counter()
        type_dist = Counter()

        for md_file in self.vault_root.rglob('*.md'):
            if self._should_exclude(md_file):
                continue

            try:
                note = MarkdownNote(md_file)

                # 점수 계산
                score_result = self.scorer.score_document(md_file)
                grade = score_result['grade']
                grade_dist[grade] += 1

                # 타입 분류
                classification = self.classifier.classify(md_file)
                note_type = classification['note_type']
                type_dist[note_type] += 1

                # 이번 주 생성 여부
                if self._is_created_this_week(note, md_file):
                    new_this_week.append(str(md_file.relative_to(self.vault_root)))

                all_notes[str(md_file.relative_to(self.vault_root))] = {
                    'score': score_result['total_score'],
                    'grade': grade,
                    'type': note_type
                }

            except Exception as e:
                continue

        # 평균 점수
        total_score = sum(data['score'] for data in all_notes.values())
        avg_score = total_score / len(all_notes) if all_notes else 0

        return {
            'total_notes': len(all_notes),
            'new_this_week': len(new_this_week),
            'new_notes_list': new_this_week[:10],  # 최대 10개만
            'average_score': round(avg_score, 1),
            'grade_distribution': dict(grade_dist),
            'type_distribution': dict(type_dist)
        }

    def _get_top_documents(self, limit: int = 10) -> List[Dict]:
        """우수 문서 찾기"""
        scored_notes = []

        for md_file in self.vault_root.rglob('*.md'):
            if self._should_exclude(md_file):
                continue

            try:
                score_result = self.scorer.score_document(md_file)
                note = MarkdownNote(md_file)

                scored_notes.append({
                    'path': str(md_file.relative_to(self.vault_root)),
                    'title': note.frontmatter.get('title', md_file.stem),
                    'score': score_result['total_score'],
                    'grade': score_result['grade']
                })
            except Exception:
                continue

        # 점수순 정렬
        top_notes = sorted(scored_notes, key=lambda x: x['score'], reverse=True)[:limit]
        return top_notes

    def _find_documents_needing_attention(self) -> Dict:
        """주의 필요 문서 찾기"""
        config = WEEKLY_REVIEW_CONFIG

        low_score = []
        orphaned = []
        stale = []
        unclassified_inbox = []

        # Link suggester 인덱스 구축
        self.link_suggester.build_index()

        for md_file in self.vault_root.rglob('*.md'):
            if self._should_exclude(md_file):
                continue

            try:
                note = MarkdownNote(md_file)
                rel_path = str(md_file.relative_to(self.vault_root))

                # 1. 저품질 문서
                score_result = self.scorer.score_document(md_file)
                if score_result['total_score'] < config['low_score_threshold']:
                    low_score.append({
                        'path': rel_path,
                        'title': note.frontmatter.get('title', md_file.stem),
                        'score': score_result['total_score']
                    })

                # 2. 고아 노트
                backlinks = self.link_suggester.find_backlinks(md_file)
                outgoing = len(note.get_links())
                if outgoing == 0 and len(backlinks) == 0:
                    orphaned.append({
                        'path': rel_path,
                        'title': note.frontmatter.get('title', md_file.stem)
                    })

                # 3. 오래된 문서
                days_old = self._days_since_modified(md_file)
                if days_old > config['stale_days']:
                    stale.append({
                        'path': rel_path,
                        'title': note.frontmatter.get('title', md_file.stem),
                        'days_old': days_old
                    })

                # 4. Inbox에 오래 머물러 있는 노트
                if rel_path.startswith(FOLDERS['inbox']):
                    days_in_inbox = self._days_since_created(md_file)
                    if days_in_inbox > 7:  # 7일 이상
                        unclassified_inbox.append({
                            'path': rel_path,
                            'title': note.frontmatter.get('title', md_file.stem),
                            'days_in_inbox': days_in_inbox
                        })

            except Exception:
                continue

        return {
            'low_score': sorted(low_score, key=lambda x: x['score'])[:20],
            'orphaned': orphaned[:20],
            'stale': sorted(stale, key=lambda x: x['days_old'], reverse=True)[:20],
            'unclassified_inbox': sorted(unclassified_inbox, key=lambda x: x['days_in_inbox'], reverse=True)
        }

    def _analyze_network(self) -> Dict:
        """지식 네트워크 분석"""
        # Link suggester 사용
        if not self.link_suggester._note_cache:
            self.link_suggester.build_index()

        network_stats = self.link_suggester.generate_network_stats()

        # 추가 분석
        # 1. 허브 노트 (가장 많이 참조되는 노트)
        hubs = network_stats['most_linked'][:5]

        # 2. 클러스터 분석 (태그 기반)
        tag_clusters = self._analyze_tag_clusters()

        return {
            **network_stats,
            'hub_notes': hubs,
            'tag_clusters': tag_clusters
        }

    def _analyze_tag_clusters(self) -> List[Dict]:
        """태그 기반 클러스터 분석"""
        tag_index = self.link_suggester._tag_index

        clusters = []
        for tag, note_paths in tag_index.items():
            if len(note_paths) >= 3:  # 3개 이상 노트가 있는 태그만
                clusters.append({
                    'tag': tag,
                    'note_count': len(note_paths),
                    'notes': list(note_paths)[:5]  # 상위 5개만
                })

        # 노트 개수순 정렬
        return sorted(clusters, key=lambda x: x['note_count'], reverse=True)[:10]

    def _generate_recommendations(
        self,
        statistics: Dict,
        needs_attention: Dict,
        network_insights: Dict
    ) -> List[Dict]:
        """개선 제안 생성"""
        recommendations = []

        # 1. Inbox 정리
        inbox_count = len(needs_attention['unclassified_inbox'])
        if inbox_count >= WEEKLY_REVIEW_CONFIG['inbox_warning_count']:
            recommendations.append({
                'type': 'cleanup_inbox',
                'priority': 'high',
                'message': f'Inbox에 {inbox_count}개 노트가 쌓여 있습니다',
                'action': '10분 투자해서 분류하세요',
                'estimated_time': '10분'
            })

        # 2. 고아 노트 연결
        orphan_count = len(needs_attention['orphaned'])
        if orphan_count > 10:
            recommendations.append({
                'type': 'connect_orphans',
                'priority': 'medium',
                'message': f'{orphan_count}개 고아 노트 발견',
                'action': '관련 노트와 링크 연결',
                'affected_notes': needs_attention['orphaned'][:5]
            })

        # 3. 저품질 문서 개선
        low_score_count = len(needs_attention['low_score'])
        if low_score_count > 5:
            recommendations.append({
                'type': 'improve_quality',
                'priority': 'low',
                'message': f'{low_score_count}개 저품질 문서',
                'action': '내용 보완 또는 삭제',
                'affected_notes': needs_attention['low_score'][:5]
            })

        # 4. Permanent Note 생성 기회
        # (A/S 등급 프로젝트 노트에서)
        recommendations.append({
            'type': 'create_permanent_notes',
            'priority': 'medium',
            'message': '우수 프로젝트에서 영구 지식 추출',
            'action': '재사용 가능한 개념을 Zettelkasten으로',
        })

        # 5. 네트워크 강화
        avg_links = network_insights['avg_links_per_note']
        if avg_links < 2:
            recommendations.append({
                'type': 'strengthen_network',
                'priority': 'medium',
                'message': f'평균 링크 수가 낮습니다 ({avg_links:.1f}개)',
                'action': '관련 노트들을 더 연결하세요',
                'target': '평균 3개 이상'
            })

        return recommendations

    def save_report(self, report: Dict, output_path: Path = None):
        """리포트를 Markdown 파일로 저장"""
        if output_path is None:
            # 30-Flow/Weekly/ 폴더에 저장
            weekly_folder = self.vault_root / FOLDERS['flow'] / 'Weekly'
            weekly_folder.mkdir(parents=True, exist_ok=True)
            output_path = weekly_folder / f"{report['period']}-Review.md"

        content = self._format_report_markdown(report)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Report saved to: {output_path}")
        return output_path

    def _format_report_markdown(self, report: Dict) -> str:
        """리포트를 Markdown으로 포맷"""
        stats = report['statistics']
        needs = report['needs_attention']
        network = report['network_insights']
        recs = report['recommendations']

        md = f"""---
type: weekly-review
period: {report['period']}
generated: {report['generated_at']}
tags: [review, weekly, knowledge-curator]
---

# 📊 Weekly Knowledge Review: {report['period']}

> **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **System**: Knowledge Curator v1.0.0

---

## 📈 Statistics

**Overall Progress**:
- Total Notes: **{stats['total_notes']}**
- New This Week: **{stats['new_this_week']}**
- Average Score: **{stats['average_score']}/100**

**Grade Distribution**:
"""

        for grade in ['S', 'A', 'B', 'C', 'D']:
            count = stats['grade_distribution'].get(grade, 0)
            pct = (count / stats['total_notes'] * 100) if stats['total_notes'] > 0 else 0
            bar = '█' * int(pct / 5)
            md += f"- {grade}: {count:3d} ({pct:5.1f}%) {bar}\n"

        md += f"\n**Note Type Distribution**:\n"
        for note_type, count in sorted(stats['type_distribution'].items()):
            md += f"- {note_type}: {count}\n"

        md += f"\n---\n\n## 🌟 Top Documents\n\n"
        for i, doc in enumerate(report['top_documents'][:5], 1):
            md += f"{i}. **[{doc['title']}]({doc['path']})** - {doc['score']}/100 ({doc['grade']})\n"

        md += f"\n---\n\n## ⚠️  Needs Attention\n\n"

        if needs['low_score']:
            md += f"### 📉 Low Quality ({len(needs['low_score'])})\n\n"
            for doc in needs['low_score'][:5]:
                md += f"- [{doc['title']}]({doc['path']}) - {doc['score']}/100\n"

        if needs['orphaned']:
            md += f"\n### 🏝️  Orphaned Notes ({len(needs['orphaned'])})\n\n"
            for doc in needs['orphaned'][:5]:
                md += f"- [{doc['title']}]({doc['path']})\n"

        if needs['stale']:
            md += f"\n### 📅 Stale Documents ({len(needs['stale'])})\n\n"
            for doc in needs['stale'][:5]:
                md += f"- [{doc['title']}]({doc['path']}) - {doc['days_old']}일 미수정\n"

        if needs['unclassified_inbox']:
            md += f"\n### 📥 Inbox Backlog ({len(needs['unclassified_inbox'])})\n\n"
            for doc in needs['unclassified_inbox'][:5]:
                md += f"- [{doc['title']}]({doc['path']}) - {doc['days_in_inbox']}일째\n"

        md += f"\n---\n\n## 🕸️  Network Insights\n\n"
        md += f"- Total Links: **{network['total_links']}**\n"
        md += f"- Average Links per Note: **{network['avg_links_per_note']}**\n"
        md += f"- Orphaned Notes: **{network['orphaned_notes']}**\n"

        md += f"\n**Hub Notes** (Most Linked):\n"
        for hub in network['hub_notes'][:5]:
            md += f"- [{hub['title']}]({hub['path']}) - {hub['link_count']} links\n"

        if 'tag_clusters' in network and network['tag_clusters']:
            md += f"\n**Tag Clusters**:\n"
            for cluster in network['tag_clusters'][:5]:
                md += f"- #{cluster['tag']}: {cluster['note_count']} notes\n"

        md += f"\n---\n\n## 💡 Recommendations\n\n"
        for i, rec in enumerate(recs, 1):
            priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
            emoji = priority_emoji.get(rec['priority'], '⚪')
            md += f"### {i}. {emoji} {rec['message']}\n\n"
            md += f"**Priority**: {rec['priority'].upper()}\n\n"
            md += f"**Action**: {rec['action']}\n\n"

            if 'estimated_time' in rec:
                md += f"**Estimated Time**: {rec['estimated_time']}\n\n"

        md += f"\n---\n\n## 📝 Action Items\n\n"
        md += f"- [ ] Review and address recommendations\n"
        md += f"- [ ] Clean up Inbox\n"
        md += f"- [ ] Connect orphaned notes\n"
        md += f"- [ ] Extract permanent notes from completed projects\n"
        md += f"- [ ] Update stale documents or archive them\n"

        md += f"\n---\n\n*Generated by Knowledge Curator* 🤖\n"

        return md

    def _get_current_week(self) -> str:
        """현재 주차 (YYYY-WXX)"""
        now = datetime.now()
        week_num = now.isocalendar()[1]
        return f"{now.year}-W{week_num:02d}"

    def _is_created_this_week(self, note: MarkdownNote, file_path: Path) -> bool:
        """이번 주에 생성된 노트인지 확인"""
        # Frontmatter에서 created 날짜 확인
        created_str = note.frontmatter.get('created') or note.frontmatter.get('imported')

        if created_str:
            try:
                created_date = datetime.fromisoformat(str(created_str).replace('Z', '+00:00'))
                week_ago = datetime.now() - timedelta(days=7)
                return created_date > week_ago
            except:
                pass

        # Frontmatter 없으면 파일 생성 시간
        try:
            created_time = datetime.fromtimestamp(file_path.stat().st_ctime)
            week_ago = datetime.now() - timedelta(days=7)
            return created_time > week_ago
        except:
            return False

    def _days_since_modified(self, file_path: Path) -> int:
        """마지막 수정 후 경과 일수"""
        try:
            modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            delta = datetime.now() - modified_time
            return delta.days
        except:
            return 0

    def _days_since_created(self, file_path: Path) -> int:
        """생성 후 경과 일수"""
        try:
            created_time = datetime.fromtimestamp(file_path.stat().st_ctime)
            delta = datetime.now() - created_time
            return delta.days
        except:
            return 0

    def _should_exclude(self, file_path: Path) -> bool:
        """파일 제외 여부"""
        # automation 폴더
        if 'automation' in file_path.parts:
            return True

        # 숨김 파일/폴더
        if any(part.startswith('.') for part in file_path.parts):
            return True

        return False
