#!/usr/bin/env python3
"""
Organize 본깨적 files into Life-Insights structure with proper categorization and tagging
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

# Define categorization keywords
WORK_KEYWORDS = [
    '업무', '팀', '프로젝트', '회의', '데이터', '파이프라인', '고객', '동료',
    '데니스', '회사', '크래프트', '면접', '현대', '대표', '보고', '협업',
    '커뮤니케이션', '성과', '코드', '개발', '대시보드', '서버', '클라이언트',
    '딜리버리', '기획', '설계', '테스트', '배포', '사용현황', '미팅',
    '오토에버', '나이스평가정보', '고위드', '토스', '밀리의-서재', 'factset',
    'POWER-BI', 'DB', '레아', '클로이', '패트릭', '마빈', '제이', '훈',
    '팀원', '팀장', '사장', '직원', '경쟁력', '경력', '채용', '합격', '코테'
]

PERSONAL_KEYWORDS = [
    '규림', '규리미', '가족', '엄마', '아빠', '친구', '결혼', '운동', '여행',
    '취미', '콘서트', '마라톤', '헬스', '롯데월드', '불꽃축제', '백예린',
    '콜드플레이', '한라산', '아카데미하우스', '아이폰', '아울렛', '교육비',
    '민철', '세훈', '션', '고모', '외할머니', '상견례', '이사', '집',
    '도모카레', '볼트', '노량진집', '출퇴근', '건강', '간호', '형'
]

WORK_TAGS_MAP = {
    'team': ['팀', '팀원', '팀장', '동료', '레아', '클로이', '패트릭', '마빈'],
    'project': ['프로젝트', '기획', '설계', '개발', '배포'],
    'communication': ['회의', '미팅', '보고', '소통', '커뮤니케이션', '협업'],
    'growth': ['성장', '학습', '공부', '배움', '깨달음'],
    'learning': ['배움', '공부', '훈련', '연습', '학습'],
    'frustration': ['답답', '역겨운', '불만', '화', '시불', '힘들'],
    'achievement': ['성과', '인정', '성공', '잘함', '개선'],
    'process': ['계획', '진행', '관리', '정리', '설계', '구조'],
    'conflict': ['불화', '기류', '어려움', '문제', '오류'],
    'collaboration': ['협업', '같이', '함께', '공유'],
    'career': ['면접', '채용', '이직', '합격', '연봉'],
    'leadership': ['사장', '대표', 'CEO', 'CFO', 'MD'],
    'technical': ['코드', '데이터', '서버', 'DB', '파이프라인', '대시보드', 'BI']
}

PERSONAL_TAGS_MAP = {
    'relationship': ['규림', '사랑', '연애', '데이트', '관계'],
    'family': ['가족', '엄마', '아빠', '부모', '친척', '외할머니'],
    'reflection': ['생각', '깨달음', '느낀', '반성'],
    'love': ['사랑', '결혼', '헤어', '규림'],
    'health': ['운동', '헬스', '마라톤', '건강', '간호'],
    'friends': ['친구', '민철', '세훈', '션', '로몬'],
    'life-decision': ['결심', '선택', '도전', '변화'],
    'gratitude': ['감사', '고마운', '배푸'],
    'happiness': ['행복', '즐거움', '긍정', '웃음'],
    'entertainment': ['콘서트', '축제', '여행', '취미']
}

OBSERVATION_TAGS_MAP = {
    'philosophy': ['인생', '철학', '의미', '가치'],
    'insight': ['깨달음', '배운', '느낀'],
    'human-nature': ['사람', '인간', '인품', '성격'],
    'work-life': ['일', '업무', '직장', '회사'],
    'mindset': ['마인드', '생각', '태도', '자세']
}

def extract_frontmatter(content: str) -> Tuple[Dict, str]:
    """Extract YAML frontmatter from markdown content"""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
                body = parts[2].strip()
                return frontmatter or {}, body
            except:
                pass
    return {}, content

def categorize_file(title: str, frontmatter: Dict, body: str) -> str:
    """Categorize file into Work/Personal/Observations"""
    text = f"{title} {frontmatter.get('깨달은 것', '')} {frontmatter.get('본 것', '')} {frontmatter.get('일기', '')} {body}".lower()

    work_score = sum(1 for kw in WORK_KEYWORDS if kw.lower() in text)
    personal_score = sum(1 for kw in PERSONAL_KEYWORDS if kw.lower() in text)

    # Strong work indicators
    if any(kw in title for kw in ['면접', '합격', '코테', '미팅', '보고', '팀', '프로젝트']):
        return 'Work'

    # Strong personal indicators
    if any(kw in title for kw in ['규림', '가족', '엄마', '아빠', '친구', '결혼', '콘서트', '여행']):
        return 'Personal'

    # Check 회고종류
    review_type = frontmatter.get('회고종류', '')
    if '주간회고' in review_type or '일일회고' in review_type:
        if work_score > personal_score:
            return 'Work'
        elif personal_score > work_score:
            return 'Personal'

    # Score-based decision
    if work_score > personal_score * 1.5:
        return 'Work'
    elif personal_score > work_score * 1.5:
        return 'Personal'
    elif work_score > 0 or personal_score > 0:
        # Has some specific keywords but unclear
        if work_score >= personal_score:
            return 'Work'
        else:
            return 'Personal'

    # Default to observations for philosophical/general content
    return 'Observations'

def extract_tags(title: str, frontmatter: Dict, body: str, category: str) -> List[str]:
    """Extract relevant tags based on content and category"""
    text = f"{title} {frontmatter.get('적용할 것', '')} {frontmatter.get('깨달은 것', '')} {frontmatter.get('본 것', '')} {frontmatter.get('일기', '')} {body}".lower()

    tags = set()

    # Add category tag
    tags.add(category.lower())

    # Add based on category
    if category == 'Work':
        for tag, keywords in WORK_TAGS_MAP.items():
            if any(kw.lower() in text for kw in keywords):
                tags.add(tag)
    elif category == 'Personal':
        for tag, keywords in PERSONAL_TAGS_MAP.items():
            if any(kw.lower() in text for kw in keywords):
                tags.add(tag)
    else:  # Observations
        for tag, keywords in OBSERVATION_TAGS_MAP.items():
            if any(kw.lower() in text for kw in keywords):
                tags.add(tag)

    # Add review type
    review_type = frontmatter.get('회고종류', '')
    if review_type:
        tags.add('reflection')

    return sorted(list(tags))

def find_similar_files(file_info: Dict, all_files: List[Dict], max_related: int = 5) -> List[str]:
    """Find similar files based on tags and content"""
    current_tags = set(file_info['tags'])
    similar = []

    for other in all_files:
        if other['path'] == file_info['path']:
            continue

        other_tags = set(other['tags'])
        overlap = len(current_tags & other_tags)

        if overlap >= 2:  # At least 2 common tags
            similar.append((overlap, other['title'], other['new_path']))

    # Sort by overlap and return top matches
    similar.sort(reverse=True, key=lambda x: x[0])
    return [f"[[{path}|{title}]]" for _, title, path in similar[:max_related]]

def process_files():
    """Main processing function"""
    source_dir = Path('/Users/qraft_hongjinyoung/DAE-Second-Brain/본깨적')
    target_base = Path('/Users/qraft_hongjinyoung/DAE-Second-Brain/30-Flow/Life-Insights')

    # Collect all file info first
    all_files = []
    category_counts = defaultdict(int)
    tag_counts = defaultdict(int)

    print("📊 Reading all files...")
    for md_file in source_dir.glob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        frontmatter, body = extract_frontmatter(content)

        title = frontmatter.get('title', md_file.stem)
        category = categorize_file(title, frontmatter, body)
        tags = extract_tags(title, frontmatter, body, category)

        new_path = f"30-Flow/Life-Insights/{category}/{md_file.name}"

        all_files.append({
            'path': str(md_file),
            'title': title,
            'category': category,
            'tags': tags,
            'frontmatter': frontmatter,
            'body': body,
            'new_path': new_path,
            'filename': md_file.name
        })

        category_counts[category] += 1
        for tag in tags:
            tag_counts[tag] += 1

    print(f"✅ Analyzed {len(all_files)} files\n")

    # Print summary
    print("📁 Category Distribution:")
    for cat, count in sorted(category_counts.items()):
        print(f"  - {cat}: {count} files")

    print(f"\n🏷️  Top 20 Tags:")
    for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  - {tag}: {count}")

    # Process each file
    print(f"\n🔄 Moving and updating files...")
    moved_count = 0
    error_count = 0

    for file_info in all_files:
        try:
            # Find related files
            related = find_similar_files(file_info, all_files)

            # Update frontmatter
            fm = file_info['frontmatter']

            # Add/update tags
            existing_tags = fm.get('tags', [])
            if not isinstance(existing_tags, list):
                existing_tags = [existing_tags] if existing_tags else []

            # Merge tags (keep notion-import, 본깨적, add new ones)
            new_tags = list(set(existing_tags + file_info['tags']))
            fm['tags'] = new_tags

            # Build new content
            new_content = "---\n"
            new_content += yaml.dump(fm, allow_unicode=True, default_flow_style=False)
            new_content += "---\n\n"
            new_content += file_info['body']

            # Add related section if we have related files
            if related and '## Related' not in file_info['body']:
                new_content += "\n\n## Related\n\n"
                new_content += "\n".join(f"- {link}" for link in related)
                new_content += "\n"

            # Write to new location
            target_path = target_base / file_info['category'] / file_info['filename']
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(new_content, encoding='utf-8')

            moved_count += 1

            if moved_count % 50 == 0:
                print(f"  Processed {moved_count}/{len(all_files)} files...")

        except Exception as e:
            print(f"  ❌ Error processing {file_info['filename']}: {e}")
            error_count += 1

    print(f"\n✅ Successfully moved {moved_count} files")
    if error_count > 0:
        print(f"❌ Encountered {error_count} errors")

    # Final summary
    print(f"\n📊 Final Summary:")
    print(f"  Total files: {len(all_files)}")
    print(f"  Work: {category_counts['Work']}")
    print(f"  Personal: {category_counts['Personal']}")
    print(f"  Observations: {category_counts['Observations']}")
    print(f"  Unique tags: {len(tag_counts)}")
    print(f"  Cross-references created: {sum(1 for f in all_files if find_similar_files(f, all_files))}")

if __name__ == '__main__':
    process_files()
