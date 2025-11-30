---
title: Snowflake
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

Snowflake는 Qraft의 중앙 데이터 웨어하우스로, 전사 데이터 저장 및 분석을 담당합니다.

### 주요 적용 영역
- **중앙 DW**: Raw, Stage, Mart 계층 데이터 저장
- **DBT 타겟**: 데이터 변환 및 모델링
- **BI/Analytics**: Tableau, Python 분석 도구 연동
- **비용 관리**: 저장소 최적화, 사용량 모니터링

### 주요 이슈
- **비용 급증** (2025년 9월): 무분별한 데이터 적재로 연간 2억 비용 낭비 발견
- **Postgres 회귀**: 일부 데이터를 Postgres/NAS로 이전
- **조직 갈등** (2025년 11월): 팀별 비용 분담 논쟁 발생

---

## 📎 Related

### 사용된 프로젝트 (Qraft)

**1. [[팀별-원천-데이터-계약현황-파악|데이터 계약 현황 파악]]** (2025년 9월)
   - **시기**: [[2025년-9월-22일|2025년 9월 22일]]
   - **문제**: Snowflake 비용 급증, 연간 약 2억 불필요 과금 발견
   - **원인**: 거버넌스 부재, 중복 데이터 적재, 사용하지 않는 데이터 방치
   - **대응**: 데이터 사용 현황 전수 조사 시작

**2. [[qraft-data-platform-통합프로젝트|Qraft Data Platform]]** (2025년 9월)
   - **시기**: [[2025년-9월-29일|2025년 9월 29일]]
   - **역할**: Airflow + DBT 기반 Snowflake 데이터 관리 체계화
   - **성과**: Medallion Layer 구조화 (Raw → Stage → Mart)
   - **통합**: DataHub로 Snowflake 메타데이터 자동 수집

**3. [[MFT팀-배치-작업|Snowflake 저장소 정리]]** (2025년 10월)
   - **시기**: [[2025년-10월-13일|2025년 10월 13일]]
   - **작업**: 90일 미사용 테이블 식별 및 아카이브
   - **성과**: 저장소 용량 약 35% 절감
   - **기술**: DataHub Tag로 메타데이터 반영 (last_accessed, storage_bytes)

**4. Snowflake 조직 갈등** (2025년 11월)
   - **시기**: [[2025년-11월-10일|2025년 11월 10일]]
   - **사건**: ATS 조직장 "우리는 infra팀 도움 안 받으니 판관비 알아서 부담"
   - **문제**: 경영진/조직장 간 거버넌스 컨센서스 부재
   - **결과**: 조직 체계 붕괴, 감정 싸움 발생

### Knowledge

- [[Airflow|Airflow]] - Snowflake 데이터 적재 오케스트레이션
- [[DBT|DBT]] - Snowflake 데이터 변환
- [[DataHub|DataHub]] - Snowflake 메타데이터 관리
- [[PostgreSQL|PostgreSQL]] - Snowflake 비용 절감을 위한 대안

### Insights

