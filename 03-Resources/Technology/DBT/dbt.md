---
title: DBT
type: resource
tags:
  - dbt
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---


---

## 📋 Qraft 적용 사례

DBT는 Qraft Data Platform의 데이터 변환 계층으로, Snowflake/Postgres 데이터 모델링 및 품질 관리를 담당합니다.

### 주요 적용 영역
- **4-Layer 아키텍처**: Raw → Stage → Intermediate → Mart
- **Incremental Materialization**: 대용량 데이터 효율적 처리
- **DataHub 통합**: 컬럼 레벨 리니지 자동 추적
- **Data Quality**: dbt test 기반 품질 검증

---

## 📎 Related

### Technology (상세 구현)
- [[DBT-구현]] - 4-Layer 아키텍처, Incremental materialization, Custom macros, DataHub 통합 등 DBT 실제 구현 내용

### 사용된 프로젝트 (Qraft)

**1. [[qraft-data-platform-통합프로젝트|Qraft Data Platform]]** (2025년 9월 확립)
   - **시기**: [[2025년-9월-29일|2025년 9월 29일]]
   - **역할**: Airflow + DBT 기반 데이터 변환 표준화
   - **성과**: Medallion Layer 체계화 (Raw → Stage → Mart)
   - **통합**: Snowflake, Postgres, DataHub Lineage

**2. [[MFT팀-배치-작업|MFT 배치 최적화]]** (2025년 10월)
   - **시기**: [[2025년-10월-13일|2025년 10월 13일]]
   - **역할**: DBT 모델 성능 최적화
   - **성과**: Incremental 전략으로 실행 시간 단축

**3. [[DataHub-커스텀-구현-상세|DataHub 통합]]** (2025년 11월)
   - **시기**: [[2025년-11월-24일|2025년 11월 24일]]
   - **역할**: DBT 메타데이터 자동 수집 (Custom Patches)
   - **기능**: 컬럼 레벨 리니지, Tag URL 인코딩 패치

### Knowledge

- [[Airflow|Airflow]] - DBT 실행 오케스트레이션
- [[DataHub|DataHub]] - 메타데이터 관리
- [[Snowflake]] - 주요 타겟 데이터 웨어하우스

### Insights

