# RecordMaster Database Schema

## 📋 Overview

**RecordMaster**는 모든 콘텐츠를 관리하는 단일 Notion 데이터베이스입니다.

**핵심 원칙**:
- 단일 진입점 (Single Entry Point)
- Content Type 기반 자동 분류
- 간소화된 속성 (Essential Properties Only)
- Obsidian 동기화 최적화

## 🏗️ Database Properties (10개)

### 1. Core Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| **이름** | Title | ✅ | 페이지 제목 |
| **Content_Type** | Select | ✅ | Project, Experience, Reference, Insight, Article, Book |
| **Mig_Status** | Select | ✅ | NEEDED, DONE, SKIP, ERROR |
| **Created** | Created time | Auto | 생성 시간 |
| **Updated** | Last edited time | Auto | 수정 시간 |

### 2. Classification Properties

| Property | Type | Required | Description | Examples |
|----------|------|----------|-------------|----------|
| **Category** | Multi-select | ⚪ | 주제 분류 | Technology, Career, Investment, Life |
| **Company** | Select | ⚪ | 회사/조직 | aivelabs, Qraft |
| **Tags** | Multi-select | ⚪ | 세부 태그 | #Airflow, #DBT, #회고 |
| **Status** | Select | ⚪ | 상태 (프로젝트용) | Active, Completed, Archived |
| **Period** | Select | ⚪ | 기간 (프로젝트/경험용) | 2025-Q1, 2025-Q2 |

## 📊 Property Details

### Content_Type Options

| Value | Description | Obsidian Location | Framework |
|-------|-------------|-------------------|-----------|
| **Project** | 업무 프로젝트 | `02-Areas/.../Projects/` | SMART + STAR + KPT |
| **Experience** | 주간 회고 | `02-Areas/.../Experience/Weekly/` | ORID |
| **Reference** | 기술 지식 | `03-Resources/Technology/` | Feynman + First Principles |
| **Insight** | 본깨적 | `30-Flow/Life-Insights/` | First Principles + Mental Models |
| **Article** | 아티클 요약 | `03-Resources/Articles/` | Progressive Summarization |
| **Book** | 책 정리 | `03-Resources/Books/` | Action-oriented |

### Mig_Status Options

| Value | Description | When to Use |
|-------|-------------|-------------|
| **NEEDED** | 동기화 대기 | 콘텐츠 작성 완료 후 설정 |
| **DONE** | 동기화 완료 | 자동 설정 (notion_sync.py) |
| **SKIP** | 동기화 제외 | 템플릿 페이지 (항상 SKIP) |
| **ERROR** | 동기화 오류 | 자동 설정 (오류 발생 시) |

### Category Options

**Technology**:
- Airflow, DBT, DataHub
- PostgreSQL, AWS
- Python, FastAPI

**Career**:
- Interviews, Resume
- Achievements, Skills

**Investment**:
- Stock, Crypto
- Analysis, Strategy

**Life**:
- Personal, Health
- Relationships, Growth

**Data-Governance**:
- Architecture, Patterns
- Access Control, Quality

### Company Options

| Value | Description | Period |
|-------|-------------|--------|
| **aivelabs** | 에이블랩스 | 2022-2023 |
| **Qraft** | 크래프트테크놀로지스 | 2025-08+ |

### Status Options (for Projects)

| Value | Description |
|-------|-------------|
| **Active** | 진행 중 |
| **Completed** | 완료 |
| **Archived** | 보관 (과거 프로젝트) |

### Period Options

Format: `YYYY-QN` (quarter) or `YYYY-MM` (month)

Examples:
- `2025-Q1`, `2025-Q2`, `2025-Q3`, `2025-Q4`
- `2025-08`, `2025-09`, `2025-10`

## 🔄 Workflow

### 1️⃣ Notion에서 작성

```
1. RecordMaster DB 열기
2. 템플릿 선택 (Content_Type에 맞게)
3. Duplicate
4. 내용 작성
5. Properties 설정:
   - Content_Type ✅
   - Category, Tags (optional)
   - Company (if work-related)
   - Status (if Project)
6. Mig_Status = NEEDED로 변경
```

### 2️⃣ 자동 동기화

```
GitHub Actions (매일 자동 실행):
1. Mig_Status=NEEDED 필터링
2. Updated 시간 순으로 정렬 (최신순)
3. Content_Type별로 적절한 위치에 파일 생성
4. Frontmatter 생성 (notion_id, tags, company 등)
5. Mig_Status = DONE으로 업데이트
```

### 3️⃣ Obsidian에서 재분류

```
Claude Code의 /organize 명령어:
1. 콘텐츠 분석
2. 적절한 위치로 이동 제안
3. 관련 노트 백링크 생성
4. 태그 정규화
5. 지식 네트워크 구축
```

## 📝 Template Guidelines

### What Templates Include

**All templates have**:
1. 📝 Callout (사용 가이드)
2. Content_Type에 맞는 구조화된 섹션
3. 질문/프롬프트 (풍부한 콘텐츠 유도)
4. 관련 문서 링크 섹션

**Templates do NOT include**:
- ❌ Unnecessary metadata sections
- ❌ Excessive properties
- ❌ Migration-related fields

### Template Properties

**모든 템플릿의 기본 설정**:
```yaml
이름: "[템플릿] {Content_Type}"
Content_Type: {해당 타입}
Mig_Status: SKIP  # 템플릿은 항상 SKIP!
Category: [적절한 기본값]
```

**사용자가 복제 후 설정**:
- 제목 변경 (실제 콘텐츠 제목으로)
- Category 조정
- Tags 추가
- Company 설정 (업무 관련 시)
- Mig_Status = NEEDED로 변경

## 🎯 Best Practices

### ✅ DO

1. **템플릿 복제**
   - 템플릿을 Duplicate 사용
   - 제목을 구체적으로 변경
   - Properties 정확히 설정

2. **구체적인 제목**
   - ❌ "DataHub 설정"
   - ✅ "Airflow 3.x와 DataHub 연동 (Custom Source 개발)"

3. **적절한 분류**
   - Content_Type 정확히 선택
   - Category/Tags 일관되게 사용
   - Company 구분 (aivelabs vs Qraft)

4. **동기화 트리거**
   - 작성 완료 후 Mig_Status = NEEDED
   - Properties 모두 설정 후 동기화

### ❌ DON'T

1. **템플릿 직접 수정**
   - 템플릿은 항상 Mig_Status=SKIP
   - 수정하면 동기화 안 됨

2. **불완전한 콘텐츠**
   - 빈 템플릿 그대로 동기화
   - Properties 미설정 상태로 동기화

3. **중복 생성**
   - 같은 콘텐츠 여러 번 생성
   - Mig_Status=DONE인 것 다시 NEEDED로 변경

## 🔧 Database Setup

### 초기 설정 (최초 1회)

```
1. Notion에서 Full Page Database 생성
2. 이름: "RecordMaster"
3. 위 10개 속성 추가:
   - 이름 (Title) - 자동 생성됨
   - Content_Type (Select) - 6개 옵션
   - Mig_Status (Select) - 4개 옵션
   - Category (Multi-select)
   - Company (Select) - 2개 옵션
   - Tags (Multi-select)
   - Status (Select) - 3개 옵션
   - Period (Select)
   - Created (Created time) - 자동
   - Updated (Last edited time) - 자동
4. 6개 템플릿 생성 (create_upgraded_templates.py 실행)
```

### Notion Views 제안

**View 1: 동기화 대기**
- Filter: `Mig_Status = NEEDED`
- Sort: `Updated (최신순)`
- Properties: 이름, Content_Type, Category, Tags

**View 2: 템플릿**
- Filter: `Mig_Status = SKIP`
- Group: `Content_Type`
- Properties: 이름

**View 3: Content Type별**
- Filter: `Mig_Status ≠ SKIP`
- Group: `Content_Type`
- Sort: `Updated (최신순)`
- Properties: 이름, Tags, Company, Status

**View 4: 회사별**
- Filter: `Company is not empty`
- Group: `Company`
- Sort: `Updated (최신순)`
- Properties: 이름, Content_Type, Period

## 🔗 Related Documentation

- [README.md](README.md) - Automation 개요
- [TEMPLATE_SUMMARY.md](TEMPLATE_SUMMARY.md) - 템플릿 빠른 참조
- [TEMPLATE_USAGE_GUIDE.md](TEMPLATE_USAGE_GUIDE.md) - 템플릿 상세 가이드
- [RECORD_MASTER_OVERVIEW.md](RECORD_MASTER_OVERVIEW.md) - RecordMaster 개념

---

**Last Updated**: 2025-11-30
**Schema Version**: 2.0 (Simplified - 10 properties)
