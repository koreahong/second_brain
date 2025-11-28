#!/usr/bin/env python3
"""
Migrate files to new structure
"""
import os
from pathlib import Path
import re
import shutil

# Import categorization logic
CATEGORY_RULES = [
    # Investment - check first before other keywords
    {
        'keywords': ['투자노트', '텐베거', '코인관련', 'dell', 'tss', 'holtec', '갤럭시_디지털', '코어위브'],
        'category': 'Knowledge/Personal/Investment',
        'type': 'concept',
        'priority': 10
    },
    # Personal - Well-being
    {
        'keywords': ['우울증'],
        'category': 'Knowledge/Personal/Well-being',
        'type': 'concept',
        'priority': 10
    },
    # Career - specific
    {
        'keywords': ['커리어_패스'],
        'category': 'Knowledge/Career/Learning-Path',
        'type': 'concept',
        'priority': 10
    },
    # Technology - Orchestration
    {
        'keywords': ['airflow', 'dag', 'taskflow', 'cosmos', 'operator', 'backfill', 'keycloak'],
        'category': 'Knowledge/Technology/Orchestration',
        'type': None,
        'priority': 5
    },
    # Technology - Transformation
    {
        'keywords': ['dbt', 'ref_source'],
        'category': 'Knowledge/Technology/Transformation',
        'type': None,
        'priority': 5
    },
    # Technology - Storage - PostgreSQL
    {
        'keywords': ['postgresql', 'postgres', 'trigger', 'alembic'],
        'category': 'Knowledge/Technology/Storage/PostgreSQL',
        'type': None,
        'priority': 5
    },
    # Technology - Storage - BigQuery
    {
        'keywords': ['bigquery'],
        'category': 'Knowledge/Technology/Storage/BigQuery',
        'type': None,
        'priority': 5
    },
    # Technology - Storage - Snowflake
    {
        'keywords': ['snowflake'],
        'category': 'Knowledge/Technology/Storage/Snowflake',
        'type': None,
        'priority': 5
    },
    # Technology - Storage - Elasticsearch
    {
        'keywords': ['elasticsearch'],
        'category': 'Knowledge/Technology/Storage/Elasticsearch',
        'type': None,
        'priority': 5
    },
    # Technology - Storage - Trino
    {
        'keywords': ['trino'],
        'category': 'Knowledge/Technology/Storage/Trino',
        'type': None,
        'priority': 5
    },
    # Technology - Infrastructure - Kubernetes
    {
        'keywords': ['kubernetes', '쿠버네티스', '클러스터'],
        'category': 'Knowledge/Technology/Infrastructure/Kubernetes',
        'type': None,
        'priority': 5
    },
    # Technology - Infrastructure - Docker
    {
        'keywords': ['docker', 'container'],
        'category': 'Knowledge/Technology/Infrastructure/Docker',
        'type': None,
        'priority': 5
    },
    # Technology - Infrastructure - AWS
    {
        'keywords': ['aws', 'ecs', 'lambda', 'sqs', 's3', 'iam', 'vpc'],
        'category': 'Knowledge/Technology/Infrastructure/AWS',
        'type': None,
        'priority': 5
    },
    # Technology - CI/CD
    {
        'keywords': ['jenkins', 'codedeploy'],
        'category': 'Knowledge/Technology/CI-CD',
        'type': None,
        'priority': 5
    },
    # Technology - Languages - Python
    {
        'keywords': ['python', 'fastapi', 'sqlalchemy', '비동기', 'async'],
        'category': 'Knowledge/Technology/Languages/Python',
        'type': None,
        'priority': 5
    },
    # Technology - Languages - SQL
    {
        'keywords': ['sql', '쿼리', 'lateral', 'exists', 'upsert', 'case_when', 'group_by', 'over()', '재귀함수_쿼리', '윈도우_함수'],
        'category': 'Knowledge/Technology/Languages/SQL',
        'type': None,
        'priority': 5
    },
    # Data Management - Data Quality
    {
        'keywords': ['gx', 'great_expectations', 'data_quality'],
        'category': 'Knowledge/Data-Management/Data-Quality',
        'type': None,
        'priority': 5
    },
    # Data Management - Data Modeling
    {
        'keywords': ['modeling', '모델링', '정규화', 'orm'],
        'category': 'Knowledge/Data-Management/Data-Modeling',
        'type': None,
        'priority': 5
    },
    # Data Management - Data Governance
    {
        'keywords': ['권한', 'governance', 'lineage'],
        'category': 'Knowledge/Data-Management/Data-Governance',
        'type': None,
        'priority': 5
    },
    # Data Architecture
    {
        'keywords': ['data_mesh', 'data_medaillon', 'lakehouse', 'kafka', 'streaming', 'architecture'],
        'category': 'Knowledge/Data-Architecture',
        'type': None,
        'priority': 5
    },
    # Analytics - Product
    {
        'keywords': ['aarrr', 'gtm', '퍼널'],
        'category': 'Knowledge/Analytics/Product-Analytics',
        'type': None,
        'priority': 5
    },
    # Analytics - Web
    {
        'keywords': ['웹로그', 'referrer', 'web'],
        'category': 'Knowledge/Analytics/Web-Analytics',
        'type': None,
        'priority': 5
    },
    # Analytics - Marketing
    {
        'keywords': ['crm', 'personalize', '마케팅'],
        'category': 'Knowledge/Analytics/Marketing-Analytics',
        'type': None,
        'priority': 5
    },
    # Career - Certifications
    {
        'keywords': ['sqlp', 'cka', '자격증', '과목', '암기'],
        'category': 'Knowledge/Career/Certifications',
        'type': 'concept',
        'priority': 5
    },
    # Career - Interview
    {
        'keywords': ['면접', 'interview', '과제풀기'],
        'category': 'Knowledge/Career/Interview',
        'type': 'experience',
        'priority': 5
    },
    # Career - Portfolio
    {
        'keywords': ['포트폴리오', 'portfolio', '이력서', '링크드인', '리맴버', 'IT_기술블로그'],
        'category': 'Knowledge/Career/Portfolio',
        'type': 'concept',
        'priority': 5
    },
    # Career - Learning
    {
        'keywords': ['udemy', '학습', '교육', 'learning', '코딩테스트', '코테'],
        'category': 'Knowledge/Career/Learning-Path',
        'type': 'concept',
        'priority': 5
    },
    # Experiences - Company specific
    {
        'keywords': ['qraft', '크래프트'],
        'category': 'Experiences/Qraft',
        'type': 'experience',
        'priority': 5
    },
    {
        'keywords': ['coupang', '쿠팡', '에이브랩스'],
        'category': 'Experiences/Coupang',
        'type': 'experience',
        'priority': 5
    },
    {
        'keywords': ['요기요', 'yogiyo', '네파', 'nepa', '직방', '하이퍼커넥트', 'typeb', 'skt_도입'],
        'category': 'Experiences/Companies',
        'type': 'experience',
        'priority': 5
    },
]

def determine_note_type(content, filename):
    """Determine if note is concept, experience, or pattern"""
    content_lower = content.lower()
    filename_lower = filename.lower()

    # Pattern indicators
    pattern_keywords = ['rules', 'best', 'pattern', '명령어', 'command', '사용법', '예시', '시행착오']
    if any(keyword in filename_lower or keyword in content_lower for keyword in pattern_keywords):
        return 'Patterns'

    # Experience indicators
    experience_keywords = ['경험', '적용', '구축', '개선', '트러블', '문제', '해결', 'dag_code', '학습', '_실습', '프로젝트']
    if any(keyword in filename_lower for keyword in experience_keywords):
        return 'Experiences'

    # Default to concept
    return 'Concepts'

def categorize_file(filepath):
    """Categorize a single file"""
    filename = filepath.name
    filename_lower = filename.lower()

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content_lower = content.lower()

    # Sort rules by priority
    sorted_rules = sorted(CATEGORY_RULES, key=lambda x: x.get('priority', 0), reverse=True)

    # Try to match against rules
    for rule in sorted_rules:
        if any(keyword in filename_lower or keyword in content_lower for keyword in rule['keywords']):
            category = rule['category']

            # Determine type if not specified
            if rule['type']:
                note_type = rule['type']
            else:
                note_type = determine_note_type(content, filename)

            # For some categories, don't append type subdirectory
            if 'Personal' in category or 'Career' in category or 'Experiences' in category:
                return category
            else:
                return f"{category}/{note_type}"

    # Default fallback
    return 'Knowledge/Uncategorized'

def is_file_empty(filepath):
    """Check if file is essentially empty"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove YAML frontmatter
    content_no_yaml = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Remove markdown headers and empty lines
    lines = [line.strip() for line in content_no_yaml.split('\n') if line.strip()]

    # Filter out common template text
    template_markers = [
        '📝 내용', '🏷️ 분류', '🔗 연결', 'PARA', '구분',
        'Hub:', '활용 프로젝트', '관련 레퍼런스', '(아직 없음)',
        'Notion에서 재마이그레이션됨', '---', '#'
    ]

    real_content_lines = [
        line for line in lines
        if not any(marker in line for marker in template_markers)
        and len(line) > 10
    ]

    real_content_chars = sum(len(line) for line in real_content_lines)
    num_real_lines = len(real_content_lines)

    return real_content_chars < 100 or num_real_lines < 3

def main():
    base_dir = Path('/Users/qraft_hongjinyoung/DAE-Second-Brain')
    refs_dir = base_dir / 'Resources' / 'References'

    # Create necessary directories
    os.makedirs(base_dir / 'Experiences' / 'Companies', exist_ok=True)

    moved_count = 0
    deleted_count = 0
    skipped_count = 0

    print("🚀 파일 마이그레이션 시작")
    print("=" * 100)

    for filepath in sorted(refs_dir.glob('*.md')):
        if filepath.name.startswith('_HUB'):
            print(f"⏭️  Skipping hub file: {filepath.name}")
            skipped_count += 1
            continue

        # Check if empty
        if is_file_empty(filepath):
            print(f"🗑️  Deleting empty file: {filepath.name}")
            filepath.unlink()
            deleted_count += 1
            continue

        # Categorize
        category = categorize_file(filepath)
        target_dir = base_dir / category

        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)

        # Move file
        target_path = target_dir / filepath.name

        try:
            shutil.move(str(filepath), str(target_path))
            print(f"✅ {filepath.name:<50} → {category}")
            moved_count += 1
        except Exception as e:
            print(f"❌ Error moving {filepath.name}: {e}")

    print()
    print("=" * 100)
    print(f"📊 마이그레이션 완료")
    print(f"  - 이동된 파일: {moved_count}개")
    print(f"  - 삭제된 파일: {deleted_count}개")
    print(f"  - 스킵된 파일: {skipped_count}개")

if __name__ == '__main__':
    main()
