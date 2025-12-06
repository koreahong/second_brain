# Connection Quality Convention

> **이 문서 업데이트 시**: 연결 원칙, 검증 기준, 금지 사항만 추가. 설명 간결하게.

이 문서는 AI가 노트 연결 시 따라야 할 컨벤션입니다.

**⚠️ CRITICAL**: 표면적 연결이 아닌 의미있는 연결을 만들어야 합니다.

## 4단계 연결 원칙

### 1️⃣ READ FIRST (내용부터 읽기)

**❌ 절대 하지 말 것:**
- 제목이나 폴더만 보고 연결
- 키워드 매칭만으로 연결
- 추측으로 연결

**✅ 반드시 할 것:**
```python
# Obsidian MCP로 실제 내용 읽기
mcp__obsidian__read_note(path="note1.md")
mcp__obsidian__read_note(path="note2.md")

# Frontmatter 확인
- created: 노트 작성일
- updated: 마지막 수정일
- company: 회사 (aivelabs/qraft/personal)
- type: 노트 유형

# 내용 이해
- 무엇을 다루는가?
- 언제 작성되었는가?
- 왜 중요한가?
```

### 2️⃣ CHECK TIMELINE (시간맥락 확인)

**날짜 기반 연결 우선:**
1. 노트 날짜 확인 (created: 2025-10-29)
2. 같은 시기 찾기:
   - 같은 주 Weekly 회고
   - 같은 달 프로젝트
   - 시간적으로 연관된 인사이트
3. 시간 맥락 설명 추가

**시간 범위:**
```python
# 우선순위 순서
same_day = created_date
same_week = created_date ± 3 days
same_month = created_date ± 15 days
same_quarter = created_date ± 45 days

# Weekly 회고 검색
mcp__obsidian__search_notes(
    query=f"created:{start_date}..{end_date} type:reflection"
)
```

### 3️⃣ COMPANY PERIOD (회사/기간 구분)

**시기별 엄격한 구분:**

```yaml
aivelabs (2022-2023):
  - 조건: created < 2025-08
  - 연결: ❌ Qraft 프로젝트와 절대 연결 금지!
  - 허용: 교훈 추출만 가능
  - 예시:
    - [[aivelabs-프로젝트]] ❌ [[qraft-프로젝트]]
    - [[aivelabs-프로젝트]] ✅ [[인사이트-교훈]]

qraft (2025-08+):
  - 조건: created >= 2025-08
  - 연결: ✅ Projects/, Weekly/, Resources/
  - 맥락: 구체적인 업무 컨텍스트 포함
  - 예시:
    - [[qraft-프로젝트]] ✅ [[2025년-10월-27일]]
    - [[qraft-프로젝트]] ✅ [[Resources/Airflow/]]
```

**검증 로직:**
```python
note1_company = frontmatter1['company']
note2_company = frontmatter2['company']

if note1_company == 'aivelabs' and note2_company == 'qraft':
    → ❌ 연결 금지!
    → 대신: aivelabs 노트에서 인사이트 추출 → 별도 노트 → qraft와 연결

if note1_company == note2_company:
    → ✅ 연결 가능 (시간/주제 맥락 추가)
```

### 4️⃣ ADD CONTEXT (맥락 설명)

**❌ Bad (맥락 없음):**
```markdown
## Related
- [[팀별-데이터-현황-파악]]
- [[2025년-10월-27일]]
```

**✅ Good (맥락 포함):**
```markdown
## 📎 Related

### 관련 프로젝트 (8월~10월 현황파악 결과)
이 인사이트는 2개월간의 데이터 현황 조사 프로젝트의 결과입니다:
- [[팀별-원천-데이터-계약현황-파악]] (8월 25일 시작)
  - CFO님이 중지 검토한 데이터들 → 실제 사용 여부 확인
  - 결과: 거버넌스 필요성 깨달음

### 주간 회고 (같은 시기)
- [[2025년-10월-27일]] (2일 전)
  - 데이터 공유 유도 시도 → **거버넌스의 중요성 재인식**
  - 이 주의 핵심 깨달음
```

## 연결 유형

### Temporal (시간적 연결) - 최우선

**같은 주 회고:**
```markdown
### Weekly 회고 (같은 주)
- [[2025년-12월-07일]] (3일 전)
  - 컨텍스트: 프로젝트 진행 중 주간 회고
  - 연결: 이 주의 주요 작업이 이 노트와 관련
```

**같은 시기 프로젝트:**
```markdown
### 관련 프로젝트 (같은 기간)
- [[다른-프로젝트]] (2025-11월)
  - 컨텍스트: 동시 진행
  - 연결: 같은 기술 스택 사용
```

### Hierarchical (계층적 연결)

**프로젝트 → 작업:**
```markdown
### 상위 프로젝트
- [[메인-프로젝트]]
  - 컨텍스트: 이 노트는 해당 프로젝트의 세부 작업

### 하위 작업
- [[세부-작업-1]]
  - 컨텍스트: DAG 구현 부분
- [[세부-작업-2]]
  - 컨텍스트: DBT 모델링 부분
```

### Thematic (주제적 연결)

**프로젝트 → 지식 리소스:**
```markdown
### 사용된 기술 지식
- [[03-Resources/Technology/Airflow/DAG-패턴]]
  - 컨텍스트: 이 패턴을 프로젝트에 적용
  - 결과: 성능 30% 개선

### 참조한 방법론
- [[03-Resources/Data-Governance/거버넌스-원칙]]
  - 컨텍스트: 데이터 정책 수립에 활용
```

### Insight Chain (인사이트 체인)

**프로젝트 → 경험 → 인사이트:**
```markdown
### 프로젝트 경험
- [[02-Areas/.../Projects/Active/현황-파악-프로젝트]]
  - 컨텍스트: 8월~10월 수행

### 주간 회고
- [[02-Areas/.../Experience/Weekly/2025년-10월-27일]]
  - 컨텍스트: 프로젝트 진행 중 주간 정리

### 생성된 인사이트
- [[30-Flow/Life-Insights/Work/거버넌스의-중요성]]
  - 컨텍스트: 프로젝트 수행하며 깨달은 핵심 교훈
```

## 연결 품질 기준

### High Quality (95+)
```yaml
조건:
  - ✅ 실제 내용 읽음 (제목만 보지 않음)
  - ✅ 시간적 맥락 포함 (같은 주/달)
  - ✅ 회사 기간 일치 (aivelabs ↔ qraft 분리)
  - ✅ 1-2문장 컨텍스트 설명
  - ✅ 양방향 연결 (backlink)
  - ✅ 구조화된 섹션 (Project/Weekly/Knowledge/Insight)

예시:
  "[[프로젝트]] (2025-10월) - 데이터 현황 파악 작업 진행 중
   거버넌스 필요성을 처음 깨달은 계기"
```

### Medium Quality (70-94)
```yaml
조건:
  - ✅ 내용 읽음
  - ✅ 회사 기간 일치
  - ⚠️ 시간적 맥락 부족 (날짜만 있음)
  - ⚠️ 컨텍스트 설명 간략

예시:
  "[[프로젝트]] - 관련 작업"
```

### Low Quality (< 70)
```yaml
조건:
  - ❌ 키워드 매칭만 (내용 읽지 않음)
  - ❌ 시간적 맥락 없음
  - ❌ 회사 기간 불일치
  - ❌ 컨텍스트 설명 없음

예시:
  "[[프로젝트]]" (bare link)
```

## 금지 사항

### ❌ 키워드 매칭만으로 연결
```python
# Bad
if "airflow" in note1 and "airflow" in note2:
    create_link(note1, note2)  # ❌

# Good
content1 = read_note(note1)
content2 = read_note(note2)

if is_temporally_related(content1, content2) and \
   is_thematically_related(content1, content2) and \
   same_company_period(content1, content2):
    create_link_with_context(note1, note2, context)  # ✅
```

### ❌ 회사 기간 교차 연결
```python
# ❌ 절대 금지
aivelabs_project (2023) → qraft_project (2025)

# ✅ 허용 (교훈 추출)
aivelabs_project (2023) → insight (2023) → qraft_project (2025)
```

### ❌ 컨텍스트 없는 bare link
```markdown
# ❌ Bad
## Related
- [[Note 1]]
- [[Note 2]]

# ✅ Good
## 📎 Related

### 프로젝트 체인
- [[Note 1]] (2025-10월)
  - 이 작업의 상위 프로젝트
  - 데이터 현황 파악 목적

### 같은 주 회고
- [[Note 2]] (같은 주)
  - 프로젝트 진행 중 주간 정리
  - 핵심 깨달음 기록
```

## 검증 체크리스트

### Connection Curator가 연결 생성 전 확인

```python
def validate_connection(note1, note2):
    """
    연결 품질 검증
    """
    # 1️⃣ READ FIRST
    content1 = mcp__obsidian__read_note(note1)
    content2 = mcp__obsidian__read_note(note2)

    if not (content1 and content2):
        return False, "내용을 읽을 수 없음"

    # 2️⃣ CHECK TIMELINE
    date1 = content1['frontmatter']['created']
    date2 = content2['frontmatter']['created']

    temporal_gap = abs(date1 - date2)
    if temporal_gap > 90:  # 3개월 이상 차이
        warning = "시간적 거리가 멀어 맥락 확인 필요"

    # 3️⃣ COMPANY PERIOD
    company1 = content1['frontmatter']['company']
    company2 = content2['frontmatter']['company']

    if company1 == 'aivelabs' and company2 == 'qraft':
        return False, "회사 기간 교차 금지"

    # 4️⃣ ADD CONTEXT
    if not has_context_explanation:
        return False, "컨텍스트 설명 필요"

    return True, "연결 가능"
```

### Reviewer Agent가 기존 연결 검증

```python
def review_existing_connection(link):
    """
    기존 연결 품질 점수
    """
    score = 0

    # 내용 읽음? (+20)
    if link_created_after_reading_content:
        score += 20

    # 시간적 맥락? (+20)
    if has_temporal_context:
        score += 20

    # 회사 기간 일치? (+20)
    if same_company_period:
        score += 20

    # 컨텍스트 설명? (+20)
    if has_context_explanation:
        score += 20

    # 양방향? (+10)
    if has_backlink:
        score += 10

    # 구조화? (+10)
    if has_categorized_section:
        score += 10

    return score  # Max 100
```

## 연결 템플릿

### 프로젝트 체인
```markdown
## 📎 Related

### 프로젝트 컨텍스트 ({{period}})
{{project_summary_1sentence}}

- [[상위-프로젝트]] ({{date}})
  - 이 노트는 해당 프로젝트의 {{role}}
  - {{specific_contribution}}

### 사용된 지식
- [[03-Resources/Technology/{{tech}}/{{topic}}]]
  - {{how_used}}
  - 결과: {{outcome}}

### 주간 회고 (같은 주)
- [[Experience/Weekly/{{date}}]] ({{days_diff}}일 전)
  - {{what_reflected}}
  - 이 주의 {{highlight}}

### 생성된 인사이트
- [[Life-Insights/{{category}}/{{insight}}]]
  - 프로젝트 수행 중 깨달음: {{key_lesson}}
```

## 참조
- [vault-structure.md](vault-structure.md) - PARA 구조
- [capture-workflow.md](capture-workflow.md) - 캡처 워크플로우
