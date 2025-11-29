"""
Knowledge Curator 설정
"""

import os
from pathlib import Path

# Vault 경로
VAULT_ROOT = Path(__file__).parent.parent.parent.parent
AUTOMATION_ROOT = VAULT_ROOT / "automation"
KNOWLEDGE_CURATOR_ROOT = AUTOMATION_ROOT / "knowledge_curator"

# 폴더 구조 (PARA + Zettelkasten)
FOLDERS = {
    'inbox': '00-Inbox',
    'projects': '01-Projects',
    'areas': '02-Areas',
    'resources': '03-Resources',
    'archives': '04-Archives',
    'zettelkasten': '10-Zettelkasten',
    'maps': '20-Maps',
    'flow': '30-Flow',
    'assets': '99-Assets'
}

# 점수 기준
SCORE_THRESHOLDS = {
    'S': 90,
    'A': 75,
    'B': 60,
    'C': 40,
    'D': 0
}

# 점수 가중치
SCORE_WEIGHTS = {
    'completeness': 25,    # 완성도
    'organization': 25,    # 구조화
    'connectivity': 25,    # 연결성
    'actionability': 25    # 실행가능성
}

# Note Type 분류 기준
NOTE_TYPE_KEYWORDS = {
    'fleeting': {
        'indicators': ['빠르게', '메모', '나중에', 'TODO'],
        'max_length': 500,  # 500자 이하
        'min_links': 0
    },
    'literature': {
        'indicators': ['출처', 'source', 'url', '문서', '읽음', '정리'],
        'required_fields': ['source'],
    },
    'permanent': {
        'indicators': ['개념', '방법', '패턴', '원리'],
        'min_length': 300,
        'min_links': 2,
        'required_structure': True  # 헤딩 구조 필요
    },
    'project': {
        'indicators': ['프로젝트', 'project', '완료', '목표', 'deadline'],
        'required_fields': ['type'],
        'type_value': 'project'
    }
}

# 자동 링크 생성 설정
AUTO_LINK_CONFIG = {
    'min_keyword_match': 3,      # 최소 3개 키워드 매칭
    'min_similarity_score': 0.6,  # 최소 유사도 60%
    'max_suggestions': 5,         # 최대 5개 제안
    'exclude_patterns': [         # 제외 패턴
        'README.md',
        'index.md',
        '.template.md'
    ]
}

# Weekly Review 설정
WEEKLY_REVIEW_CONFIG = {
    'stale_days': 30,           # 30일 미수정 = stale
    'inbox_warning_count': 10,  # Inbox 10개 이상 = 경고
    'orphan_threshold': 0,      # 링크 0개 = 고아
    'low_score_threshold': 40   # 40점 이하 = 주의 필요
}

# GitHub Actions 설정
GITHUB_ACTIONS_CONFIG = {
    'score_on_sync': True,      # Notion 동기화 시 자동 점수화
    'weekly_review_day': 'FRI', # 금요일 리뷰
    'weekly_review_time': '18:00'
}
