---
tags:
  - automation
  - notion
  - github-actions
  - setup
created: '2025-11-28'
updated: '2025-11-30'
type: documentation
---
# RecordMaster Automation Setup

## 📋 Overview

**RecordMaster**는 모든 콘텐츠를 관리하는 단일 Notion 데이터베이스에서 Obsidian으로 자동 동기화하는 시스템입니다.

**핵심 특징**:
- ✅ 단일 데이터베이스 (RecordMaster)
- ✅ Content Type 기반 자동 분류
- ✅ GitHub Actions 자동 실행
- ✅ 간소화된 속성 (10개)

## 🏗️ Architecture

```
┌──────────────────────┐
│  Notion              │
│  RecordMaster DB     │  1. 템플릿으로 작성
│  Mig_Status=NEEDED   │  2. Properties 설정
└──────────┬───────────┘
           │
           │ 3. GitHub Actions
           │    (매일 자동 / 수동)
           ↓
┌──────────────────────┐
│  notion_sync.py      │  4. Content_Type별 분류
│                      │  5. Frontmatter 생성
└──────────┬───────────┘
           │
           │ 6. 파일 생성
           ↓
┌──────────────────────┐
│  Obsidian Vault      │
│  02-Areas/           │  Project, Experience
│  03-Resources/       │  Reference, Article, Book
│  30-Flow/            │  Insight
└──────────┬───────────┘
           │
           │ 7. Mig_Status 업데이트
           ↓
┌──────────────────────┐
│  Notion              │
│  Mig_Status=DONE     │  8. 동기화 완료
└──────────────────────┘
```

## 🔐 Security Setup

### 1. Notion API Token 생성

**단계**:
1. [Notion Integrations](https://www.notion.so/my-integrations) 접속
2. "New integration" 클릭
3. Integration 이름: `Obsidian Sync`
4. Workspace 선택
5. "Submit" 클릭
6. **Internal Integration Token** 복사 (안전하게 보관!)

**형식**: `secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 2. RecordMaster Database 생성

**Notion에서**:
1. 새 Full Page Database 생성
2. 이름: `RecordMaster`
3. 10개 속성 추가 ([RECORD_MASTER_SCHEMA.md](RECORD_MASTER_SCHEMA.md) 참조):
   - 이름 (Title)
   - Content_Type (Select) - 6개 옵션
   - Mig_Status (Select) - 4개 옵션
   - Category (Multi-select)
   - Company (Select)
   - Tags (Multi-select)
   - Status (Select)
   - Period (Select)
   - Created (Created time)
   - Updated (Last edited time)

### 3. Database에 Integration 연결

**RecordMaster DB에서**:
1. 우측 상단 `...` 메뉴 클릭
2. "Add connections" 선택
3. `Obsidian Sync` Integration 선택
4. ✅ 연결 확인

### 4. Database ID 확인

**Notion URL에서**:
```
https://www.notion.so/workspace/abc123def456?v=...
                              ^^^^^^^^^^^^
                              Database ID (32자리 hex)
```

**하이픈 제거**:
- ✅ `abc123def456abc123def456abc123de`
- ❌ `abc123de-f456-abc1-23de-f456abc123de`

### 5. GitHub Secrets 설정

**Repository Settings → Secrets and variables → Actions → New repository secret**

**필수 Secrets** (2개):

```bash
# 1. Notion API Token
NOTION_API_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 2. RecordMaster Database ID (32자리 hex, 하이픈 없음)
RECORD_MASTER_DB_ID=abc123def456abc123def456abc123de
```

**추가 Secret** (GitHub Actions용):

```bash
# GitHub Personal Access Token (자동 커밋용)
GH_PAT=ghp_xxxxxxxxxxxxxxxxxxxxx
```

### 6. GitHub Personal Access Token (PAT) 생성

**단계**:
1. GitHub Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. "Generate new token (classic)"
4. 권한 선택:
   - ✅ `repo` (전체)
   - ✅ `workflow`
5. Token 생성 후 복사
6. Repository Secrets에 `GH_PAT`으로 저장

## 🚀 Usage

### 1️⃣ 로컬 설정 (최초 1회)

```bash
# 1. config.json 생성
cp automation/config.template.json automation/config.json

# 2. config.json 편집
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

# ⚠️ 주의: config.json은 .gitignore에 포함되어 있음 (절대 커밋 금지!)
```

### 2️⃣ 로컬 테스트

```bash
# 의존성 설치
pip install requests

# 동기화 실행
python automation/notion_sync.py

# 결과 확인
# - Obsidian vault에 파일 생성됨
# - Notion에서 Mig_Status가 DONE으로 변경됨
```

**자세한 내용**: [LOCAL_TESTING_GUIDE.md](LOCAL_TESTING_GUIDE.md)

### 3️⃣ GitHub Actions 자동 실행

**설정 파일**: `.github/workflows/notion-sync.yml`

**자동 실행**:
- 매일 한국시간 오전 9시 (UTC 0시)
- `Mig_Status=NEEDED`인 페이지만 동기화

**수동 실행**:
1. GitHub → Actions 탭
2. "Notion to Obsidian Sync" 워크플로우 선택
3. "Run workflow" 클릭
4. Branch 선택 후 실행

## 📁 File Structure

```
Second-Brain/
├── .github/
│   └── workflows/
│       └── notion-sync.yml          # GitHub Actions
│
├── automation/
│   ├── notion_sync.py               # 🔄 메인 동기화
│   ├── create_upgraded_templates.py # 📋 템플릿 생성
│   ├── delete_old_templates.py      # 🗑️  템플릿 삭제
│   ├── check_db_schema.py           # 🔍 스키마 확인
│   ├── remove_database_properties.py# ⚙️  속성 제거
│   │
│   ├── config.json                  # 🔐 설정 (gitignore)
│   ├── config.template.json         # 📝 템플릿
│   ├── requirements.txt             # 📦 의존성
│   │
│   └── [Documentation]
│       ├── README.md
│       ├── AUTOMATION_SETUP.md      # 이 문서
│       ├── GITHUB_SECRETS_SETUP.md
│       ├── LOCAL_TESTING_GUIDE.md
│       ├── RECORD_MASTER_OVERVIEW.md
│       ├── RECORD_MASTER_SCHEMA.md
│       ├── TEMPLATE_SUMMARY.md
│       └── TEMPLATE_USAGE_GUIDE.md
│
├── 02-Areas/
│   └── 크래프트테크놀로지스/
│       ├── Projects/                # Project → Active/Completed/Archived
│       └── Experience/
│           └── Weekly/              # Experience
│
├── 03-Resources/
│   ├── Technology/                  # Reference
│   ├── Articles/                    # Article
│   └── Books/                       # Book
│
└── 30-Flow/
    └── Life-Insights/               # Insight
```

## 🔍 How It Works

### 1. Filtering

```python
# Mig_Status=NEEDED인 레코드만 조회
filter_config = {
    "filter": {
        "property": "Mig_Status",
        "select": {
            "equals": "NEEDED"
        }
    },
    "sorts": [
        {
            "property": "Updated",
            "direction": "descending"  # 최근 수정된 것부터
        }
    ]
}
```

### 2. Content Type별 분류

```python
location_mapping = {
    "Project": "02-Areas/.../Projects/Active",
    "Experience": "02-Areas/.../Experience/Weekly",
    "Reference": "03-Resources",
    "Insight": "30-Flow/Life-Insights",
    "Article": "03-Resources/Articles",
    "Book": "03-Resources/Books"
}
```

**추가 분류**:
- **Project**: Status에 따라 Active/Completed/Archived
- **Reference**: Category에 따라 Technology/Career/Investment 등
- **Insight**: Company에 따라 Work/Personal

### 3. Frontmatter 생성

```yaml
---
notion_id: abc123def456
content_type: Project
created: 2025-11-30T09:00:00.000Z
updated: 2025-11-30T10:30:00.000Z
tags:
  - Airflow
  - DBT
company: Qraft
status: Active
category:
  - Technology
---
```

### 4. Status Update

**성공 시**:
```python
# Notion에서 Mig_Status를 DONE으로 업데이트
properties = {
    "Mig_Status": {
        "select": {"name": "DONE"}
    }
}
```

**실패 시**:
```python
# ERROR로 업데이트
properties = {
    "Mig_Status": {
        "select": {"name": "ERROR"}
    }
}
```

### 5. Git Commit (GitHub Actions)

```bash
git add .
git commit -m "🔄 Notion sync: 2025-11-30 09:00:00"
git push
```

## 🛠️ Troubleshooting

### "config.json not found"

**원인**: config.json 파일이 없음

**해결**:
```bash
cp automation/config.template.json automation/config.json
# config.json 편집하여 실제 값 입력
```

### "API Error: 401" (Unauthorized)

**원인**:
- 잘못된 Notion API token
- Integration이 Database에 연결되지 않음

**해결**:
1. Notion Integration token 재확인
2. RecordMaster DB에 Integration 연결 확인
3. Token 앞부분이 `secret_`으로 시작하는지 확인

### "API Error: 404" (Not Found)

**원인**: 잘못된 Database ID

**해결**:
1. Notion RecordMaster URL에서 ID 확인
2. 32자리 hex 문자열인지 확인
3. 하이픈 제거 확인

### "Property 'Name' not found"

**원인**: Database 속성 이름 불일치

**해결**:
```bash
# 스키마 확인
python automation/check_db_schema.py

# 출력에서 "이름" (한글) 확인
# notion_sync.py는 "Name"이 아닌 실제 속성명 사용
```

### GitHub Actions 실행 실패

**원인**: GitHub Secrets 미설정

**해결**:
1. Repository Settings → Secrets 확인
2. 필수 Secrets 설정:
   - `NOTION_API_TOKEN`
   - `RECORD_MASTER_DB_ID`
   - `GH_PAT` (자동 커밋용)

### 파일이 잘못된 위치에 생성됨

**원인**: Content_Type 또는 분류 로직

**해결**:
1. Notion에서 Content_Type 확인
2. `config.json`의 `location_mapping` 확인
3. `notion_sync.py`의 `determine_target_path()` 확인

## 📊 Monitoring

### Notion에서 확인

**Mig_Status 상태**:
- `NEEDED` → 동기화 대기 중
- `DONE` → 동기화 완료
- `SKIP` → 템플릿 (동기화 안 함)
- `ERROR` → 동기화 오류 발생

**View 추천**:
- "동기화 대기" View: `Mig_Status = NEEDED`
- "완료" View: `Mig_Status = DONE`
- "오류" View: `Mig_Status = ERROR`

### GitHub Actions 로그

**확인 방법**:
1. Actions 탭 이동
2. 최근 실행 내역 선택
3. 상세 로그 확인

**로그 예시**:
```
🔄 Starting Record Master Sync...
🔍 Fetching records with Mig_Status=NEEDED...
📊 Found 5 records

[1/5] 📝 Airflow 3.0 학습...
   ✅ Created: 03-Resources/Technology/Airflow/Airflow-3.0-학습.md

...

✅ Success: 5
❌ Errors: 0
```

### Obsidian에서 확인

**파일 위치**:
- Project → `02-Areas/.../Projects/`
- Experience → `02-Areas/.../Experience/Weekly/`
- Reference → `03-Resources/`
- Insight → `30-Flow/Life-Insights/`

**Frontmatter**:
- `notion_id`로 원본 페이지 추적 가능
- `content_type`, `tags`, `company` 등 메타데이터 확인

## 🔄 Workflow Example

### 일반적인 사용 흐름

**1. Notion에서 작성**
```
1. RecordMaster DB 열기
2. 템플릿 선택 (예: 📋 Project)
3. Duplicate
4. 내용 작성
5. Properties 설정:
   - Content_Type: Project
   - Category: Technology
   - Tags: #Airflow, #DBT
   - Company: Qraft
6. Mig_Status = NEEDED로 변경
```

**2. 자동 동기화** (매일 9시 또는 수동)
```
GitHub Actions 실행
↓
notion_sync.py 동작
↓
Obsidian 파일 생성
↓
Git 자동 커밋
```

**3. Obsidian에서 확인**
```
1. Git pull (최신 상태 유지)
2. 02-Areas/.../Projects/에서 파일 확인
3. /organize 명령어로 재분류 (선택)
```

**4. Notion 상태 자동 업데이트**
```
Mig_Status: NEEDED → DONE
(자동으로 변경됨)
```

## 🎯 Best Practices

### Notion

**✅ DO**:
- 템플릿 복제 사용 (Duplicate)
- Properties 정확히 설정
- 구체적인 제목 작성
- Mig_Status=NEEDED로 동기화 트리거

**❌ DON'T**:
- 템플릿 직접 수정 (항상 Duplicate)
- Properties 미설정 상태로 동기화
- 빈 템플릿 그대로 동기화

### Git

**✅ DO**:
- 자동 커밋 전 로컬 변경사항 커밋
- Obsidian에서 수정 후 수동 커밋

**❌ DON'T**:
- 동기화된 파일을 Obsidian에서 직접 수정
  (Notion에서 수정 후 재동기화 권장)

### Security

**⚠️ CRITICAL**:
- `config.json` 절대 커밋 금지 (`.gitignore` 확인)
- Notion token 노출 금지
- GitHub PAT 최소 권한만 부여
- Secrets 정기적으로 재발급

## 📚 References

- [Notion API Documentation](https://developers.notion.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Obsidian Markdown Guide](https://help.obsidian.md/How+to/Format+your+notes)

## 🔗 Related Documentation

- [README.md](README.md) - Automation 개요
- [RECORD_MASTER_OVERVIEW.md](RECORD_MASTER_OVERVIEW.md) - RecordMaster 개념
- [RECORD_MASTER_SCHEMA.md](RECORD_MASTER_SCHEMA.md) - Database 스키마
- [TEMPLATE_USAGE_GUIDE.md](TEMPLATE_USAGE_GUIDE.md) - 템플릿 사용법
- [LOCAL_TESTING_GUIDE.md](LOCAL_TESTING_GUIDE.md) - 로컬 테스트
- [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) - GitHub Secrets

---

**Last Updated**: 2025-11-30
**Version**: 2.0 (RecordMaster only)
