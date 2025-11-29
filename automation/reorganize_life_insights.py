#!/usr/bin/env python3
"""
Life-Insights Reorganizer
Automatically categorize 222 root-level files based on content analysis
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
import yaml

@dataclass
class NoteClassification:
    filepath: Path
    category: str  # 'Work', 'Personal', 'Observations'
    confidence: float
    reasons: List[str]
    suggested_location: Path

class LifeInsightsOrganizer:
    def __init__(self, vault_root: Path):
        self.vault_root = vault_root
        self.life_insights_root = vault_root / "30-Flow" / "Life-Insights"

        # Classification keywords
        self.work_keywords = [
            # Company/Team
            "크래프트", "데니스", "마빈", "레아", "패트릭", "팀",
            "현대", "홈쇼핑", "오토에버", "고위드", "나이스평가정보",
            "대표님", "팀장", "책임", "PM", "PO",

            # Work activities
            "프로젝트", "업무", "보고", "회의", "미팅", "발표",
            "고객", "클라이언트", "요구사항", "마감", "딜리버리",
            "커뮤니케이션", "소통", "협업",

            # Technical
            "데이터", "파이프라인", "DB", "서버", "크롤러",
            "리포트", "대시보드", "Power BI", "SQL",
            "코드", "개발", "테스트", "배포",

            # Work emotions/situations
            "성과", "목표", "계획", "KPI", "평가",
            "퇴사", "이직", "면접", "연봉",
        ]

        self.personal_keywords = [
            # Relationships
            "규리미", "규림", "엄마", "아빠", "형", "부모님",
            "가족", "연인", "결혼", "데이트", "만남",

            # Personal activities
            "운동", "헬스", "마라톤", "등반",
            "콘서트", "여행", "롯데월드",
            "건강", "다이어트", "살",

            # Emotions
            "사랑", "그리움", "외로움", "행복",
            "책임", "선택", "결심",
        ]

        self.observation_keywords = [
            # Abstract concepts
            "생각", "깨달은", "느낀", "배운",
            "본질", "철학", "관점", "시각",
            "인생", "삶", "가치", "의미",

            # General principles
            "사람", "인간", "관계", "사회",
            "시간", "돈", "성공", "실패",
            "습관", "태도", "마인드",
            "성장", "변화", "발전",
        ]

    def read_frontmatter(self, filepath: Path) -> Dict:
        """Extract YAML frontmatter from markdown file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for frontmatter
            if not content.startswith('---'):
                return {}

            # Extract frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}

            frontmatter_text = parts[1]
            return yaml.safe_load(frontmatter_text) or {}

        except Exception as e:
            print(f"⚠️  Error reading {filepath.name}: {e}")
            return {}

    def read_content(self, filepath: Path) -> str:
        """Read markdown content without frontmatter"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    return parts[2].strip()

            return content

        except Exception as e:
            print(f"⚠️  Error reading {filepath.name}: {e}")
            return ""

    def classify_note(self, filepath: Path) -> NoteClassification:
        """Classify a note based on content and metadata"""

        frontmatter = self.read_frontmatter(filepath)
        content = self.read_content(filepath)

        # Combine title + content for analysis
        title = frontmatter.get('title', filepath.stem)
        full_text = f"{title} {content}".lower()

        # Count keyword matches
        work_score = sum(1 for kw in self.work_keywords if kw.lower() in full_text)
        personal_score = sum(1 for kw in self.personal_keywords if kw.lower() in full_text)
        observation_score = sum(1 for kw in self.observation_keywords if kw.lower() in full_text)

        # Additional signals from frontmatter
        fm_signals = []

        # Check specific frontmatter fields
        if '회고종류' in frontmatter:
            if frontmatter['회고종류'] in ['하루일기', '일일회고']:
                # These are often work-related daily reflections
                work_score += 2
                fm_signals.append(f"회고종류: {frontmatter['회고종류']}")

        # Check 일기 field for work clues
        if '일기' in frontmatter:
            diary_content = str(frontmatter['일기']).lower()
            if any(kw in diary_content for kw in ['팀', '프로젝트', '업무', '회의']):
                work_score += 3
                fm_signals.append("일기 필드에 업무 키워드")

        # Determine category
        scores = {
            'Work': work_score,
            'Personal': personal_score,
            'Observations': observation_score
        }

        category = max(scores, key=scores.get)
        max_score = scores[category]
        confidence = max_score / (sum(scores.values()) + 1)  # Avoid division by zero

        # Build reasons
        reasons = []
        if work_score > 0:
            reasons.append(f"Work keywords: {work_score}")
        if personal_score > 0:
            reasons.append(f"Personal keywords: {personal_score}")
        if observation_score > 0:
            reasons.append(f"Observation keywords: {observation_score}")
        reasons.extend(fm_signals)

        # Determine suggested location
        if category == 'Work':
            suggested_location = self.life_insights_root / "Work" / filepath.name
        elif category == 'Personal':
            suggested_location = self.life_insights_root / "Personal" / filepath.name
        else:  # Observations
            suggested_location = self.life_insights_root / "Observations" / filepath.name

        return NoteClassification(
            filepath=filepath,
            category=category,
            confidence=confidence,
            reasons=reasons,
            suggested_location=suggested_location
        )

    def classify_all_root_files(self) -> List[NoteClassification]:
        """Classify all markdown files in Life-Insights root"""

        root_files = [
            f for f in self.life_insights_root.iterdir()
            if f.is_file() and f.suffix == '.md'
        ]

        print(f"📊 Found {len(root_files)} root-level files to classify\n")

        classifications = []
        for filepath in root_files:
            classification = self.classify_note(filepath)
            classifications.append(classification)

        return classifications

    def generate_report(self, classifications: List[NoteClassification]) -> str:
        """Generate classification report"""

        # Group by category
        by_category = {'Work': [], 'Personal': [], 'Observations': []}
        for c in classifications:
            by_category[c.category].append(c)

        report = "# Life-Insights Classification Report\n\n"

        report += f"**Total Files:** {len(classifications)}\n\n"

        for category, items in by_category.items():
            report += f"## {category} ({len(items)} files)\n\n"

            # Show high-confidence classifications
            high_conf = [c for c in items if c.confidence > 0.5]
            low_conf = [c for c in items if c.confidence <= 0.5]

            if high_conf:
                report += f"### High Confidence ({len(high_conf)})\n"
                for c in high_conf[:10]:  # Show first 10
                    report += f"- {c.filepath.name} (conf: {c.confidence:.2f})\n"
                    report += f"  - {', '.join(c.reasons[:3])}\n"
                if len(high_conf) > 10:
                    report += f"  - ... and {len(high_conf)-10} more\n"
                report += "\n"

            if low_conf:
                report += f"### Low Confidence - Review Needed ({len(low_conf)})\n"
                for c in low_conf[:5]:  # Show first 5
                    report += f"- {c.filepath.name} (conf: {c.confidence:.2f})\n"
                if len(low_conf) > 5:
                    report += f"  - ... and {len(low_conf)-5} more\n"
                report += "\n"

        return report

    def move_files(self, classifications: List[NoteClassification], dry_run: bool = True):
        """Move files to their classified locations"""

        print("\n" + "="*60)
        if dry_run:
            print("DRY RUN - No files will be moved")
        else:
            print("MOVING FILES")
        print("="*60 + "\n")

        moved = 0
        for c in classifications:
            # Skip low-confidence in actual run
            if not dry_run and c.confidence < 0.3:
                print(f"⏭️  Skipping (low conf): {c.filepath.name}")
                continue

            if dry_run:
                print(f"{'✓' if c.confidence > 0.5 else '?'} {c.filepath.name} → {c.category}/")
                print(f"   Confidence: {c.confidence:.2f} | {', '.join(c.reasons[:2])}")
            else:
                try:
                    # Ensure target directory exists
                    c.suggested_location.parent.mkdir(parents=True, exist_ok=True)

                    # Move file
                    c.filepath.rename(c.suggested_location)
                    print(f"✅ Moved: {c.filepath.name} → {c.category}/")
                    moved += 1

                except Exception as e:
                    print(f"❌ Error moving {c.filepath.name}: {e}")

        print(f"\n{'Preview:' if dry_run else 'Moved:'} {moved if not dry_run else len([c for c in classifications if c.confidence > 0.3])} files")

        if dry_run:
            print("\n💡 Run with --execute to actually move files")

    def interactive_review(self, classifications: List[NoteClassification]):
        """Interactively review low-confidence classifications"""

        low_conf = [c for c in classifications if c.confidence < 0.5]

        if not low_conf:
            print("✅ All classifications have high confidence!")
            return classifications

        print(f"\n📋 Reviewing {len(low_conf)} low-confidence classifications\n")

        for c in low_conf:
            print(f"\n📄 {c.filepath.name}")
            print(f"   Suggested: {c.category} (confidence: {c.confidence:.2f})")
            print(f"   Reasons: {', '.join(c.reasons)}")

            # Show a snippet of content
            content = self.read_content(c.filepath)
            snippet = content[:200] + "..." if len(content) > 200 else content
            print(f"\n   Preview: {snippet}\n")

            choice = input(f"   Keep as {c.category}? (y/n/w=Work/p=Personal/o=Observations/s=skip): ").lower()

            if choice == 'y':
                continue
            elif choice == 'w':
                c.category = 'Work'
                c.suggested_location = self.life_insights_root / "Work" / c.filepath.name
            elif choice == 'p':
                c.category = 'Personal'
                c.suggested_location = self.life_insights_root / "Personal" / c.filepath.name
            elif choice == 'o':
                c.category = 'Observations'
                c.suggested_location = self.life_insights_root / "Observations" / c.filepath.name
            elif choice == 's':
                print("   ⏭️  Skipped")
                c.confidence = 0  # Mark for skipping

        return classifications

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Reorganize Life-Insights notes')
    parser.add_argument('--execute', action='store_true', help='Actually move files (default: dry run)')
    parser.add_argument('--interactive', action='store_true', help='Interactively review low-confidence items')
    parser.add_argument('--report', type=str, help='Save classification report to file')

    args = parser.parse_args()

    # Initialize
    vault_root = Path(__file__).parent.parent
    organizer = LifeInsightsOrganizer(vault_root)

    # Classify
    print("🔍 Classifying notes...\n")
    classifications = organizer.classify_all_root_files()

    # Generate report
    report = organizer.generate_report(classifications)
    print("\n" + report)

    if args.report:
        report_path = Path(args.report)
        report_path.write_text(report, encoding='utf-8')
        print(f"\n💾 Report saved: {report_path}")

    # Interactive review if requested
    if args.interactive:
        classifications = organizer.interactive_review(classifications)

    # Move files
    organizer.move_files(classifications, dry_run=not args.execute)

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    by_category = {'Work': 0, 'Personal': 0, 'Observations': 0}
    for c in classifications:
        by_category[c.category] += 1

    for category, count in by_category.items():
        print(f"{category}: {count} files")

    print(f"\nTotal: {len(classifications)} files")

if __name__ == '__main__':
    main()
