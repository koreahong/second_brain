# 🧠 DAE Second Brain - PARA 기반 지식 흐름 구조

> **구상 → 과정 → 결과 → 연결** 순환 시스템

## 🎯 핵심 철학

```
1. PARA 방법론 (Tiago Forte)
2. Zettelkasten (연결된 사고)
3. 지식 흐름 (Idea → Process → Outcome → Network)
```

## 📁 완전히 새로운 구조

```
DAE-Second-Brain/
│
├── 📂 Projects/                    # P: 진행 중인 프로젝트 (10-15개)
│   ├── Active/                     # 현재 진행 중
│   │   ├── MPD-75-DataHub-OIDC/
│   │   │   ├── 00-구상.md          # Ideation
│   │   │   ├── 01-과정.md          # Process (시행착오)
│   │   │   ├── 02-결과.md          # Outcome
│   │   │   └── assets/
│   │   └── ...
│   └── Staging/                    # 준비 중 (아직 시작 안함)
│
├── 📂 Areas/                       # A: 지속적 책임 영역
│   ├── Development/                # 개발 영역
│   │   ├── Data-Governance/
│   │   │   ├── _INDEX.md          # 영역 대시보드
│   │   │   ├── Metadata-Management/
│   │   │   ├── Data-Quality/
│   │   │   └── Lineage/
│   │   └── Infrastructure/
│   │       ├── _INDEX.md
│   │       ├── Keycloak-Auth/
│   │       └── Snowflake-Storage/
│   │
│   ├── Learning-Growth/            # 학습과 성장
│   │   ├── _INDEX.md
│   │   ├── Skills-Development/
│   │   └── Knowledge-Base/
│   │
│   └── Health-Energy/              # 건강과 에너지
│       └── _INDEX.md
│
├── 📂 Resources/                   # R: 참고 자료
│   ├── References/                 # 참고 문서
│   │   ├── Documentation/
│   │   ├── Articles/
│   │   └── Papers/
│   │
│   ├── Inspiration/                # 영감
│   │   ├── Ideas/
│   │   └── Quotes/
│   │
│   └── Tools-Methods/              # 도구와 방법론
│       ├── Frameworks/
│       └── Techniques/
│
├── 📂 Archives/                    # A: 보관함
│   ├── Projects/                   # 완료된 프로젝트
│   │   └── 2025-Q4/
│   └── Areas/                      # 비활성화된 영역
│
├── 📂 Atoms/                       # ⚛️ 원자적 지식 (Zettelkasten)
│   ├── Concepts/                   # 개념 노트
│   │   ├── C001-OIDC.md
│   │   ├── C002-JWT.md
│   │   └── ...
│   │
│   ├── Problems/                   # 문제 해결 패턴
│   │   ├── P001-Redirect-URI-오류.md
│   │   ├── P002-Snowflake-RBAC.md
│   │   └── ...
│   │
│   └── Patterns/                   # 재사용 가능한 패턴
│       ├── PT001-인증-흐름.md
│       └── ...
│
├── 📂 Flow/                        # 🌊 일일 흐름
│   ├── Daily/                      # 데일리 노트
│   │   └── 2025-11-27.md
│   ├── Weekly/                     # 주간 회고
│   │   └── 2025-W48.md
│   └── Inbox/                      # 받은 편지함 (정리 전)
│
└── 📂 Assets/                      # 🎨 자산
    ├── Templates/
    ├── Attachments/
    └── Scripts/
```

## 🔄 지식 흐름 (Knowledge Flow)

### 1단계: 구상 (Ideation) 💡

```markdown
# Projects/Active/MPD-75-DataHub-OIDC/00-구상.md

## 아이디어
DataHub에 Keycloak OIDC 인증을 통합하고 싶다

## 목표
- 사용자 SSO 로그인
- 그룹 기반 권한 관리

## 참고 자료
- [[Resources/Documentation/DataHub-Auth]]
- [[Resources/Documentation/Keycloak-OIDC]]

## 관련 개념
- [[Atoms/Concepts/C001-OIDC]]
- [[Atoms/Concepts/C002-JWT]]
```

### 2단계: 과정 (Process) 🔥

```markdown
# Projects/Active/MPD-75-DataHub-OIDC/01-과정.md

## 시행착오

### 문제 1: Redirect URI 오류
[[Atoms/Problems/P001-Redirect-URI-오류]]

**발생**: 2025-11-27 10:00
**증상**: callback URL 불일치
**시도**:
1. localhost:9002 → ❌
2. https 설정 → ✅

**배운 개념**: [[Atoms/Concepts/C003-OAuth-Redirect]]

### 문제 2: Groups Claim Null
[[Atoms/Problems/P002-Groups-Claim-Null]]

**발생**: 2025-11-27 14:00
**해결**: Keycloak Client Scope 설정

**새 패턴 발견**: [[Atoms/Patterns/PT001-Keycloak-Claim-Mapping]]

## 일일 로그
- [[Flow/Daily/2025-11-27]]
```

### 3단계: 결과 (Outcome) ✅

```markdown
# Projects/Active/MPD-75-DataHub-OIDC/02-결과.md

## 완성된 것

**기능**:
- ✅ SSO 로그인
- ✅ 그룹 기반 권한

**산출물**:
- 코드: `git: abc1234`
- 문서: [[Resources/Documentation/DataHub-OIDC-Setup]]

## 추출된 지식

### 개념 (Atoms)
- [[Atoms/Concepts/C001-OIDC]] ← 재사용 가능
- [[Atoms/Concepts/C003-OAuth-Redirect]] ← 새로 생성

### 패턴 (Atoms)
- [[Atoms/Patterns/PT001-Keycloak-Claim-Mapping]] ← 재사용 가능

## 연결된 프로젝트
→ [[Projects/Active/MPD-80-Snowflake-권한]]에서 이 지식 재활용

## 완료 후 이동
→ [[Archives/Projects/2025-Q4/MPD-75-DataHub-OIDC]]
```

### 4단계: 연결 (Network) 🕸️

```markdown
# Atoms/Concepts/C001-OIDC.md

## 개념
OpenID Connect - OAuth 2.0 기반 인증

## 활용된 프로젝트
- [[Projects/Active/MPD-75-DataHub-OIDC]]
- [[Projects/Active/MPD-82-Keycloak-Setup]]
- [[Projects/Archives/2025-Q3/MPD-65-Auth-System]]

## 연관 개념
- [[Atoms/Concepts/C002-JWT]]
- [[Atoms/Concepts/C004-OAuth2]]

## 관련 문제
- [[Atoms/Problems/P001-Redirect-URI-오류]]
- [[Atoms/Problems/P003-Token-Expiry]]

## 재사용 횟수
`= length(this.file.inlinks)` → 12번 재활용!
```

## 🎯 PARA 원칙 적용

### Projects (10-15개 유지)

**특징**:
- 명확한 마감일/완료 기준
- 3가지 상태: 구상 → 과정 → 결과

**예시**:
```
✅ Active (8개):
  - MPD-75: DataHub OIDC
  - MPD-80: Snowflake 권한
  ...

📋 Staging (3개):
  - MPD-85: MFT Git Sync (준비 중)
  ...
```

### Areas (무기한)

**특징**:
- 마감일 없음
- 지속적 관리
- 각 Area에 _INDEX.md 대시보드

**예시**:
```
Areas/Development/Data-Governance/_INDEX.md

## 현재 프로젝트
```dataview
FROM "Projects/Active"
WHERE contains(area, "Data-Governance")
```

## 축적된 지식
```dataview
FROM "Atoms"
WHERE contains(area, "Data-Governance")
SORT reuse-count DESC
```
```

### Resources (언젠가/아마도)

**특징**:
- 관심 주제
- 아직 프로젝트 아님
- 참고 자료

### Archives (비활성)

**특징**:
- 완료된 프로젝트
- 분기별 정리

## ⚛️ Atoms (원자적 지식)

### Concept (개념)
```markdown
---
id: C001
type: concept
created: 2025-11-27
reuse-count: 0
---

# OIDC

한 줄: OAuth 2.0 기반 인증 프로토콜

[상세 내용]

## 연결
- 상위: [[OAuth2]]
- 하위: [[JWT]], [[Claims]]
- 활용: [[MPD-75]], [[MPD-82]]
```

### Problem (문제)
```markdown
---
id: P001
type: problem
solved: true
pattern: PT001
---

# Redirect URI 오류

문제 → 시도 → 해결 → 패턴 추출

→ 재사용 가능한 패턴: [[PT001-OAuth-Redirect-Pattern]]
```

### Pattern (패턴)
```markdown
---
id: PT001
type: pattern
reuse-count: 5
---

# Keycloak Claim Mapping Pattern

언제: Keycloak에서 custom claim 필요 시
방법: [단계별]
주의: [...]

## 활용 사례
1. [[MPD-75]] - Groups claim
2. [[MPD-82]] - Roles claim
...
```

## 🌊 일일 워크플로우

### 아침
```
1. Flow/Inbox/ 검토
2. Projects/Active/ 확인
3. Flow/Daily/2025-11-27.md 생성
```

### 작업 중
```
문제 발생 →
1. Flow/Inbox/문제-제목.md
2. 해결 → Atoms/Problems/P00X.md
3. 프로젝트 01-과정.md에 링크
```

### 저녁
```
1. Daily 회고
2. Inbox → Projects/Areas/Atoms로 분류
3. Graph View 확인 (연결 시각화)
```

### 금요일
```
1. Weekly 회고 생성
2. 완료 프로젝트 → Archives
3. Atoms 재활용 횟수 확인
```

## 📊 Dataview 대시보드

### Home Dashboard
```dataview
# 진행 중 프로젝트
TABLE status, deadline
FROM "Projects/Active"
WHERE status != "archived"
SORT deadline ASC

# 가장 많이 재활용된 지식
TABLE type, reuse-count
FROM "Atoms"
SORT reuse-count DESC
LIMIT 10

# 이번 주 생성된 Atoms
LIST
FROM "Atoms"
WHERE created >= date(today) - dur(7 days)
```

## 🕸️ Graph View 활용

### 필터 예시
```
# 특정 프로젝트의 지식 네트워크
path:Projects/Active/MPD-75

# Atoms만 (지식 네트워크)
path:Atoms

# 재활용 횟수 높은 것만
reuse-count > 5
```

## 🔄 순환 흐름

```
📥 Inbox (아이디어)
  ↓
💡 Projects/구상
  ↓
🔥 Projects/과정 (시행착오)
  ↓ (지식 추출)
⚛️ Atoms (개념/문제/패턴)
  ↓ (재활용)
✅ Projects/결과
  ↓ (완료)
📦 Archives
  ↓ (연결)
🕸️ Knowledge Network (Graph)
  ↓ (재활용)
💡 새 Projects (지식 활용!)
```

---

**Sources**:
- [The PARA Method by Tiago Forte](https://fortelabs.com/blog/para/)
- [PARA Method Summary - Thomas Frank](https://thomasjfrank.com/productivity/books/the-para-method-by-tiago-forte-summary-and-book-notes/)
- [How to Organize with PARA](https://www.todoist.com/productivity-methods/para-method)

**이제 완벽한 세컨드 브레인이 준비되었습니다!** 🧠✨
