---
tags:
- python
- anger
- qraft
- project
created: '2025-11-30'
updated: '2025-11-30'
title: AUTOMATION
aliases: []
---
# Automation Agent 지침서

## 🎯 목적

이 문서는 Claude Agent가 `automation/` 디렉토리에서 작업할 때 따라야 할 규칙과 컨텍스트를 정의합니다.

## 📁 디렉토리 구조

```
automation/
├── .claude/
│   └── AUTOMATION_AGENT.md      # 이 파일 (Agent 지침)
├── notion_sync.py               # 메인 동기화 스크립트
├── README.md                    # 빠른 시작 가이드
├── AUTOMATION_SETUP.md          # 전체 설정 가이드
├── GITHUB_SECRETS_SETUP.md      # GitHub Secrets 설정
└── LOCAL_TESTING_GUIDE.md       # 로컬 테스트 가이드
```

## 🤖 Agent 역할

### 자동 감지 트리거

다음 상황에서 이 지침서를 자동으로 참조:

1. **파일 경로 기반**
   - `automation/` 내 모든 파일
   - `.github/workflows/notion-sync.yml`
   - 루트의 `config.json`, `config.template.json`

2. **키워드 기반**
   - "notion sync", "notion 동기화"
   - "github actions", "워크플로우"
   - "automation", "자동화"
   - "mig_status", "마이그레이션"

3. **작업 유형 기반**
   - Notion API 관련 질문
   - 동기화 스크립트 수정
   - 워크플로우 설정 변경
   - Secret 관리

## 📋 핵심 개념

### 1. 동기화 플로우

```
Notion Database (mig_status=NEEDED)
  ↓ Query with filter
GitHub Actions / Local Script
  ↓ Fetch & Convert
Markdown Files (Experiences/Qraft/)
  ↓ Update status
Notion Database (mig_status=Done)
```

### 2. 주요 컴포넌트

#### notion_sync.py
- **역할**: Notion ↔ Obsidian 동기화
- **입력**: 환경 변수 (`TARGET_DB`, `FORCE_SYNC`)
- **출력**: Markdown 파일 + Notion 상태 업데이트
- **의존성**: `requests`, `config.json`

#### config.json (gitignored)
- **절대 커밋 금지**: .gitignore에 포함됨
- **실제 값 포함**: Notion token, Database IDs
- **로컬 전용**: GitHub Actions는 Secrets 사용

#### config.template.json
- **템플릿 파일**: 실제 값 없음
- **커밋 가능**: 구조만 정의
- **사용자 가이드**: 로컬 설정 시 복사

#### .github/workflows/notion-sync.yml
- **트리거**: `workflow_dispatch` (수동 실행만)
- **Secrets 사용**: GitHub Secrets에서 config 생성
- **자동 커밋**: 변경사항 있으면 자동 push

### 3. mig_status 상태

| 상태 | 의미 | 누가 설정 |
|------|------|-----------|
| `NEEDED` | 동기화 필요 | 사용자 (Notion) |
| `Done` | 동기화 완료 | 스크립트 (자동) |
| `Skip` | 건너뛰기 | 사용자 (Notion) |

## 🔧 작업 규칙

### 코드 수정 시

**✅ 해야 할 것:**
1. 기존 코드 스타일 유지
2. 에러 처리 추가
3. 디버그 출력 고려
4. 관련 문서 즉시 업데이트
5. 하위 호환성 유지

**❌ 하지 말아야 할 것:**
1. Secret 하드코딩
2. 기존 API 계약 변경 (환경 변수 등)
3. 파일 구조 임의 변경
4. vault 내부 로직 변경 (카테고리 분류 등)
5. 자동 스케줄 활성화 (사용자 명시 요청 시에만)

### 문서 수정 시

**업데이트 우선순위:**
1. **코드 변경** → 관련 문서 모두 업데이트
2. **API 추가** → `AUTOMATION_SETUP.md` 업데이트
3. **설정 변경** → `GITHUB_SECRETS_SETUP.md` 업데이트
4. **버그 수정** → `LOCAL_TESTING_GUIDE.md`에 트러블슈팅 추가

**문서 스타일:**
- 명확한 헤딩 구조 (##, ###)
- 코드 블록에 언어 지정 (```bash, ```python)
- 체크리스트 활용
- 이모지 일관성 유지
- 실제 예시 포함

### 새 기능 추가 시

**체크리스트:**
- [ ] 기능 구현 (`notion_sync.py`)
- [ ] 환경 변수/파라미터 문서화
- [ ] 에러 처리 추가
- [ ] 로컬 테스트 가이드 업데이트
- [ ] GitHub Actions 워크플로우 업데이트 (필요시)
- [ ] README.md에 간단한 예시 추가
- [ ] AUTOMATION_SETUP.md에 상세 설명 추가

## 🔍 문서 참조 가이드

### 사용자가 다음을 요청하면:

**"설정 방법이 뭐야?"**
→ `AUTOMATION_SETUP.md` 참조

**"Secrets는 어떻게 설정해?"**
→ `GITHUB_SECRETS_SETUP.md` 참조

**"로컬에서 테스트하려면?"**
→ `LOCAL_TESTING_GUIDE.md` 참조

**"빠르게 시작하려면?"**
→ `README.md` 참조

**"스크립트 수정하려면?"**
→ `notion_sync.py` + `LOCAL_TESTING_GUIDE.md`

**"워크플로우 변경하려면?"**
→ `.github/workflows/notion-sync.yml` + `AUTOMATION_SETUP.md`

## 🧪 테스트 가이드라인

### 코드 변경 후 필수 확인

```bash
# 1. 문법 체크
python3 -m py_compile automation/notion_sync.py

# 2. 로컬 실행 테스트
python3 automation/notion_sync.py

# 3. 다양한 시나리오
TARGET_DB=dae_work python3 automation/notion_sync.py
FORCE_SYNC=true python3 automation/notion_sync.py

# 4. GitHub Actions 워크플로우 검증 (선택)
gh workflow view notion-sync.yml
```

### 문서 변경 후 확인

```bash
# 1. Markdown 문법 검증
# - Obsidian에서 미리보기
# - 또는 markdownlint 사용

# 2. 링크 검증
# - 모든 내부 링크가 유효한지 확인
# - 파일 경로가 정확한지 확인

# 3. 코드 블록 테스트
# - 예시 명령어가 실제로 작동하는지 확인
```

## 🔐 보안 체크리스트

### 모든 변경 전 확인

- [ ] `config.json`이 .gitignore에 있는가?
- [ ] 코드에 Secret이 하드코딩되지 않았는가?
- [ ] 문서에 실제 token/ID가 노출되지 않았는가?
- [ ] 예시에는 플레이스홀더를 사용했는가?
- [ ] GitHub Actions는 Secrets를 사용하는가?

### 안전한 예시

**✅ 좋은 예시:**
```python
token = config["notion"]["token"]  # config.json에서 읽기
database_id = os.getenv("NOTION_DB_WORK_LIST")  # 환경 변수
```

**❌ 나쁜 예시:**
```python
token = "secret_abc123..."  # 하드코딩 금지!
database_id = "2b8c6d43..."  # 실제 ID 노출 금지!
```

## 📊 품질 기준

### 코드 품질

- **가독성**: 명확한 변수명, 적절한 주석
- **모듈성**: 함수 단위로 분리
- **에러 처리**: try-except, 명확한 에러 메시지
- **로깅**: print 문으로 진행 상황 표시

### 문서 품질

- **완결성**: 모든 단계 포함
- **정확성**: 실제 작동하는 예시
- **명확성**: 초보자도 이해 가능
- **최신성**: 코드와 동기화

## 🎯 일반 워크플로우

### 1. 사용자 요청 분석

```
요청: "Notion 동기화 스크립트 수정해줘"
  ↓
이 문서 참조
  ↓
관련 파일 확인 (notion_sync.py)
  ↓
변경 사항 구현
  ↓
문서 업데이트
  ↓
테스트 가이드 제공
```

### 2. 문제 해결

```
오류 보고
  ↓
LOCAL_TESTING_GUIDE.md 확인
  ↓
기존 해결책 있는지 확인
  ↓
없으면 디버깅 후 해결
  ↓
트러블슈팅 섹션에 추가
```

### 3. 기능 추가

```
새 기능 요청
  ↓
현재 아키텍처 분석
  ↓
기능 설계 및 구현
  ↓
모든 관련 문서 업데이트
  ↓
테스트 방법 제공
  ↓
README.md에 간단히 추가
```

## 🔄 유지보수 규칙

### 정기 점검 (사용자 요청 시)

- [ ] Notion API 버전 확인
- [ ] Python 의존성 업데이트
- [ ] GitHub Actions 버전 확인
- [ ] 문서와 코드 동기화 확인
- [ ] 보안 설정 검토

### 버전 관리

**변경 시 업데이트:**
- 각 문서 하단의 "마지막 업데이트" 날짜
- 주요 변경 사항은 README.md에 기록
- Breaking changes는 명확히 표시

## 💡 베스트 프랙티스

### 코드

1. **환경 변수 우선**: 하드코딩 대신 환경 변수
2. **페이지네이션 처리**: Notion API 응답 항상 페이지네이션
3. **재귀 처리**: Child blocks 깊이 제한 없음
4. **상태 업데이트**: 성공 시에만 mig_status 변경
5. **에러 복구**: 일부 실패해도 계속 진행

### 문서

1. **단계별 설명**: 스크린샷 없이도 이해 가능하게
2. **실제 예시**: 작동하는 명령어만 포함
3. **링크 활용**: 중복 설명 대신 다른 문서 참조
4. **체크리스트**: 복잡한 설정은 체크리스트로
5. **트러블슈팅**: 일반적인 오류 미리 문서화

### 워크플로우

1. **수동 실행 우선**: 자동 스케줄은 선택사항
2. **파라미터화**: 하드코딩 대신 입력 파라미터
3. **로그 상세**: 각 단계 명확히 출력
4. **조건부 실행**: 변경사항 없으면 커밋 안 함
5. **Summary 제공**: 실행 결과 요약

## 📚 참고 자료

### 외부 문서

- [Notion API Reference](https://developers.notion.com/reference)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Requests Library](https://requests.readthedocs.io/)

### 내부 문서

- [메인 Agent 지침](../../.claude/CLAUDE.md)
- [Vault 구조](../../README.md)
- [프로젝트 가이드](../../QUICK_START.md)

---

**이 문서의 목적**: Claude Agent가 automation 작업 시 일관성 있고 안전하게 작업하도록 가이드

**마지막 업데이트**: 2025-11-28
**유지보수**: 코드 변경 시 즉시 업데이트

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

