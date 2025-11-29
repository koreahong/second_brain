---
tags:
- anger
- achievement
- company
- data
- datahub
- dbt
- project
- qraft
created: '2025-11-30'
updated: '2025-11-30'
title: CLAUDE
aliases: []
---
# DAE Second Brain - Claude Code 설정

## 📋 프로젝트 개요

이 프로젝트는 Obsidian vault로, Notion에서 마이그레이션된 개인 지식 베이스입니다.

## 🎯 Tool Usage Policy

### Obsidian Vault 작업 (최고 우선순위)

**✅ 항상 Obsidian MCP 사용:**
- 노트 읽기, 검색, 생성, 수정
- 태그 및 frontmatter 관리
- 백링크 탐색
- 메타데이터 추출

**💡 이유:**
- 40-60% 토큰 절감
- 구조화된 데이터 반환
- Obsidian 특화 기능 (백링크, 태그 등)

**🚫 금지:**
- `cat`, `grep`, `find`로 .md 파일 직접 접근
- `Read` 도구로 vault 내 노트 읽기
- CLI로 노트 검색

**예외:**
- vault 외부 파일은 Read 도구 사용 가능
- 긴급한 단순 읽기는 허용 (단, MCP 우선 고려)

### Git 작업

**✅ CLI 사용 (우선):**
- `git status`, `git add`, `git commit`, `git push`
- `git diff`, `git log` (간단한 조회)
- 일반적인 git 워크플로우

**⚠️ Git MCP 고려 (선택):**
- 커밋 통계 분석
- 복잡한 변경 패턴 분석
- 여러 브랜치 비교

### 일반 파일 작업

**✅ Read 도구 우선:**
- vault 외부의 모든 파일
- 코드 파일, 설정 파일 등

**🚫 금지:**
- `cat`, `head`, `tail` 대신 항상 Read 도구 사용

### 검색 작업

**✅ Grep 도구 사용:**
- vault 외부 파일 검색
- 코드 검색

**✅ Obsidian MCP 사용:**
- vault 내 노트 검색 (전체 텍스트, 태그, 제목 등)

**✅ Notion MCP 사용:**
- Notion 페이지/데이터베이스 검색
- Notion 콘텐츠 조회
- Notion 데이터 추출 및 분석

**✅ Context7 MCP 사용:**
- 라이브러리 최신 문서 조회
- API 레퍼런스 및 코드 예제
- 기술 스택 개념 가이드

## 🔧 MCP 서버 설정

### Obsidian MCP
- **서버**: `@mauricio.wolff/mcp-obsidian`
- **Vault 경로**: `/Users/qraft_hongjinyoung/DAE-Second-Brain`
- **설정 파일**: `.mcp.json`

### Notion MCP
- **서버**: `@notionhq/notion-mcp-server`
- **설정 파일**: `.mcp.json`
- **용도**: Notion 페이지/데이터베이스 조회 및 관리

### Context7 MCP
- **서버**: `@context-labs/mcp-server-context7`
- **설정 파일**: `.mcp.json`
- **용도**: 라이브러리/프레임워크 최신 문서 조회

## 📝 작업 가이드라인

### 노트 작성 시
- frontmatter 포함 (tags, created, updated 등)
- 관련 노트에 백링크 생성
- 적절한 태그 사용

### 검색 시
- MCP의 구조화된 검색 활용
- 필요한 필드만 요청 (토큰 최적화)
- 메타데이터 필터링 활용

### 파일 수정 시
- 기존 frontmatter 보존
- 백링크 유지
- 일관된 포맷 유지

## 🎨 Vault 구조 (PARA + Zettelkasten)

### 핵심 구조

```
02-Areas/크래프트테크놀로지스/    # 회사 관련 (업무리스트 + 회고록)
├── Projects/
│   ├── Active/               # 진행중 프로젝트
│   ├── Completed/            # 완료된 프로젝트
│   └── Archived/             # 과거 프로젝트
├── Experience/
│   └── Weekly/               # 주간 회고
└── Achievements/             # 성과 기록

03-Resources/                 # 공유 지식 (레퍼런스)
├── DAE/                      # DAE 역할/범위
├── Data-Governance/          # 데이터 거버넌스
├── Technology/               # 기술 지식
│   ├── Airflow/
│   ├── DBT/
│   ├── DataHub/
│   └── [기술별 폴더]
└── Methodologies/            # 방법론

30-Flow/Life-Insights/        # 인생 회고 (본깨적)
├── Work/                     # 업무 관련 인사이트
├── Personal/                 # 개인적 경험
└── Observations/             # 일상 관찰

10-Zettelkasten/              # 원자적 지식
├── Permanent/                # 영구 노트
└── Literature/               # 레퍼런스 요약

automation/                   # 🤖 자동화 모듈
```

### 마이그레이션된 데이터베이스

현재 4개 Notion 데이터베이스가 마이그레이션되어 임시 위치에 있음:
- `업무리스트/` (46 files) → Projects/로 이동 예정
- `회고록/` (15 files) → Experience/Weekly/로 이동 예정
- `레퍼런스/` (238 files) → Resources/로 이동 예정
- `본깨적/` (229 files) → Life-Insights/로 이동 예정

**재구성 명령어:** `/organize` 또는 "organize all migrated content"

## 🤖 Automation 모듈

### 위치 및 역할
- **경로**: `automation/`
- **용도**: Notion ↔ Obsidian 자동 동기화
- **독립 관리**: 별도의 설정 및 문서 보유

### 작업 시 자동 인식 규칙

**automation 관련 작업 감지:**
- `automation/` 디렉토리 내 파일 수정/생성
- Notion 동기화 관련 질문
- GitHub Actions 워크플로우 관련 작업
- `notion_sync.py` 관련 작업

**자동 참조 문서:**
1. `automation/README.md` - 빠른 시작
2. `automation/AUTOMATION_SETUP.md` - 전체 가이드
3. `automation/.claude/AUTOMATION_AGENT.md` - Agent 지침

### Automation 작업 가이드라인

**✅ 항상:**
- `automation/.claude/AUTOMATION_AGENT.md` 먼저 확인
- 기존 구조 및 네이밍 규칙 준수
- 문서 업데이트 (코드 변경 시)
- 로컬 테스트 가능하도록 유지

**🚫 금지:**
- `config.json` 직접 생성/수정 (템플릿만 제공)
- Secret 정보 하드코딩
- vault 내부 구조 임의 변경
- GitHub Actions 스케줄 무단 활성화

**📝 문서 우선순위:**
1. 코드 변경 → 해당 문서 즉시 업데이트
2. API 변경 → `AUTOMATION_SETUP.md` 업데이트
3. 새 기능 → `README.md`에 추가
4. 오류 해결 → `LOCAL_TESTING_GUIDE.md`에 추가

### Automation 디렉토리 접근

```bash
# Obsidian MCP 사용 (문서 읽기)
mcp__obsidian__read_note(path="automation/README.md")

# Read 도구 사용 (코드 읽기)
Read(file_path="/Users/.../automation/notion_sync.py")

# 일반 파일 작업 (설정, 워크플로우)
Read(file_path="/Users/.../.github/workflows/notion-sync.yml")
```

## 🔓 자동 승인 도구 (Auto-approved Tools)

다음 도구들은 사용자 승인 없이 자동으로 실행 가능:

### Notion MCP
- `mcp__notion__notion-search` - Notion 검색
- `mcp__notion__notion-fetch` - Notion 페이지/데이터베이스 조회
- `mcp__notion__notion-create-pages` - Notion 페이지 생성
- `mcp__notion__notion-update-page` - Notion 페이지 업데이트
- `mcp__notion__notion-create-database` - Notion 데이터베이스 생성
- `mcp__notion__notion-update-database` - Notion 데이터베이스 업데이트
- `mcp__notion__notion-get-users` - Notion 사용자 조회
- `mcp__notion__notion-get-self` - Notion 봇 정보 조회

### Obsidian MCP
- `mcp__obsidian__read_note` - 노트 읽기
- `mcp__obsidian__write_note` - 노트 작성
- `mcp__obsidian__patch_note` - 노트 부분 수정
- `mcp__obsidian__list_directory` - 디렉토리 목록
- `mcp__obsidian__search_notes` - 노트 검색
- `mcp__obsidian__move_note` - 노트 이동
- `mcp__obsidian__read_multiple_notes` - 여러 노트 읽기
- `mcp__obsidian__update_frontmatter` - Frontmatter 업데이트
- `mcp__obsidian__get_notes_info` - 노트 메타데이터 조회
- `mcp__obsidian__get_frontmatter` - Frontmatter 조회
- `mcp__obsidian__manage_tags` - 태그 관리

### Context7 MCP
- `mcp__context7__resolve-library-id` - 라이브러리 ID 조회
- `mcp__context7__get-library-docs` - 라이브러리 문서 조회

### 기본 파일 시스템 명령어
- `Bash(mkdir:*)` - 디렉토리 생성 (mkdir -p 포함)
- `Bash(mv:*)` - 파일/디렉토리 이동
- `Bash(cp:*)` - 파일/디렉토리 복사
- `Bash(touch:*)` - 파일 생성
- `Bash(ls:*)` - 디렉토리 목록 조회
- `Bash(tree:*)` - 디렉토리 트리 구조 조회
- `Bash(pwd:*)` - 현재 디렉토리 확인
- `Bash(cd:*)` - 디렉토리 이동

## 💬 선호하는 작업 방식

1. **토큰 효율성 우선**: 항상 가장 효율적인 도구 선택
2. **구조화된 데이터**: 가능한 MCP 활용
3. **일관성**: 기존 패턴 유지
4. **명확성**: 작업 전 의도 확인

## 🔍 유용한 패턴

### 최근 노트 조회
```
✅ MCP: get_recent_notes(limit=10, fields=["title", "tags", "updated"])
❌ find + cat + grep 조합
```

### 태그로 검색
```
✅ MCP: search_by_tag(tag="프로젝트")
❌ grep "#프로젝트" **/*.md
```

### 노트 읽기
```
✅ MCP: read_note(path="...")
❌ Read 도구 또는 cat
```

### 라이브러리 문서 조회
```
✅ MCP: resolve-library-id(libraryName="airflow")
       → get-library-docs(context7CompatibleLibraryID="/apache/airflow")
❌ WebSearch 또는 수동 검색
```

## 🤖 Agent & Hook 시스템

### Content Organizer Agent
**위치:** `.claude/agents/content-organizer.md`

**역할:**
- 마이그레이션된 Notion 콘텐츠를 PARA 구조로 재구성
- Projects-Knowledge-Experience-Results 자동 연결
- 콘텐츠 분석 후 적절한 위치로 이동

**사용법:**
```
/organize
또는
"organize all migrated content"
"organize 업무리스트"
```

**주요 기능:**
1. **업무리스트** → 상태별 Projects/ 분류
2. **회고록** → Experience/Weekly/
3. **레퍼런스** → 주제별 Resources/ 분류
4. **본깨적** → 컨텍스트별 Life-Insights/ 분류
5. 자동 태그 추가
6. 관련 문서 링크 생성

### Auto-Organize Hook
**위치:** `.claude/hooks/auto-organize.md`

**트리거:** 파일 생성/수정 시 자동 실행

**기능:**
1. **위치 감지:** 임시 폴더에 있는 파일 알림
2. **자동 태그:** 내용 분석 후 기술 태그 추가
3. **자동 링크:** 관련 프로젝트/지식 연결
4. **백링크 생성:** 양방향 링크 유지

**설정 (frontmatter):**
```yaml
auto_organize: true   # 자동 구성 제안
auto_tag: true        # 자동 태그
auto_link: true       # 자동 링크
auto_backlink: true   # 자동 백링크
```

## 📋 컨텐츠 연결 전략

### Projects → Knowledge → Experience → Results

각 프로젝트는 다음과 자동 연결됨:
```markdown
# 프로젝트 예시

## Related Knowledge
- [[03-Resources/Technology/Airflow/...]]
- [[03-Resources/Data-Governance/...]]

## Weekly Reflections
- [[Experience/Weekly/2025년-11월-24일]]

## Insights
- [[Life-Insights/Work/...]]

## Results
- 성과 지표
- 개선율
```

---

**마지막 업데이트**: 2025-11-29 (Context7 MCP 추가)
**Claude Code 버전**: Sonnet 4.5
