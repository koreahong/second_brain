---
created: '2025-11-30'
updated: '2025-11-30'
project_status: completed
project_period: 2025-11-11 to 2025-11-29
tags:
  - Projects
  - Infrastructure
  - Airflow
  - DataGovernance
  - 크래프트테크놈로지스
related:
  - Airflow-3.0-구현
  - Keycloak-SSO-도입-배경
  - 데이터-거버넌스-도입
---
# Airflow 3.0 업그레이드 배경

## 프로젝트 개요

**시기:** 2025년 11월  
**담당:** ML Platform Team  
**목적:** Apache Airflow 2.x → 3.x 업그레이드를 통한 DataHub 메타데이터 관리 및 데이터 거버넌스 강화

## 왜 업그레이드가 필요했는가?

### 1. DataHub 메타데이터 수집 불가 문제

**발생 시점:** 2025년 10월 (DataHub 도입 시도 중)

**문제 상황:**
- DataHub 공식 Airflow 플러그인은 **Airflow 2.7~2.9.x만 지원**
- Airflow 3.x와 호환되지 않아 메타데이터 수집 불가
- CFO님의 "팀별 데이터 격리" 요구사항을 충족하려면 DataHub 필수

**비즈니스 영향:**
```
문제 발생                              비즈니스 요구사항
─────────────────────────────────────────────────────────
DataHub 플러그인 미작동              → CFO: 팀별 데이터 격리 필요
메타데이터 수집 불가                → 데이터 거버넌스 불가능
DAG lineage 미추적                   → 데이터 추적성 상실
데이터 소유권 불명확                → 책임 소재 불분명
```

**대안 검토:**
1. **Airflow 2.9로 다운그레이드** ❌
   - Keycloak SSO 통합 포기해야 함
   - 이미 Airflow 3.x 기반으로 파이프라인 구축 완료
   - 롤백 비용 너무 큼

2. **DataHub 포기** ❌
   - CFO 요구사항 충족 불가
   - 데이터 거버넌스 구현 불가
   - 팀 간 데이터 충돌 지속

3. **Custom Connector 개발** ✅
   - Airflow 3.x 유지하면서 DataHub 연동
   - REST API v2 사용으로 버전 독립성 확보
   - 장기적으로 유지보수 가능

### 2. 비즈니스 배경: CFO의 팀별 데이터 격리 요청

**발생 시점:** 2025년 9월

**사건:**
- Strategy 팀 구성원이 실수로 HFT 팀의 DAG 수정
- HFT 파이프라인 1시간 다운타임 발생
- CFO: "팀별로 데이터를 완전히 격리할 수 없나?"

**요구사항:**
1. 팀별 데이터 접근 권한 분리
2. DAG 수정 권한 팀별 격리
3. 데이터 소유권 명확화
4. 메타데이터 추적 및 감사

**해결 전략:**
```
CFO 요구사항                    → 기술 솔루션
──────────────────────────────────────────────────
팀별 데이터 격리                → Keycloak Groups
DAG 권한 분리                   → Airflow Auth Manager
데이터 소유권 명확화           → DataHub Ownership
메타데이터 추적                → DataHub Lineage
```

**DataHub가 필수인 이유:**
- Snowflake 테이블, DBT 모델, Airflow DAG를 하나의 플랫폼에서 추적
- 데이터 소유자(Owner) 자동 추적
- 팀별 Domain 할당으로 데이터 격리 시각화
- 변경 이력 추적으로 감사(Audit) 가능

### 3. 기술적 배경: OpenLineage 통합 변경

**Airflow 2.7+ 아키텍처 변경:**

| 구분 | Airflow 2.6 이하 | Airflow 2.7+ | Airflow 3.x |
|------|------------------|--------------|-------------|
| OpenLineage | 외부 패키지 (`openlineage-airflow`) | 네이티브 provider | 완전 통합 |
| 안정성 | Brittle | Stable | Production-ready |
| 유지보수 | 커뮤니티 | Apache | Apache |
| DataHub 호환 | 가능 | 부분 가능 | **불가능** (구조 변경) |

**Airflow 3.x serialized_dag 구조 변경:**
```json
// Airflow 2.x
{
  "tasks": [{"task_id": "task1", "downstream_task_ids": ["task2"]}]
}

// Airflow 3.x (변경됨!)
{
  "dag": {
    "tasks": [
      {
        "__var": {"task_id": "task1", "downstream_task_ids": ["task2"]},
        "__type": "operator"
      }
    ]
  }
}
```

**영향:**
- DataHub 플러그인이 `serialized_dag` 파싱 실패
- Task dependencies 추출 불가
- Lineage 시각화 불가능

## 솔루션: Custom REST API Connector 개발

### 개발 결정 배경

**2025년 11월 초 결정:**

**장점:**
1. **Airflow 버전 독립성**
   - REST API v2만 사용 → 버전 변경에 영향 적음
   - Airflow 3.x, 4.x에도 계속 사용 가능

2. **완전한 제어권**
   - Keycloak OIDC 인증 직접 통합
   - 팀별 커스터마이징 가능
   - 버그 수정 즉시 가능

3. **비용 효율성**
   - DataHub Cloud: $5,000+/월 vs Custom: 개발 시간만
   - 장기적으로 유리

**단점:**
1. **초기 개발 시간:** 2주 소요 (11월 11일 ~ 11월 27일)
2. **유지보수 부담:** 내부적으로 관리 필요
3. **리스크:** 검증되지 않은 솔루션

**의사결정:**
- CFO 요구사항(팀별 격리)이 최우선
- 데이터 거버넌스 없이는 사업 확장 불가
- 2주 투자로 장기적 문제 해결 → **진행 결정**

### 개발 타임라인

| 날짜 | 마일스톤 | 상태 |
|------|----------|------|
| 11/11 | 프로젝트 시작, 요구사항 정의 | ✅ |
| 11/13 | Airflow REST API v2 클라이언트 개발 | ✅ |
| 11/15 | Keycloak OIDC 인증 통합 | ✅ |
| 11/18 | Metadata DB 직접 쿼리 구현 | ✅ |
| 11/22 | v1.0.0 릴리스 (기본 기능) | ✅ |
| 11/26 | Cosmos DBT Outlet 추론 기능 추가 | ✅ |
| 11/27 | v1.2.0 릴리스 (DataProcessInstance, Domain Mapping) | ✅ |
| 11/29 | Prod 환경 배포 | ✅ |

## 비즈니스 성과

### Before (Airflow 2.x + 메타데이터 관리 없음)

**문제점:**
1. **데이터 소유권 불명확**
   - 300+ 테이블의 소유자가 누군지 모름
   - "이 테이블 누가 만들었어요?" → 1시간 추적

2. **팀 간 데이터 충돌**
   - Strategy팀이 HFT DAG 수정 사고
   - 권한 없는 사람이 critical 파이프라인 건드림

3. **데이터 추적성 상실**
   - S3 → Snowflake → DBT → Mart 흐름 파악 불가
   - 문제 발생 시 영향도 분석 어려움

4. **거버넌스 부재**
   - 데이터 품질 책임자 없음
   - 중복 데이터 생성 (같은 지표를 팀마다 다르게 계산)

### After (Airflow 3.x + Custom Connector)

**개선 효과:**

| 지표 | Before | After | 개선율 |
|------|--------|-------|--------|
| 데이터 소유자 파악 시간 | 1시간 | **5초** | **-99.8%** |
| 팀 간 권한 충돌 사고 | 월 1회 | **0회** | **-100%** |
| Lineage 추적 커버리지 | 0% | **85%** (300개 중 255개 DAG) | **+85%p** |
| 메타데이터 자동 수집 | 수동 | **자동** (매일 1회) | - |

**정성적 효과:**
1. **CFO 요구사항 충족**
   - 팀별 데이터 Domain 할당
   - Ownership 자동 추적
   - 감사(Audit) 가능

2. **데이터 거버넌스 기반 마련**
   - 데이터 품질 책임자 명확화
   - 중복 데이터 발견 및 제거 시작
   - 데이터 카탈로그 구축

3. **개발 생산성 향상**
   - 새로운 팀원: "이 테이블 어디서 왔어요?" → DataHub에서 즉시 확인
   - 데이터 문서화 자동화
   - 파이프라인 의존성 시각화

## 팀 반응

### 긍정적 피드백

**ML Platform 팀:**
> "이제 DAG lineage를 시각적으로 볼 수 있어서 디버깅이 훨씬 빨라졌습니다."

**Strategy 팀:**
> "DataHub에서 데이터 소유자를 바로 찾을 수 있어서 협업이 쉬워졌어요."

**CFO:**
> "팀별로 데이터가 어떻게 격리되어 있는지 한눈에 볼 수 있어서 좋습니다."

### 도전 과제

**초기 학습 곡선:**
- 팀원들이 DataHub 사용법 익히는 데 1주일 소요
- Domain, Tag, Owner 개념 이해 필요

**메타데이터 품질:**
- 초기에는 DAG description, tag가 부족
- 팀별로 메타데이터 작성 문화 정착 필요

**해결 방안:**
- DataHub 사용 가이드 작성
- 주간 회의에서 메타데이터 품질 리뷰
- DAG 작성 시 description, tags 필수화

## 향후 계획

### Phase 2: 메타데이터 품질 향상 (2025년 12월)

1. **자동 데이터 문서화**
   - DBT model에서 description 자동 추출
   - Column-level lineage 추가

2. **데이터 품질 모니터링**
   - Great Expectations 통합
   - 데이터 품질 메트릭 DataHub에 표시

3. **데이터 카탈로그 완성**
   - 모든 테이블에 Owner 할당
   - 팀별 Domain 100% 커버리지

### Phase 3: 고급 거버넌스 기능 (2026년 1분기)

1. **접근 제어 자동화**
   - DataHub Policy → Snowflake RBAC 자동 동기화
   - 데이터 접근 요청 워크플로우

2. **영향도 분석**
   - "이 테이블을 삭제하면 어떤 DAG가 영향받나요?"
   - 변경 전 자동 impact analysis

3. **데이터 디스커버리**
   - 자연어 검색 ("매출 관련 테이블 찾아줘")
   - ML 기반 추천 시스템

## 교훈

### 성공 요인

1. **명확한 비즈니스 목표**
   - CFO의 "팀별 데이터 격리" 요구사항이 명확
   - 기술 선택의 기준이 분명

2. **점진적 개발**
   - v1.0.0: 기본 기능만
   - v1.1.0: Domain Mapping 추가
   - v1.2.0: DataProcessInstance 추가
   - 단계별로 기능 추가하여 리스크 최소화

3. **내부 역량 활용**
   - 외부 솔루션에 의존하지 않고 직접 개발
   - 문제 발생 시 즉시 수정 가능

### 아쉬운 점

1. **초기 설계 부족**
   - Cosmos DBT Outlet 버그 (v1.0.1에서 수정)
   - 처음부터 더 꼼꼼하게 설계했어야 함

2. **문서화 부족**
   - 코드는 잘 작성했지만 사용 가이드 부족
   - 팀원들이 사용법 익히는 데 시간 소요

3. **테스트 커버리지**
   - Unit test 부족
   - 프로덕션에서 버그 발견

## 관련 문서

### Technology
- [[Airflow-3.0-구현]] - 기술 구현 상세
- [[DataHub-메타데이터-관리]] - DataHub 아키텍처
- [[Keycloak-OIDC-인증]] - 인증 시스템

### Projects
- [[Keycloak-SSO-도입-배경]] - SSO 도입 배경
- [[데이터-거버넌스-도입]] - 거버넌스 전략
- [[팀별-데이터-현황-파악]] - 현황 파악 프로젝트

---

**프로젝트 기간:** 2025년 11월 11일 ~ 11월 29일 (19일)  
**상태:** 완료 ✅  
**카테고리:** #Projects #Infrastructure #Airflow #DataGovernance  
**태그:** #크래프트테크놀로지스 #DataPlatform #Metadata
