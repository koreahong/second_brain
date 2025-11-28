#!/usr/bin/env python3
"""
Categorize files based on content and filename
"""
import os
from pathlib import Path
import re
import shutil

# Category mapping based on keywords
CATEGORY_RULES = [
    # Technology - Orchestration
    {
        'keywords': ['airflow', 'dag', 'taskflow', 'cosmos', 'operator', 'backfill', 'keycloak'],
        'category': 'Knowledge/Technology/Orchestration',
        'type': None  # Will determine based on content
    },
    # Technology - Transformation
    {
        'keywords': ['dbt', 'ref_source'],
        'category': 'Knowledge/Technology/Transformation',
        'type': None
    },
    # Technology - Storage - PostgreSQL
    {
        'keywords': ['postgresql', 'postgres', 'trigger', 'alembic'],
        'category': 'Knowledge/Technology/Storage/PostgreSQL',
        'type': None
    },
    # Technology - Storage - BigQuery
    {
        'keywords': ['bigquery'],
        'category': 'Knowledge/Technology/Storage/BigQuery',
        'type': None
    },
    # Technology - Storage - Snowflake
    {
        'keywords': ['snowflake'],
        'category': 'Knowledge/Technology/Storage/Snowflake',
        'type': None
    },
    # Technology - Storage - Elasticsearch
    {
        'keywords': ['elasticsearch'],
        'category': 'Knowledge/Technology/Storage/Elasticsearch',
        'type': None
    },
    # Technology - Storage - Trino
    {
        'keywords': ['trino'],
        'category': 'Knowledge/Technology/Storage/Trino',
        'type': None
    },
    # Technology - Infrastructure - Kubernetes
    {
        'keywords': ['kubernetes', '쿠버네티스', '클러스터'],
        'category': 'Knowledge/Technology/Infrastructure/Kubernetes',
        'type': None
    },
    # Technology - Infrastructure - Docker
    {
        'keywords': ['docker', 'container'],
        'category': 'Knowledge/Technology/Infrastructure/Docker',
        'type': None
    },
    # Technology - Infrastructure - AWS
    {
        'keywords': ['aws', 'ecs', 'lambda', 'sqs', 's3', 'iam', 'vpc'],
        'category': 'Knowledge/Technology/Infrastructure/AWS',
        'type': None
    },
    # Technology - CI/CD
    {
        'keywords': ['jenkins', 'codedeploy'],
        'category': 'Knowledge/Technology/CI-CD',
        'type': None
    },
    # Technology - Languages - Python
    {
        'keywords': ['python', 'fastapi', 'sqlalchemy', '비동기', 'async'],
        'category': 'Knowledge/Technology/Languages/Python',
        'type': None
    },
    # Technology - Languages - SQL
    {
        'keywords': ['sql', '쿼리', 'lateral', 'exists', 'upsert', 'case_when', 'group_by', 'over()', '재귀함수_쿼리', '윈도우_함수'],
        'category': 'Knowledge/Technology/Languages/SQL',
        'type': None
    },
    # Data Management - Data Quality
    {
        'keywords': ['gx', 'great_expectations', 'data_quality'],
        'category': 'Knowledge/Data-Management/Data-Quality',
        'type': None
    },
    # Data Management - Data Modeling
    {
        'keywords': ['modeling', '모델링', '정규화', 'orm'],
        'category': 'Knowledge/Data-Management/Data-Modeling',
        'type': None
    },
    # Data Management - Data Governance
    {
        'keywords': ['권한', 'governance', 'lineage'],
        'category': 'Knowledge/Data-Management/Data-Governance',
        'type': None
    },
    # Data Architecture
    {
        'keywords': ['data_mesh', 'data_medaillon', 'lakehouse', 'kafka', 'streaming', 'architecture'],
        'category': 'Knowledge/Data-Architecture',
        'type': None
    },
    # Analytics - Product
    {
        'keywords': ['aarrr', 'gtm', '퍼널'],
        'category': 'Knowledge/Analytics/Product-Analytics',
        'type': None
    },
    # Analytics - Web
    {
        'keywords': ['웹로그', 'referrer', 'web'],
        'category': 'Knowledge/Analytics/Web-Analytics',
        'type': None
    },
    # Analytics - Marketing
    {
        'keywords': ['crm', 'personalize', '마케팅'],
        'category': 'Knowledge/Analytics/Marketing-Analytics',
        'type': None
    },
    # Career - Certifications
    {
        'keywords': ['sqlp', 'cka', '자격증', '과목'],
        'category': 'Knowledge/Career/Certifications',
        'type': 'concept'
    },
    # Career - Interview
    {
        'keywords': ['면접', 'interview', '과제풀기'],
        'category': 'Knowledge/Career/Interview',
        'type': 'experience'
    },
    # Career - Portfolio
    {
        'keywords': ['포트폴리오', 'portfolio', '이력서', '링크드인', '리맴버'],
        'category': 'Knowledge/Career/Portfolio',
        'type': 'concept'
    },
    # Career - Learning
    {
        'keywords': ['udemy', '학습', '교육', 'learning', '코딩테스트', '코테'],
        'category': 'Knowledge/Career/Learning-Path',
        'type': 'concept'
    },
    # Personal - Investment
    {
        'keywords': ['투자', 'investment', '주식', '텐베거', '코인', 'dell', 'tss', 'holtec', '갤럭시'],
        'category': 'Knowledge/Personal/Investment',
        'type': 'concept'
    },
    # Personal - Well-being
    {
        'keywords': ['우울증', 'well-being'],
        'category': 'Knowledge/Personal/Well-being',
        'type': 'concept'
    },
    # Experiences - Company specific
    {
        'keywords': ['qraft', '크래프트'],
        'category': 'Experiences/Qraft',
        'type': 'experience'
    },
    {
        'keywords': ['coupang', '쿠팡'],
        'category': 'Experiences/Coupang',
        'type': 'experience'
    },
    {
        'keywords': ['요기요', 'yogiyo', '네파', 'nepa', '직방', '하이퍼커넥트', 'typeb'],
        'category': 'Experiences/Companies',
        'type': 'experience'
    },
]

def determine_note_type(content, filename):
    """Determine if note is concept, experience, or pattern"""
    content_lower = content.lower()
    filename_lower = filename.lower()

    # Pattern indicators
    pattern_keywords = ['rules', 'best', 'pattern', '명령어', 'command', '사용법', '예시']
    if any(keyword in filename_lower or keyword in content_lower for keyword in pattern_keywords):
        return 'Patterns'

    # Experience indicators
    experience_keywords = ['경험', '시행착오', '적용', '구축', '개선', '트러블', '문제', '해결', 'dag_code']
    if any(keyword in filename_lower or keyword in content_lower for keyword in experience_keywords):
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

    # Try to match against rules
    for rule in CATEGORY_RULES:
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

def main():
    refs_dir = Path('/Users/qraft_hongjinyoung/DAE-Second-Brain/Resources/References')

    categorization = {}

    # Analyze all files
    for filepath in sorted(refs_dir.glob('*.md')):
        if filepath.name.startswith('_HUB'):
            continue

        # Check if file has substance
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        content_no_yaml = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        if len(content_no_yaml.strip()) < 100:  # Skip empty files
            continue

        category = categorize_file(filepath)

        if category not in categorization:
            categorization[category] = []

        categorization[category].append(filepath.name)

    # Print categorization
    print("📁 파일 분류 결과")
    print("=" * 100)
    for category in sorted(categorization.keys()):
        files = categorization[category]
        print(f"\n{category} ({len(files)}개)")
        print("-" * 100)
        for filename in sorted(files):
            print(f"  - {filename}")

    print(f"\n총 분류된 파일: {sum(len(files) for files in categorization.values())}개")

if __name__ == '__main__':
    main()
