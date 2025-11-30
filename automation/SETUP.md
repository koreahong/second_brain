---
tags:
  - automation
  - setup
created: '2025-11-30'
type: guide
---
# RecordMaster Setup Guide

## 🎯 개요

Notion RecordMaster → Obsidian 자동 동기화 시스템 설정

**소요 시간**: 약 10분

## 1️⃣ Notion 설정

### Step 1: Integration 생성

1. [Notion Integrations](https://www.notion.so/my-integrations) 접속
2. "New integration" 클릭
3. 이름: `Obsidian Sync`
4. "Submit" → Token 복사
   - 형식: `secret_xxxxxxxxx`

### Step 2: RecordMaster DB 생성

**Notion에서**:
1. 새 Full Page Database 생성
2. 이름: `RecordMaster`
3. 10개 속성 추가:
   ```
   - 이름 (Title) - 자동
   - Content_Type (Select): Project, Experience, Reference, Insight, Article, Book
   - Mig_Status (Select): NEEDED, DONE, SKIP, ERROR
   - Category (Multi-select)
   - Company (Select): aivelabs, Qraft
   - Tags (Multi-select)
   - Status (Select): Active, Completed, Archived
   - Period (Select): 2025-Q1, 2025-Q2 등
   - Created (Created time) - 자동
   - Updated (Last edited time) - 자동
   ```

**자세한 스키마**: [SCHEMA.md](SCHEMA.md)

### Step 3: Integration 연결

1. RecordMaster DB 열기
2. 우측 상단 `...` → "Add connections"
3. `Obsidian Sync` 선택

### Step 4: Database ID 확인

**URL에서 추출**:
```
https://www.notion.so/workspace/abc123def456?v=...
                              ^^^^^^^^^^^^
                              Database ID
```

**32자리 hex, 하이픈 제거**:
- ✅ `abc123def456abc123def456abc123de`
- ❌ `abc123de-f456-abc1-23de-f456abc123de`

### Step 5: 템플릿 생성

```bash
python automation/create_upgraded_templates.py
```

6개 템플릿 자동 생성 (Mig_Status=SKIP)

## 2️⃣ GitHub 설정

### GitHub Secrets 추가

**Repository → Settings → Secrets and variables → Actions**

```bash
# 1. Notion API Token
NOTION_API_TOKEN=secret_xxxxxxxxx

# 2. RecordMaster Database ID
RECORD_MASTER_DB_ID=abc123def456abc123def456abc123de

# 3. GitHub PAT (자동 커밋용)
GH_PAT=ghp_xxxxxxxxxxxxx
```

### GitHub PAT 생성

1. GitHub Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. "Generate new token"
4. 권한: `repo`, `workflow`
5. Token 복사 → `GH_PAT`로 저장

## 3️⃣ 로컬 설정

### config.json 생성

```bash
cp automation/config.template.json automation/config.json
```

### config.json 편집

```json
{
  "notion": {
    "api_token": "secret_xxxxxxxxx",
    "record_master_db_id": "abc123def456abc123def456abc123de",
    "sync_settings": {
      "filter_status": "NEEDED",
      "batch_size": 100
    }
  },
  "obsidian": {
    "vault_path": "/Users/username/Second-Brain",
    "location_mapping": {
      "Project": "02-Areas/크래프트테크놀로지스/Projects/Active",
      "Experience": "02-Areas/크래프트테크놀로지스/Experience/Weekly",
      "Reference": "03-Resources",
      "Insight": "30-Flow/Life-Insights",
      "Article": "03-Resources/Articles",
      "Book": "03-Resources/Books"
    }
  }
}
```

**⚠️ 주의**: config.json은 `.gitignore`에 포함됨 (절대 커밋 금지!)

### 로컬 테스트

```bash
# 의존성 설치
pip install requests

# 동기화 실행
python automation/notion_sync.py

# 결과 확인
# - Obsidian vault에 파일 생성
# - Notion에서 Mig_Status=DONE
```

## 🔄 사용법

### Notion에서 콘텐츠 작성

1. RecordMaster DB 열기
2. 템플릿 선택 (예: 📋 Project)
3. **Duplicate** (복제)
4. 제목 변경 (구체적으로)
5. 내용 작성
6. Properties 설정:
   - Content_Type ✅
   - Category, Tags (선택)
   - Company (업무 관련 시)
7. **Mig_Status = NEEDED**

### 자동 동기화

**GitHub Actions** (매일 자동):
- 시간: 오전 9시 (KST)
- Filter: Mig_Status=NEEDED
- 결과: Obsidian 파일 생성

**수동 실행**:
1. GitHub → Actions 탭
2. "Notion to Obsidian Sync"
3. "Run workflow"

**로컬 실행**:
```bash
python automation/notion_sync.py
```

## 🛠️ Troubleshooting

### "config.json not found"
```bash
cp automation/config.template.json automation/config.json
# 편집 후 재실행
```

### "API Error: 401"
- Notion token 재확인
- Integration 연결 확인
- Token 형식: `secret_`로 시작

### "API Error: 404"
- Database ID 재확인
- 32자리 hex 확인
- 하이픈 제거 확인

### "Property not found"
```bash
# 스키마 확인
python automation/check_db_schema.py
```

## 📊 Monitoring

### Notion View 추천

**동기화 대기**:
- Filter: `Mig_Status = NEEDED`
- Sort: `Updated (최신순)`

**완료**:
- Filter: `Mig_Status = DONE`
- Sort: `Updated (최신순)`

**오류**:
- Filter: `Mig_Status = ERROR`

### GitHub Actions 로그

```
🔄 Starting Record Master Sync...
📊 Found 5 records

[1/5] 📝 Airflow 3.0 학습...
   ✅ Created: 03-Resources/Technology/Airflow/...

✅ Success: 5
❌ Errors: 0
```

## 🎯 Best Practices

### ✅ DO
- 템플릿 복제 (Duplicate)
- 구체적인 제목
- Properties 정확히 설정
- Mig_Status=NEEDED로 트리거

### ❌ DON'T
- 템플릿 직접 수정
- 빈 내용으로 동기화
- config.json 커밋
- 동기화된 파일 Obsidian에서 직접 수정

## 🔗 Related

- [README.md](README.md) - 전체 개요
- [SCHEMA.md](SCHEMA.md) - Database 스키마

---

**Last Updated**: 2025-11-30
