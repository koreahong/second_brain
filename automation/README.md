---
tags:
  - automation
  - index
created: '2025-11-28'
updated: '2025-11-30'
type: index
---
# Automation 🤖

> **RecordMaster**: Notion 단일 DB → Obsidian 자동 동기화

## 🎯 핵심 개념

**하나의 Notion 데이터베이스로 모든 것을 관리**

```
Notion RecordMaster
├── 📋 Project (업무)
├── 📝 Experience (회고)
├── 📚 Reference (기술문서)
├── 💡 Insight (본깨적)
├── 📰 Article (아티클)
└── 📕 Book (독서노트)
        ↓
   Mig_Status=NEEDED
        ↓
  GitHub Actions 자동 실행
        ↓
  Obsidian Vault에 자동 생성
  - 02-Areas/ (Project, Experience)
  - 03-Resources/ (Reference, Article, Book)
  - 30-Flow/ (Insight)
```

## 🚀 빠른 시작

### 1. Notion 설정 (5분)

```
1. Notion Integration 생성
2. RecordMaster DB 생성 (10개 속성)
3. Integration 연결
4. 템플릿 생성 실행
```

**자세한 내용**: [SETUP.md](SETUP.md)

### 2. GitHub 설정 (2분)

```bash
# Repository Secrets 추가
NOTION_API_TOKEN=secret_xxxxx
RECORD_MASTER_DB_ID=abc123def456
```

### 3. 로컬 테스트 (1분)

```bash
# config.json 생성
cp automation/config.template.json automation/config.json

# 설정 편집 후 실행
python automation/notion_sync.py
```

## 📊 RecordMaster 시스템

### Content Types (6가지)

| Type | Obsidian 위치 | 템플릿 |
|------|--------------|--------|
| **Project** | 02-Areas/.../Projects/ | SMART + STAR + KPT |
| **Experience** | 02-Areas/.../Experience/Weekly/ | ORID |
| **Reference** | 03-Resources/Technology/ | Feynman + First Principles |
| **Insight** | 30-Flow/Life-Insights/ | First Principles + Mental Models |
| **Article** | 03-Resources/Articles/ | Progressive Summarization |
| **Book** | 03-Resources/Books/ | Action-oriented |

### Properties (10개)

**Core** (5):
- 이름, Content_Type, Mig_Status, Created, Updated

**Classification** (5):
- Category, Company, Tags, Status, Period

**자세한 내용**: [SCHEMA.md](SCHEMA.md)

## 🔄 Workflow

### Notion에서

1. 템플릿 복제 (Duplicate)
2. 내용 작성
3. Properties 설정 (Category, Tags, Company 등)
4. Mig_Status = **NEEDED**

### 자동 동기화

- **매일**: GitHub Actions 자동 실행 (오전 9시)
- **수동**: Actions 탭에서 "Run workflow"

### Obsidian에서

1. Git pull (최신 상태 유지)
2. 파일 확인 (Content_Type별 위치)
3. `/organize` 명령어로 재분류 (선택)

## 📁 구조

```
automation/
├── notion_sync.py          # 메인 동기화
├── create_upgraded_templates.py
├── delete_old_templates.py
├── check_db_schema.py
├── remove_database_properties.py
│
├── config.json             # 설정 (gitignore)
├── config.template.json
├── requirements.txt
│
├── README.md               # 이 파일
├── SETUP.md                # 설정 가이드
└── SCHEMA.md               # DB 스키마
```

## 🔧 Scripts

### notion_sync.py
메인 동기화 스크립트. Mig_Status=NEEDED → Obsidian 파일 생성 → Mig_Status=DONE

```bash
python automation/notion_sync.py
```

### create_upgraded_templates.py
6개 템플릿 생성 (사용자 패턴 기반)

```bash
python automation/create_upgraded_templates.py
```

### check_db_schema.py
RecordMaster 스키마 확인

```bash
python automation/check_db_schema.py
```

## 💡 Best Practices

### ✅ DO
- 템플릿 복제 후 제목 변경
- Properties 정확히 설정
- 구체적인 제목 작성
- Mig_Status=NEEDED로 동기화

### ❌ DON'T
- 템플릿 직접 수정
- 빈 내용으로 동기화
- config.json 커밋

## 🔗 Documentation

- **[SETUP.md](SETUP.md)** - 전체 설정 가이드 (Notion, GitHub, 로컬)
- **[SCHEMA.md](SCHEMA.md)** - Database 스키마 상세

## 🎓 핵심 장점

**Before** (기존 방식):
- ❌ 4개 개별 DB (업무리스트, 회고록, 레퍼런스, 본깨적)
- ❌ 복잡한 속성 (16개)
- ❌ 분산된 관리

**After** (RecordMaster):
- ✅ 단일 DB
- ✅ 간소화된 속성 (10개)
- ✅ Content Type 기반 자동 분류
- ✅ 템플릿 기반 풍부한 콘텐츠

---

**Last Updated**: 2025-11-30
**Version**: 2.0
