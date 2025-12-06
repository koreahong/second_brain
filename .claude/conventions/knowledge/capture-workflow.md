# Capture Workflow Convention

> **이 문서 업데이트 시**: Frontmatter 형식, 태그 전략, 원자성 원칙만 추가. 설명 간결하게.

이 문서는 AI가 노트 캡처 시 따라야 할 컨벤션입니다.

## 원자적 노트 (Atomic Note) 원칙

### 하나의 개념 = 하나의 노트
- 200-500 단어 (이상적)
- 단일 주제/아이디어
- 재사용 가능한 단위

**❌ Bad (여러 개념 혼재):**
```markdown
# Airflow와 DBT 설정

## Airflow 설정
...

## DBT 설정
...

## 통합 방법
...
```

**✅ Good (원자적):**
```markdown
# Airflow-DAG-설계-패턴
(200-500 단어, 하나의 패턴만)

---

# DBT-Incremental-모델
(200-500 단어, 하나의 모델 타입만)

---

# Airflow-DBT-통합-패턴
(200-500 단어, 통합 방법만)
```

## Frontmatter 필수 형식

### 기본 템플릿
```yaml
---
created: {{date:YYYY-MM-DD}}
updated: {{date:YYYY-MM-DD}}
tags:
  - category-tag
  - technology-tag
  - concept-tag
company: aivelabs|qraft|personal
status: draft|active|completed|archived
type: project|reflection|reference|insight|concept
---
```

### 필드 설명

**created**: 노트 작성일
- 형식: YYYY-MM-DD
- 자동 설정 (현재 날짜)
- 변경 금지

**updated**: 마지막 수정일
- 형식: YYYY-MM-DD
- 노트 수정 시마다 갱신

**tags**: 태그 배열
- 최소 2개 이상
- 계층적 태그: `data-engineering/airflow`
- 자동 탐지 + 수동 추가

**company**: 회사 구분
- `aivelabs`: 2022-2023 (created < 2025-08)
- `qraft`: 2025-08+ (created >= 2025-08)
- `personal`: 개인 학습/경험

**status**: 상태
- `draft`: 작성중 (초안)
- `active`: 진행중 (프로젝트)
- `completed`: 완료
- `archived`: 보류/취소

**type**: 노트 유형
- `project`: 프로젝트 노트
- `reflection`: 회고 (Weekly)
- `reference`: 기술 레퍼런스
- `insight`: 인생 인사이트 (본깨적)
- `concept`: Zettelkasten 개념

## 자동 태그 전략

### 기술 탐지
```python
content_keywords = {
    "airflow": ["#airflow", "#data-engineering", "#orchestration"],
    "dbt": ["#dbt", "#analytics", "#data-modeling"],
    "datahub": ["#datahub", "#data-governance", "#metadata"],
    "python": ["#python", "#programming"],
    "snowflake": ["#snowflake", "#data-warehouse"],
}

# 키워드 발견 시 자동 추가
if "airflow" in content.lower():
    tags.extend(["airflow", "data-engineering"])
```

### 도메인 탐지
```python
domain_keywords = {
    "거버넌스": ["#data-governance", "#policy"],
    "파이프라인": ["#data-pipeline", "#ETL"],
    "크롤링": ["#web-scraping", "#crawling"],
    "협업": ["#collaboration", "#teamwork"],
}
```

### 회사 기간 자동 설정
```python
created_date = frontmatter['created']

if created_date < "2025-08-01":
    frontmatter['company'] = "aivelabs"
elif created_date >= "2025-08-01":
    frontmatter['company'] = "qraft"
else:
    frontmatter['company'] = "personal"  # 명시적 지정 필요
```

## 위치 제안 (Suggestion Only)

### Type 기반 제안
```python
type_to_location = {
    'project': {
        'active': '02-Areas/크래프트테크놀로지스/Projects/Active/',
        'completed': '02-Areas/크래프트테크놀로지스/Projects/Completed/',
        'archived': '02-Areas/크래프트테크놀로지스/Projects/Archived/'
    },
    'reflection': '02-Areas/크래프트테크놀로지스/Experience/Weekly/{year}/',
    'reference': '03-Resources/{technology}/',
    'insight': '30-Flow/Life-Insights/{Work|Personal|Observations}/',
    'concept': '10-Zettelkasten/Permanent/'
}
```

### 태그 기반 세분화 (Reference)
```python
# 기술별 Resources 폴더
tech_tags = {
    '#airflow': '03-Resources/Technology/Airflow/',
    '#dbt': '03-Resources/Technology/DBT/',
    '#datahub': '03-Resources/Technology/DataHub/',
    '#python': '03-Resources/Technology/Python/',
}

# 도메인별 Resources 폴더
domain_tags = {
    '#data-governance': '03-Resources/Data-Governance/',
    '#dae': '03-Resources/DAE/',
    '#methodology': '03-Resources/Methodologies/',
}
```

### 유사 노트 검색
```python
# 기존 노트 검색하여 위치 참조
mcp__obsidian__search_notes(
    query=f"{primary_tags} {secondary_tags}",
    limit=5
)

# 가장 많이 사용된 위치 제안
suggested_location = most_common_location(search_results)
```

## 초기 연결 제안 (생성 금지!)

### 시간적 후보
```python
# 같은 주 노트 검색
created_date = frontmatter['created']
week_start = get_week_start(created_date)
week_end = get_week_end(created_date)

mcp__obsidian__search_notes(
    query=f"created:{week_start}..{week_end}",
    limit=5
)

# 제안 형식
suggestions['temporal'] = [
    f"[[{note.title}]] - Same week ({note.created})"
]
```

### 주제적 후보
```python
# 같은 태그 노트 검색
for tag in frontmatter['tags']:
    mcp__obsidian__search_notes(
        query=f"tag:{tag}",
        limit=3
    )

# 제안 형식
suggestions['thematic'] = [
    f"[[{note.title}]] - Related topic: {tag}"
]
```

### 회사 기간 후보
```python
# 같은 회사 기간 노트만
company = frontmatter['company']

mcp__obsidian__search_notes(
    query=f"company:{company} {tags}",
    limit=5
)

suggestions['company_context'] = [
    f"[[{note.title}]] - Same company period ({company})"
]
```

**⚠️ CRITICAL**: 연결 제안만 하고 실제로 생성하지 않음!
- Connection Curator가 검증 후 생성

## 노트 구조 템플릿

### 프로젝트 노트
```markdown
---
created: {{date}}
updated: {{date}}
tags: [project, {{tech}}, {{domain}}]
company: qraft
status: active
type: project
---

# {{Project Title}}

## Overview
{{1-2 sentence summary}}

## Context
- **기간**: {{start_date}} ~ {{end_date}}
- **목적**: {{purpose}}
- **팀/역할**: {{team_and_role}}

## Progress
- [x] Task 1
- [ ] Task 2

## Technical Details
{{implementation details}}

## Challenges
{{obstacles and solutions}}

## 📎 Related
(Connection Curator가 추가)
```

### 회고 노트 (Weekly)
```markdown
---
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
tags: [reflection, weekly, {{year}}]
company: qraft|personal
status: active
type: reflection
---

# {{YYYY년 MM월 DD일}}

## 이번 주 주요 활동
- {{activity 1}}
- {{activity 2}}

## 배운 것
- {{learning 1}}
- {{learning 2}}

## 느낀 점
{{insights and reflections}}

## 다음 주 계획
- [ ] {{plan 1}}
- [ ] {{plan 2}}

## 📎 Related
### 이번 주 프로젝트
(Connection Curator가 추가)

### 생성된 인사이트
(Connection Curator가 추가)
```

### 기술 레퍼런스
```markdown
---
created: {{date}}
updated: {{date}}
tags: [reference, {{technology}}, {{concept}}]
company: personal|qraft
status: active
type: reference
---

# {{Technology}} - {{Concept}}

## 개념
{{200-500 words explaining the concept}}

## 사용 예시
\`\`\`python
{{code example}}
\`\`\`

## 베스트 프랙티스
- {{practice 1}}
- {{practice 2}}

## 참조
- {{external source 1}}
- {{external source 2}}

## 📎 Related
### 적용한 프로젝트
(Connection Curator가 추가)
```

### 인사이트 노트
```markdown
---
created: {{date}}
updated: {{date}}
tags: [insight, {{category}}, {{topic}}]
company: qraft|aivelabs|personal
status: active
type: insight
---

# {{Insight Title}}

## 배경
{{what triggered this insight}}

## 핵심 깨달음
{{key realization - 200-500 words}}

## 적용 가능성
{{how to apply this insight}}

## 📎 Related
### 경험한 프로젝트
(Connection Curator가 추가)

### 관련 회고
(Connection Curator가 추가)
```

### Zettelkasten 개념
```markdown
---
created: {{date}}
updated: {{date}}
tags: [concept, {{domain}}, {{keyword}}]
company: personal
status: active
type: concept
---

# {{Concept Name}}

{{200-500 words explaining the concept}}

## 정의
{{precise definition}}

## 예시
{{concrete examples}}

## 관련 개념
- {{related concept 1}}
- {{related concept 2}}

## 📎 Related
### 문헌 참조
(Connection Curator가 추가)
```

## 캡처 워크플로우

### 1. 입력 분석
```python
user_input = """
사용자가 제공한 텍스트 (생각, 인사이트, 레퍼런스 등)
"""

# 내용 분석
content_type = analyze_content_type(user_input)
# → project | reflection | reference | insight | concept

keywords = extract_keywords(user_input)
technologies = detect_technologies(user_input)
domain = detect_domain(user_input)
```

### 2. Frontmatter 생성
```python
frontmatter = {
    'created': today(),
    'updated': today(),
    'tags': auto_detect_tags(user_input),
    'company': determine_company_period(today()),
    'status': 'draft',  # 기본값
    'type': content_type
}
```

### 3. 노트 생성 (draft 상태)
```python
note_content = f"""---
{format_frontmatter(frontmatter)}
---

# {generate_title(user_input)}

{user_input}

## 📎 Related
(Connection Curator가 추가)
"""

# Obsidian MCP로 생성
mcp__obsidian__write_note(
    path=f"임시위치/{title}.md",
    content=note_content
)
```

### 4. 위치 및 연결 제안
```python
# 위치 제안
suggested_location = suggest_location(frontmatter, keywords)

# 연결 후보 검색
temporal_candidates = search_by_date(created_date)
thematic_candidates = search_by_tags(tags)
company_candidates = search_by_company(company)

# 출력
output = f"""
✅ Note captured

**Title**: {title}
**Location**: {suggested_location} (not moved yet)
**Tags**: {tags}
**Company**: {company}

**Suggested connections** (not created yet):
- {temporal_candidates}
- {thematic_candidates}

**Next steps**:
1. Review and move to suggested location (Curator)
2. Create connections (Connection Curator)
3. Validate quality (Reviewer)
"""
```

## 검증 기준

### Frontmatter 완전성
```python
required_fields = [
    'created',
    'updated',
    'tags',      # 최소 2개
    'company',
    'status',
    'type'
]

for field in required_fields:
    if field not in frontmatter:
        → ❌ 필수 필드 누락
```

### 원자성 검증
```python
word_count = len(content.split())

if 200 <= word_count <= 500:
    → ✅ 원자적 (ideal)
elif 100 <= word_count < 200 or 500 < word_count <= 1000:
    → ⚠️ 허용 가능 (acceptable)
else:
    → ❌ 너무 짧거나 길음 (split or summarize)
```

### 태그 관련성
```python
content_keywords = extract_keywords(content)
frontmatter_tags = frontmatter['tags']

relevance = calculate_overlap(content_keywords, frontmatter_tags)

if relevance > 0.8:
    → ✅ 관련성 높음
elif relevance > 0.5:
    → ⚠️ 관련성 보통
else:
    → ❌ 태그 재검토 필요
```

## 금지 사항

### ❌ 여러 개념 혼재
```markdown
# Bad: Airflow와 DBT 전체 가이드
(2000+ 단어, 여러 주제)

# Good: 원자적 분리
- Airflow-DAG-설계.md (300 단어)
- DBT-모델-구조.md (400 단어)
- Airflow-DBT-통합.md (250 단어)
```

### ❌ Frontmatter 누락
```markdown
# Bad
# My Note

Content...

# Good
---
created: 2025-12-07
updated: 2025-12-07
tags: [airflow, data-engineering]
company: qraft
status: draft
type: reference
---

# My Note

Content...
```

### ❌ 즉시 연결 생성
```python
# ❌ Capture Agent가 직접 연결 생성
create_link(new_note, related_note)

# ✅ Connection Curator에게 위임
suggest_connection(new_note, related_note)
```

## 참조
- [vault-structure.md](vault-structure.md) - PARA 구조
- [connection-quality.md](connection-quality.md) - 연결 원칙
