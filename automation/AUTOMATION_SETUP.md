---
tags:
  - automation
  - notion
  - github-actions
  - setup
created: '2025-11-28'
updated: '2025-11-28'
type: documentation
---
# Notion to Obsidian 자동화 설정

## 📋 개요

이 문서는 Notion에서 Obsidian vault로 자동으로 데이터를 마이그레이션하는 시스템의 설정 및 사용 방법을 설명합니다.

## 🏗️ 아키텍처

```
┌─────────────────────┐
│  Notion Database    │
│  (mig_status=NEEDED)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   GitHub Actions    │
│  (매일 자동 실행)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  automation/        │
│  notion_sync.py     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Obsidian Vault      │
│ Experiences/Qraft/  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Notion Update       │
│ (mig_status=Done)   │
└─────────────────────┘
```

## 🔐 보안 설정

### 1. Notion API Token 생성

1. [Notion Integrations](https://www.notion.so/my-integrations) 접속
2. "New integration" 클릭
3. Integration 이름 입력 (예: "Obsidian Sync")
4. Workspace 선택
5. "Submit" 클릭
6. **Internal Integration Token** 복사 (잘 보관!)

### 2. Notion Database 연결

각 Database에서:
1. Database 페이지 열기
2. 우측 상단 `...` 메뉴 클릭
3. "Add connections" 선택
4. 생성한 Integration 선택

### 3. Database에 mig_status 속성 추가

각 Database에 다음 속성 추가:
- **속성명**: `mig_status`
- **타입**: Select
- **옵션**:
  - `NEEDED` (마이그레이션 필요)
  - `Done` (완료됨)
  - `Skip` (건너뛰기)

### 4. GitHub Secrets 설정

Repository Settings → Secrets and variables → Actions → New repository secret

필요한 Secrets:

```bash
# Notion API Token
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxx

# Database IDs (32자리 hex, 하이픈 없음)
NOTION_DB_WORK_LIST=253c6d433b4d80e58babc19e1f5956e3
NOTION_DB_DAE_WORK=2b8c6d433b4d806c8a0cd5c55a808ff5
NOTION_DB_MEMOIR=262c6d433b4d8077877cc459b1d2c977

# GitHub Personal Access Token (repo 권한)
GH_PAT=ghp_xxxxxxxxxxxxxxxxxxxxx
```

### 5. GitHub Personal Access Token (PAT) 생성

1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token (classic)" 클릭
3. 다음 권한 선택:
   - `repo` (전체)
   - `workflow`
4. Token 생성 후 복사
5. Repository Secrets에 `GH_PAT`으로 저장

## 🚀 사용 방법

### 자동 실행 (매일)

- **시간**: 매일 한국 시간 오전 9시 (UTC 0시)
- **동작**: `mig_status=NEEDED`인 페이지만 동기화
- **설정 파일**: [.github/workflows/notion-sync.yml](.github/workflows/notion-sync.yml)

### 수동 실행

GitHub Actions 페이지에서:

1. Actions 탭 이동
2. "Notion to Obsidian Sync" 워크플로우 선택
3. "Run workflow" 클릭
4. 옵션 설정:
   - **database**: 동기화할 DB (`work_list`, `dae_work`, `memoir`)
   - **force**: 모든 항목 동기화 (mig_status 무시)
5. "Run workflow" 실행

### 로컬에서 실행

```bash
# 1. 의존성 설치
pip install requests

# 2. config.json 생성 (config.template.json에서 복사)
cp config.template.json config.json

# 3. config.json 편집 (Notion token과 Database ID 입력)
# 주의: config.json은 .gitignore에 포함되어 절대 커밋되지 않습니다

# 4. 스크립트 실행
python automation/notion_sync.py

# 또는 환경 변수로 옵션 설정
TARGET_DB=dae_work python automation/notion_sync.py
FORCE_SYNC=true python automation/notion_sync.py
```

## 📁 파일 구조

```
DAE-Second-Brain/
├── .github/
│   └── workflows/
│       └── notion-sync.yml          # GitHub Actions 워크플로우
├── automation/
│   ├── notion_sync.py               # 메인 동기화 스크립트
│   └── AUTOMATION_SETUP.md          # 이 문서
├── Experiences/
│   └── Qraft/
│       ├── Projects/                # 프로젝트 관련 노트
│       ├── Achievements/            # 성과 관련 노트
│       └── Learning/                # 학습 관련 노트
├── config.json                      # 설정 파일 (gitignore됨)
└── config.template.json             # 설정 템플릿
```

## 🔍 동작 원리

### 1. 필터링

```python
# mig_status가 "NEEDED"인 항목만 조회
payload = {
    'filter': {
        'property': 'mig_status',
        'select': {
            'equals': 'NEEDED'
        }
    }
}
```

### 2. 마이그레이션

- Notion API로 페이지 내용 가져오기
- Child blocks 재귀적으로 처리
- Markdown 형식으로 변환
- Frontmatter 추가:
  ```yaml
  ---
  type: qraft-experience
  category: projects
  title: 페이지 제목
  imported: 2025-11-28
  notion_id: xxxxx
  mig_status: synced
  ---
  ```

### 3. 상태 업데이트

성공적으로 저장되면 Notion의 `mig_status`를 `Done`으로 자동 변경

### 4. Git Commit

변경사항 자동 커밋:
```
🔄 Notion sync: 2025-11-28 09:00:00
```

## 🛠️ 트러블슈팅

### "config.json not found" 오류

**원인**: config.json이 없음

**해결**:
```bash
cp config.template.json config.json
# config.json 편집하여 실제 값 입력
```

### "API Error: 401" (Unauthorized)

**원인**: 
- 잘못된 Notion API token
- Integration이 Database에 연결되지 않음

**해결**:
1. Notion Integration token 확인
2. Database에 Integration 연결 확인

### "API Error: 404" (Not Found)

**원인**: 잘못된 Database ID

**해결**:
1. Notion Database URL에서 ID 확인
2. 32자리 hex 문자열 (하이픈 제거)

### GitHub Actions 실행 실패

**원인**: GitHub Secrets 미설정

**해결**:
1. Repository Settings → Secrets 확인
2. 모든 필수 Secret 설정 확인
3. `GH_PAT` 권한 확인

### 파일이 잘못된 위치에 생성됨

**원인**: 카테고리 분류 로직

**해결**:
`automation/notion_sync.py`의 `categorize()` 함수 수정:
```python
def categorize(title):
    # 키워드 기반 분류 로직 커스터마이즈
    if '프로젝트' in title:
        return 'Projects'
    # ...
```

## 📊 모니터링

### GitHub Actions 로그

- Actions 탭에서 실행 내역 확인
- 각 실행의 상세 로그 확인
- Summary에서 동기화 결과 확인

### Notion에서 확인

```
mig_status = "NEEDED"  → 동기화 대기 중
mig_status = "Done"    → 동기화 완료
mig_status = "Skip"    → 건너뛰기
```

### Obsidian에서 확인

- `Experiences/Qraft/` 디렉토리 확인
- Frontmatter의 `notion_id`로 원본 페이지 추적 가능

## 🔄 워크플로우 예시

### 일반적인 사용 흐름

1. **Notion에서 작업**
   - 새로운 페이지 작성
   - `mig_status`를 `NEEDED`로 설정

2. **자동 동기화 (매일 9시) 또는 수동 실행**
   - GitHub Actions가 자동 실행
   - 또는 수동으로 워크플로우 실행

3. **Obsidian에서 확인**
   - `Experiences/Qraft/`에 새 파일 생성됨
   - Git으로 pull하여 최신 상태 유지

4. **Notion 상태 자동 업데이트**
   - `mig_status`가 자동으로 `Done`으로 변경

## 🎯 베스트 프랙티스

### Notion

- 마이그레이션할 페이지에만 `mig_status=NEEDED` 설정
- 중요한 페이지는 먼저 수동 테스트
- Database 속성 변경 시 스크립트 업데이트 필요

### Git

- 자동 커밋 전 로컬 변경사항 커밋
- 충돌 방지를 위해 `Experiences/Qraft/` 직접 수정 지양
- 수정이 필요하면 Notion에서 수정 후 재동기화

### 보안

- `config.json` 절대 커밋 금지 (.gitignore 확인)
- Notion token 정기적으로 재발급
- GitHub PAT는 최소 권한만 부여

## 📝 참고 자료

- [Notion API Documentation](https://developers.notion.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Obsidian Markdown 가이드](https://help.obsidian.md/How+to/Format+your+notes)

---

**마지막 업데이트**: 2025-11-28  
**작성자**: Claude Code  
**버전**: 1.0
