# DAE Second Brain - Knowledge Network Architecture

## 설계 철학

**"지식(Knowledge) + 경험(Experience) + 결과(Result) = 네트워크"**

각 주제마다 외부 지식, 실제 경험, 그 결과물이 연결된 지식 네트워크를 구축합니다.

---

## 📁 새로운 폴더 구조

```
DAE-Second-Brain/
├── Knowledge/                    # 주제별 지식 체계
│   ├── Data-Management/
│   │   ├── Data-Governance/
│   │   │   ├── Concepts/        # 학습한 개념, 외부 지식
│   │   │   ├── Experiences/     # 실제 작업 경험
│   │   │   └── Patterns/        # 반복 가능한 패턴, 결과
│   │   ├── Data-Quality/
│   │   │   ├── Concepts/
│   │   │   ├── Experiences/
│   │   │   └── Patterns/
│   │   ├── Data-Modeling/
│   │   │   ├── Concepts/
│   │   │   ├── Experiences/
│   │   │   └── Patterns/
│   │   └── Data-Lineage/
│   │       ├── Concepts/
│   │       ├── Experiences/
│   │       └── Patterns/
│   │
│   ├── Data-Architecture/
│   │   ├── Data-Mesh/
│   │   ├── Data-Lakehouse/
│   │   ├── Data-Medallion/
│   │   └── Streaming/
│   │
│   ├── Technology/
│   │   ├── Orchestration/       # Airflow
│   │   │   ├── Concepts/
│   │   │   ├── Experiences/
│   │   │   └── Patterns/
│   │   ├── Transformation/      # DBT
│   │   │   ├── Concepts/
│   │   │   ├── Experiences/
│   │   │   └── Patterns/
│   │   ├── Storage/
│   │   │   ├── PostgreSQL/
│   │   │   ├── BigQuery/
│   │   │   ├── Snowflake/
│   │   │   └── Elasticsearch/
│   │   ├── Infrastructure/
│   │   │   ├── Kubernetes/
│   │   │   ├── Docker/
│   │   │   └── AWS/
│   │   ├── CI-CD/
│   │   │   ├── Jenkins/
│   │   │   └── CodeDeploy/
│   │   └── Languages/
│   │       ├── Python/
│   │       └── SQL/
│   │
│   └── Analytics/
│       ├── Product-Analytics/   # AARRR, GTM 등
│       ├── Web-Analytics/       # 웹로그 분석
│       └── Marketing-Analytics/ # CRM, Personalize
│
├── Projects/                     # 실제 프로젝트
│   ├── Active/
│   └── Completed/
│
├── Experiences/                  # 회사/프로젝트별 경험 정리
│   ├── Qraft/
│   ├── Coupang/
│   └── ABLabs/
│
├── Career/                       # 커리어 관련
│   ├── Interview/
│   ├── Portfolio/
│   └── Learning-Path/
│
└── Templates/                    # 템플릿
    ├── concept-note.md
    ├── experience-note.md
    ├── pattern-note.md
    └── project-note.md
```

---

## 🏷️ 메타데이터 시스템

### 노트 타입 (type)
- `concept`: 외부 학습, 공부한 개념, 이론
- `experience`: 실제 작업 경험, 트러블슈팅, 시행착오
- `pattern`: 반복 가능한 패턴, 베스트 프랙티스
- `project`: 프로젝트 결과물
- `hub`: 주제별 허브 (MOC - Map of Content)

### 도메인 (domain)
- `data-engineering`: 데이터 엔지니어링
- `data-architecture`: 데이터 아키텍처
- `analytics`: 분석
- `devops`: 데브옵스
- `career`: 커리어

### 상태 (status)
- `learning`: 학습 중
- `practicing`: 실습/적용 중
- `mastered`: 숙달됨
- `archived`: 아카이브됨

### 표준 메타데이터 구조

```yaml
---
type: [concept|experience|pattern|project|hub]
domain: [data-engineering|data-architecture|analytics|devops]
topic: [구체적인 주제]
tags: [세부 태그들]
status: [learning|practicing|mastered|archived]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

---

## 📝 노트 타입별 템플릿

### Concept Note (개념 노트)
```markdown
---
type: concept
domain: data-engineering
topic: airflow
tags: [orchestration, workflow, dag]
status: learning
created: 2025-11-28
updated: 2025-11-28
---

# [개념명]

## 핵심 요약
한 문장으로 핵심을 정리

## 학습 내용
외부 소스에서 학습한 내용

## 주요 개념
- 개념 1
- 개념 2

## 참고 자료
- [링크 1](URL)
- [링크 2](URL)

## 관련 노트
- [[관련 경험]]
- [[관련 패턴]]

---
*Sources: [출처]*
```

### Experience Note (경험 노트)
```markdown
---
type: experience
domain: data-engineering
topic: airflow
tags: [troubleshooting, production, optimization]
status: practicing
project: [[프로젝트명]]
created: 2025-11-28
updated: 2025-11-28
---

# [경험 제목]

## 상황
어떤 상황이었는가

## 문제
무엇이 문제였는가

## 해결 과정
1. 시도 1
2. 시도 2
3. 최종 해결

## 결과
어떤 결과를 얻었는가

## 배운 점
이 경험에서 배운 교훈

## 관련 개념
- [[관련 개념 1]]
- [[관련 개념 2]]

## 생성된 패턴
- [[패턴명]]

---
*Date: YYYY-MM-DD*
*Project: [[프로젝트명]]*
```

### Pattern Note (패턴 노트)
```markdown
---
type: pattern
domain: data-engineering
topic: airflow
tags: [best-practice, reusable, template]
status: mastered
created: 2025-11-28
updated: 2025-11-28
---

# [패턴명]

## 언제 사용하는가
이 패턴이 적용되는 상황

## 구현 방법
```python
# 코드 예시
```

## 장점
- 장점 1
- 장점 2

## 주의사항
- 주의사항 1
- 주의사항 2

## 실제 적용 사례
- [[경험 1]]
- [[경험 2]]

## 관련 개념
- [[개념 1]]
- [[개념 2]]

---
*Pattern Type: [architectural|code|workflow]*
```

### Hub Note (허브 노트)
```markdown
---
type: hub
domain: data-engineering
topic: airflow
tags: [moc, orchestration]
created: 2025-11-28
updated: 2025-11-28
---

# Airflow Hub

## 개요
Airflow 관련 모든 지식과 경험을 연결하는 허브

## 📚 개념 (Concepts)
- [[Airflow 기본 개념]]
- [[DAG 작성 원칙]]
- [[Operator 종류]]

## 💼 경험 (Experiences)
- [[Airflow ECS 배포 경험]]
- [[Custom Operator 개발]]
- [[성능 최적화 경험]]

## 🎯 패턴 (Patterns)
- [[좋은 DAG 작성 패턴]]
- [[Backfill 처리 패턴]]
- [[에러 핸들링 패턴]]

## 🚀 프로젝트
- [[Qraft 데이터 파이프라인]]
- [[TypeB CRM 서비스]]

## 🔗 관련 주제
- [[DBT Hub]] - Transformation
- [[Kubernetes Hub]] - Infrastructure
- [[PostgreSQL Hub]] - Storage

---
*Last Updated: YYYY-MM-DD*
```

---

## 🔗 네트워크 연결 원칙

### 1. 양방향 링크
- 개념 ↔ 경험 ↔ 패턴이 서로 연결
- Hub에서 모든 하위 노트로 연결
- 하위 노트에서 Hub로 역연결

### 2. 수평적 연결
- 비슷한 주제끼리 연결
- 기술 스택 간 연결 (예: Airflow ↔ DBT ↔ PostgreSQL)

### 3. 수직적 연결
- 상위 개념 → 하위 구현
- 이론 → 실습 → 적용

---

## 📊 태그 시스템

### 기술 스택 태그
- `#airflow`, `#dbt`, `#docker`, `#kubernetes`
- `#postgresql`, `#bigquery`, `#snowflake`
- `#python`, `#sql`

### 도메인 태그
- `#orchestration`, `#transformation`, `#storage`
- `#data-quality`, `#data-modeling`, `#data-governance`
- `#analytics`, `#monitoring`

### 작업 타입 태그
- `#troubleshooting`, `#optimization`, `#migration`
- `#best-practice`, `#anti-pattern`
- `#learning`, `#reference`

### 프로젝트 태그
- `#qraft`, `#coupang`, `#ablabs`
- `#crm`, `#pipeline`, `#analytics`

---

## 🚀 마이그레이션 계획

### Phase 1: 구조 생성
1. 새 폴더 구조 생성
2. 템플릿 파일 생성
3. Hub 노트 생성

### Phase 2: 콘텐츠 분류
1. 현재 156개 파일을 타입별로 분류
   - Concept: 개념, 학습 자료
   - Experience: 실제 경험, 트러블슈팅
   - Pattern: 반복 사용 코드, 베스트 프랙티스
   - Deprecated: 삭제할 파일

2. 주제별로 분류
   - Data Management
   - Technology
   - Analytics
   - Career

### Phase 3: 마이그레이션
1. 파일을 적절한 폴더로 이동
2. 메타데이터 업데이트
3. 링크 연결
4. Hub 노트에 연결

### Phase 4: 정리
1. 중복 파일 제거
2. 불필요한 파일 삭제
3. Resources/References 폴더 정리

---

## 💡 사용 예시

### Airflow 학습 흐름
1. **Concept**: [Airflow 기본 개념](Knowledge/Technology/Orchestration/Concepts/Airflow-기본개념.md)
   - 외부 자료 학습, 책 내용 정리

2. **Experience**: [Airflow ECS 배포](Knowledge/Technology/Orchestration/Experiences/Airflow-ECS-배포.md)
   - 실제 배포하면서 겪은 문제와 해결

3. **Pattern**: [좋은 DAG 작성 패턴](Knowledge/Technology/Orchestration/Patterns/좋은-DAG-작성-패턴.md)
   - 경험을 통해 얻은 재사용 가능한 패턴

4. **Hub**: [Airflow Hub](Knowledge/Technology/Orchestration/Airflow-Hub.md)
   - 위 모든 내용을 연결하는 허브

### 프로젝트 연결
- Projects/Active/Qraft-데이터-파이프라인.md
  - 이 프로젝트에서 사용한 모든 기술의 Experience 노트와 연결
  - 새로 만든 Pattern 링크
  - 학습한 Concept 참조

---

## ✅ 체크리스트

- [ ] 새 폴더 구조 생성
- [ ] 템플릿 파일 생성
- [ ] Hub 노트 생성
- [ ] 파일 분류 (Concept/Experience/Pattern)
- [ ] 파일 마이그레이션
- [ ] 메타데이터 업데이트
- [ ] 링크 연결
- [ ] 불필요한 파일 삭제
- [ ] Resources/References 폴더 정리

---

*Design Date: 2025-11-28*
*Status: 설계 완료, 승인 대기*
