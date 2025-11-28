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

## 🔧 MCP 서버 설정

### Obsidian MCP
- **서버**: `@mauricio.wolff/mcp-obsidian`
- **Vault 경로**: `/Users/qraft_hongjinyoung/DAE-Second-Brain`
- **설정 파일**: `.mcp.json`

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

## 🎨 프로젝트 구조

```
DAE-Second-Brain/
├── automation/       # 🤖 자동화 모듈 (별도 관리)
├── Resources/        # 참고 자료
├── Projects/         # 프로젝트 노트
├── Daily Notes/      # 일일 노트
├── Templates/        # 템플릿
└── Archive/          # 보관
```

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

---

**마지막 업데이트**: 2025-11-28
**Claude Code 버전**: Sonnet 4.5
