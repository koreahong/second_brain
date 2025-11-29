---
title: "postgres / snowflake 권한관리"
source: notion
notion_id: 271c6d43-3b4d-8019-b9fd-ddb80b6fedc2
imported: 2025-11-29
database: 업무리스트
태그: []
Git 커밋: ""
Jira Key: ""
상태: "완료"
시행착오 (Trial & Error): ""
업무 구상 1: []
날짜: "2025-10-10"
작업 히스토리: ""
상위 항목: []
Jira 결과: ""
업무 구상: ["288c6d43-3b4d-80c5-91fc-d09666ca7443"]
생성 일시: "2025-09-17T06:17:00.000Z"
주차: "41주차"
하위 항목: []
tags: ["notion-import", "업무리스트"]
---

postgres도 organization이 있어서 

### 권한부여

```sql
SELECT ROLE
FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_USERS
WHERE GRANTEE_NAME = 'LONG_TERM_STG';


LONG_TERM_STG_ROLE;
show roles;
Use role useradmin;
USE ROLE ACCOUNTADMIN;
show users Like '%chung%';
SELECT CURRENT_ROLE();

CREATE USER "inyeol.choi"
  PASSWORD = 'Temp123412341234@'  -- ✅ 임시 비밀번호 (최초 로그인 시 변경 권장)
  DEFAULT_ROLE = public   -- 기본 롤
  MUST_CHANGE_PASSWORD = TRUE  -- 첫 로그인 시 비밀번호 변경 강제
  COMMENT = 'inyeol.choi 계정';

ALTER USER "dongyeon.park" SET PASSWORD = 'Temp123412341234@' MUST_CHANGE_PASSWORD = TRUE;
ALTER USER "dongyeon.park" SET DEFAULT_ROLE = LONG_TERM_STG_ROLE;

  QRAFT_ORIGIN.ZEROIN.FILESQRAFT_ORIGIN.ZEROIN.FILESCREATE OR REPLACE USER jaehyeok.heo_new
PASSWORD = 'sn0wf@ll'
LOGIN_NAME = 'jaehyeok.heo'
FIRST_NAME = 'jaehyeok'
LAST_NAME = 'heo'
EMAIL = 'jaehyeok.heo@qraftec.com'
MUST_CHANGE_PASSWORD = true
DEFAULT_WAREHOUSE = data_engineer;


GRANT ROLE public TO USER "hoesu.chung";
GRANT ROLE public TO USER "dongyeon.park";
SHOW MFA METHODS FOR USER LONG_TERM_STG_TEAM2;


GRANT ROLE LONG_TERM_STG_ROLE TO USER "dongyeon.park";;
GRANT ROLE LONG_TERM_STG_TEAM2 TO USER "dongyeon.park";

```

### stage 조회

```sql
-- 1️⃣ 스테이지 파일 목록 조회
LIST @zeroin.public.zeroin_fund_fdtcd001_migration;

-- 2️⃣ 바로 아래 쿼리로 결과 필터링
SELECT *
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
WHERE "name" LIKE '%FDTCD001.20251015%';
```

### table 생성 For문

```sql
DECLARE
    rs RESULTSET;
    v_sql STRING;
    v_table STRING;
BEGIN
    -- 1️⃣ 테이블 목록 가져오기
    rs := (
        SELECT TABLE_NAME
        FROM ALPHA_PLATFORM.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'BARRA'
    );

    -- 2️⃣ 테이블별 CLONE 실행
    FOR rec IN rs DO
        v_table := rec.TABLE_NAME;
        v_sql := 'CREATE OR REPLACE TABLE QRAFT_ORIGIN.BARRA.' || v_table ||
                 ' CLONE ALPHA_PLATFORM.BARRA.' || v_table;
        EXECUTE IMMEDIATE v_sql;
    END FOR;

    -- 3️⃣ 실행 완료 메시지 반환
    RETURN '✅ All tables cloned from ALPHA_PLATFORM.BARRA to QRAFT_ORIGIN.BARRA.';
END;
```

### external storage 연결

```sql
CREATE FILE FORMAT QRAFT_ORIGIN.staging.PORTPOLIO_REBALANCING_CSV_FORMAT
  TYPE = CSV
  RECORD_DELIMITER = '\n'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  PARSE_HEADER = FALSE
  DATE_FORMAT = 'AUTO'
  TIME_FORMAT = 'AUTO'
  TIMESTAMP_FORMAT = 'AUTO'
  BINARY_FORMAT = 'HEX'
  ESCAPE = 'NONE'
  ESCAPE_UNENCLOSED_FIELD = '\\'
  TRIM_SPACE = FALSE
  FIELD_OPTIONALLY_ENCLOSED_BY = 'NONE'
  NULL_IF = ('\\N')
  COMPRESSION = 'AUTO'
  ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
  VALIDATE_UTF8 = TRUE
  SKIP_BLANK_LINES = TRUE
  REPLACE_INVALID_CHARACTERS = FALSE
  EMPTY_FIELD_AS_NULL = TRUE
  SKIP_BYTE_ORDER_MARK = TRUE
  ENCODING = 'UTF8';

DROP STORAGE INTEGRATION portpolio_rebalancing;
CREATE STORAGE INTEGRATION portpolio_rebalancing
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::717473574740:role/snowflake-integration-portpolio-rebalancing'
  STORAGE_ALLOWED_LOCATIONS = ('s3://portpolio-rebalancing/')
  COMMENT = 'Snowflake <-> Qraft S3 connection for rebalancing data';


DESC STORAGE INTEGRATION portpolio_rebalancing; 'ExternalId' 확인

s3 정책 설정
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::530467106055:user/s1q00000-s"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "DOB17693_SFCRole=3_K1F0kYECV5J9cdIi6aO4462BUkk="
                }
            }
        }
    ]
}

CREATE STAGE qraft_origin.staging.portpolio_rebalancing
  URL = 's3://portpolio-rebalancing/'
  STORAGE_INTEGRATION = portpolio_rebalancing
  FILE_FORMAT = (FORMAT_NAME = qraft_origin.staging.portpolio_rebalancing_csv_format)
  COMMENT = 'Stage for portfolio rebalancing CSV files (using predefined file format)';

ALTER STAGE qraft_origin.staging.portpolio_rebalancing 
SET DIRECTORY = (ENABLE = TRUE);


LIST @qraft_origin.staging.portpolio_rebalancing;
ALTER STAGE qraft_origin.staging.portpolio_rebalancing REFRESH;


SELECT 
    p.portid,
    d.RELATIVE_PATH AS file_path,
    d.SIZE,
    d.LAST_MODIFIED
FROM (
    SELECT DISTINCT SUBSTRING(PORTID, 1, LENGTH(PORTID) - 1) AS portid
    FROM qraft_origin.mart.PORT_META
    WHERE teams = 'strategy' 
        AND use_yn = 'Y'
) p
Left JOIN DIRECTORY(@qraft_origin.staging.portpolio_rebalancing) d
    ON d.RELATIVE_PATH LIKE '%' || p.portid || '/%' || p.portid || '_%'
    AND d.RELATIVE_PATH LIKE '%2025-09-30.csv'
ORDER BY p.portid;

ALTER STAGE qraft_origin.staging.portpolio_rebalancing REFRESH;
SELECT 
    RELATIVE_PATH,
    SIZE,
    LAST_MODIFIED
FROM DIRECTORY(@qraft_origin.staging.portpolio_rebalancing)
-- WHERE RELATIVE_PATH LIKE '%2025-09-30.csv%'
LIMIT 10;

```

## LIST vs DIRECTORY 차이

directory는 테이블로 활용할 수 있지만 Refresh를 해줘야 함

ALTER STAGE qraft_origin.mart.portpolio_rebalancing REFRESH;

alembic + 컨플루언스 권한 관리

```sql
"""Setup Snowflake RBAC for qraft_origin database

Revision ID: a7c3f8d29e41
Revises: b40f0d315567
Create Date: 2025-11-06 19:06:14.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a7c3f8d29e41"
down_revision: Union[str, Sequence[str], None] = "b40f0d315567"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def execute_statements(statements: list[str]) -> None:
    """Execute multiple SQL statements individually for Snowflake."""
    for stmt in statements:
        stmt = stmt.strip()
        if stmt and not stmt.startswith("--"):
            op.execute(stmt)


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


def downgrade() -> None:
    """Remove RBAC permissions and roles."""

    # BARRA
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

