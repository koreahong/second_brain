"""
Knowledge Curator CLI

사용법:
  python -m knowledge_curator.cli.main score [path]
  python -m knowledge_curator.cli.main curate [path] [--auto-update]
  python -m knowledge_curator.cli.main review
  python -m knowledge_curator.cli.main links [path]
"""

import sys
import argparse
from pathlib import Path
from ..agents.document_curator import DocumentCurator
from ..agents.weekly_reviewer import WeeklyReviewer
from ..core.link_suggester import LinkSuggester
from ..core.config import VAULT_ROOT


def score_command(args):
    """점수화 명령"""
    vault_root = Path(args.vault) if args.vault else VAULT_ROOT
    target = Path(args.path) if args.path else vault_root

    curator = DocumentCurator(vault_root)

    if target.is_file():
        # 단일 파일
        result = curator.curate_document(target, auto_update=False)
        print_score_result(result)
    else:
        # 폴더
        results = curator.curate_folder(target, auto_update=False)
        print(curator.generate_summary_report(results))


def curate_command(args):
    """큐레이션 명령"""
    vault_root = Path(args.vault) if args.vault else VAULT_ROOT
    target = Path(args.path) if args.path else vault_root

    curator = DocumentCurator(vault_root)

    if target.is_file():
        result = curator.curate_document(target, auto_update=args.auto_update)
        print_curation_result(result)
    else:
        results = curator.curate_folder(target, auto_update=args.auto_update)
        print(curator.generate_summary_report(results))


def review_command(args):
    """주간 리뷰 명령"""
    vault_root = Path(args.vault) if args.vault else VAULT_ROOT

    reviewer = WeeklyReviewer(vault_root)
    report = reviewer.generate_weekly_report(args.week)

    if args.save:
        output_path = reviewer.save_report(report)
        print(f"\n✓ Report saved to: {output_path}")
    else:
        print_review_report(report)


def links_command(args):
    """링크 제안 명령"""
    vault_root = Path(args.vault) if args.vault else VAULT_ROOT
    target = Path(args.path)

    link_suggester = LinkSuggester(vault_root)

    if args.orphans:
        # 고아 노트 찾기
        orphans = link_suggester.find_orphaned_notes()
        print(f"\n🏝️  Found {len(orphans)} orphaned notes:\n")
        for orphan in orphans[:20]:
            print(f"  - [{orphan['title']}]({orphan['path']})")

    elif args.stats:
        # 네트워크 통계
        stats = link_suggester.generate_network_stats()
        print_network_stats(stats)

    else:
        # 링크 제안
        suggestions = link_suggester.suggest_links(target)
        print(f"\n🔗 Link suggestions for: {target.name}\n")
        for i, sug in enumerate(suggestions, 1):
            print(f"{i}. [{sug['title']}]({sug['path']})")
            print(f"   Similarity: {sug['similarity']}")
            print(f"   Reasons: {', '.join(sug['reasons'])}\n")


def print_score_result(result):
    """점수 결과 출력"""
    score = result['score']
    print(f"\n{'='*60}")
    print(f"📊 Document Quality Score")
    print(f"{'='*60}")
    print(f"\nTotal Score: {score['total_score']}/100 (Grade: {score['grade']})")
    print(f"\nBreakdown:")
    for category, value in score['breakdown'].items():
        print(f"  - {category.capitalize():20s}: {value:5.1f}")

    if score['suggestions']:
        print(f"\n💡 Suggestions:")
        for sug in score['suggestions']:
            print(f"  - {sug}")

    print(f"\n{'='*60}\n")


def print_curation_result(result):
    """큐레이션 결과 출력"""
    print_score_result(result)

    classification = result['classification']
    print(f"📝 Note Type: {classification['note_type']} (confidence: {classification['confidence']:.2f})")
    print(f"📍 Suggested Location: {classification['suggested_location']}")
    print(f"✓ Well Placed: {classification['is_well_placed']}")

    if result['link_suggestions']:
        print(f"\n🔗 Link Suggestions ({len(result['link_suggestions'])}):")
        for sug in result['link_suggestions'][:5]:
            print(f"  - [{sug['title']}]({sug['path']}) - {sug['similarity']}")

    if result['actions']:
        print(f"\n⚡ Actions ({len(result['actions'])}):")
        for action in result['actions']:
            priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
            emoji = priority_emoji.get(action['priority'], '⚪')
            print(f"  {emoji} {action['message']}")


def print_review_report(report):
    """리뷰 리포트 출력 (간단 버전)"""
    stats = report['statistics']
    print(f"\n📅 Weekly Review: {report['period']}")
    print(f"{'='*60}")
    print(f"\nTotal Notes: {stats['total_notes']}")
    print(f"New This Week: {stats['new_this_week']}")
    print(f"Average Score: {stats['average_score']}/100")

    print(f"\nGrade Distribution:")
    for grade in ['S', 'A', 'B', 'C', 'D']:
        count = stats['grade_distribution'].get(grade, 0)
        print(f"  {grade}: {count:3d}")

    print(f"\n💡 Recommendations ({len(report['recommendations'])}):")
    for rec in report['recommendations']:
        print(f"  - {rec['message']}")

    print(f"\n{'='*60}\n")


def print_network_stats(stats):
    """네트워크 통계 출력"""
    print(f"\n🕸️  Knowledge Network Statistics")
    print(f"{'='*60}")
    print(f"\nTotal Notes: {stats['total_notes']}")
    print(f"Total Links: {stats['total_links']}")
    print(f"Avg Links per Note: {stats['avg_links_per_note']}")
    print(f"Orphaned Notes: {stats['orphaned_notes']}")

    print(f"\nMost Linked Notes:")
    for i, note in enumerate(stats['most_linked'][:10], 1):
        print(f"  {i}. [{note['title']}]({note['path']}) - {note['link_count']} links")

    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Knowledge Curator: 세컨드 브레인 자동 정리 시스템'
    )

    parser.add_argument(
        '--vault',
        type=str,
        help='Vault root path (기본: 현재 vault)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # score 명령
    score_parser = subparsers.add_parser('score', help='문서 점수화')
    score_parser.add_argument('path', nargs='?', help='파일 또는 폴더 경로')
    score_parser.set_defaults(func=score_command)

    # curate 명령
    curate_parser = subparsers.add_parser('curate', help='문서 큐레이션')
    curate_parser.add_argument('path', nargs='?', help='파일 또는 폴더 경로')
    curate_parser.add_argument('--auto-update', action='store_true', help='Frontmatter 자동 업데이트')
    curate_parser.set_defaults(func=curate_command)

    # review 명령
    review_parser = subparsers.add_parser('review', help='주간 리뷰 생성')
    review_parser.add_argument('--week', type=str, help='주차 (YYYY-WXX)')
    review_parser.add_argument('--save', action='store_true', help='리포트 저장')
    review_parser.set_defaults(func=review_command)

    # links 명령
    links_parser = subparsers.add_parser('links', help='링크 제안')
    links_parser.add_argument('path', nargs='?', help='노트 경로')
    links_parser.add_argument('--orphans', action='store_true', help='고아 노트 찾기')
    links_parser.add_argument('--stats', action='store_true', help='네트워크 통계')
    links_parser.set_defaults(func=links_command)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 명령 실행
    try:
        args.func(args)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
