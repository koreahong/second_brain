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

## 🌐 공통 컨벤션 (모든 프로젝트 공유)
@~/claude-shared/conventions/quality/security.md
@~/claude-shared/conventions/infrastructure/git-workflow.md

## 📋 프로젝트 개요

이 프로젝트는 Obsidian vault로, Notion에서 마이그레이션된 개인 지식 베이스입니다.

**Second-Brain의 특수성**:
- 다른 프로젝트(qraft_data_platform, sub_crawling)에서 발견하거나 경험한 내용을 **요약하고 정리**하는 공간
- qraft의 Airflow/DBT/DataHub 학습 내용을 노트로 작성
- sub_crawling의 크롤링 패턴과 안티 디텍션 전략 정리
- 개인 학습과 프로젝트 경험을 연결하는 지식 허브

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

## 🔧 MCP 서버 설정 (Common + Project-Specific)

### 🌐 Common MCP Servers (Global)
**위치:** `~/.claude-code/mcp.json`

모든 프로젝트에서 사용 가능한 공통 MCP:

#### Obsidian MCP
- **서버**: `@mauricio.wolff/mcp-obsidian`
- **Vault 경로**: `/Users/qraft_hongjinyoung/Second-Brain`
- **용도**: 개인 지식 베이스 접근

#### Notion MCP
- **서버**: `@notionhq/notion-mcp-server`
- **용도**: Notion 페이지/데이터베이스 조회 및 관리

#### Context7 MCP
- **서버**: `@upstash/context7-mcp`
- **용도**: 라이브러리/프레임워크 최신 문서 조회

#### GitHub MCP (Official)
- **서버**: `ghcr.io/github/github-mcp-server` (Docker)
- **용도**: GitHub 리포지토리, 이슈, PR 관리, CI/CD 통합, 코드 분석
- **환경 변수**: `GITHUB_PERSONAL_ACCESS_TOKEN`
- **실행 방식**: Docker 기반 (공식 GitHub MCP 서버)
- **업데이트**: 2025-12-06 (deprecated npm 패키지에서 공식 Docker 이미지로 마이그레이션)

### 📌 Project-Specific MCP (Second-Brain)
**위치:** `Second-Brain/.mcp.json`

프로젝트별 전용 MCP:

#### DataHub MCP
- **서버**: `datahub-mcp`
- **용도**: 데이터 거버넌스 및 메타데이터 관리
- **환경 변수**: `DATAHUB_SERVER`, `DATAHUB_TOKEN`
- **사용 프로젝트**: qraft_data_platform (DataHub 통합 프로젝트)

### 📋 설정 구조

```
~/.claude-code/mcp.json          # 공통 MCP (모든 프로젝트)
├── obsidian
├── notion
├── context7
└── github

Second-Brain/.mcp.json            # 프로젝트 전용 MCP
└── datahub

qraft_data_platform/.mcp.json     # (예정) DataHub 통합
└── datahub
```

### 🔄 MCP 상속 방식

- **공통 MCP**: 모든 프로젝트에서 자동으로 로드
- **프로젝트 MCP**: 해당 프로젝트 내에서만 로드
- **충돌 해결**: 프로젝트 MCP가 공통 MCP를 오버라이드 (필요시)

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

## 🤖 Agent 시스템 (Knowledge Management Agents)

### Orchestrator 역할 정의

**CRITICAL: Claude Code는 Orchestrator로만 동작:**

- ✅ **Agent 선택**: 요청 분석 → 적절한 Agent 호출
- ✅ **Agent 조정**: 여러 Agent를 순차/병렬 실행
- ❌ **직접 구현**: 노트 작성/연결 생성 직접 금지
- ❌ **Convention 암기**: 각 Agent가 자신의 convention 읽음

**🚨 필수 Orchestrator 호출 🚨**

**다음 요청 시 반드시 Task tool로 Orchestrator agent 사용:**
1. **"capture and organize..."** → Orchestrator (직접 처리 금지!)
2. **"migrate all content..."** → Orchestrator (직접 처리 금지!)
3. **"connect related notes..."** → Orchestrator (직접 처리 금지!)
4. **"full vault review..."** → Orchestrator (직접 처리 금지!)
5. **여러 agent 필요한 작업** → Orchestrator

**Convention 읽기 규칙:**
- Orchestrator: Agent 목록과 트리거 조건만 (이 파일)
- 각 Agent: 자신의 convention-*.md만 읽음 (lazy load)

### Agent 사용 강제 규칙 (MANDATORY)

**CRITICAL**: 다음 작업은 **반드시 Task tool로 전문 Agent 실행**. 직접 처리 금지!

| 작업 카테고리 | 필수 Agent | 조건 |
|-------------|-----------|------|
| **노트 캡처** | Capture Agent | • "capture note", "save thought", "캡처"<br>• 새로운 생각/인사이트 기록<br>• Fleeting → Permanent 변환 |
| **연결 생성** | Connection Curator | • "connect notes", "create links", "연결"<br>• 백링크 생성<br>• 시간적/주제적 관계 매핑 |
| **Vault 정리** | Curator Agent | • "organize vault", "curate", "정리"<br>• PARA 구조 이동<br>• 임시→영구 위치 마이그레이션 |
| **품질 검증** | Reviewer Agent | • "review", "validate", "검증"<br>• 연결 품질 점수<br>• Orphan 탐지 |
| **멀티스텝** | **Orchestrator** | • **"capture and organize"**<br>• **"migrate all content"**<br>• **여러 Agent 조합 필요** |

**Mandatory Execution Examples**:

```python
# ❌ NEVER - Direct processing
User: "capture this insight about DataHub"
Claude: [Directly creates note] → ❌ RULE VIOLATION!

# ✅ REQUIRED - Use Capture Agent
User: "capture this insight about DataHub"
Claude: [Task tool → Capture Agent] → ✅ CORRECT!

# ❌ NEVER - Direct organization
User: "organize all migrated content"
Claude: [Directly moves files] → ❌ RULE VIOLATION!

# ✅ REQUIRED - Orchestrator → Specialist Agents
User: "organize all migrated content"
Claude: [Task tool → Orchestrator] → ✅ CORRECT!
# Orchestrator coordinates: Curator → Connection Curator → Reviewer
```

**Critical Orchestrator Triggers** (MUST use Orchestrator):

| User Request Pattern | Why Orchestrator Required | Example |
|---------------------|--------------------------|---------|
| "capture and organize" | Needs: Capture → Curator → Connection | "capture this and organize" |
| "migrate all content" | Needs: Curator (bulk) → Connection → Review | "migrate 업무리스트" |
| "full vault review" | Needs: Multiple validators | "check vault health" |
| "connect and review" | Needs: Connection → Validation | "create connections and review" |

**예외 케이스** (Agent 없이 직접 처리 가능):
- 단순 질문/설명 요청
- 특정 노트 1개만 읽기
- 문서 요약
- MCP 서버 상태 확인

### Specialist Agent 목록

#### Knowledge Management Agents

**Capture Agent** (`.claude/agents/knowledge__capture-agent.md`)
- **Triggers**: "capture", "save thought", "quick note", "캡처", "메모"
- **Scope**: 원자적 노트 생성, 자동 태그, 위치 제안
- **Forbidden**: 연결 생성 (Connection Curator), 파일 이동 (Curator)

**Connection Curator** (`.claude/agents/knowledge__connection-curator.md`)
- **Triggers**: "connect", "create links", "백링크", "연결"
- **Scope**: 시간적/주제적 연결, 4-step principle, 양방향 링크
- **Forbidden**: 노트 생성 (Capture), 파일 이동 (Curator)

**Curator Agent** (`.claude/agents/knowledge__curator-agent.md`)
- **Triggers**: "organize", "curate", "PARA", "정리", "이동"
- **Scope**: PARA 구조 이동, 임시→영구, Orphan 탐지
- **Forbidden**: 노트 생성 (Capture), 연결 생성 (Connection Curator)

**Reviewer Agent** (`.claude/agents/knowledge__reviewer-agent.md`)
- **Triggers**: "review", "validate", "check quality", "검증"
- **Scope**: 품질 점수, 연결 검증, Vault health
- **Forbidden**: 노트 생성/수정 (report only)

**Orchestrator** (`.claude/agents/orchestrator.md`)
- **Triggers**: "capture and organize", "migrate all", "full review", "전체 검증"
- **Scope**: Multi-agent coordination, wave execution
- **Output**: Integrated report

### Convention Mapping

| Convention File | Used By | Purpose |
|----------------|---------|---------|
| [vault-structure.md](.claude/conventions/knowledge/vault-structure.md) | All agents | PARA + Zettelkasten 구조 |
| [connection-quality.md](.claude/conventions/knowledge/connection-quality.md) | Connection Curator, Reviewer | 4-step principle |
| [capture-workflow.md](.claude/conventions/knowledge/capture-workflow.md) | Capture Agent | Frontmatter, 원자성 |

### Agent 실행 흐름

#### Quick Capture (단일 Agent)
```
User: "capture this DataHub insight"
  ↓
Capture Agent
  - Create atomic note
  - Auto-tag (#datahub, #data-governance)
  - Suggest location (draft, not moved)
  - Suggest connections (not created)
  ↓
Output: Draft note + suggestions
```

#### Full Organization (Multi-agent via Orchestrator)
```
User: "organize all migrated content"
  ↓
Orchestrator
  ↓
Wave 1: Curator Agent (bulk)
  - 업무리스트 → Projects/
  - 회고록 → Experience/Weekly/
  - 레퍼런스 → Resources/
  - 본깨적 → Life-Insights/
  ↓
Wave 2: Connection Curator
  - Temporal connections (same week)
  - Project chains (Project → Knowledge → Insight)
  - Company period validation
  ↓
Wave 3: Reviewer Agent
  - Quality scores
  - Orphan detection
  - PARA compliance
  ↓
Output: Organized vault + quality report
```

### Agent 자동 탐색 (Dynamic Discovery)

**⚠️ CRITICAL**: Orchestrator는 항상 동적으로 Agent 탐색:

```bash
# 1. 사용 가능한 Agent 탐색
Glob: .claude/agents/*.md

# 2. 각 Agent의 YAML frontmatter 읽기
Read: .claude/agents/{agent}.md (first 20 lines)

# 3. 동적 Agent 맵 생성
agents_map = {
    "knowledge__capture-agent": {...},
    "knowledge__connection-curator": {...},
    # ... auto-discovered
}

# 4. 요청 키워드로 매칭
```

**하드코딩 금지!** 새 Agent 추가 시 자동 인식.

## 🔗 연결 품질 원칙 (Connection Quality Principles)

**⚠️ CRITICAL: 표면적 연결이 아닌 의미있는 연결을 만들어야 합니다**

### 연결 생성 4단계 원칙

#### 1️⃣ READ FIRST (내용부터 읽기)
```yaml
❌ 절대 하지 말 것:
  - 제목이나 폴더만 보고 연결
  - 키워드 매칭만으로 연결
  - 추측으로 연결

✅ 반드시 할 것:
  - mcp__obsidian__read_note로 실제 내용 읽기
  - frontmatter의 created, updated 날짜 확인
  - 노트가 "무엇을", "언제", "왜" 다루는지 이해
```

#### 2️⃣ CHECK TIMELINE (시간맥락 확인)
```yaml
날짜 기반 연결 우선:
  1. 노트 날짜 확인 (created: 2025-10-29)
  2. 같은 시기 찾기:
     - 같은 주 Weekly 회고
     - 같은 달 프로젝트
     - 시간적으로 연관된 인사이트
  3. 시간 맥락 설명 추가
```

#### 3️⃣ COMPANY PERIOD (회사/기간 구분)
```yaml
시기별 엄격한 구분:
  aivelabs (2022-2023):
    - 2025년 이전 날짜
    - ❌ Qraft 프로젝트와 연결 금지!
    - 교훈만 추출

  Qraft (2025-08+):
    - 2025년 8월 이후
    - Projects/, Weekly/ 와 연결
    - 구체적인 업무 맥락 포함
```

#### 4️⃣ ADD CONTEXT (맥락 설명)
```markdown
❌ Bad (맥락 없음):
## Related
- [[팀별-데이터-현황-파악]]
- [[2025년-10월-27일]]

✅ Good (맥락 포함):
## 📎 Related

### 관련 프로젝트 (8월~10월 현황파악 결과)
이 인사이트는 2개월간의 데이터 현황 조사 프로젝트의 결과입니다:
- [[팀별-원천-데이터-계약현황-파악]] (8월 25일 시작)
  - CFO님이 중지 검토한 데이터들 → 실제 사용 여부 확인

### 주간 회고 (같은 시기)
- [[2025년-10월-27일]] (2일 전)
  - 데이터 공유 유도 → **거버넌스의 중요성 깨달음**
```

### 자동화 시스템

**Linker Agent** ([.claude/agents/linker-agent.md](.claude/agents/linker-agent.md)):
- 위 4단계 원칙 자동 적용
- 내용 읽기 → 시간확인 → 회사구분 → 맥락설명

**Auto-Organize Hook** ([.claude/hooks/auto-organize.md](.claude/hooks/auto-organize.md)):
- 파일 생성/수정 시 자동 실행
- Temporal connections 우선
- Company period 자동 감지

**Curator Agent** ([.claude/agents/curator-agent.md](.claude/agents/curator-agent.md)):
- 연결 품질 검증
- Orphan 노트에 의미있는 연결 추천

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

### GitHub MCP (전체 자동 승인 - Delete 제외)
- `mcp__github__add_comment_to_pending_review` - PR 리뷰 코멘트 추가
- `mcp__github__add_issue_comment` - 이슈 코멘트 추가
- `mcp__github__assign_copilot_to_issue` - Copilot을 이슈에 할당
- `mcp__github__create_branch` - 브랜치 생성
- `mcp__github__create_or_update_file` - 파일 생성/업데이트
- `mcp__github__create_pull_request` - PR 생성
- `mcp__github__create_repository` - 리포지토리 생성
- `mcp__github__fork_repository` - 리포지토리 포크
- `mcp__github__get_commit` - 커밋 조회
- `mcp__github__get_file_contents` - 파일 내용 조회
- `mcp__github__get_label` - 라벨 조회
- `mcp__github__get_latest_release` - 최신 릴리즈 조회
- `mcp__github__get_me` - 현재 사용자 정보 조회
- `mcp__github__get_release_by_tag` - 태그로 릴리즈 조회
- `mcp__github__get_tag` - 태그 조회
- `mcp__github__get_team_members` - 팀 멤버 조회
- `mcp__github__get_teams` - 팀 목록 조회
- `mcp__github__issue_read` - 이슈 읽기
- `mcp__github__issue_write` - 이슈 작성/수정
- `mcp__github__list_branches` - 브랜치 목록
- `mcp__github__list_commits` - 커밋 목록
- `mcp__github__list_issue_types` - 이슈 타입 목록
- `mcp__github__list_issues` - 이슈 목록
- `mcp__github__list_pull_requests` - PR 목록
- `mcp__github__list_releases` - 릴리즈 목록
- `mcp__github__list_tags` - 태그 목록
- `mcp__github__merge_pull_request` - PR 병합
- `mcp__github__pull_request_read` - PR 읽기
- `mcp__github__pull_request_review_write` - PR 리뷰 작성
- `mcp__github__push_files` - 파일 푸시
- `mcp__github__request_copilot_review` - Copilot 리뷰 요청
- `mcp__github__search_code` - 코드 검색
- `mcp__github__search_issues` - 이슈 검색
- `mcp__github__search_pull_requests` - PR 검색
- `mcp__github__search_repositories` - 리포지토리 검색
- `mcp__github__search_users` - 사용자 검색
- `mcp__github__sub_issue_write` - 하위 이슈 작성
- `mcp__github__update_pull_request` - PR 업데이트
- `mcp__github__update_pull_request_branch` - PR 브랜치 업데이트

**참고:** Delete 작업(`delete_file`, `delete_a_block` 등)은 자동 승인에서 제외되며 사용자 확인이 필요합니다.

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

## 🏗️ MCP 인프라 설정 가이드

### 🌐 Common MCP (모든 프로젝트 공용)

**파일:** `~/.claude-code/mcp.json`

이 설정은 모든 Claude Code 프로젝트에서 자동으로 로드됩니다.

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "@mauricio.wolff/mcp-obsidian", "/Users/qraft_hongjinyoung/Second-Brain"]
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server@latest"],
      "env": { "NOTION_TOKEN": "${NOTION_TOKEN}" }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}" }
    }
  }
}
```

**참고**: Claude Code CLI에서는 `claude mcp add` 명령어로 관리되며, 실제 설정은 `~/.claude.json`에 저장됩니다.

**특징:**
- ✅ Obsidian vault 접근 (개인 지식 베이스)
- ✅ Notion 데이터 조회 (모든 프로젝트)
- ✅ Context7 (라이브러리 문서)
- ✅ GitHub (리포지토리, 이슈, PR 관리)
- 💾 환경 변수: `NOTION_TOKEN`, `GITHUB_PERSONAL_ACCESS_TOKEN`

### 📌 Project-Specific MCP (프로젝트별)

**파일:** `{프로젝트}/.mcp.json`

각 프로젝트는 공통 MCP에 추가로 전용 MCP를 로드할 수 있습니다.

#### Second-Brain (현재 프로젝트)

```json
{
  "mcpServers": {
    "datahub": {
      "command": "npx",
      "args": ["datahub-mcp"],
      "env": {
        "DATAHUB_SERVER": "${DATAHUB_SERVER}",
        "DATAHUB_TOKEN": "${DATAHUB_TOKEN}"
      }
    }
  }
}
```

**사용:**
- DataHub 메타데이터 조회 및 거버넌스 작업
- qraft_data_platform과 연동 가능

### 🔄 로드 순서

1. **공통 MCP 로드** (`~/.claude-code/mcp.json`)
   - obsidian, notion, context7, github
2. **프로젝트 MCP 로드** (`{프로젝트}/.mcp.json`)
   - 추가 전용 서버 로드
3. **충돌 처리** (프로젝트 MCP가 우선)

### 📋 현재 MCP 구성 요약

| MCP | 위치 | 범위 | 용도 |
|-----|------|------|------|
| Obsidian | 공통 | 모든 프로젝트 | 개인 지식 베이스 |
| Notion | 공통 | 모든 프로젝트 | 데이터 조회 |
| Context7 | 공통 | 모든 프로젝트 | 라이브러리 문서 |
| GitHub | 공통 | 모든 프로젝트 | 리포지토리/이슈/PR 관리 |
| DataHub | Second-Brain | 이 프로젝트만 | 메타데이터 관리 |

### 🔐 환경 변수 설정

**위치:** `~/.zshrc`

```bash
# MCP 서버 환경 변수
export NOTION_TOKEN="ntn_***"
export GITHUB_PERSONAL_ACCESS_TOKEN="gho_***"
export DATAHUB_SERVER="http://localhost:8080"
export DATAHUB_TOKEN="your_token"
```

**설정 확인:**
```bash
source ~/.zshrc
echo $GITHUB_PERSONAL_ACCESS_TOKEN  # 토큰 확인
```

---

## 📚 참고 문서

### GitHub MCP 서버
- [공식 저장소](https://github.com/github/github-mcp-server)
- [Claude Code 설치 가이드](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md)
- [VS Code MCP 문서](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)

### 설치 방법
```bash
# Docker 이미지 가져오기
docker pull ghcr.io/github/github-mcp-server

# Claude Code에 추가
claude mcp add github -e GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_PERSONAL_ACCESS_TOKEN -- \
  docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server

# 확인
claude mcp list
claude mcp get github
```

---

**마지막 업데이트**: 2025-12-06 (GitHub MCP 공식 Docker 버전으로 마이그레이션)
**Claude Code 버전**: Claude Sonnet 4.5
