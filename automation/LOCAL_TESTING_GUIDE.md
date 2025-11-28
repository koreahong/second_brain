---
tags:
  - automation
  - testing
  - local-development
created: '2025-11-28'
type: guide
---
# 로컬 테스트 환경 설정 가이드

## 📋 개요

GitHub Actions에 배포하기 전에 로컬 환경에서 Notion 동기화를 테스트하는 방법을 설명합니다.

## 🔧 사전 요구사항

### 필수 소프트웨어

- Python 3.8 이상
- pip (Python 패키지 관리자)
- Git
- 텍스트 에디터 (VS Code, Sublime Text 등)

### Python 버전 확인

```bash
python3 --version
# 또는
python --version
```

출력 예시: `Python 3.11.0`

## 📦 설치

### 1. Python 의존성 설치

```bash
# 프로젝트 루트로 이동
cd /Users/qraft_hongjinyoung/DAE-Second-Brain

# requests 라이브러리 설치
pip install requests

# 또는 pip3 사용
pip3 install requests
```

### 2. 가상 환경 사용 (권장)

```bash
# 가상 환경 생성
python3 -m venv venv

# 가상 환경 활성화
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# 의존성 설치
pip install requests

# 가상 환경 비활성화 (작업 완료 후)
deactivate
```

### 3. config.json 생성

```bash
# 템플릿 복사
cp config.template.json config.json

# config.json 편집
# VS Code 사용 시:
code config.json

# 또는 다른 에디터:
open -a "Visual Studio Code" config.json
nano config.json
vim config.json
```

### 4. config.json 설정

`config.json`을 열어 다음 값을 입력:

```json
{
  "notion": {
    "token": "secret_YOUR_ACTUAL_TOKEN_HERE",
    "databases": {
      "dae_work": {
        "id": "YOUR_ACTUAL_DATABASE_ID",
        "name": "DAE 작업 통합",
        "url": "https://notion.so/YOUR_ACTUAL_DATABASE_ID",
        "description": "DAE 메인 작업 관리 DB"
      },
      "work_list": {
        "id": "YOUR_ACTUAL_DATABASE_ID",
        "name": "업무리스트",
        "url": "https://notion.so/YOUR_ACTUAL_DATABASE_ID",
        "description": "일일 작업 리스트"
      },
      "memoir": {
        "id": "YOUR_ACTUAL_DATABASE_ID",
        "name": "회고록",
        "url": "https://notion.so/YOUR_ACTUAL_DATABASE_ID",
        "description": "주간 회고록"
      }
    }
  }
}
```

**값을 얻는 방법**:
- `token`: [[GITHUB_SECRETS_SETUP#1. NOTION_TOKEN]] 참고
- `databases.*.id`: [[GITHUB_SECRETS_SETUP#2. NOTION_DB_WORK_LIST]] 참고

⚠️ **경고**: `config.json`은 `.gitignore`에 포함되어 있으므로 절대 Git에 커밋되지 않습니다!

## 🧪 테스트 실행

### 기본 테스트

```bash
# 기본 실행 (work_list 데이터베이스, mig_status=NEEDED만)
python3 automation/notion_sync.py
```

**예상 출력**:
```
🔄 Starting Notion to Obsidian sync...

🔍 Querying: 업무리스트 (mig_status='NEEDED')
✅ Found 3 pages to sync

[1/3] ✅ 프로젝트 A 진행사항.md
[2/3] ✅ 팀별 데이터 계약현황 파악.md
[3/3] ✅ 학습 노트 - Python.md

============================================================
📊 Sync Summary
============================================================

Projects/ (2개)
  - 프로젝트 A 진행사항.md
  - 팀별 데이터 계약현황 파악.md

Learning/ (1개)
  - 학습 노트 - Python.md

✅ Successfully synced 3/3 pages
📁 Location: /Users/qraft_hongjinyoung/DAE-Second-Brain/Experiences/Qraft
```

### 특정 Database 테스트

```bash
# DAE 작업 통합 데이터베이스
TARGET_DB=dae_work python3 automation/notion_sync.py

# 회고록 데이터베이스
TARGET_DB=memoir python3 automation/notion_sync.py
```

### 강제 동기화 (모든 항목)

```bash
# mig_status 무시하고 모든 항목 동기화
FORCE_SYNC=true python3 automation/notion_sync.py

# 특정 DB의 모든 항목
TARGET_DB=dae_work FORCE_SYNC=true python3 automation/notion_sync.py
```

### 환경 변수 조합

```bash
# 여러 환경 변수 동시 사용
TARGET_DB=memoir FORCE_SYNC=true python3 automation/notion_sync.py
```

## 🔍 디버깅

### 상세 로그 보기

스크립트에 디버그 출력 추가:

```python
# automation/notion_sync.py 상단에 추가
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### API 응답 확인

특정 부분에 디버그 출력:

```python
# query_database_with_filter 함수 내부
response = requests.post(url, headers=headers, json=payload)
print(f"DEBUG: Response status: {response.status_code}")
print(f"DEBUG: Response body: {response.text[:500]}")
```

### 드라이런 모드 (저장 없이 테스트)

스크립트를 수정하여 파일 저장 건너뛰기:

```python
# save_page 함수에서 파일 쓰기 부분 주석 처리
# with open(output_file, 'w', encoding='utf-8') as f:
#     f.write(frontmatter + f"\n# {title}\n\n" + content_md)

print(f"DRY RUN: Would save to {output_file}")
return output_file, category
```

## ✅ 테스트 체크리스트

### 1. 설정 확인

- [ ] Python 3.8+ 설치됨
- [ ] `requests` 라이브러리 설치됨
- [ ] `config.json` 생성됨
- [ ] `config.json`에 올바른 token과 Database ID 입력됨
- [ ] Notion Integration이 각 Database에 연결됨
- [ ] 각 Database에 `mig_status` 속성 존재

### 2. 기능 테스트

- [ ] 기본 실행 성공 (`python3 automation/notion_sync.py`)
- [ ] `mig_status=NEEDED` 필터링 동작
- [ ] 파일이 올바른 카테고리에 생성됨
- [ ] Frontmatter가 올바르게 생성됨
- [ ] Child blocks가 올바르게 변환됨
- [ ] Notion에서 `mig_status`가 `Done`으로 변경됨

### 3. 다양한 시나리오

- [ ] 다른 Database 테스트 (`TARGET_DB=dae_work`)
- [ ] 강제 동기화 테스트 (`FORCE_SYNC=true`)
- [ ] 동기화할 항목이 없을 때 동작 확인
- [ ] 중복 실행 시 동작 확인

### 4. 오류 처리

- [ ] 잘못된 token으로 테스트 (401 오류 처리)
- [ ] 잘못된 Database ID로 테스트 (404 오류 처리)
- [ ] 네트워크 오류 시나리오

## 🛠️ 문제 해결

### "ModuleNotFoundError: No module named 'requests'"

**해결**:
```bash
pip3 install requests
```

### "FileNotFoundError: config.json not found"

**해결**:
```bash
cp config.template.json config.json
# config.json 편집
```

### "API Error: 401"

**원인**: 잘못된 Notion token

**해결**:
1. Notion Integration 페이지에서 token 재확인
2. `config.json`의 `notion.token` 값 확인
3. Token이 `secret_`으로 시작하는지 확인

### "API Error: 403"

**원인**: Integration이 Database에 연결되지 않음

**해결**:
1. Notion Database → `...` → "Add connections"
2. Integration 선택하여 연결

### "API Error: 400 - Property 'mig_status' does not exist"

**원인**: Database에 `mig_status` 속성이 없음

**해결**:
1. Database에 Select 속성 추가
2. 이름: `mig_status`
3. 옵션: `NEEDED`, `Done`, `Skip`

### 파일이 예상과 다른 위치에 생성됨

**원인**: 카테고리 분류 로직

**확인**:
```python
# automation/notion_sync.py의 categorize() 함수 확인
def categorize(title):
    title_lower = title.lower()
    
    # 키워드 확인
    if any(kw in title_lower for kw in ['%', '달성', '개선', ...]):
        return 'Achievements'
    # ...
```

**커스터마이즈**:
필요에 따라 키워드 수정

### Git에 config.json이 커밋되려 함

**확인**:
```bash
git status

# config.json이 나타나면:
git rm --cached config.json

# .gitignore 확인
cat .gitignore | grep config.json
```

`.gitignore`에 `config.json`이 있는지 확인

## 📝 테스트 시나리오 예시

### 시나리오 1: 새 페이지 동기화

1. Notion에서 새 페이지 생성
2. `mig_status`를 `NEEDED`로 설정
3. 로컬에서 동기화 실행:
   ```bash
   python3 automation/notion_sync.py
   ```
4. `Experiences/Qraft/`에서 새 파일 확인
5. Notion에서 `mig_status`가 `Done`인지 확인

### 시나리오 2: 여러 Database 동기화

```bash
# 1. work_list 동기화
TARGET_DB=work_list python3 automation/notion_sync.py

# 2. dae_work 동기화
TARGET_DB=dae_work python3 automation/notion_sync.py

# 3. memoir 동기화
TARGET_DB=memoir python3 automation/notion_sync.py
```

### 시나리오 3: 전체 재동기화

```bash
# 모든 항목을 강제로 다시 동기화
FORCE_SYNC=true python3 automation/notion_sync.py
```

⚠️ **주의**: 기존 파일을 덮어씁니다!

## 🧹 정리

### 테스트 후 정리

```bash
# 1. 테스트로 생성된 파일 삭제 (선택사항)
rm -rf Experiences/Qraft/Projects/*
rm -rf Experiences/Qraft/Achievements/*
rm -rf Experiences/Qraft/Learning/*

# 2. Notion에서 테스트 페이지의 mig_status를 NEEDED로 재설정

# 3. 가상 환경 비활성화
deactivate

# 4. Git 상태 확인
git status
```

### config.json 보안

절대 Git에 커밋하지 마세요!

```bash
# config.json이 tracked 되었는지 확인
git ls-files | grep config.json

# 만약 tracked 되어 있다면:
git rm --cached config.json
git commit -m "Remove config.json from tracking"
```

## 🎯 다음 단계

테스트가 성공적으로 완료되었다면:

1. [[GITHUB_SECRETS_SETUP]] - GitHub Secrets 설정
2. [[AUTOMATION_SETUP#GitHub Actions]] - GitHub Actions 배포
3. Actions 탭에서 워크플로우 수동 실행 테스트
4. 스케줄 실행 확인 (다음날 오전 9시)

## 📚 참고 자료

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Requests Library Documentation](https://requests.readthedocs.io/)
- [Notion API Reference](https://developers.notion.com/reference)

---

**마지막 업데이트**: 2025-11-28  
**관련 문서**: [[AUTOMATION_SETUP]], [[GITHUB_SECRETS_SETUP]]
