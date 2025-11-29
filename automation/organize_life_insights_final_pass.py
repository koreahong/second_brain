#!/usr/bin/env python3
"""
Life-Insights Final Pass Classification
Target: 51 remaining files - mostly philosophical observations
"""

import os
from pathlib import Path
import shutil

def classify_final_pass(filename: str, stem: str) -> tuple[str, str]:
    """
    Returns: (destination_folder, category_name)
    More aggressive classification for philosophical content
    """

    # Strong Observation indicators - life philosophy
    if any(kw in stem for kw in [
        '감각', '훈련', '생각', '인생', '사람', '신념', '가치관',
        '본질', '세상', '사건', '선택', '시간', '의미', '차이',
        '이유', '방법', '존재', '지옥', '여유', '하늘', '기회',
        '채워', '배푸', '도구', '소음', '시계', '남자와-여자',
        '다르지-않았다', '모두', '알지-못하는', '알아볼까',
        '무엇이-더-커', '아무도-몰라', '쏟아부어야', '커보이는'
    ]):
        return "Observations", "Observations"

    # Personal relationships and life events
    if any(kw in stem for kw in [
        '훈이', '벤슨', 'Beautiful', '건강', '에브리데이',
        '커피를-사주는', '만나야-하는가', '챙긴다'
    ]):
        return "Personal", "Personal"

    # Career/Work reflections
    if any(kw in stem for kw in [
        '일을-던지는', '페이즈', '매듭', '출퇴근', '규칙',
        '사업-대토론', '스마트-했음'
    ]):
        return "Work/Career-Reflections", "Career-Reflections"

    # Work challenges
    if any(kw in stem for kw in [
        '1등을-하는-순간', '지옥', '부러워하면'
    ]):
        return "Work/Challenges", "Challenges"

    # General work
    if any(kw in stem for kw in [
        '기여', '시그널', '작성예시'
    ]):
        return "Work/Projects", "Projects"

    # Default to Observations for philosophical content
    return "Observations", "Observations"


def main():
    vault_root = Path(__file__).parent.parent
    work_root = vault_root / "30-Flow" / "Life-Insights" / "Work"
    personal_folder = vault_root / "30-Flow" / "Life-Insights" / "Personal"
    observations_folder = vault_root / "30-Flow" / "Life-Insights" / "Observations"

    print("🔄 Life-Insights Final Pass Classification")
    print("Target: Remaining 51 philosophical/observation files\n")

    # Get remaining files
    files = [f for f in work_root.glob("*.md") if f.is_file()]
    print(f"Found {len(files)} files to classify\n")

    # Classify
    plan = {
        "Personal": [],
        "Observations": [],
        "Career-Reflections": [],
        "Challenges": [],
        "Projects": []
    }

    for file in files:
        dest_folder, category = classify_final_pass(file.name, file.stem)
        plan[category].append((file, dest_folder))

    # Show plan
    print("=" * 70)
    print("FINAL CLASSIFICATION PLAN")
    print("=" * 70)

    total = 0
    for category, items in sorted(plan.items(), key=lambda x: -len(x[1])):
        if items:
            print(f"\n{category}: {len(items)} files")
            for file, dest in items[:8]:
                print(f"  • {file.name}")
            if len(items) > 8:
                print(f"  ... and {len(items) - 8} more")
            total += len(items)

    print(f"\n{'='*70}")
    print(f"Total to move: {total} files")
    print(f"{'='*70}\n")

    # Execute
    print("✅ Proceeding with final classification...\n")

    moved = 0
    for category, items in plan.items():
        for file, dest_folder in items:
            if category == "Personal":
                dest_path = personal_folder / file.name
            elif category == "Observations":
                dest_path = observations_folder / file.name
            else:
                # Work subcategory
                dest_path = work_root / dest_folder.split('/')[-1] / file.name

            shutil.move(str(file), str(dest_path))
            print(f"✅ {file.name} → {category}/")
            moved += 1

    # Final summary
    print(f"\n{'='*70}")
    print("FINAL SUMMARY - Life-Insights Organization Complete!")
    print(f"{'='*70}")
    print(f"Files moved in final pass: {moved}")
    print(f"Files remaining in Work root: {len(list(work_root.glob('*.md')))}")

    print("\n📊 Complete Distribution:")
    print(f"  Personal: {len(list(personal_folder.glob('*.md')))} files")
    print(f"  Observations: {len(list(observations_folder.glob('*.md')))} files")
    print(f"  Work/Team-Dynamics: {len(list((work_root / 'Team-Dynamics').glob('*.md')))} files")
    print(f"  Work/Technical-Growth: {len(list((work_root / 'Technical-Growth').glob('*.md')))} files")
    print(f"  Work/Projects: {len(list((work_root / 'Projects').glob('*.md')))} files")
    print(f"  Work/Communication: {len(list((work_root / 'Communication').glob('*.md')))} files")
    print(f"  Work/Career-Reflections: {len(list((work_root / 'Career-Reflections').glob('*.md')))} files")
    print(f"  Work/Client-Work: {len(list((work_root / 'Client-Work').glob('*.md')))} files")
    print(f"  Work/Challenges: {len(list((work_root / 'Challenges').glob('*.md')))} files")

    total_organized = (
        len(list(personal_folder.glob('*.md'))) +
        len(list(observations_folder.glob('*.md'))) +
        len(list((work_root / 'Team-Dynamics').glob('*.md'))) +
        len(list((work_root / 'Technical-Growth').glob('*.md'))) +
        len(list((work_root / 'Projects').glob('*.md'))) +
        len(list((work_root / 'Communication').glob('*.md'))) +
        len(list((work_root / 'Career-Reflections').glob('*.md'))) +
        len(list((work_root / 'Client-Work').glob('*.md'))) +
        len(list((work_root / 'Challenges').glob('*.md')))
    )

    print(f"\n🎉 Total organized: {total_organized} files")
    print(f"✅ Life-Insights folder is now fully organized!")

if __name__ == '__main__':
    main()
