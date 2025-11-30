---
title: Airflow
type: resource
tags:
  - airflow
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---


---

## 📋 Qraft 적용 사례

Airflow는 Qraft Data Platform의 핵심 워크플로우 엔진으로, 2025년 8월부터 전사 데이터 파이프라인을 관리하고 있습니다.

### 주요 적용 영역
- **ETL 파이프라인 오케스트레이션**: Snowflake, Postgres 데이터 적재 및 변환
- **DBT 실행 관리**: dbt 모델 실행 스케줄링
- **DataHub 메타데이터 수집**: 리니지 추적 자동화
- **팀별 DAG 격리**: Keycloak 기반 권한 관리

---

## 📎 Related

### 사용된 프로젝트 (Qraft)

**1. [[qraft-data-platform-통합프로젝트|Qraft Data Platform]]** (2025년 9월 확립)
   - **시기**: [[2025년-9월-29일|2025년 9월 29일]]
   - **역할**: Airflow + DBT 기반 ETL 파이프라인 표준화
   - **성과**: 데이터 문의·단순작업 40% 감소
   - **통합**: Snowflake, Postgres, GitLab CI/CD

**2. [[MFT팀-배치-작업|MFT 배치 최적화]]** (2025년 10월)
   - **시기**: [[2025년-10월-13일|2025년 10월 13일]]
   - **역할**: DAG 성능 최적화 (pyarrow.dataset, sqlparse 검증)
   - **성과**: DAG 평균 실행 시간 40% 단축
   - **기술**: Airflow Hook 기반 WHERE 조건 자동 검증

**3. [[airflow-3.0,-dbt-local-test|Airflow 3.1.3 적용]]** (2025년 11월)
   - **시기**: [[2025년-11월-17일|2025년 11월 17일]]
   - **역할**: Airflow 3.0 → 3.1.3 버전 업그레이드
   - **성과**: 레포 분리, 환경별 이미지 빌드 자동화
   - **테스트**: 2개월 로컬 테스트 (9/16~11/17)

**4. [[dag권한-관리|DAG 권한 관리]]** (2025년 11월)
   - **시기**: [[2025년-11월-10일|2025년 11월 10일]]
   - **역할**: Keycloak 기반 팀별 DAG 격리
   - **목적**: 팀별 데이터 프로세싱 보안 강화

**5. [[DataHub-커스텀-구현-상세|DataHub 통합]]** (2025년 11월)
   - **시기**: [[2025년-11월-24일|2025년 11월 24일]]
   - **역할**: Airflow 메타데이터 자동 수집 (Custom Source)
   - **기능**: DAG, Task 리니지 추적

### Knowledge

- [[airflow-3.0|Airflow 3.0 변경사항]]
- [[DBT|DBT]] - 함께 사용되는 변환 도구
- [[DataHub|DataHub]] - 메타데이터 관리
- [[Keycloak]] - 인증 통합

### Insights

