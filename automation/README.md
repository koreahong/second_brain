---
tags:
  - automation
  - index
created: '2025-11-28'
updated: '2025-11-30'
type: index
---
# Automation 🤖

> **RecordMaster 동기화**: Notion RecordMaster 데이터베이스에서 Obsidian vault로 자동 동기화

## 📋 개요

이 디렉토리는 **Notion RecordMaster → Obsidian** 자동 동기화 시스템입니다.

**핵심 워크플로우**:
1. Notion RecordMaster에서 템플릿으로 콘텐츠 작성
2. `Mig_Status` = `NEEDED`로 설정
3. GitHub Actions가 자동으로 Obsidian에 동기화
4. Obsidian에서 `/organize`로 재분류 및 지식 네트워크 구축

## 📁 파일 구조

```
automation/
├── notion_sync.py                  # 🔄 메인 동기화 스크립트
│
├── create_upgraded_templates.py    # 📋 템플릿 생성
├── delete_old_templates.py         # 🗑️  템플릿 삭제
│
├── check_db_schema.py              # 🔍 스키마 확인
├── remove_database_properties.py   # ⚙️  속성 제거
├── analyze_notion_databases.py     # 📊 DB 분석
├── deep_analyze_databases.py       # 📊 상세 분석
├── list_all_databases.py           # 📋 DB 목록
├── fetch_notion_examples.py        # 📄 예제 조회
│
├── config.json                     # 🔐 설정 (gitignore)
├── config.template.json            # 📝 설정 템플릿
├── requirements.txt                # 📦 의존성
│
├── README.md                       # 📖 이 파일
├── AUTOMATION_SETUP.md             # ⚙️  전체 설정 가이드
├── GITHUB_SECRETS_SETUP.md         # 🔐 GitHub Secrets
├── LOCAL_TESTING_GUIDE.md          # 🧪 로컬 테스트
│
├── RECORD_MASTER_OVERVIEW.md       # 🎯 RecordMaster 개요
├── RECORD_MASTER_SCHEMA.md         # 📊 DB 스키마
├── TEMPLATE_SUMMARY.md             # 📋 템플릿 요약
└── TEMPLATE_USAGE_GUIDE.md         # 📖 템플릿 사용법
```

## 🚀 빠른 시작

### 1️⃣ 설정 (최초 1회)

```bash
# 1. config.json 생성
cp automation/config.template.json automation/config.json

# 2. config.json 편집
# - Notion API Token
# - RecordMaster Database ID
# - Vault Path
```

**상세 가이드**: [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md)

### 2️⃣ Notion에서 콘텐츠 작성

1. RecordMaster 데이터베이스 열기
2. 템플릿 선택 (Project, Experience, Reference, Insight, Article, Book)
3. 템플릿 복제 (Duplicate)
4. 내용 작성
5. `Mig_Status` = `NEEDED`로 설정

**템플릿 가이드**: [TEMPLATE_USAGE_GUIDE.md](TEMPLATE_USAGE_GUIDE.md)

### 3️⃣ 동기화 실행

**로컬 테스트**:
```bash
python automation/notion_sync.py
```

**자동 실행**: GitHub Actions (매일 자동)

**상세 가이드**: [LOCAL_TESTING_GUIDE.md](LOCAL_TESTING_GUIDE.md)

### 4️⃣ Obsidian에서 재분류

```
/organize
```

Obsidian에서 `/organize` 명령어로 PARA 구조로 자동 분류 및 지식 네트워크 구축

## 🎯 RecordMaster 시스템

### 핵심 개념

**RecordMaster**는 모든 콘텐츠를 관리하는 단일 Notion 데이터베이스입니다.

**Content Types** (6가지):
- **Project**: 업무 프로젝트 (SMART + STAR + KPT)
- **Experience**: 주간 회고 (ORID)
- **Reference**: 기술 지식 (Feynman + First Principles)
- **Insight**: 본깨적 (First Principles + Mental Models)
- **Article**: 아티클 요약 (Progressive Summarization)
- **Book**: 책 정리 (Action-oriented)

**Migration Status**:
- `NEEDED`: 동기화 대기
- `DONE`: 동기화 완료
- `SKIP`: 템플릿 (동기화 안 함)
- `ERROR`: 오류 발생

**자세한 내용**: [RECORD_MASTER_OVERVIEW.md](RECORD_MASTER_OVERVIEW.md)

## 📊 Database Schema

**10개 속성**:
- `이름` (title): 페이지 제목
- `Content_Type` (select): Project, Experience, Reference, Insight, Article, Book
- `Mig_Status` (select): NEEDED, DONE, SKIP, ERROR
- `Category` (multi_select): 카테고리
- `Company` (select): aivelabs, Qraft
- `Tags` (multi_select): 태그
- `Status` (select): Active, Completed, Archived
- `Period` (select): 2025-Q1, 2025-Q2, etc.
- `Created` (created_time): 생성 시간
- `Updated` (last_edited_time): 수정 시간

**자세한 내용**: [RECORD_MASTER_SCHEMA.md](RECORD_MASTER_SCHEMA.md)

## 🔄 Workflow

```
┌─────────────────┐
│  Notion         │
│  RecordMaster   │  1. 템플릿으로 작성
│                 │  2. Mig_Status=NEEDED
└────────┬────────┘
         │
         │ 3. GitHub Actions
         │    (자동 또는 수동)
         ↓
┌─────────────────┐
│  notion_sync.py │  4. 동기화 실행
│                 │  5. Mig_Status=DONE
└────────┬────────┘
         │
         │ 6. 파일 생성
         ↓
┌─────────────────┐
│  Obsidian       │  7. /organize
│  Vault          │  8. 지식 네트워크 구축
└─────────────────┘
```

## 🤖 GitHub Actions

**파일**: `.github/workflows/notion-sync.yml`

**자동 실행**: 매일 한국시간 오전 9시 (UTC 0시)

**수동 실행**: GitHub Actions 탭에서 "Run workflow"

**필요한 Secrets**:
- `NOTION_API_TOKEN`
- `RECORD_MASTER_DB_ID`

**설정 가이드**: [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)

## 📖 Documentation

### 설정 & 테스트
- [AUTOMATION_SETUP.md](AUTOMATION_SETUP.md) - 전체 설정 가이드
- [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) - GitHub Secrets 설정
- [LOCAL_TESTING_GUIDE.md](LOCAL_TESTING_GUIDE.md) - 로컬 테스트 방법

### RecordMaster
- [RECORD_MASTER_OVERVIEW.md](RECORD_MASTER_OVERVIEW.md) - RecordMaster 개요
- [RECORD_MASTER_SCHEMA.md](RECORD_MASTER_SCHEMA.md) - Database 스키마

### Templates
- [TEMPLATE_SUMMARY.md](TEMPLATE_SUMMARY.md) - 템플릿 요약 (빠른 참조)
- [TEMPLATE_USAGE_GUIDE.md](TEMPLATE_USAGE_GUIDE.md) - 템플릿 상세 사용법

## 🔧 Scripts

### notion_sync.py
메인 동기화 스크립트. `Mig_Status=NEEDED`인 페이지를 Obsidian으로 동기화.

```bash
python automation/notion_sync.py
```

### create_upgraded_templates.py
RecordMaster에 6개 템플릿 생성 (사용자 패턴 + 연구 기반 프레임워크).

```bash
python automation/create_upgraded_templates.py
```

### delete_old_templates.py
`Mig_Status=SKIP`인 템플릿 페이지 삭제.

```bash
python automation/delete_old_templates.py
```

### check_db_schema.py
RecordMaster 스키마 조회 (속성 확인).

```bash
python automation/check_db_schema.py
```

## 🎓 Template System

**6개 템플릿** (사용자의 실제 작성 패턴 기반):

1. **📋 Project** - SMART + STAR + KPT
2. **📝 Experience** - 사용자의 Obsidian weekly 구조 + ORID
3. **📚 Reference** - Feynman + First Principles
4. **💡 Insight** - First Principles + Mental Models
5. **📰 Article** - 사용자의 컨텐츠 리스트 구조 + Progressive Summarization
6. **📕 Book** - Progressive Summarization + Action-oriented

**템플릿 사용법**: [TEMPLATE_USAGE_GUIDE.md](TEMPLATE_USAGE_GUIDE.md)

## 💡 Best Practices

### ✅ DO
- 템플릿 복제 후 Properties 설정 (Company, Category, Tags)
- 구체적으로 작성 ("DataHub 설정" ❌ → "Airflow 3.x와 DataHub 연동" ✅)
- Mig_Status를 NEEDED로 설정하여 동기화 트리거
- Obsidian에서 `/organize`로 재분류

### ❌ DON'T
- 템플릿을 직접 수정하지 마세요 (항상 Duplicate)
- 템플릿 가이드를 그대로 두지 마세요 (내용으로 채우기)
- Mig_Status=SKIP인 템플릿은 동기화되지 않음

## 🔗 Related

- **Main Project**: [.claude/CLAUDE.md](../.claude/CLAUDE.md)
- **Vault Structure**: [02-Areas](../02-Areas), [03-Resources](../03-Resources)
- **Slash Commands**: [/organize](.claude/commands/organize.md)

---

**Last Updated**: 2025-11-30
**Version**: 2.0 (RecordMaster only)
