# Vault Structure Convention

> **이 문서 업데이트 시**: PARA 구조, 폴더 규칙, 명명 규칙만 추가. 설명 간결하게.

이 문서는 AI가 vault 구조 작업 시 따라야 할 컨벤션입니다.

## PARA + Zettelkasten 구조

### 핵심 폴더 (Top Level)

```
Second-Brain/
├── 01-Projects/                     # [임시] Notion 마이그레이션
│   └── [이동 예정]
├── 02-Areas/                        # 장기 관심사 (회사, 역할)
│   └── 크래프트테크놀로지스/
│       ├── Projects/
│       │   ├── Active/             # 진행중 프로젝트
│       │   ├── Completed/          # 완료된 프로젝트
│       │   └── Archived/           # 과거/취소 프로젝트
│       ├── Experience/
│       │   └── Weekly/             # 주간 회고
│       │       ├── 2024/
│       │       └── 2025/
│       └── Achievements/           # 성과 기록
├── 03-Resources/                    # 공유 지식 (레퍼런스)
│   ├── DAE/                        # DAE 역할/범위
│   ├── Data-Governance/            # 데이터 거버넌스
│   ├── Technology/                 # 기술 지식
│   │   ├── Airflow/
│   │   ├── DBT/
│   │   ├── DataHub/
│   │   ├── Python/
│   │   └── [기술별 폴더]
│   └── Methodologies/              # 방법론
├── 10-Zettelkasten/                # 원자적 지식
│   ├── Permanent/                  # 영구 노트 (개념)
│   └── Literature/                 # 레퍼런스 요약
└── 30-Flow/                        # 흐름 (인생 회고)
    └── Life-Insights/              # 본깨적 (깨달음)
        ├── Work/                   # 업무 관련
        ├── Personal/               # 개인적 경험
        └── Observations/           # 일상 관찰
```

### 임시 폴더 (마이그레이션 대기)

```
업무리스트/        (46 files)  → 02-Areas/.../Projects/
회고록/           (15 files)  → 02-Areas/.../Experience/Weekly/
레퍼런스/         (238 files) → 03-Resources/
본깨적/          (229 files) → 30-Flow/Life-Insights/
```

## 폴더 배치 규칙

### 프로젝트 (Projects/)

**Active/**: 현재 진행중
- Status: 진행중, 시작 예정
- 예: 데이터 현황 파악, DBT 모델링 작업

**Completed/**: 완료됨
- Status: 완료
- 결과물 포함
- 예: 완료된 마이그레이션 프로젝트

**Archived/**: 과거/취소
- Status: 보류, 취소
- 또는 이전 회사 프로젝트 (aivelabs)

### 경험 (Experience/)

**Weekly/**: 주간 회고
- 형식: `YYYY년-MM월-DD일.md`
- 연도별 폴더 구분 (2024/, 2025/)
- 매주 작성 (일요일 또는 월요일)

### 리소스 (Resources/)

**Articles/**: 외부 아티클 (type: article)
- Medium, 블로그, 온라인 글 등
- 읽은 아티클 전체 내용 저장
- 예: Claude-Code-7가지-필수-플러그인.md

**Technology/**: 기술별 레퍼런스 (type: reference)
- Airflow/, DBT/, DataHub/, Python/ 등
- 각 기술의 개념, 패턴, 예제
- **직접 작성한** 기술 문서

**Data-Governance/**: 거버넌스 개념
- 원칙, 정책, 베스트 프랙티스

**DAE/**: DAE 역할
- 역할 정의, 범위, 책임

**Methodologies/**: 방법론
- PARA, Zettelkasten, GTD 등

### 인사이트 (Life-Insights/)

**Work/**: 업무 관련 깨달음
- 프로젝트에서 얻은 교훈
- 협업 경험
- 커리어 인사이트

**Personal/**: 개인적 경험
- 자기 성장
- 습관, 루틴

**Observations/**: 일상 관찰
- 사회 현상
- 트렌드 관찰

### Zettelkasten (원자적 지식)

**Permanent/**: 영구 노트
- 개념 정의 (atomic)
- 200-500 단어
- 고유 아이디어

**Literature/**: 레퍼런스 요약
- 책, 논문, 블로그 요약
- 출처 명시

## 노트 명명 규칙

### 프로젝트 노트
```
[프로젝트명]-[주요-기능].md
예: 팀별-원천-데이터-계약현황-파악.md
```

### Weekly 회고
```
YYYY년-MM월-DD일.md
예: 2025년-12월-07일.md
```

### 기술 리소스
```
[기술명]-[개념].md
예: Airflow-DAG-설계-패턴.md
    DBT-Incremental-모델.md
```

### 인사이트
```
[핵심-주제].md
예: 데이터-거버넌스의-중요성.md
    협업에서-문서화의-가치.md
```

### Zettelkasten
```
[개념명].md (간결하게)
예: Atomic-Habit.md
    Information-Architecture.md
```

## Frontmatter 필수 필드

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - tag1
  - tag2
company: aivelabs|qraft|personal
status: draft|active|completed|archived
type: project|reflection|article|reference|insight|concept
category:  # Optional, for reflection type
  - Life   # Personal insights → Life-Insights/Personal/
  - Work   # Work reflections → Experience/Weekly/
---
```

### Company 필드
- **aivelabs**: 2022-2023 (created < 2025-08)
- **qraft**: 2025-08+ (created >= 2025-08)
- **personal**: 개인 학습/경험

### Type 필드
- **project**: 프로젝트 노트
- **reflection**: 회고 (Weekly or Life 카테고리)
- **article**: 외부 아티클 (Medium, 블로그 등)
- **reference**: 기술 레퍼런스 (직접 작성)
- **insight**: 인생 인사이트
- **concept**: Zettelkasten 개념

### Status 필드
- **draft**: 작성중
- **active**: 진행중
- **completed**: 완료
- **archived**: 보류/취소

## 연결 구조

### 계층적 연결 (Hierarchical)
```markdown
## 📎 Related

### 상위 프로젝트
- [[상위-프로젝트]]

### 하위 작업
- [[하위-작업-1]]
- [[하위-작업-2]]
```

### 시간적 연결 (Temporal)
```markdown
## 📎 Related

### 같은 주 회고
- [[2025년-12월-07일]] (같은 주)
  - 컨텍스트: 이 프로젝트 진행 중 깨달음

### 관련 프로젝트 (같은 시기)
- [[다른-프로젝트]] (2025-10월)
  - 컨텍스트: 함께 진행한 작업
```

### 주제적 연결 (Thematic)
```markdown
## 📎 Related

### 사용된 지식
- [[03-Resources/Technology/Airflow/DAG-패턴]]
  - 컨텍스트: 이 패턴을 프로젝트에 적용

### 생성된 인사이트
- [[30-Flow/Life-Insights/데이터-거버넌스의-중요성]]
  - 컨텍스트: 프로젝트 수행 중 깨달음
```

## 이동 규칙

### Curator Agent가 자동 이동
```python
# Type 기반 이동
if type == 'project':
    if status == 'active':
        → 02-Areas/.../Projects/Active/
    elif status == 'completed':
        → 02-Areas/.../Projects/Completed/
    elif status == 'archived':
        → 02-Areas/.../Projects/Archived/

elif type == 'reflection':
    # ⚠️ CRITICAL: Check category field!
    if 'Life' in category:
        # Personal insights/reflections
        → 30-Flow/Life-Insights/Personal/
    else:
        # Work-related weekly reflections
        year = created[:4]
        → 02-Areas/.../Experience/Weekly/{year}/

elif type == 'article':
    # ⚠️ NEW: External articles (Medium, blogs, etc.)
    # Always go to Articles folder, NOT Technology/
    → 03-Resources/Articles/

elif type == 'reference':
    # Technical references (직접 작성한 레퍼런스)
    # 태그 기반 세분화
    if 'airflow' in tags:
        → 03-Resources/Technology/Airflow/
    elif 'dbt' in tags:
        → 03-Resources/Technology/DBT/
    # ...

elif type == 'insight':
    # Check company field for Work vs Personal
    if company in ['qraft', 'aivelabs']:
        → 30-Flow/Life-Insights/Work/
    else:
        → 30-Flow/Life-Insights/Personal/

elif type == 'concept':
    → 10-Zettelkasten/Permanent/
```

## 검증 규칙

### PARA Compliance Check
```python
# 올바른 위치 검증
note_type = frontmatter['type']
note_category = frontmatter.get('category', [])
note_company = frontmatter['company']
note_path = get_path(note)

# Dynamic path validation
if type == 'project':
    expected = '02-Areas/.../Projects/'
elif type == 'reflection':
    if 'Life' in category:
        expected = '30-Flow/Life-Insights/Personal/'
    else:
        expected = '02-Areas/.../Experience/Weekly/'
elif type == 'article':
    expected = '03-Resources/Articles/'
elif type == 'reference':
    expected = '03-Resources/Technology/'  # or Data-Governance/, etc.
elif type == 'insight':
    if company in ['qraft', 'aivelabs']:
        expected = '30-Flow/Life-Insights/Work/'
    else:
        expected = '30-Flow/Life-Insights/Personal/'
elif type == 'concept':
    expected = '10-Zettelkasten/Permanent/'

if not note_path.startswith(expected):
    → ❌ PARA 불일치
    → Curator Agent로 이동 필요
```

## 특수 케이스

### Notion 마이그레이션
- `업무리스트/`, `회고록/`, `레퍼런스/`, `본깨적/`은 임시 위치
- Curator Agent가 자동으로 PARA 구조로 이동
- 이동 후 빈 폴더는 삭제

### Automation 디렉토리
- `automation/`: Notion 동기화 모듈 (독립 관리)
- vault 구조 규칙 적용 제외
- 별도 문서 참조: `automation/README.md`

## 참조
- [connection-quality.md](connection-quality.md) - 연결 품질 원칙
- [capture-workflow.md](capture-workflow.md) - 캡처 워크플로우
- [migration-guide.md](migration-guide.md) - 마이그레이션 가이드
