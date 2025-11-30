# Synthesizer Agent (통합 Agent)

## Purpose
흩어진 지식을 연결하여 새로운 통찰을 만듭니다.
"The whole is greater than the sum of its parts"

## Role
- MOC (Map of Content) 자동 생성
- Hub Note 업데이트
- 패턴 발견 및 통찰 제안
- 클러스터링 및 주제 분석
- Knowledge Gap 감지

## Usage
- `/synthesize [주제]` - 특정 주제 MOC 생성
- `/patterns` - 패턴 발견
- `/gaps` - 지식 격차 분석
- 월간 자동 실행

## MOC Auto-Generation

**Input:**
```
/synthesize airflow
```

**Process:**
1. Airflow 관련 노트 수집
2. 클러스터링 (AI)
3. 카테고리 생성
4. MOC 구조 생성
5. Hub 노트 연결

**Output:**
```markdown
---
type: moc
topic: Airflow
coverage: 85%
notes-count: 23
created: 2025-11-30
updated: 2025-11-30
status: evergreen
---

# Airflow - Map of Content

> Apache Airflow 관련 모든 지식을 연결하는 지도

## 📊 Overview
- **Total Notes**: 23
- **Coverage**: 85% (estimated)
- **Last Updated**: 2025-11-30

## 🎯 핵심 개념

### 기본 (Fundamentals)
- [[202511270815|Airflow DAG 개념]]
- [[202511270820|Operator 종류]]
- [[202511270830|Task 의존성]]
- [[202511270840|Scheduler 작동 방식]]

### Task 통신 (Task Communication)
- [[202511280901|XCom: Task 간 데이터 전달]] 🌲
- [[202511280905|XCom S3 패턴]]
- [[202511280910|TaskFlow API]]

### 고급 패턴 (Advanced Patterns)
- [[202511270940|Dynamic DAG 생성]]
- [[202511270950|Custom Operator 개발]]
- [[202511270955|Sensor 활용 패턴]]

## 💼 실전 경험

### 프로젝트
- [[01-Projects/Active/DataHub-OIDC]] - XCom 활용
- [[02-Areas/크래프트/Projects/Completed/Airflow-ECS-배포]]

### 트러블슈팅
- [[XCom-1MB-제한-해결]]
- [[DAG-Parsing-성능-개선]]

## 📖 참고 자료

### Literature Notes
- [[03-Resources/Airflow-공식문서-XCom]]
- [[03-Resources/책-Data-Pipelines-with-Airflow]]

### External
- [Official Docs](https://airflow.apache.org)
- [Best Practices](...)

## 🗺️ Related Maps
- [[Python-Map]] (Airflow는 Python 기반)
- [[Docker-Map]] (배포 환경)
- [[Data-Engineering-Map]] (상위 주제)

## 📈 학습 로드맵

### 🌱 Beginner (1주)
1. [[Airflow-DAG-개념]] 이해
2. [[Operator-종류]] 학습
3. 간단한 DAG 작성

### 🌿 Intermediate (2-3주)
4. [[XCom]] 활용
5. [[복잡한-의존성]] 처리
6. [[Metadata-DB]] 이해

### 🌲 Advanced (1개월+)
7. [[Dynamic-DAG]] 생성
8. [[Custom-Operator]] 개발
9. 프로덕션 배포

## 🔍 Knowledge Gaps

⚠️ 아직 다루지 않은 주제:
- Airflow 2.0+ 새 기능
- REST API 활용
- 보안 설정 (RBAC)
- 모니터링 & 알림

→ 다음 학습 우선순위!

## 📊 Statistics
- Permanent Notes: 18
- Literature Notes: 5
- Projects: 3
- Average Links: 9.2 ✅
- Evergreen: 12 (67%)

---
**Auto-generated**: 2025-11-30
**Next Review**: 2025-12-30
```

## Pattern Discovery

```python
def discover_patterns():
    """지식 베이스에서 패턴 발견"""

    patterns = []

    # 1. 반복되는 주제
    topics = analyze_frequent_topics()
    for topic in topics:
        if topic.count >= 3:
            patterns.append({
                'type': 'recurring_theme',
                'topic': topic.name,
                'notes': topic.notes,
                'suggestion': f"Create Hub: {topic.name}"
            })

    # 2. 공통 패턴
    # "Airflow DAG", "DBT model", "Iceberg table"
    # → 모두 "선언적 정의" 패턴
    common_patterns = find_common_patterns()

    # 3. 연결 밀도 높은 클러스터
    clusters = detect_clusters()

    return patterns
```

**Example Output:**
```
🔍 발견된 패턴:

1. **선언적 vs 명령적 설계**
   관련 노트: [[Airflow-DAG]], [[DBT-Model]], [[Iceberg-Table]]
   공통점: YAML/SQL로 정의, 실행은 엔진이 담당
   💡 제안: "선언적 데이터 파이프라인 패턴" Permanent Note 생성

2. **OIDC 통합 패턴**
   관련 노트: [[Keycloak-OIDC]], [[DataHub-Auth]], [[Airflow-Auth]]
   공통점: Client 설정 → Callback URL → Token 검증
   💡 제안: "OIDC 통합 체크리스트" Hub Note 생성

3. **메타데이터 관리**
   관련 노트: 12개 (DataHub, Iceberg, DBT)
   🔗 밀도: 높음 (avg 14 links)
   💡 제안: "Data-Governance-Map" MOC 확장
```

## Hub Note Management

```markdown
# Hub Note Update

**Before:**
[[Airflow-Hub]] - 15 notes

**After:**
[[Airflow-Hub]] - 23 notes (+8)

**Added Sections:**
- Task Communication (3 new notes)
- Troubleshooting (2 new notes)

**Updated:**
- Learning Roadmap
- Statistics
```

## Knowledge Gap Analysis

```python
def analyze_knowledge_gaps():
    """지식 격차 분석"""

    gaps = []

    # 1. MOC 대비 누락된 주제
    expected_topics = get_expected_topics_from_moc()
    existing_topics = get_existing_topics()
    missing = expected_topics - existing_topics

    # 2. 링크는 있지만 노트가 없는 것
    broken_links = find_broken_links()

    # 3. 자주 검색하지만 없는 주제
    search_gaps = analyze_search_history()

    return gaps
```

**Output:**
```
🔍 Knowledge Gaps 발견:

## 우선순위 높음
1. **Airflow REST API**
   - 5번 검색됨
   - 3개 노트에서 링크 (빈 링크)
   → 액션: Literature Note 작성

2. **DBT Incremental 전략**
   - DataHub 프로젝트에서 필요
   - 관련 노트 없음
   → 액션: 공식 문서 읽고 정리

## 우선순위 중간
3. **Docker Multi-stage Build**
   - 2개 프로젝트에서 언급
   - 상세 노트 없음

## 제안
- 이번 주: 1, 2 학습 및 노트 작성
- 다음 주: 3 학습
```

## Integration

- **Curator Agent**: Evergreen 노트를 MOC 재료로 활용
- **Linker Agent**: 생성된 MOC를 자동 링크 대상에 추가
- **Reviewer Agent**: Monthly에 새 MOC/패턴 보고

---

**Last Updated**: 2025-11-30
**Version**: 1.0
