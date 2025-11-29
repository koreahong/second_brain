# Auto-Link Hook

**Trigger:** After file save in vault

**Purpose:** 자동으로 관련 노트를 찾아 8+ links를 생성

## Behavior

파일이 저장될 때:

1. **Skip conditions (이런 경우 건너뛰기):**
   - 파일이 vault 외부
   - 파일이 `.git/` 또는 `.obsidian/` 내부
   - 파일이 이미 8개 이상의 링크를 가짐

2. **Analysis (분석):**
   - `frontmatter.domain` 확인
   - `frontmatter.tags` 확인
   - Content에서 키워드 추출
   - 기존 링크 수 계산

3. **Find related notes (관련 노트 찾기):**
   - **Same domain** (2개): 같은 domain 태그
   - **Same technology** (2개): 같은 기술 스택
   - **Temporal** (2개): 같은 시간대 (±7일)
   - **Hub** (1개): 해당 domain의 hub note
   - **MOC** (1개): 해당 domain의 MOC

4. **Add connections (연결 추가):**
   ```markdown
   ## Connections

   ### Related
   - [[note1]] - Same domain: {{domain}}
   - [[note2]] - Same technology: {{tech}}

   ### Temporal
   - [[note3]] - Same week
   - [[note4]] - Related project

   ### Structure
   - [[hub]] - {{domain}} Hub
   - [[moc]] - {{domain}} MOC
   ```

5. **Update backlinks (백링크 업데이트):**
   - 연결된 각 노트에 자동 백링크 추가

6. **Report (보고):**
   ```
   ✅ Auto-linked: {{filename}}
   📊 Links: {{old-count}} → {{new-count}}
   🎯 Target: 8+ ✓

   Added:
   - [[note1]] (domain)
   - [[note2]] (tech)
   - [[note3]] (temporal)
   ...
   ```

## Configuration

```yaml
auto_link:
  enabled: true
  target_links: 8
  strategies:
    - domain_match: 2
    - tech_match: 2
    - temporal_match: 2
    - hub: 1
    - moc: 1
```

## Example

**Before:**
```markdown
---
domain: data-engineering/orchestration
tags: [airflow, dag]
---

# DAG 설계 원칙

Content here...
```

**After:**
```markdown
---
domain: data-engineering/orchestration
tags: [airflow, dag]
---

# DAG 설계 원칙

Content here...

## Connections

### Related Concepts
- [[Airflow Task Dependencies]] - Same domain
- [[DAG Best Practices]] - Same technology

### Temporal
- [[2025-11-20 Airflow 구축]] - Related project
- [[2025-11-25 DAG 리팩토링]] - Same week

### Structure
- [[Airflow Hub]] - Data Engineering Hub
- [[Data Orchestration MOC]] - Domain MOC

---
**Links:** 6/8 (progress)
```
