#!/usr/bin/env python3
"""
Consolidate Career Files
Move interview-related files from Work to 커리어/면접기록/
Remove duplicates
"""

import os
from pathlib import Path
import shutil

def main():
    vault_root = Path(__file__).parent.parent

    # Source and destinations
    work_folder = vault_root / "30-Flow" / "Life-Insights" / "Work"
    career_folder = vault_root / "커리어"
    interview_folder = career_folder / "면접기록"

    # Ensure interview folder exists
    interview_folder.mkdir(parents=True, exist_ok=True)

    # Files to move (interview/career-specific)
    interview_files = [
        "고위드-면접.md",
        "나이스평가정보-면접.md",
        "돌고-돌아-코테.md",
        "오토에버-합격.md",
        "크래프트-면접.md",
        "크레프트-최종면접.md",
        "토스면접.md",
        "현대오토에버-코테.md"
    ]

    print("🔄 Consolidating Career Files\n")
    print(f"Source: {work_folder}")
    print(f"Destination: {interview_folder}\n")

    moved = 0
    skipped = 0
    duplicates = 0

    for filename in interview_files:
        source = work_folder / filename
        dest = interview_folder / filename
        career_dest = career_folder / filename

        # Check if file exists in source
        if not source.exists():
            print(f"⏭️  Not found in Work: {filename}")
            skipped += 1
            continue

        # Check for duplicate in career root
        if career_dest.exists():
            print(f"🔍 Checking duplicate: {filename}")

            # Compare file sizes
            source_size = source.stat().st_size
            career_size = career_dest.stat().st_size

            if source_size == career_size:
                # Same file, delete from Work
                print(f"   ❌ Exact duplicate - deleting from Work")
                source.unlink()
                duplicates += 1
            elif career_size > source_size:
                # Career version has more content, delete Work version
                print(f"   ❌ Career version is larger - deleting from Work")
                source.unlink()
                duplicates += 1
            else:
                # Work version has more content, keep it and move
                print(f"   ⚠️  Work version is larger - moving to 면접기록/")
                print(f"   ⚠️  Deleting smaller career root version")
                career_dest.unlink()
                shutil.move(str(source), str(dest))
                moved += 1
        else:
            # No duplicate, just move
            print(f"✅ Moving: {filename} → 면접기록/")
            shutil.move(str(source), str(dest))
            moved += 1

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Moved: {moved}")
    print(f"Duplicates removed: {duplicates}")
    print(f"Skipped: {skipped}")
    print(f"\n📁 All interview records now in: {interview_folder}")

if __name__ == '__main__':
    main()
