---
title: Snowflake 권한 마이그레이션
date: '2025-10-10'
type: project
status: evergreen
tags:
  - snowflake
  - rbac
  - alembic
  - migration
  - access-control
  - qraft_origin
created: '2025-11-30'
updated: '2025-11-30'
aliases:
  - Snowflake RBAC Migration
maturity: 3
---
# Snowflake 권한 마이그레이션

## 📌 개요

`qraft_origin` 데이터베이스의 RBAC(Role-Based Access Control) 권한을 Alembic 마이그레이션으로 관리하는 프로젝트

**목적:**
- 권한 변경 이력 추적
- Code Review 가능
- Rollback 가능
- CI/CD 통합

---

## 🎯 Domain Role 구조

### 전체 Role

| Role | 접근 스키마 | 권한 | 용도 |
|------|------------|------|------|
| PUBLIC | core | SELECT | 공통 마스터 데이터 (모든 사용자) |
| role_zeroin_user | zeroin | SELECT, INSERT, UPDATE, DELETE | Zeroin 팀 (읽기/쓰기) |
| role_index_domain | slickcharts, invesco, mart | SELECT | 인덱스 구성 데이터 |
| role_us_simul_domain | staging, intermediate, mart | SELECT | 미국 시뮬레이션 데이터 |
| role_portfolio_domain | staging, intermediate, mart | SELECT | 포트폴리오 리밸런싱 |
| role_barra_domain | barra | SELECT | BARRA 리스크 모델 |

---

## 💻 Alembic Migration 코드

### Revision 정보

```python
"""Setup Snowflake RBAC for qraft_origin database

Revision ID: a7c3f8d29e41
Revises: b40f0d315567
Create Date: 2025-11-06 19:06:14.000000
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "a7c3f8d29e41"
down_revision: Union[str, Sequence[str], None] = "b40f0d315567"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
```

### Helper 함수

```python
def execute_statements(statements: list[str]) -> None:
    """Execute multiple SQL statements individually for Snowflake."""
    for stmt in statements:
        stmt = stmt.strip()
        if stmt and not stmt.startswith("--"):
            op.execute(stmt)
```

**특징:**
- Snowflake는 단일 `op.execute()`에 여러 문장 실행 불가
- 주석(--) 제외하고 각 문장 개별 실행

---

## 🔼 Upgrade (권한 부여)

### 1. PUBLIC ACCESS: CORE 스키마

```python
def upgrade() -> None:
    """Setup RBAC permissions for Snowflake."""

    # ============================================================================
    # 1. PUBLIC ACCESS: CORE 스키마 (전체 오픈)
    # ============================================================================
    execute_statements(
        [
            "USE DATABASE qraft_origin",
            "USE SCHEMA core",
            "GRANT USAGE ON SCHEMA qraft_origin.core TO PUBLIC",
            "GRANT SELECT ON TABLE qraft_origin.core.dim_holiday TO PUBLIC",
            "GRANT SELECT ON TABLE qraft_origin.core.dim_ticker TO PUBLIC",
            "GRANT SELECT ON TABLE qraft_origin.core.dim_ticker_manually TO PUBLIC",
            "GRANT SELECT ON FUTURE TABLES IN SCHEMA qraft_origin.core TO PUBLIC",
        ]
    )
```

**목적:**
- 공통 마스터 데이터 (휴일, 종목코드)
- 모든 사용자 접근 가능

### 2. ZEROIN 스키마

```python
    # ============================================================================
    # 2. ZEROIN 스키마 (별도 Role 생성 및 관리)
    # ============================================================================
    execute_statements(
        [
            "CREATE ROLE IF NOT EXISTS role_zeroin_user",
            "GRANT USAGE ON DATABASE qraft_origin TO ROLE role_zeroin_user",
            "GRANT USAGE ON SCHEMA qraft_origin.zeroin TO ROLE role_zeroin_user",
            "GRANT SELECT ON ALL TABLES IN SCHEMA qraft_origin.zeroin TO ROLE role_zeroin_user",
            "GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA qraft_origin.zeroin TO ROLE role_zeroin_user",
            "GRANT SELECT ON FUTURE TABLES IN SCHEMA qraft_origin.zeroin TO ROLE role_zeroin_user",
            "GRANT INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA qraft_origin.zeroin TO ROLE role_zeroin_user",
        ]
    )
```

**특징:**
- 읽기 + 쓰기 권한
- FUTURE TABLES로 자동 권한 부여

### 3. DOMAIN GROUP: INDEX

```python
    # ============================================================================
    # 3. DOMAIN GROUP: INDEX
    # ============================================================================
    execute_statements(
        [
            "CREATE ROLE IF NOT EXISTS role_index_domain",
            "GRANT USAGE ON DATABASE qraft_origin TO ROLE role_index_domain",
            "GRANT USAGE ON SCHEMA qraft_origin.slickcharts TO ROLE role_index_domain",
            "GRANT USAGE ON SCHEMA qraft_origin.invesco TO ROLE role_index_domain",
            "GRANT USAGE ON SCHEMA qraft_origin.mart TO ROLE role_index_domain",
            "GRANT SELECT ON TABLE qraft_origin.slickcharts.nasdaq100 TO ROLE role_index_domain",
            "GRANT SELECT ON TABLE qraft_origin.slickcharts.nasdaq100_temp TO ROLE role_index_domain",
            "GRANT SELECT ON TABLE qraft_origin.slickcharts.sp500 TO ROLE role_index_domain",
            "GRANT SELECT ON TABLE qraft_origin.slickcharts.sp500_temp TO ROLE role_index_domain",
            "GRANT SELECT ON TABLE qraft_origin.invesco.qqq TO ROLE role_index_domain",
            "GRANT SELECT ON TABLE qraft_origin.invesco.qqq_temp TO ROLE role_index_domain",
            "GRANT SELECT ON TABLE qraft_origin.mart.index_const TO ROLE role_index_domain",
        ]
    )
```

**포함 데이터:**
- slickcharts: NASDAQ100, S&P500 지수 구성
- invesco: QQQ ETF 구성
- mart.index_const: 통합 인덱스 구성

### 4. DOMAIN GROUP: US_SIMULATION_DATA

```python
    # ============================================================================
    # 4. DOMAIN GROUP: US_SIMULATION_DATA
    # ============================================================================
    execute_statements(
        [
            "CREATE ROLE IF NOT EXISTS role_us_simul_domain",
            "GRANT USAGE ON DATABASE qraft_origin TO ROLE role_us_simul_domain",
            "GRANT USAGE ON SCHEMA qraft_origin.staging TO ROLE role_us_simul_domain",
            "GRANT USAGE ON SCHEMA qraft_origin.intermediate TO ROLE role_us_simul_domain",
            "GRANT USAGE ON SCHEMA qraft_origin.mart TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.staging.stg_csvsecuritymapping TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.staging.stg_us_sec_meta_base TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.staging.stg_us_sec_price_metrics TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.staging.us_sec_meta_base TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.staging.us_sec_price_metrics TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_base TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_mrkcap TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_rolling TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_short_int TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.mart.us_simul_data TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.mart.us_sec_meta TO ROLE role_us_simul_domain",
            "GRANT SELECT ON TABLE qraft_origin.mart.index_const TO ROLE role_us_simul_domain",
        ]
    )
```

**데이터 파이프라인:**
- staging: Raw 데이터
- intermediate: 중간 처리 데이터
- mart: 최종 분석 데이터

### 5. DOMAIN GROUP: PORTFOLIO_REBALANCING

```python
    # ============================================================================
    # 5. DOMAIN GROUP: PORTFOLIO_REBALANCING
    # ============================================================================
    execute_statements(
        [
            "CREATE ROLE IF NOT EXISTS role_portfolio_domain",
            "GRANT USAGE ON DATABASE qraft_origin TO ROLE role_portfolio_domain",
            "GRANT USAGE ON SCHEMA qraft_origin.staging TO ROLE role_portfolio_domain",
            "GRANT USAGE ON SCHEMA qraft_origin.intermediate TO ROLE role_portfolio_domain",
            "GRANT USAGE ON SCHEMA qraft_origin.mart TO ROLE role_portfolio_domain",
            "GRANT SELECT ON TABLE qraft_origin.staging.port_const TO ROLE role_portfolio_domain",
            "GRANT SELECT ON TABLE qraft_origin.staging.port_const_from_s3 TO ROLE role_portfolio_domain",
            "GRANT SELECT ON TABLE qraft_origin.staging.prop_l_dbht_fmff_fulltwo_from_s3 TO ROLE role_portfolio_domain",
            "GRANT SELECT ON TABLE qraft_origin.intermediate.int_port_const TO ROLE role_portfolio_domain",
            "GRANT SELECT ON TABLE qraft_origin.mart.port_const TO ROLE role_portfolio_domain",
            "GRANT SELECT ON TABLE qraft_origin.mart.port_index TO ROLE role_portfolio_domain",
            "GRANT SELECT ON TABLE qraft_origin.mart.port_meta TO ROLE role_portfolio_domain",
            "GRANT SELECT ON TABLE qraft_origin.mart.us_simul_data TO ROLE role_portfolio_domain",
        ]
    )
```

**포트폴리오 데이터:**
- port_const: 포트폴리오 구성
- port_meta: 포트폴리오 메타데이터
- port_index: 포트폴리오 인덱스 정보

### 6. DOMAIN GROUP: BARRA

```python
    # ============================================================================
    # 6. DOMAIN GROUP: BARRA (Risk Model Team)
    # ============================================================================
    execute_statements(
        [
            "CREATE ROLE IF NOT EXISTS role_barra_domain",
            "GRANT USAGE ON DATABASE qraft_origin TO ROLE role_barra_domain",
            "GRANT USAGE ON SCHEMA qraft_origin.barra TO ROLE role_barra_domain",
            "GRANT SELECT ON ALL TABLES IN SCHEMA qraft_origin.barra TO ROLE role_barra_domain",
            "GRANT SELECT ON FUTURE TABLES IN SCHEMA qraft_origin.barra TO ROLE role_barra_domain",
        ]
    )
```

**BARRA 리스크 모델:**
- 전체 스키마 접근
- FUTURE TABLES로 자동 권한 부여

---

## 🔽 Downgrade (권한 회수)

### Rollback 순서

```python
def downgrade() -> None:
    """Remove RBAC permissions and roles."""

    # BARRA (역순으로 회수)
    execute_statements(
        [
            "REVOKE SELECT ON ALL TABLES IN SCHEMA qraft_origin.barra FROM ROLE role_barra_domain",
            "DROP ROLE IF EXISTS role_barra_domain",
        ]
    )

    # PORTFOLIO
    execute_statements(
        [
            "REVOKE SELECT ON TABLE qraft_origin.mart.us_simul_data FROM ROLE role_portfolio_domain",
            "REVOKE SELECT ON TABLE qraft_origin.mart.port_meta FROM ROLE role_portfolio_domain",
            "REVOKE SELECT ON TABLE qraft_origin.mart.port_index FROM ROLE role_portfolio_domain",
            "REVOKE SELECT ON TABLE qraft_origin.mart.port_const FROM ROLE role_portfolio_domain",
            "REVOKE SELECT ON TABLE qraft_origin.intermediate.int_port_const FROM ROLE role_portfolio_domain",
            "REVOKE SELECT ON TABLE qraft_origin.staging.prop_l_dbht_fmff_fulltwo_from_s3 FROM ROLE role_portfolio_domain",
            "REVOKE SELECT ON TABLE qraft_origin.staging.port_const_from_s3 FROM ROLE role_portfolio_domain",
            "REVOKE SELECT ON TABLE qraft_origin.staging.port_const FROM ROLE role_portfolio_domain",
            "DROP ROLE IF EXISTS role_portfolio_domain",
        ]
    )

    # US_SIMUL
    execute_statements(
        [
            "REVOKE SELECT ON TABLE qraft_origin.mart.index_const FROM ROLE role_us_simul_domain",
            "REVOKE SELECT ON TABLE qraft_origin.mart.us_sec_meta FROM ROLE role_us_simul_domain",
            "REVOKE SELECT ON TABLE qraft_origin.mart.us_simul_data FROM ROLE role_us_simul_domain",
            "REVOKE SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_short_int FROM ROLE role_us_simul_domain",
            "REVOKE SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_rolling FROM ROLE role_us_simul_domain",
            "REVOKE SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_mrkcap FROM ROLE role_us_simul_domain",
            "REVOKE SELECT ON TABLE qraft_origin.intermediate.int_us_simul_data_base FROM ROLE role_us_simul_domain",
            "REVOKE SELECT ON TABLE qraft_origin.staging.us_sec_price_metrics FROM ROLE role_us_simul_domain",
            "REVOKE SELECT ON TABLE qraft_origin.staging.us_sec_meta_base FROM ROLE role_us_simul_domain",
            "REVOKE SELECT ON TABLE qraft_origin.staging.stg_us_sec_price_metrics FROM ROLE role_us_simul_domain",
            "REVOKE SELECT ON TABLE qraft_origin.staging.stg_us_sec_meta_base FROM ROLE role_us_simul_domain",
            "REVOKE SELECT ON TABLE qraft_origin.staging.stg_csvsecuritymapping FROM ROLE role_us_simul_domain",
            "DROP ROLE IF EXISTS role_us_simul_domain",
        ]
    )

    # INDEX
    execute_statements(
        [
            "REVOKE SELECT ON TABLE qraft_origin.mart.index_const FROM ROLE role_index_domain",
            "REVOKE SELECT ON TABLE qraft_origin.invesco.qqq_temp FROM ROLE role_index_domain",
            "REVOKE SELECT ON TABLE qraft_origin.invesco.qqq FROM ROLE role_index_domain",
            "REVOKE SELECT ON TABLE qraft_origin.slickcharts.sp500_temp FROM ROLE role_index_domain",
            "REVOKE SELECT ON TABLE qraft_origin.slickcharts.sp500 FROM ROLE role_index_domain",
            "REVOKE SELECT ON TABLE qraft_origin.slickcharts.nasdaq100_temp FROM ROLE role_index_domain",
            "REVOKE SELECT ON TABLE qraft_origin.slickcharts.nasdaq100 FROM ROLE role_index_domain",
            "DROP ROLE IF EXISTS role_index_domain",
        ]
    )

    # ZEROIN
    execute_statements(
        [
            "REVOKE INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA qraft_origin.zeroin FROM ROLE role_zeroin_user",
            "REVOKE SELECT ON ALL TABLES IN SCHEMA qraft_origin.zeroin FROM ROLE role_zeroin_user",
            "DROP ROLE IF EXISTS role_zeroin_user",
        ]
    )

    # PUBLIC ACCESS: CORE
    execute_statements(
        [
            "REVOKE SELECT ON TABLE qraft_origin.core.dim_ticker_manually FROM PUBLIC",
            "REVOKE SELECT ON TABLE qraft_origin.core.dim_ticker FROM PUBLIC",
            "REVOKE SELECT ON TABLE qraft_origin.core.dim_holiday FROM PUBLIC",
        ]
    )
```

**주의:**
- Role 삭제 전 권한 먼저 회수
- 생성의 역순으로 삭제

---

## 🚀 사용 방법

### Migration 적용

```bash
# Upgrade (권한 부여)
alembic upgrade a7c3f8d29e41

# 또는 최신 버전으로
alembic upgrade head
```

### Rollback

```bash
# 이전 버전으로 Downgrade
alembic downgrade b40f0d315567

# 또는 1단계 Rollback
alembic downgrade -1
```

### Migration 이력 확인

```bash
# 현재 버전 확인
alembic current

# 이력 조회
alembic history
```

---

## 📊 적용 결과

### 생성된 Role

```sql
SHOW ROLES LIKE 'role_%';
```

**출력:**
- role_zeroin_user
- role_index_domain
- role_us_simul_domain
- role_portfolio_domain
- role_barra_domain

### 권한 확인

```sql
-- 특정 Role의 권한 조회
SHOW GRANTS TO ROLE role_index_domain;

-- 특정 테이블의 권한 조회
SHOW GRANTS ON TABLE qraft_origin.mart.us_simul_data;
```

---

## 📎 Related

### Technology (Concepts & Patterns)
- [[03-Resources/Technology/Snowflake/Snowflake-RBAC-가이드|Snowflake RBAC 가이드]] - RBAC 개념 및 패턴 **이 마이그레이션이 어떤 원칙을 따르는지**
- [[03-Resources/Technology/Snowflake/Snowflake-Storage-Integration|Snowflake Storage Integration]] - Storage Integration 권한 관리

### Related Projects
- [[원천-데이터-적재-파이프라인-개발]] - 데이터 파이프라인 인프라
- [[jira,-keycloak-권한-자동화]] - 통합 권한 관리 자동화

### Knowledge
- [[03-Resources/Data-Governance/Access-Control/data-권한|Data 권한]] - 전체 데이터 거버넌스 체계

---

**Metadata:**
