---
title: Snowflake RBAC 가이드
type: resource
tags:
  - snowflake
  - rbac
  - access-control
  - security
  - role
  - permissions
  - domain
created: '2025-11-30'
updated: '2025-11-30'
aliases:
  - Snowflake Role-Based Access Control
status: evergreen
maturity: 3
---
# Snowflake RBAC 가이드

## 📌 개요

Snowflake의 Role-Based Access Control (RBAC)을 사용하여 데이터 권한을 관리하는 방법을 설명합니다.

## 🎓 핵심 개념

### RBAC (Role-Based Access Control)이란?

사용자에게 직접 권한을 부여하는 대신, **역할(Role)**에 권한을 부여하고 사용자를 역할에 할당하는 방식

**장점:**
- 중앙화된 권한 관리
- 역할 재사용 가능
- 사용자 추가/제거 시 개별 권한 수정 불필요
- 권한 변경 시 역할만 수정

### Snowflake Role 계층 구조

```
ACCOUNTADMIN (최상위)
    ├── SECURITYADMIN (보안 관리)
    │   └── USERADMIN (사용자/역할 관리)
    └── SYSADMIN (시스템 관리)
        └── Custom Roles (커스텀 역할)
            └── PUBLIC (기본 역할)
```

**내장 역할:**
- `ACCOUNTADMIN`: 모든 권한 (계정 관리)
- `SECURITYADMIN`: 권한 및 역할 관리
- `USERADMIN`: 사용자 및 역할 생성
- `SYSADMIN`: 웨어하우스, 데이터베이스, 스키마 관리
- `PUBLIC`: 모든 사용자가 기본으로 보유

---

## 🏗️ Domain-Based RBAC 아키텍처

### 전체 구조

```
qraft_origin Database
├── core Schema (PUBLIC 접근)
│   ├── dim_holiday
│   ├── dim_ticker
│   └── dim_ticker_manually
│
├── zeroin Schema (role_zeroin_user)
│   └── All Tables (SELECT, INSERT, UPDATE, DELETE)
│
├── slickcharts Schema (role_index_domain)
│   ├── nasdaq100
│   └── sp500
│
├── invesco Schema (role_index_domain)
│   └── qqq
│
├── barra Schema (role_barra_domain)
│   └── All Tables (SELECT)
│
├── staging/intermediate/mart Schemas
│   ├── us_simul_data (role_us_simul_domain)
│   └── port_const (role_portfolio_domain)
```

### Domain Role 설계 원칙

1. **도메인별 역할 분리**
   - `role_index_domain`: 인덱스 구성 데이터
   - `role_us_simul_domain`: 미국 시뮬레이션 데이터
   - `role_portfolio_domain`: 포트폴리오 리밸런싱 데이터
   - `role_barra_domain`: BARRA 리스크 모델 데이터

2. **최소 권한 원칙**
   - 각 도메인은 필요한 스키마/테이블만 접근
   - 기본적으로 SELECT만 부여
   - 수정 권한(INSERT/UPDATE/DELETE)은 필요한 경우만

3. **계층적 권한**
   - Database USAGE → Schema USAGE → Table SELECT 순서
   - 상위 권한 없으면 하위 객체 접근 불가

---

## 💻 RBAC 구현 패턴

### 1. PUBLIC 접근 (Core 데이터)

**용도:** 모든 사용자가 접근해야 하는 공통 마스터 데이터

```sql
GRANT USAGE ON SCHEMA qraft_origin.core TO PUBLIC;
GRANT SELECT ON TABLE qraft_origin.core.dim_holiday TO PUBLIC;
GRANT SELECT ON TABLE qraft_origin.core.dim_ticker TO PUBLIC;
GRANT SELECT ON TABLE qraft_origin.core.dim_ticker_manually TO PUBLIC;

-- 향후 추가되는 테이블도 자동 허용
GRANT SELECT ON FUTURE TABLES IN SCHEMA qraft_origin.core TO PUBLIC;
```

**특징:**
- `PUBLIC`: 모든 사용자가 기본 보유
- `FUTURE TABLES`: 나중에 생성되는 테이블도 자동 권한 부여

### 2. 별도 Role 생성 (Zeroin 데이터)

**용도:** 특정 팀/프로젝트만 접근, 수정 권한 필요

```sql
-- 1. Role 생성
CREATE ROLE IF NOT EXISTS role_zeroin_user;

-- 2. Database & Schema 접근 권한
GRANT USAGE ON DATABASE qraft_origin TO ROLE role_zeroin_user;
GRANT USAGE ON SCHEMA qraft_origin.zeroin TO ROLE role_zeroin_user;

-- 3. 기존 테이블 권한
GRANT SELECT ON ALL TABLES IN SCHEMA qraft_origin.zeroin TO ROLE role_zeroin_user;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA qraft_origin.zeroin TO ROLE role_zeroin_user;

-- 4. 향후 테이블 권한
GRANT SELECT ON FUTURE TABLES IN SCHEMA qraft_origin.zeroin TO ROLE role_zeroin_user;
GRANT INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA qraft_origin.zeroin TO ROLE role_zeroin_user;
```

**특징:**
- 읽기 + 쓰기 권한 모두 부여
- `FUTURE TABLES`로 스키마 확장 시 자동 권한 부여

### 3. Domain Group (INDEX)

**용도:** 여러 스키마에 걸친 도메인 데이터 접근

```sql
-- 1. Role 생성
CREATE ROLE IF NOT EXISTS role_index_domain;

-- 2. Database 접근
GRANT USAGE ON DATABASE qraft_origin TO ROLE role_index_domain;

-- 3. 여러 스키마 접근
GRANT USAGE ON SCHEMA qraft_origin.slickcharts TO ROLE role_index_domain;
GRANT USAGE ON SCHEMA qraft_origin.invesco TO ROLE role_index_domain;
GRANT USAGE ON SCHEMA qraft_origin.mart TO ROLE role_index_domain;

-- 4. 특정 테이블만 접근 (세밀한 제어)
GRANT SELECT ON TABLE qraft_origin.slickcharts.nasdaq100 TO ROLE role_index_domain;
GRANT SELECT ON TABLE qraft_origin.slickcharts.nasdaq100_temp TO ROLE role_index_domain;
GRANT SELECT ON TABLE qraft_origin.slickcharts.sp500 TO ROLE role_index_domain;
GRANT SELECT ON TABLE qraft_origin.slickcharts.sp500_temp TO ROLE role_index_domain;
GRANT SELECT ON TABLE qraft_origin.invesco.qqq TO ROLE role_index_domain;
GRANT SELECT ON TABLE qraft_origin.invesco.qqq_temp TO ROLE role_index_domain;
GRANT SELECT ON TABLE qraft_origin.mart.index_const TO ROLE role_index_domain;
```

**특징:**
- 여러 스키마에 분산된 관련 데이터 접근
- 테이블 단위 세밀한 제어
- 읽기 전용 (SELECT만)

### 4. Domain Group (US_SIMULATION_DATA)

**용도:** 데이터 파이프라인의 여러 레이어 접근 (staging → intermediate → mart)

```sql
CREATE ROLE IF NOT EXISTS role_us_simul_domain;

GRANT USAGE ON DATABASE qraft_origin TO ROLE role_us_simul_domain;
GRANT USAGE ON SCHEMA qraft_origin.staging TO ROLE role_us_simul_domain;
GRANT USAGE ON SCHEMA qraft_origin.intermediate TO ROLE role_us_simul_domain;
GRANT USAGE ON SCHEMA qraft_origin.mart TO ROLE role_us_simul_domain;

-- Staging layer
GRANT SELECT ON TABLE qraft_origin.staging.stg_csvsecuritymapping TO ROLE role_us_simul_domain;
GRANT SELECT ON TABLE qraft_origin.staging.stg_us_sec_meta_base TO ROLE role_us_simul_domain;
GRANT SELECT ON TABLE qraft_origin.staging.stg_us_sec_price_metrics TO ROLE role_us_simul_domain;
GRANT SELECT ON TABLE qraft_origin.staging.us_sec_meta_base TO ROLE role_us_simul_domain;
GRANT SELECT ON TABLE qraft_origin.staging.us_sec_price_metrics TO ROLE role_us_simul_domain;

-- Intermediate layer
GRANT SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_base TO ROLE role_us_simul_domain;
GRANT SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_mrkcap TO ROLE role_us_simul_domain;
GRANT SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_rolling TO ROLE role_us_simul_domain;
GRANT SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_short_int TO ROLE role_us_simul_domain;

-- Mart layer
GRANT SELECT ON TABLE qraft_origin.mart.us_simul_data TO ROLE role_us_simul_domain;
GRANT SELECT ON TABLE qraft_origin.mart.us_sec_meta TO ROLE role_us_simul_domain;
GRANT SELECT ON TABLE qraft_origin.mart.index_const TO ROLE role_us_simul_domain;
```

**특징:**
- 데이터 파이프라인의 모든 레이어 접근
- 도메인별 데이터 흐름 추적 가능
- 읽기 전용 (분석용)

---

## 🔧 사용자 및 권한 관리

### 사용자 생성

```sql
CREATE USER "inyeol.choi"
  PASSWORD = 'Temp123412341234@'  -- 임시 비밀번호
  DEFAULT_ROLE = public
  MUST_CHANGE_PASSWORD = TRUE  -- 첫 로그인 시 비밀번호 변경 강제
  COMMENT = 'inyeol.choi 계정';
```

### 사용자에게 Role 부여

```sql
-- Role 부여
GRANT ROLE role_index_domain TO USER "inyeol.choi";

-- 기본 Role 설정
ALTER USER "inyeol.choi" SET DEFAULT_ROLE = role_index_domain;
```

### 비밀번호 재설정

```sql
ALTER USER "dongyeon.park" 
SET PASSWORD = 'Temp123412341234@' 
MUST_CHANGE_PASSWORD = TRUE;
```

### 사용자 Role 확인

```sql
-- 특정 사용자의 Role 조회
SELECT ROLE
FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_USERS
WHERE GRANTEE_NAME = 'inyeol.choi';

-- 현재 활성 Role 확인
SELECT CURRENT_ROLE();

-- 모든 Role 조회
SHOW ROLES;
```

---

## 🛠️ 유지보수

### Role 권한 회수

```sql
-- 특정 테이블 권한 회수
REVOKE SELECT ON TABLE qraft_origin.mart.us_simul_data FROM ROLE role_us_simul_domain;

-- 스키마 전체 권한 회수
REVOKE SELECT ON ALL TABLES IN SCHEMA qraft_origin.zeroin FROM ROLE role_zeroin_user;

-- 사용자로부터 Role 회수
REVOKE ROLE role_index_domain FROM USER "inyeol.choi";
```

### Role 삭제

```sql
-- Role 삭제 (권한 먼저 회수 필요)
DROP ROLE IF EXISTS role_index_domain;
```

---

## 📊 Domain Role 설계 예시

### qraft_origin Database RBAC

| Domain | Role | Schemas | 권한 | 사용자 |
|--------|------|---------|------|--------|
| Core | PUBLIC | core | SELECT | 모든 사용자 |
| Zeroin | role_zeroin_user | zeroin | SELECT, INSERT, UPDATE, DELETE | Zeroin 팀 |
| Index | role_index_domain | slickcharts, invesco, mart | SELECT | 인덱스 운용팀 |
| US Simulation | role_us_simul_domain | staging, intermediate, mart | SELECT | 시뮬레이션팀 |
| Portfolio | role_portfolio_domain | staging, intermediate, mart | SELECT | 포트폴리오팀 |
| BARRA | role_barra_domain | barra | SELECT | 리스크팀 |

---

## 🔐 보안 모범 사례

### 1. 최소 권한 원칙

```sql
-- ❌ Bad: Schema 전체 권한
GRANT SELECT ON ALL TABLES IN SCHEMA qraft_origin.mart TO ROLE my_role;

-- ✅ Good: 필요한 테이블만
GRANT SELECT ON TABLE qraft_origin.mart.us_simul_data TO ROLE my_role;
GRANT SELECT ON TABLE qraft_origin.mart.us_sec_meta TO ROLE my_role;
```

### 2. FUTURE 권한 활용

```sql
-- 새로 생성되는 테이블도 자동 권한 부여
GRANT SELECT ON FUTURE TABLES IN SCHEMA qraft_origin.core TO PUBLIC;
```

### 3. 역할 계층화

```sql
-- Admin Role 생성
CREATE ROLE role_data_admin;
GRANT ROLE role_index_domain TO ROLE role_data_admin;
GRANT ROLE role_us_simul_domain TO ROLE role_data_admin;
GRANT ROLE role_portfolio_domain TO ROLE role_data_admin;

-- 사용자에게 Admin Role 부여
GRANT ROLE role_data_admin TO USER "admin.user";
```

### 4. Alembic으로 버전 관리

**장점:**
- 권한 변경 이력 추적
- Rollback 가능
- Code Review 가능
- CI/CD 통합 가능

**예시:** [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/Snowflake-권한-마이그레이션|Snowflake 권한 마이그레이션]] 참조

---

## 📎 Related

### Projects 배경 (Why)
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/Snowflake-권한-마이그레이션|Snowflake-권한-마이그레이션]] - Alembic 기반 RBAC 구현

### Technology (Core Concepts)
- [[Snowflake]] - Snowflake 기본 개념 및 Qraft 적용 사례

### Technology (Related Implementation)
- [[Snowflake-Storage-Integration]] - S3 연결 및 Stage 권한 관리
- [[DBT-구현]] - DBT 프로젝트와 Snowflake RBAC 통합
- [[Keycloak-Airflow-인증-개념]] - Airflow의 RBAC 개념 (비교 참고)

### Projects (실제 사용)
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/팀별-데이터-격리-체계|팀별-데이터-격리-체계]] - 팀별 권한 격리 전략
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/데이터-거버넌스-전략-수립|데이터-거버넌스-전략-수립]] - 거버넌스 전략

---

**Metadata:**
