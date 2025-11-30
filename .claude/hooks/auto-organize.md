---
tags:
- datahub
- dbt
- airflow
- snowflake
- work
created: '2025-11-30'
updated: '2025-11-30'
title: auto organize
aliases: []
---
# Auto-Organize Hook

## Trigger
When Claude Code writes or edits a markdown file in the vault

## Behavior

### 1. Detect Misplaced Files
If a file is in one of these temporary locations:
- `업무리스트/`
- `회고록/`
- `레퍼런스/`
- `본깨적/`
- `00-Inbox/`

**Action:**
- Alert user: "📍 This file appears to be in a temporary location. Would you like me to organize it?"
- If yes → invoke content-organizer agent

### 2. Auto-Tag Based on Content
When creating/editing any file, scan content and auto-add tags:

**Technology tags:**
- Mentions `airflow` → add `#airflow`
- Mentions `dbt` → add `#dbt`
- Mentions `datahub` → add `#datahub`
- Mentions `snowflake` → add `#snowflake`
- etc.

**Context tags:**
- In `Projects/Active/` → add `#active-project`
- In `Projects/Completed/` → add `#completed`
- In `Experience/Weekly/` → add `#weekly-reflection`
- In `Life-Insights/Work/` → add `#work-insight`

**Apply tags using:** `mcp__obsidian__manage_tags`

### 3. Auto-Link Creation - CONTENT-FIRST APPROACH

**⚠️ CRITICAL: Read content and check dates BEFORE creating links!**

**Process:**
```yaml
Step 1: READ THE NOTE
  - Use: mcp__obsidian__read_note(path=note_path)
  - Get: content, frontmatter (created, updated dates, type)
  - Understand: What happened? When? Why?

Step 2: DETECT NOTE TYPE
  Check frontmatter 'type' or path:
  - type: reference OR path: 03-Resources/ → Reference 노트
  - type: project OR path: Projects/ → Project 노트
  - type: weekly-reflection OR path: Weekly/ → Weekly 노트
  - type: insight OR path: Life-Insights/ → Insight 노트

Step 3a: FOR REFERENCE NOTES (기술/방법론)
  ✅ Reference 노트는 시간성이 약함
  ✅ 대신 "어디서 사용했는가"가 중요

  연결 전략:
  1. 이 기술을 사용한 프로젝트 찾기
  2. 이 기술을 사용한 경험 찾기 (Weekly)
  3. 유사/대안 기술 찾기
  4. 커스텀 구현 찾기

  → Linker Agent의 link_reference_note() 호출

Step 3b: FOR TIME-BASED NOTES (프로젝트/경험/인사이트)
  ✅ 시간 맥락이 중요

  DETECT TIME PERIOD & COMPANY:
    created: 2025-10-29
    → Company: Qraft (2025-08+)

    created: 2023-05-12
    → Company: aivelabs (2022-2023)

  ❌ NEVER mix companies!
  ❌ NEVER connect 2023 note to 2025 Qraft project!

Step 3: FIND TEMPORAL CONNECTIONS
  Note date: 2025-10-29
  
  Search same week reflections:
  - mcp__obsidian__search_notes(query="2025년 10월")
  - Filter: weekly-reflection tag
  - Find: 2025년-10월-27일 (2 days before!)
  
  Search same period projects:
  - Look for projects active in Oct 2025
  - Read each project to verify relevance
  - Check if note content mentions project

Step 4: CREATE CONTEXTUAL LINKS
  ❌ Bad (no context):
  ## Related
  - [[팀별-데이터-현황-파악]]
  
  ✅ Good (with context):
  ## 📎 Related
  
  ### 관련 프로젝트 (8월~10월 현황파악 결과)
  이 인사이트는 2개월간의 데이터 현황 조사 프로젝트의 결과입니다:
  - [[팀별-원천-데이터-계약현황-파악]] (8월 25일 시작)
    - CFO님이 중지 검토한 데이터들 → 실제 사용 여부 확인
  
  ### 주간 회고 (같은 시기)
  - [[2025년-10월-27일]] (2일 전)
    - 데이터 공유 유도 → **거버넌스의 중요성 깨달음**
```

**Technology mentions (Secondary):**
- Extract tech keywords AFTER understanding context
- Search: `mcp__obsidian__search_notes(query="{tech}", searchContent=true)`
- BUT: Read each result to verify actual relevance
- Add only if contextually related, not just keyword match

### 4. Backlink Creation
When a link is created, ensure backlink exists in target:

Example:
- If `Projects/Active/datahub-구축.md` links to `Technology/DataHub/Installation.md`
- Then add to `Installation.md`:
  ```markdown
  ## Used In
  - [[Projects/Active/datahub-구축]]
  ```

## 4. Company/Period Detection

**CRITICAL: Never mix different employment periods!**

```python
def detect_company_period(note_date):
    """
    Detect which company based on date
    """
    if note_date < "2025-08-01":
        return "aivelabs"  # 2022-2023
    else:
        return "Qraft"  # 2025-08+

def get_company_marker(company, note_date):
    """
    Add company context marker
    """
    if company == "aivelabs":
        return f"> **Note**: 이 인사이트는 aivelabs 재직 시절({note_date.year}년 {note_date.month}월)의 경험입니다."
    else:
        return ""  # Current company, no marker needed
```

**Rules:**
- ❌ NEVER connect 2023 note to 2025 Qraft project
- ❌ NEVER link aivelabs notes to Qraft weekly reflections
- ✅ For aivelabs notes: extract lessons learned only
- ✅ For Qraft notes: connect to actual projects and weeklies

## Configuration

Enable/disable behaviors in frontmatter:
```yaml
auto_organize: true     # Auto-suggest organization
auto_tag: true          # Auto-add tags
auto_link: true         # Auto-create links
auto_backlink: true     # Auto-create backlinks
```

## Real Example: Temporal Connection Done Right

### Scenario
Note: `데이터-공유.md`
- Date: 2025-10-29
- Content: "MFT팀... 왜 데이터 공유를 해야하는지"
- Company: Qraft

### ❌ BAD Approach
```markdown
## Related
- [[Data-Governance-Hub]]  # Generic, no context
- [[Airflow-Best-Practices]]  # Wrong! Not mentioned
```

### ✅ GOOD Approach

**Step 1: Read and understand**
```python
note = read_note("데이터-공유.md")
# Content: "MFT팀... 왜 데이터 공유를 해야하나"
# Date: 2025-10-29
# Company: Qraft
```

**Step 2: Find same week weekly**
```python
weekly = find_weekly("2025-10-27")  # 2 days before
read weekly → "본인팀은 잘하고 있는데, 왜 못하는 팀에게 공유를 해야하나"
# EXACT SAME INCIDENT! Perfect match!
```

**Step 3: Find related projects**
```python
projects = search_projects(date="2025-10", keywords=["데이터", "공유"])
read each → Find data governance projects active in October
```

**Step 4: Create connection**
```markdown
## 📎 Related

### 주간 회고 (같은 시기)
- [[02-Areas/크래프트테크놀로지스/Experience/Weekly/2025년-10월-27일|2025년 10월 27일]] (2일 전)
  - "본인팀은 잘하고 있는데, 왜 못하는 팀에게 공유를 해야하나"
  - **완전히 같은 사건!** MFT팀과의 데이터 공유 갈등

### 관련 프로젝트
- [[데이터-거버넌스-구축]]
  - 데이터 공유 문화 개선의 필요성
```

## Important Notes
- **ALWAYS read content first** - never guess!
- **ALWAYS check dates** - temporal context is essential
- **ALWAYS explain WHY** - add context to connections
- Preserve all existing frontmatter
- Use Obsidian MCP tools only
- Run silently - don't spam user with notifications
- Only alert for significant suggestions
