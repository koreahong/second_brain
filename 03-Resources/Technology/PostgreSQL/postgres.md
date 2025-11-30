---
title: postgres
type: resource
tags:
  - technology
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---


---

## 📋 Qraft 적용 사례

PostgreSQL은 Qraft에서 메타데이터 저장소, 운영 데이터베이스, 소규모 데이터 마트로 활용됩니다.

### 주요 적용 영역
- **메타데이터 저장**: Airflow, DataHub 메타데이터
- **마스터 데이터**: Employee Master, 권한 관리
- **운영 DB**: 내부 도구 및 서비스 데이터
- **데이터 마트**: Snowflake 비용 절감을 위한 경량 데이터

---

## 📎 Related

### 사용된 프로젝트 (Qraft)

**1. [[qraft-data-platform-통합프로젝트|Qraft Data Platform]]** (2025년 9월)
   - **시기**: [[2025년-9월-29일|2025년 9월 29일]]
   - **역할**: Airflow + DBT 기반 파이프라인 통합 (Snowflake, Postgres)
   - **용도**: 소규모 데이터 마트, 메타데이터 저장

**2. [[MFT팀-배치-작업|MFT 배치 최적화]]** (2025년 10월)
   - **시기**: [[2025년-10월-13일|2025년 10월 13일]]
   - **역할**: Postgres WHERE 조건 필수 검증 (sqlparse)
   - **성과**: Full Scan 방지로 쿼리 성능 개선
   - **기술**: sqlparse 기반 WHERE 절 검증 Hook

**3. [[jira,-keycloak-권한-자동화|Keycloak 권한 자동화]]** (2025년 11월)
   - **시기**: [[2025년-11월-03일|2025년 11월 3일]]
   - **역할**: Employee Master 테이블 저장소
   - **스키마**: 사번, 조직, 직책, 입사일, 퇴사일 등
   - **기술**: Alembic 스키마 관리

### Knowledge

- [[Airflow|Airflow]] - Postgres 메타데이터 저장
- [[DataHub|DataHub]] - Postgres 메타데이터 저장
- [[Snowflake]] - Postgres와 함께 사용되는 DW

### Insights

