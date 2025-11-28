---
tags:
  - automation
  - github
  - secrets
  - security
created: '2025-11-28'
type: guide
---
# GitHub Secrets 설정 가이드

## 📋 개요

GitHub Actions에서 Notion API를 사용하기 위해 필요한 Secrets를 안전하게 설정하는 방법을 설명합니다.

## 🔐 필요한 Secrets

### 1. NOTION_TOKEN

**용도**: Notion API 인증

**획득 방법**:
1. [Notion Integrations](https://www.notion.so/my-integrations) 접속
2. 로그인 후 "New integration" 클릭
3. Integration 정보 입력:
   - **Name**: `Obsidian Sync` (또는 원하는 이름)
   - **Associated workspace**: 본인의 workspace 선택
   - **Type**: Internal
4. "Submit" 클릭
5. **Internal Integration Token** 복사
   - 형식: `secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - ⚠️ 이 값은 다시 볼 수 없으니 안전한 곳에 보관!

**GitHub에 설정**:
1. Repository → Settings → Secrets and variables → Actions
2. "New repository secret" 클릭
3. Name: `NOTION_TOKEN`
4. Secret: 복사한 Integration Token
5. "Add secret" 클릭

### 2. NOTION_DB_WORK_LIST

**용도**: 업무리스트 Database ID

**획득 방법**:
1. Notion에서 "업무리스트" Database 열기
2. 우측 상단 `...` → "Copy link" 클릭
3. URL에서 Database ID 추출:
   ```
   https://www.notion.so/253c6d433b4d80e58babc19e1f5956e3?v=...
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        이 부분이 Database ID (32자리 hex)
   ```
4. 하이픈 없는 32자리 hex 문자열 복사

**GitHub에 설정**:
- Name: `NOTION_DB_WORK_LIST`
- Secret: Database ID (예: `253c6d433b4d80e58babc19e1f5956e3`)

### 3. NOTION_DB_DAE_WORK

**용도**: DAE 작업 통합 Database ID

**획득 방법**: (NOTION_DB_WORK_LIST와 동일)

**GitHub에 설정**:
- Name: `NOTION_DB_DAE_WORK`
- Secret: Database ID (예: `2b8c6d433b4d806c8a0cd5c55a808ff5`)

### 4. NOTION_DB_MEMOIR

**용도**: 회고록 Database ID

**획득 방법**: (NOTION_DB_WORK_LIST와 동일)

**GitHub에 설정**:
- Name: `NOTION_DB_MEMOIR`
- Secret: Database ID (예: `262c6d433b4d8077877cc459b1d2c977`)

### 5. GH_PAT (GitHub Personal Access Token)

**용도**: GitHub Actions에서 Git 커밋/푸시 권한

**획득 방법**:
1. GitHub Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. "Generate new token (classic)" 클릭
4. Token 정보 입력:
   - **Note**: `DAE Second Brain Automation`
   - **Expiration**: 90 days (또는 No expiration)
   - **Select scopes**:
     - ✅ `repo` (전체 선택)
     - ✅ `workflow`
5. "Generate token" 클릭
6. Token 복사 (형식: `ghp_xxxxxxxxxxxxxxxxxxxxx`)
   - ⚠️ 페이지를 벗어나면 다시 볼 수 없음!

**GitHub에 설정**:
- Name: `GH_PAT`
- Secret: 생성한 Personal Access Token

## 📝 설정 체크리스트

완료한 항목을 체크하세요:

- [ ] Notion Integration 생성
- [ ] Integration을 각 Database에 연결
- [ ] 각 Database에 `mig_status` 속성 추가
- [ ] `NOTION_TOKEN` Secret 설정
- [ ] `NOTION_DB_WORK_LIST` Secret 설정
- [ ] `NOTION_DB_DAE_WORK` Secret 설정
- [ ] `NOTION_DB_MEMOIR` Secret 설정
- [ ] GitHub PAT 생성
- [ ] `GH_PAT` Secret 설정
- [ ] GitHub Actions 워크플로우 테스트 실행

## 🔗 Notion Database에 Integration 연결

각 Database (업무리스트, DAE 작업 통합, 회고록)에 대해:

1. Database 페이지 열기
2. 우측 상단 `...` 메뉴 클릭
3. "Add connections" 선택
4. 생성한 Integration (예: "Obsidian Sync") 선택
5. "Confirm" 클릭

⚠️ **중요**: Integration을 연결하지 않으면 API 호출 시 403 Forbidden 오류 발생!

## 🎯 mig_status 속성 추가

각 Database에 다음 Select 속성을 추가하세요:

**속성 이름**: `mig_status`

**타입**: Select

**옵션**:
1. `NEEDED` (색상: 빨강/주황)
   - 마이그레이션이 필요한 항목
   - 자동화가 이 항목만 처리
2. `Done` (색상: 초록)
   - 마이그레이션 완료됨
   - 자동화가 완료 후 자동 설정
3. `Skip` (색상: 회색)
   - 마이그레이션 건너뛰기
   - 수동으로 설정하여 제외

**추가 방법**:
1. Database 상단의 속성 영역 클릭
2. "+ New property" 클릭
3. 속성 이름: `mig_status`
4. 타입: Select
5. 옵션 추가: `NEEDED`, `Done`, `Skip`
6. 색상 지정 (선택사항)

## 🧪 테스트

### 1. Notion API 테스트

로컬에서 테스트:

```bash
# config.json 생성
cp config.template.json config.json

# config.json 편집하여 실제 값 입력
# notion.token에 NOTION_TOKEN 값 입력
# databases.*.id에 각 Database ID 입력

# 테스트 실행
python automation/notion_sync.py
```

### 2. GitHub Actions 테스트

1. Repository → Actions 탭
2. "Notion to Obsidian Sync" 워크플로우 선택
3. "Run workflow" 클릭
4. 옵션:
   - database: `work_list`
   - force: `false`
5. "Run workflow" 실행
6. 실행 로그 확인

**예상 결과**:
- ✅ 체크아웃 성공
- ✅ Python 설정 성공
- ✅ config.json 생성 성공
- ✅ 동기화 실행 성공
- ✅ Git 커밋/푸시 성공 (변경사항이 있는 경우)

## ❌ 일반적인 오류

### "Error: API returned 401"

**원인**: 잘못된 Notion Token

**해결**:
1. Notion Integration Token 재확인
2. `NOTION_TOKEN` Secret 값 재설정
3. Token이 `secret_`으로 시작하는지 확인

### "Error: API returned 403"

**원인**: Integration이 Database에 연결되지 않음

**해결**:
1. 각 Database에 Integration 연결 확인
2. Database 페이지 → `...` → Connections 확인

### "Error: API returned 404"

**원인**: 잘못된 Database ID

**해결**:
1. Database URL에서 ID 재확인
2. 32자리 hex 문자열인지 확인 (하이픈 없음)
3. Secret 값 재설정

### "Error: Property 'mig_status' does not exist"

**원인**: Database에 mig_status 속성이 없음

**해결**:
1. Database에 `mig_status` Select 속성 추가
2. 옵션: `NEEDED`, `Done`, `Skip` 추가

### "Error: Git push failed"

**원인**: 
- GH_PAT 권한 부족
- PAT 만료

**해결**:
1. PAT에 `repo`, `workflow` 권한 확인
2. PAT 만료일 확인
3. 필요시 새 PAT 생성 후 재설정

## 🔒 보안 베스트 프랙티스

### Token 관리

- ✅ GitHub Secrets에만 저장
- ✅ 정기적으로 재발급 (3-6개월)
- ❌ 코드에 하드코딩 금지
- ❌ 공개 저장소에 노출 금지
- ❌ 로그에 출력 금지

### Git 관리

- `config.json`은 `.gitignore`에 포함
- 실수로 커밋한 경우:
  ```bash
  # 1. Git 히스토리에서 완전히 제거
  git filter-branch --force --index-filter \
    "git rm --cached --ignore-unmatch config.json" \
    --prune-empty --tag-name-filter cat -- --all
  
  # 2. Token 즉시 재발급
  # 3. 강제 푸시
  git push origin --force --all
  ```

### 권한 최소화

- GitHub PAT는 필요한 권한만 부여
- Notion Integration은 필요한 Database만 연결
- Database 속성 변경 권한만 부여

## 📊 Secrets 관리

### 현재 설정된 Secrets 확인

Repository → Settings → Secrets and variables → Actions

**확인 항목**:
- 모든 필수 Secret이 존재하는가?
- Secret 이름이 정확한가? (대소문자 구분)
- 마지막 업데이트 날짜 확인

### Secret 업데이트

1. Secret 옆의 "Update" 클릭
2. 새 값 입력
3. "Update secret" 클릭

### Secret 삭제

1. Secret 옆의 "Remove" 클릭
2. 확인

## 🔄 정기 유지보수

### 3개월마다

- [ ] Notion Integration Token 재발급
- [ ] GitHub PAT 만료일 확인
- [ ] Secrets 업데이트

### 6개월마다

- [ ] GitHub PAT 재발급
- [ ] Database 연결 상태 확인
- [ ] 워크플로우 실행 로그 점검

## 📚 참고 자료

- [Notion API - Authorization](https://developers.notion.com/docs/authorization)
- [GitHub - Encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub - Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

---

**마지막 업데이트**: 2025-11-28  
**관련 문서**: [[AUTOMATION_SETUP]]
