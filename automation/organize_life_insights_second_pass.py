#!/usr/bin/env python3
"""
Life-Insights Second Pass Classification
Classify remaining 151 files in Work root into:
- Work subcategories (existing 7 folders)
- Personal folder
- Observations folder
"""

import os
from pathlib import Path
import shutil

def classify_file(filename: str, stem: str) -> tuple[str, str, int]:
    """
    Returns: (destination_folder, category_name, confidence_score)
    Confidence: 1-100
    """

    # Personal life events - HIGH priority (should have been in Personal from start)
    personal_high = [
        '결혼', '규리미', '엄마', '아빠', '가족', '부모', '형', '친구',
        '아이폰', '선물', '식사', '콘서트', '마라톤', '헬스장', '등반',
        '롯데월드', '출근', '이사', '상견례', '추석', '노량진집', '도쿄',
        '동아마라톤', '한라산', '백예린', '콜드플레이', '아카데미하우스',
        '불꽃축제', '목욕탕', '고모', '페널티', '살빼', '아울렛'
    ]

    # Observations - life philosophy, human nature
    observation_keywords = [
        '생각', '느낀', '깨달', '본질', '인생', '사람', '관계', '세상',
        '인간', '마음', '감각', '훈련', '변하지', '선택', '기다림',
        '여유', '책임', '가치관', '인품', '간사함', '냉정', '투명',
        '멸망', '달력', '소음', '무의미', '부족', '행복', '아름다운',
        '이별', '존재', '채워', '배풀', '공감', '기회'
    ]

    # Work - Team Dynamics
    team_keywords = [
        '팀', '팀원', '데니스', '마빈', '동료', '협업', '소통', '회의',
        '리더', '후배', '선배', '사장', '대표', '보성님', '세훈이형',
        '제이', '션', 'MD', '직원', '회식', '티타임'
    ]

    # Work - Technical Growth
    tech_keywords = [
        '개념', '학습', '공부', '코드', '설계', '기본기', 'DB', 'POWER',
        '데이터', '서칭', '연구', '실습', '과학'
    ]

    # Work - Projects
    project_keywords = [
        '프로젝트', '현대', '딜리버리', '리포트', '결과', '성과',
        '오늘-우려된', '테스트', '발표', '자료', '낭비', '10억'
    ]

    # Work - Communication
    comm_keywords = [
        '말', '소통', '전달', '설득', '보고', '공유', '예의', '연락',
        '얘기', '피드백', '가르쳐', '정의를-내려'
    ]

    # Work - Career
    career_keywords = [
        '커리어', '경쟁력', '취업', '재취업', '오토에버', '크래프트',
        '출근', '업무', '직장', '일하는가', '내적동기', '동기부여',
        '잉여생활', '언해피', '회사'
    ]

    # Work - Client Work
    client_keywords = [
        '고객', '서비스', '상대방-중심', '밀리의-서재', '커피챗'
    ]

    # Work - Challenges
    challenge_keywords = [
        '문제', '실수', '못함', '부족', '어려', '힘든', '역겨운',
        '서러운', '화', '안되', '막힌', '거칠게', '서투르게',
        '프로답지-못한', '망설임', '가짜의-나', 'ㄱㅅㄲ'
    ]

    stem_lower = stem.lower()

    # Check Personal (highest priority for life events)
    personal_score = sum(2 if kw in stem else 0 for kw in personal_high)
    if personal_score >= 2:
        return "Personal", "Personal", 90

    # Check Observations (philosophy, human nature)
    obs_score = sum(1 if kw in stem else 0 for kw in observation_keywords)
    if obs_score >= 2:
        return "Observations", "Observations", 85

    # Check Work subcategories
    team_score = sum(1 if kw in stem else 0 for kw in team_keywords)
    tech_score = sum(1 if kw in stem else 0 for kw in tech_keywords)
    proj_score = sum(1 if kw in stem else 0 for kw in project_keywords)
    comm_score = sum(1 if kw in stem else 0 for kw in comm_keywords)
    career_score = sum(1 if kw in stem else 0 for kw in career_keywords)
    client_score = sum(1 if kw in stem else 0 for kw in client_keywords)
    challenge_score = sum(1 if kw in stem else 0 for kw in challenge_keywords)

    scores = [
        (team_score, "Work/Team-Dynamics", "Team-Dynamics"),
        (tech_score, "Work/Technical-Growth", "Technical-Growth"),
        (proj_score, "Work/Projects", "Projects"),
        (comm_score, "Work/Communication", "Communication"),
        (career_score, "Work/Career-Reflections", "Career-Reflections"),
        (client_score, "Work/Client-Work", "Client-Work"),
        (challenge_score, "Work/Challenges", "Challenges"),
    ]

    max_score = max(scores, key=lambda x: x[0])
    if max_score[0] >= 1:
        confidence = min(50 + (max_score[0] * 15), 95)
        return max_score[1], max_score[2], confidence

    # Default: stays in Work root (manual review needed)
    return None, "UNCLASSIFIED", 0


def main():
    vault_root = Path(__file__).parent.parent
    work_root = vault_root / "30-Flow" / "Life-Insights" / "Work"
    personal_folder = vault_root / "30-Flow" / "Life-Insights" / "Personal"
    observations_folder = vault_root / "30-Flow" / "Life-Insights" / "Observations"

    print("🔄 Life-Insights Second Pass Classification\n")
    print("Analyzing 151 files in Work root folder...\n")

    # Get all md files in Work root (not in subfolders)
    files = [f for f in work_root.glob("*.md") if f.is_file()]

    print(f"Found {len(files)} files to classify\n")

    # Classify
    classifications = {}
    for file in files:
        dest_folder, category, confidence = classify_file(file.name, file.stem)
        if dest_folder:
            if category not in classifications:
                classifications[category] = []
            classifications[category].append((file, dest_folder, confidence))

    # Show classification plan
    print("=" * 70)
    print("CLASSIFICATION PLAN")
    print("=" * 70)

    total_to_move = 0
    for category in sorted(classifications.keys()):
        files_in_cat = classifications[category]
        print(f"\n{category}: {len(files_in_cat)} files")
        for file, dest, conf in sorted(files_in_cat, key=lambda x: -x[2])[:5]:
            print(f"  [{conf:2d}%] {file.name}")
        if len(files_in_cat) > 5:
            print(f"  ... and {len(files_in_cat) - 5} more")
        total_to_move += len(files_in_cat)

    unclassified = len(files) - total_to_move
    print(f"\n{'='*70}")
    print(f"Total to move: {total_to_move}")
    print(f"Unclassified: {unclassified}")
    print(f"{'='*70}\n")

    # Auto-proceed (no confirmation needed for automation)
    print("✅ Proceeding with automatic classification...")

    # Execute moves
    print("\n🚀 Moving files...\n")
    moved = 0

    for category, files_list in classifications.items():
        for file, dest_folder, confidence in files_list:
            if category == "Personal":
                dest_path = personal_folder / file.name
            elif category == "Observations":
                dest_path = observations_folder / file.name
            else:
                # Work subcategory
                dest_path = work_root / dest_folder.split('/')[-1] / file.name

            shutil.move(str(file), str(dest_path))
            print(f"✅ [{confidence:2d}%] {file.name} → {category}/")
            moved += 1

    # Final summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Files moved: {moved}")
    print(f"Files remaining in Work root: {len(list(work_root.glob('*.md')))}")

    print("\n📊 New Distribution:")
    print(f"  Personal: {len(list(personal_folder.glob('*.md')))} files")
    print(f"  Observations: {len(list(observations_folder.glob('*.md')))} files")
    print(f"  Work/Team-Dynamics: {len(list((work_root / 'Team-Dynamics').glob('*.md')))} files")
    print(f"  Work/Technical-Growth: {len(list((work_root / 'Technical-Growth').glob('*.md')))} files")
    print(f"  Work/Projects: {len(list((work_root / 'Projects').glob('*.md')))} files")
    print(f"  Work/Communication: {len(list((work_root / 'Communication').glob('*.md')))} files")
    print(f"  Work/Career-Reflections: {len(list((work_root / 'Career-Reflections').glob('*.md')))} files")
    print(f"  Work/Client-Work: {len(list((work_root / 'Client-Work').glob('*.md')))} files")
    print(f"  Work/Challenges: {len(list((work_root / 'Challenges').glob('*.md')))} files")
    print(f"  Work (unclassified): {len(list(work_root.glob('*.md')))} files")

if __name__ == '__main__':
    main()
