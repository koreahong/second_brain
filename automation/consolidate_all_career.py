#!/usr/bin/env python3
"""
Consolidate All Career Folders
Merge /커리어, /커리어-지원내역 into /03-Resources/Career/
"""

import os
from pathlib import Path
import shutil

def main():
    vault_root = Path(__file__).parent.parent

    # Source folders
    career_root = vault_root / "커리어"
    applications_root = vault_root / "커리어-지원내역"

    # Destination
    resources_career = vault_root / "03-Resources" / "Career"

    # Create subfolders
    interview_folder = resources_career / "Interviews"
    applications_folder = resources_career / "Applications"
    achievements_folder = resources_career / "Achievements"
    preparation_folder = resources_career / "Preparation"

    for folder in [interview_folder, applications_folder, achievements_folder, preparation_folder]:
        folder.mkdir(parents=True, exist_ok=True)

    print("🔄 Consolidating All Career Folders\n")
    print(f"Sources:")
    print(f"  1. {career_root}")
    print(f"  2. {applications_root}")
    print(f"\nDestination: {resources_career}\n")

    moved = 0
    skipped = 0

    # === 1. Move 면접기록/ from 커리어 ===
    print("=== 1. Moving Interview Records ===")
    interview_source = career_root / "면접기록"
    if interview_source.exists():
        for file in interview_source.glob("*.md"):
            dest = interview_folder / file.name
            shutil.move(str(file), str(dest))
            print(f"✅ {file.name} → Interviews/")
            moved += 1
        # Remove empty folder
        interview_source.rmdir()

    # === 2. Move 커리어 root files ===
    print("\n=== 2. Moving Career Files ===")

    # Achievement files
    achievement_keywords = ["성과", "달성", "개선", "향상", "단축", "99%", "70%", "90%"]
    preparation_keywords = ["예상질문", "자신감", "목표", "경험"]

    for file in career_root.glob("*.md"):
        filename_lower = file.stem.lower()

        # Categorize
        if any(kw in filename_lower for kw in achievement_keywords):
            dest_folder = achievements_folder
            category = "Achievements"
        elif any(kw in file.stem for kw in preparation_keywords):
            dest_folder = preparation_folder
            category = "Preparation"
        else:
            dest_folder = preparation_folder  # default
            category = "Preparation"

        dest = dest_folder / file.name
        shutil.move(str(file), str(dest))
        print(f"✅ {file.name} → {category}/")
        moved += 1

    # === 3. Move 커리어-지원내역 ===
    print("\n=== 3. Moving Job Applications ===")

    for file in applications_root.glob("*.md"):
        dest = applications_folder / file.name
        shutil.move(str(file), str(dest))
        print(f"✅ {file.name} → Applications/")
        moved += 1

    # === 4. Remove empty root folders ===
    print("\n=== 4. Cleaning Up ===")
    try:
        career_root.rmdir()
        print(f"✅ Removed: {career_root.name}/")
    except:
        print(f"⚠️  Could not remove: {career_root.name}/ (not empty)")

    try:
        applications_root.rmdir()
        print(f"✅ Removed: {applications_root.name}/")
    except:
        print(f"⚠️  Could not remove: {applications_root.name}/ (not empty)")

    # === Summary ===
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total files moved: {moved}")
    print(f"\nNew Structure:")
    print(f"  {resources_career}/")
    print(f"  ├── Interviews/ ({len(list(interview_folder.glob('*.md')))} files)")
    print(f"  ├── Applications/ ({len(list(applications_folder.glob('*.md')))} files)")
    print(f"  ├── Achievements/ ({len(list(achievements_folder.glob('*.md')))} files)")
    print(f"  └── Preparation/ ({len(list(preparation_folder.glob('*.md')))} files)")

if __name__ == '__main__':
    main()
