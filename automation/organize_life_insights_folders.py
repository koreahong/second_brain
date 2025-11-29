#!/usr/bin/env python3
"""
Organize Life-Insights into Topic-based Subfolders
Work/ → Team/, Projects/, Communication/, Growth/, etc.
"""

from pathlib import Path
import shutil
import yaml

def read_frontmatter(filepath):
    """Extract YAML frontmatter"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return {}

        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}

        return yaml.safe_load(parts[1]) or {}
    except:
        return {}

def main():
    vault_root = Path(__file__).parent.parent
    life_insights = vault_root / "30-Flow" / "Life-Insights"

    # Create topic-based subfolders under Work/
    work_folder = life_insights / "Work"

    subfolders = {
        'Team-Dynamics': work_folder / "Team-Dynamics",
        'Projects': work_folder / "Projects",
        'Communication': work_folder / "Communication",
        'Technical-Growth': work_folder / "Technical-Growth",
        'Career-Reflections': work_folder / "Career-Reflections",
        'Client-Work': work_folder / "Client-Work",
        'Challenges': work_folder / "Challenges",
    }

    # Create subfolders
    for folder in subfolders.values():
        folder.mkdir(parents=True, exist_ok=True)

    print("🔄 Organizing Life-Insights into Topic-based Subfolders\n")

    # Keywords for categorization
    categories = {
        'Team-Dynamics': ['팀', '팀원', '팀장', '데니스', '마빈', '레아', '패트릭', '협업', '소통', '갈등', '와해', '스피릿'],
        'Projects': ['프로젝트', '현대', '홈쇼핑', 'factset', '딜리버리', '리포트', '대시보드'],
        'Communication': ['커뮤니케이션', '보고', '회의', '미팅', '전달', '소통', '설득', '논쟁'],
        'Technical-Growth': ['개념', '공부', '학습', '코드', '서버', 'ODBC', '설계', '구조', '기술', '개발'],
        'Career-Reflections': ['퇴사', '이직', '커리어', '성장', '목표', '계획', '평가', '연봉'],
        'Client-Work': ['고객', '클라이언트', '요구사항', '요건', '만족', '서비스'],
        'Challenges': ['문제', '오류', '실수', '어려움', '힘든', '고민', '실패'],
    }

    # Process Work folder files
    moved = 0
    categorized = {key: [] for key in categories.keys()}

    work_files = [f for f in work_folder.glob("*.md") if f.is_file()]

    print(f"📊 Found {len(work_files)} files in Work/\n")

    for file in work_files:
        title = file.stem
        title_lower = title.lower()

        # Find best category
        scores = {}
        for category, keywords in categories.items():
            score = sum(1 for kw in keywords if kw in title_lower or kw in title)
            if score > 0:
                scores[category] = score

        if scores:
            # Get category with highest score
            best_category = max(scores, key=scores.get)
            dest_folder = subfolders[best_category]
            dest = dest_folder / file.name

            shutil.move(str(file), str(dest))
            categorized[best_category].append(file.name)
            moved += 1
            print(f"✅ {file.name[:60]} → {best_category}/")
        else:
            # Default: keep in Work root
            print(f"⏭️  No category match: {file.name[:60]}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    for category, files in categorized.items():
        if files:
            print(f"\n{category}/ ({len(files)} files)")
            for f in files[:3]:
                print(f"  - {f[:60]}")
            if len(files) > 3:
                print(f"  ... and {len(files)-3} more")

    print(f"\n✅ Total moved: {moved}")
    print(f"📁 Work folder now organized by topics!")

if __name__ == '__main__':
    main()
