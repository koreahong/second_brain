# 🧠 Knowledge Curator

세컨드 브레인을 위한 AI 기반 자동 문서 정리 시스템

## 📋 개요

Knowledge Curator는 Obsidian vault의 문서들을 자동으로 분석, 정리, 개선하는 시스템입니다.

**두 가지 방식 제공**:
1. **Claude Code Subagents** (AI 기반) ⭐ 추천
2. **Python Scripts** (규칙 기반)

---

## 🤖 방식 1: Claude Code Subagents (추천)

### 설치

이미 설치되어 있습니다! `.claude/commands/` 폴더에 3개 에이전트가 준비되어 있습니다.

### 사용법

#### 1️⃣ 노트 분석

```bash
/analyze-note
```

**실행 후**:
- 분석할 노트 경로 입력
- AI가 노트를 읽고 종합 분석
- 품질 점수, 타입 분류, 개선 제안 제공

**예시**:
```
User: /analyze-note
Claude: 어떤 노트를 분석할까요?
User: 01-Projects/크래프트테크놀로지스/postgres--snowflake-권한관리.md
Claude: [분석 시작...]
```

#### 2️⃣ 노트 큐레이션

```bash
/curate-note
```

**기능**:
- 노트 분석 (점수화, 타입 분류)
- Frontmatter 자동 업데이트
- 관련 노트와 자동 링크
- 구조 개선
- Permanent Note 추출 제안

**두 가지 모드**:
1. **분석만**: 제안만 제시
2. **자동 개선**: 실제로 수정 (사용자 승인 후)

#### 3️⃣ 주간 리뷰

```bash
/weekly-review
```

**생성 내용**:
- 이번 주 통계
- 우수 노트 선정
- 주의 필요 노트
- 네트워크 분석
- 개선 권장사항

**저장 위치**: `30-Flow/Weekly/2025-W48-Review.md`

---

## 🐍 방식 2: Python Scripts

### 설치

```bash
cd automation/knowledge_curator
pip install pyyaml
```

### 사용법

#### 점수화

```bash
# 단일 파일
python automation/run_curator.py score 01-Projects/Note.md

# 폴더 전체
python automation/run_curator.py score 01-Projects/
```

#### 큐레이션

```bash
# 분석만
python automation/run_curator.py curate 01-Projects/

# Frontmatter 자동 업데이트
python automation/run_curator.py curate 01-Projects/ --auto-update
```

#### 주간 리뷰

```bash
# 리뷰 생성 및 저장
python automation/run_curator.py review --save

# 콘솔에만 출력
python automation/run_curator.py review
```

#### 링크 관리

```bash
# 링크 제안
python automation/run_curator.py links 01-Projects/Note.md

# 고아 노트 찾기
python automation/run_curator.py links --orphans

# 네트워크 통계
python automation/run_curator.py links --stats
```

---

## 🎯 어떤 방식을 선택할까?

### Claude Code Subagents (방식 1) - 추천!

**장점**:
- ✅ AI가 문맥을 이해하고 지능적으로 분석
- ✅ 자연어로 대화하며 작업
- ✅ 유연하고 정확한 판단
- ✅ 설치 불필요 (이미 준비됨)

**단점**:
- ❌ 수동 실행 필요
- ❌ GitHub Actions에서 직접 사용 불가

**추천 대상**:
- 일일/주간 수동 리뷰
- 중요한 노트 정리
- 맥락 이해가 필요한 분석

### Python Scripts (방식 2)

**장점**:
- ✅ 자동화 가능 (GitHub Actions)
- ✅ 빠른 대량 처리
- ✅ 일관된 규칙 적용

**단점**:
- ❌ 규칙 기반이라 유연성 부족
- ❌ 맥락 이해 불가
- ❌ Python 설치 필요

**추천 대상**:
- Notion 동기화 후 자동 처리
- 주간 자동 리뷰
- CI/CD 파이프라인

### 🎨 Best Practice: 둘 다 사용!

```
1. Notion → Obsidian 동기화 (자동)
   ↓
2. Python Script로 자동 점수화 (GitHub Actions)
   ↓
3. Claude Subagent로 정밀 큐레이션 (수동)
   ↓
4. 주간 리뷰 (Python 자동 + Claude 검토)
```

---

## 📊 점수 기준

### 총점: 0-100점

| 등급 | 점수 | 의미 |
|-----|------|------|
| S | 90-100 | 완벽한 노트 |
| A | 75-89 | 우수한 노트 |
| B | 60-74 | 양호한 노트 |
| C | 40-59 | 개선 필요 |
| D | 0-39 | 재작성 권장 |

### 4가지 평가 항목 (각 25점)

1. **완성도**: Frontmatter, 내용 길이, 코드 예시
2. **구조화**: 헤딩, 리스트, 태그, 날짜
3. **연결성**: 내부 링크, 백링크
4. **실행가능성**: TODO, Jira/Git 연동

---

## 📁 노트 타입

### Fleeting Note (빠른 메모)
- 짧은 길이 (500자 이하)
- 임시적 메모
- **위치**: `00-Inbox/`

### Literature Note (외부 자료 정리)
- 출처 정보 포함
- 요약 및 정리
- **위치**: `03-Resources/`

### Permanent Note (영구 지식)
- 독립적으로 이해 가능
- 재사용 가능한 개념
- **위치**: `10-Zettelkasten/`

### Project Note (프로젝트)
- 목표, 마감일, 상태
- **위치**: `01-Projects/`

---

## 🔧 고급 설정

### config.py 편집

```python
# automation/knowledge_curator/core/config.py

# 점수 기준 변경
SCORE_THRESHOLDS = {
    'S': 95,  # 더 엄격하게
    'A': 80,
    'B': 65,
    'C': 45,
    'D': 0
}

# 링크 제안 설정
AUTO_LINK_CONFIG = {
    'min_keyword_match': 2,  # 키워드 2개만 매칭되어도 제안
    'max_suggestions': 10,   # 최대 10개 제안
}
```

---

## 🤝 GitHub Actions 연동

### Notion 동기화 후 자동 큐레이션

`.github/workflows/knowledge-curator.yml` 참조

**워크플로우**:
1. Notion에서 새 노트 동기화
2. Python Script로 자동 점수화
3. Frontmatter 업데이트
4. Git commit & push

**매주 금요일 자동 리뷰**:
- 주간 리포트 자동 생성
- `30-Flow/Weekly/`에 저장
- Git commit

---

## 📚 예시

### 노트 분석 예시

**입력**: `01-Projects/postgres--snowflake-권한관리.md`

**출력**:
```markdown
# 📊 Document Analysis Report

## 품질 점수
**총점**: 72/100 (등급: A)

- 완성도: 20/25
- 구조화: 22/25
- 연결성: 12/25 ⚠️
- 실행가능성: 18/25

## 노트 타입
**분류**: Project Note

## 개선 제안
1. **[높음]**: 관련 노트와 링크 3개 이상 추가
2. **[중간]**: "## 개념" 섹션 추가하여 Permanent Note 추출
3. **[낮음]**: 코드에 주석 추가

## 관련 노트 추천
1. [[Snowflake 개념]] - 상위 개념
2. [[RBAC 패턴]] - 관련 개념
3. [[DataHub 프로젝트]] - 유사 작업
```

---

## 🆘 문제 해결

### Q: "Module not found" 오류
```bash
# Python path 문제
cd automation/knowledge_curator
pip install pyyaml
```

### Q: Obsidian MCP 연결 안 됨
- `.mcp.json` 파일 확인
- Obsidian MCP 서버 실행 중인지 확인

### Q: 점수가 너무 낮게 나옴
- `config.py`에서 기준 조정
- 또는 Claude Subagent 사용 (더 유연함)

---

## 🚀 로드맵

- [ ] Anthropic API 연동 (GitHub Actions에서 Claude 사용)
- [ ] 자동 Permanent Note 추출
- [ ] 시각화 대시보드
- [ ] 모바일 알림

---

**버전**: 1.0.0
**마지막 업데이트**: 2025-11-29
**라이선스**: MIT
