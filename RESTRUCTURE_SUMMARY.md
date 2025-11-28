---
date: 2025-11-28
type: documentation
---

# DAE Second Brain 구조 재편성 요약

## 🎯 목표

**"지식(Knowledge) + 경험(Experience) + 결과(Pattern) = 네트워크"**

DAE 직무에 최적화된 지식 네트워크 구조로 전환

---

## 📊 변경 사항

### Before: 기존 구조
```
Resources/References/
└── 156개 파일 (모두 한 폴더에 집중)
    - 체계 없이 섞여있음
    - 내용 부실한 파일 다수
    - 연결 관계 불명확
```

### After: 새로운 구조
```
Knowledge/
├── Data-Management/
│   ├── Data-Governance/ (Concepts/Experiences/Patterns)
│   ├── Data-Quality/
│   ├── Data-Modeling/
│   └── Data-Lineage/
├── Data-Architecture/
│   ├── Data-Mesh/
│   ├── Data-Lakehouse/
│   └── Streaming/
├── Technology/
│   ├── Orchestration/ (Airflow - 22개 노트)
│   ├── Transformation/ (DBT)
│   ├── Storage/ (PostgreSQL, BigQuery, Snowflake, etc)
│   ├── Infrastructure/ (K8s, Docker, AWS)
│   ├── CI-CD/
│   └── Languages/
│       ├── Python/ (15개 노트)
│       └── SQL/
├── Analytics/
│   ├── Product-Analytics/
│   ├── Web-Analytics/
│   └── Marketing-Analytics/
├── Personal/
│   ├── Well-being/
│   ├── Investment/
│   └── Learning/
└── Career/
    ├── Certifications/
    ├── Interview/
    ├── Portfolio/
    └── Learning-Path/
```

---

## 📈 처리 결과

### 파일 통계
- **원본 파일**: 156개
- **이동된 파일**: 113개
- **삭제된 파일**: 34개 (내용 부실)
- **생성된 Hub**: 2개 (Airflow, Python)
- **생성된 템플릿**: 5개

### 분류 기준
**삭제 대상**:
- 실질 내용 100자 미만
- 템플릿만 있고 내용 없음
- "TODO", "작성 예정"만 표시

**보관 대상**:
- DAE 무관해도 실제 내용 있으면 적절한 카테고리에 보관
- 예: 투자 노트 → Personal/Investment
- 예: 우울증 → Personal/Well-being

---

## 🗂️ 노트 타입 시스템

### 📚 Concept (개념)
외부 학습, 공부한 내용
- 예: `airflow_기본개념(책).md`
- 예: `ACID_개념.md`

### 💼 Experience (경험)
실제 작업 경험, 트러블슈팅
- 예: `airflow_ecs에_적용.md`
- 예: `과제풀기-_하이퍼커넥트.md`

### 🎯 Pattern (패턴)
반복 사용 가능한 베스트 프랙티스
- 예: `Rules_for_good_dags.md`
- 예: `sqlalchemy_사용법.md`

### 🏢 Hub (허브)
주제별 지식 네트워크 허브
- 예: `Airflow-Hub.md` (22개 노트 연결)
- 예: `Python-Hub.md` (15개 노트 연결)

---

## 🔧 생성된 파일들

### Hub 노트
1. **Knowledge/Technology/Orchestration/Airflow-Hub.md**
   - 22개 노트 연결 (Concepts: 14, Experiences: 1, Patterns: 7)
   - 학습 로드맵 포함
   - 빠른 참조 가이드

2. **Knowledge/Technology/Languages/Python/Python-Hub.md**
   - 15개 노트 연결 (Concepts: 9, Experiences: 1, Patterns: 5)
   - 코딩 테스트, ORM, 비동기 프로그래밍 등

### 템플릿
1. `Templates/concept-note.md` - 개념 노트 템플릿
2. `Templates/experience-note.md` - 경험 노트 템플릿
3. `Templates/pattern-note.md` - 패턴 노트 템플릿
4. `Templates/hub-note.md` - 허브 노트 템플릿
5. `Templates/project-note.md` - 프로젝트 노트 템플릿

### 문서
1. `README.md` - 전체 구조 가이드 (업데이트)
2. `KNOWLEDGE_STRUCTURE_DESIGN.md` - 상세 설계 문서
3. `RESTRUCTURE_SUMMARY.md` - 이 문서

---

## 📂 주요 카테고리별 파일 수

### Technology
- **Orchestration** (Airflow): 22개
- **Languages/Python**: 15개
- **Languages/SQL**: 13개
- **Storage/PostgreSQL**: 11개
- **Infrastructure/AWS**: 9개
- **Infrastructure/Docker**: 7개
- **Infrastructure/Kubernetes**: 6개
- **Transformation** (DBT): 4개
- **Storage/Snowflake**: 2개
- **Storage/BigQuery**: 1개
- **Storage/Elasticsearch**: 1개
- **Storage/Trino**: 1개
- **CI-CD**: 2개

### Data Management
- **Data-Governance**: 5개
- **Data-Modeling**: 3개
- **Data-Quality**: 1개

### Analytics
- **Product-Analytics**: 4개
- **Web-Analytics**: 3개

### Career
- **Certifications**: 3개
- **Learning-Path**: 4개
- **Portfolio**: 2개
- **Interview**: 1개

### Personal
- **Investment**: 4개
- **Well-being**: 1개

### Experiences
- **Companies**: 3개

### Uncategorized
- 4개 (추후 분류 필요)

---

## 🏷️ 메타데이터 시스템

모든 노트에 표준 메타데이터 적용:

```yaml
---
type: [concept|experience|pattern|hub]
domain: [data-engineering|data-architecture|analytics|devops]
topic: [구체적인 주제]
tags: [세부 태그들]
status: [learning|practicing|mastered|archived]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

---

## 🔗 네트워크 연결 구조

### 양방향 링크
```
Concept ↔ Experience ↔ Pattern ↔ Hub
```

### 예: Airflow 학습 흐름
```
[Airflow 기본 개념]
        ↓ 학습
[Airflow ECS 배포 경험]
        ↓ 적용
[좋은 DAG 작성 패턴]
        ↓ 정리
[Airflow Hub] ← 모든 Airflow 노트 통합
```

---

## ✅ 완료된 작업

1. ✅ 현재 vault 구조 분석
2. ✅ 지식 네트워크 아키텍처 설계
3. ✅ 메타데이터 및 태그 시스템 설계
4. ✅ 새 폴더 구조 생성
5. ✅ 템플릿 파일 5개 생성
6. ✅ 156개 파일 자동 분석 및 분류
7. ✅ 113개 파일 마이그레이션
8. ✅ 34개 빈 파일 삭제
9. ✅ 주요 Hub 노트 2개 생성 (Airflow, Python)
10. ✅ README 업데이트
11. ✅ 기존 HUB 파일들 Archives로 이동
12. ✅ 마이그레이션 스크립트 Archives로 이동

---

## 📝 다음 단계 제안

### 단기 (1주일)
1. 나머지 주요 Hub 생성
   - SQL Hub
   - PostgreSQL Hub
   - Docker/Kubernetes Hub
   - DBT Hub
   - Analytics Hub

2. 파일 메타데이터 업데이트
   - 각 파일에 표준 메타데이터 추가
   - Hub 링크 추가

3. Uncategorized 4개 파일 분류

### 중기 (1개월)
1. 각 Concept/Experience/Pattern 간 링크 연결
2. 프로젝트 노트 작성 (Qraft, Coupang 등)
3. 학습 로드맵 구체화
4. Dataview 쿼리로 통계 대시보드 구축

### 장기 (3개월)
1. 지속적인 노트 작성 습관화
2. 주간 회고로 지식 네트워크 강화
3. 블로그/포트폴리오와 연동
4. 팀 지식 공유 시스템으로 확장

---

## 🎓 사용 가이드

### 새 노트 작성 시
1. 주제 파악 (예: Airflow 관련)
2. 폴더 찾기 (예: `Knowledge/Technology/Orchestration/`)
3. 타입 결정 (Concept/Experience/Pattern)
4. 템플릿 사용 (`Templates/concept-note.md`)
5. 메타데이터 작성
6. Hub에 연결 (`Airflow-Hub.md`에 링크 추가)

### 학습 시
1. Concept 작성: 외부 자료 학습 내용 정리
2. Experience 기록: 실제 적용하며 경험 기록
3. Pattern 추출: 재사용 가능한 패턴 정리
4. Hub 업데이트: 연결 추가

---

## 📞 참고

### 관련 문서
- [[README|메인 README]]
- [[KNOWLEDGE_STRUCTURE_DESIGN|상세 설계 문서]]
- [[MIGRATION_SUMMARY|Notion 마이그레이션 요약]]

### 아카이브
- `Archives/Old-Structure/` - 기존 HUB 파일들
- `Archives/*.py` - 마이그레이션 스크립트들

---

*Date: 2025-11-28*
*Duration: ~2 hours*
*Status: ✅ Complete*
