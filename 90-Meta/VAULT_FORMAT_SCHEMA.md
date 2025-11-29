# Vault 포맷 스키마

> Second Brain에서 사용하는 통일된 노트 포맷 정의

## 📋 Frontmatter 스키마

### 1. Life-Insights (본깨적)

**위치**: `30-Flow/Life-Insights/`

```yaml
---
title: "노트 제목"
date: "YYYY-MM-DD"
type: "insight" | "하루일기" | "일일회고"
week: 숫자
tags:
  - 주제태그
  - 역량태그
related:
  - "[[관련 노트]]"
---
```

**본문 구조**:
```markdown
# {title}

> **날짜**: {date}
> **주차**: {week}주차

## 본 것

(관찰한 상황, 경험)

## 깨달은 것

(인사이트, 깨달음)

## 적용할 것

(실천 방안)
```

---

### 2. Weekly Reflections (주간 회고)

**위치**: `02-Areas/크래프트테크놀로지스/Experience/Weekly/`

```yaml
---
title: "YYYY년 MM월 DD일"
date: "YYYY-MM-DD"
type: "weekly-reflection"
week: 숫자
tags:
  - 주제태그
  - 역량태그
summary: "한 줄 요약"
achievements: []
challenges: []
learnings: []
next_week: []
related_projects:
  - "[[프로젝트명]]"
---
```

**본문 구조**:
```markdown
## 🌟 한 줄 요약

(주간 요약)

## ✨ 성과 / 개선점

- 성과 항목

## 🚩 문제 상황

- 문제 항목

## 🙌 배운 점

- 학습 내용

## 🔧 대처 방법

- 해결 방안

## 📋 다음 주 계획

- 계획 항목

---

### Related Projects

- [[프로젝트 링크]]
```

---

### 3. Projects (프로젝트/업무)

**위치**: `02-Areas/크래프트테크놀로지스/Projects/`

```yaml
---
title: "프로젝트명"
type: "project"
status: "planned" | "active" | "completed" | "on-hold"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
completed: "YYYY-MM-DD"
tags:
  - 기술태그
  - 도메인태그
jira_key: "KEY-123"
related:
  - "[[관련 문서]]"
---
```

**상태 매핑**:
- `리스트업` → `planned`
- `진행중` → `active`
- `완료` → `completed`
- `보류` → `on-hold`

**본문 구조**:
```markdown
## 📌 개요

(프로젝트 설명)

## 🎯 목표

- 목표 1
- 목표 2

## 📝 작업 내용

- [ ] 작업 1
- [ ] 작업 2

## 🔗 관련 자료

- [[레퍼런스]]

## 💡 시행착오

### 문제
(문제 설명)

### 해결
(해결 방법)
```

---

### 4. Resources (레퍼런스)

**위치**: `03-Resources/`

```yaml
---
title: "자료 제목"
type: "resource"
category: "Airflow" | "DBT" | "Data-Governance" | ...
tags:
  - 기술태그
  - 주제태그
url: "https://..."
author: "작성자"
date: "YYYY-MM-DD"
summary: "요약"
related:
  - "[[관련 문서]]"
---
```

**본문 구조**:
```markdown
## 📚 출처

[링크 제목](URL)

## 💡 핵심 내용

(주요 내용 요약)

## 🔑 인사이트

- 인사이트 1
- 인사이트 2

## 📋 실전 적용

(적용 방법)

## 🔗 관련 자료

- [[관련 노트]]
```

---

## 🏷️ 태그 규칙

### 1. 기술 태그 (소문자, 하이픈)
- `airflow`, `dbt`, `datahub`
- `postgresql`, `snowflake`
- `aws`, `docker`, `kubernetes`
- `python`, `sql`

### 2. 역량 태그 (한글)
- `의사소통`, `문서화`, `문제해결`
- `구조화`, `데이터모델링`, `거버넌스`

### 3. 도메인 태그
- `data-engineering`, `data-governance`
- `infrastructure`, `automation`

### 4. 제거할 태그
- `notion-import` (임시 마이그레이션 태그)
- `본깨적`, `회고록`, `업무리스트`, `레퍼런스` (DB 이름)

---

## 🔄 정규화 규칙

### 1. 날짜 필드 통일
**변경 전**:
- `날짜(생성날짜)`, `생성 일시`, `최종편집시각`
- ISO 형식: `2025-10-31T14:20:00.000Z`

**변경 후**:
- `date`, `created`, `updated`
- 간소화: `2025-10-31`

### 2. Notion 필드 제거
모든 Notion 관련 메타데이터 제거:
- `source`, `notion_id`, `imported`, `database`
- 이모지 필드: `🔧 대처 방법`, `🌟 한 줄 요약` 등
- API 용 필드: `주제(API용)`, `업무 구상 1` 등

### 3. 빈 필드 제거
- `""`, `[]` 등 빈 값은 제거

### 4. 링크 포맷 통일
- `🔖 [링크](URL)` → `[링크](URL)`
- 일반 마크다운 링크로 통일

### 5. 관계 표현
- `상위 항목`, `하위 항목` → `related`
- 위키링크 형식: `[[노트명]]`

---

## 🤖 자동화

### 스크립트 실행

```bash
# Dry-run (미리보기)
python automation/normalize_vault_format.py --dry-run

# 실제 적용
python automation/normalize_vault_format.py
```

### 처리 대상
- `30-Flow/Life-Insights/`
- `02-Areas/크래프트테크놀로지스/`
- `03-Resources/`

### 제외 대상
- `README.md`
- `automation/`
- `99-Assets/`
- `.git/`, `.obsidian/`

---

**생성일**: 2025-11-29
**마지막 업데이트**: 2025-11-29
