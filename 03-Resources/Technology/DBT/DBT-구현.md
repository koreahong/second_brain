---
created: '2025-11-30'
updated: '2025-11-30'
tags:
  - Technology
  - DBT
  - Snowflake
  - DataWarehouse
  - DataTransformation
related:
  - Airflow-3.0-구현
  - DataHub-메타데이터-관리
  - 데이터-거버넌스-도입
---
# DBT 구현

## 개요

DBT (Data Build Tool)를 사용한 Snowflake 데이터 변환 파이프라인 구현입니다. 4-레이어 아키텍처(Staging → Intermediate → Core → Marts)와 Incremental materialization을 통해 효율적인 데이터 변환을 제공합니다.

**핵심 구현:**
- 4-Layer 아키텍처 (Staging, Intermediate, Core, Marts)
- Incremental materialization with `delete+insert`
- Custom macros (`require_datadate`, `require_pre_date`)
- DataHub 메타데이터 통합 (Tag/Owner URN 패치)
- Multi-database 지원 (qraft_origin, qraft_automation)

## 주요 기술 스택

- **DBT Core 1.8+**
- **Snowflake** (Data Warehouse)
- **Airflow Cosmos** (DBT-Airflow 통합)
- **DataHub** (메타데이터 카탈로그)
- **Jinja2** (템플릿 엔진)

## 1. 4-Layer 아키텍처

### 레이어별 책임

| 레이어 | Input | Output | 주요 작업 | 비즈니스 로직 |
|--------|-------|--------|-----------|---------------|
| **Staging** | source | 표준화 테이블 | 컬럼명/타입 통일, 값 정제 | 거의 없음 |
| **Intermediate** | staging models | 논리적 데이터 모델 | 조인, 품질검증, 중간 집계 | 있음 |
| **Core** | source | conformed dimension | 공통 차원 테이블 관리 | 최소 |
| **Marts** | intermediate/staging | 최종 output | 최종 비즈니스 뷰 제공 | 있음 |

**핵심 원칙:**
- **Staging**: Source를 그대로 가져와 표준화만 수행 (1:1 매핑)
- **Intermediate**: 여러 source/staging 조인, 복잡한 계산 로직 수행
- **Core**: 전사 공통 차원 테이블 (`dim_ticker`, `dim_holiday` 등)
- **Marts**: 최종 사용자가 직접 사용하는 테이블

### 폴더 구조

```
models/
├── _sources.yml                    # 모든 source 정의
├── core/                           # Conformed dimensions
│   ├── _models.yml
│   ├── dim_ticker.sql
│   └── dim_holiday.sql
├── staging/{domain}/               # Source → 표준화
│   ├── _models.yml
│   ├── index/
│   │   ├── nasdaq100.sql
│   │   └── sp500.sql
│   └── us_sec_meta/
│       ├── stg_us_sec_meta_base.sql
│       └── stg_us_sec_price_metrics.sql
├── intermediate/{domain}/          # Staging → 논리적 변환
│   ├── _models.yml
│   ├── index/
│   │   └── int_qqq.sql
│   └── us_simul_data/
│       ├── int_us_simul_data_base.sql
│       └── int_us_simul_data_mrkcap.sql
└── marts/{domain}/                 # 최종 output
    ├── _models.yml
    ├── us_simul_data/
    │   └── us_simul_data.sql
    └── index/
        └── index_const.sql
```

### 네이밍 규칙

| Layer | Prefix | 예시 | 파일명 = 모델명 |
|-------|--------|------|----------------|
| Staging | `stg_` | `stg_us_sec_meta_base.sql` | ✅ 필수 |
| Intermediate | `int_` | `int_us_simul_data_base.sql` | ✅ 필수 |
| Core | `dim_` | `dim_ticker.sql` | ✅ 필수 |
| Marts | (없음) | `us_simul_data.sql` | ✅ 필수 |
| Views | `vw_` | `vw_security.sql` | ⚠️ 이름 변경 금지 |

**중요:**
- 파일명이 dbt 모델명이 됨
- `alias` 설정으로 물리 테이블명 제어 가능

## 2. Incremental Materialization

### 2.1 Config 템플릿

**Staging 레이어:**
```sql
{{
    config(
        materialized='incremental',
        unique_key=['datadate', 'gvkey', 'iid'],
        incremental_strategy='delete+insert',
        schema='staging',
        database='qraft_origin',
        tags=['layer:staging', 'domain:us_sec_meta']
    )
}}
```

**Intermediate 레이어:**
```sql
{{
    config(
        materialized='incremental',
        unique_key=['datadate', 'gvkey', 'iid'],
        incremental_strategy='delete+insert',
        schema='intermediate',
        database='qraft_origin',
        alias='int_us_simul_data_base',  -- 물리 테이블명 명시
        tags=['layer:intermediate', 'domain:us_simul_data', 'team:Strategy (T)']
    )
}}
```

**Marts 레이어:**
```sql
{{
    config(
        materialized='incremental',
        unique_key=['datadate', 'gvkey', 'iid'],
        incremental_strategy='delete+insert',
        schema='mart',
        database='qraft_origin',
        alias='us_simul_data',
        tags=['layer:mart', 'domain:us_simul_data', 'team:Strategy (T)']
    )
}}
```

### 2.2 Delete+Insert 전략

**동작 방식:**
1. **Check**: `is_incremental()` 조건으로 현재 incremental 모드인지 확인
2. **Delete**: `unique_key` 기준으로 기존 데이터 삭제
3. **Insert**: 새 데이터 삽입

**예시 코드:**
```sql
-- int_us_simul_data_base.sql 핵심 로직
WITH temp_sp AS (
    SELECT
        datadate,
        gvkey,
        iid,
        -- ... 기타 컬럼 ...
    FROM {{ source('ciq', 'sec_dprc') }}
    WHERE
        {% if is_incremental() %}
            -- Incremental: 이전 날짜 + 현재 날짜 (Return 계산용)
            datadate IN ('{{ pre_date }}', '{{ datadate }}')
        {% else %}
            -- Full refresh: 시작일부터 현재까지
            datadate BETWEEN '{{ var('start_date', '1900-01-01') }}' 
                AND '{{ datadate }}'
        {% endif %}
        AND iid NOT LIKE '%W'  -- Warrants 제외
)

SELECT
    -- ... 데이터 변환 ...
FROM temp_sp
WHERE
    {% if is_incremental() %}
        -- Incremental: 현재 날짜만 반환 (이전 날짜는 Return 계산용)
        datadate = '{{ datadate }}'
    {% else %}
        -- Full refresh: 모든 날짜
        datadate BETWEEN '{{ var('start_date', '1900-01-01') }}' 
            AND '{{ datadate }}'
    {% endif %}
```

**핵심 패턴:**
1. **데이터 조회 시**: `pre_date` + `datadate` (Return 계산을 위해 이전 날짜 필요)
2. **데이터 반환 시**: `datadate`만 (중복 방지)
3. **Delete+Insert**: `unique_key=['datadate', 'gvkey', 'iid']` 기준으로 기존 데이터 삭제 후 재삽입

### 2.3 Custom Macros

**`require_datadate()` macro:**
```sql
{# ✅ datadate 필수 검증 #}
{% set datadate = require_datadate() %}
```

**구현 (macros/require_datadate.sql):**
```sql
{% macro require_datadate() %}
    {# Airflow에서 전달하는 datadate 변수 가져오기 #}
    {% set datadate = var('datadate', None) %}
    
    {% if not datadate %}
        {{ exceptions.raise_compiler_error("datadate 변수가 필요합니다. --vars '{\"datadate\": \"YYYY-MM-DD\"}' 형식으로 전달하세요.") }}
    {% endif %}
    
    {{ return(datadate) }}
{% endmacro %}
```

**`require_pre_date()` macro:**
```sql
{# ✅ pre_date 가져오기 (Airflow에서 전달 권장) #}
{% set pre_date = require_pre_date() %}
```

**사용 예시 (Airflow DAG):**
```python
dbt_task = DbtDagRunOperator(
    task_id="run_dbt_model",
    vars={
        "datadate": "{{ ds }}",  # 현재 날짜
        "pre_date": "{{ macros.ds_add(ds, -1) }}"  # 이전 날짜
    }
)
```

## 3. Source & Ref 관리

### 3.1 Source 정의 (_sources.yml)

**위치:** `models/_sources.yml` (단일 파일)

```yaml
sources:
  - name: ciq
    database: ciq
    schema: xpressfeed
    description: Capital IQ Xpressfeed
    tables:
      - name: sec_dprc
        identifier: sec_dprc
        description: Security daily price
        
      - name: sec_dtrt
        identifier: sec_dtrt
        description: Security daily total return

  - name: core
    database: qraft_origin
    schema: core
    description: Core dimension tables
    tables:
      - name: dim_ticker
        identifier: dim_ticker
        description: Ticker dimension table
```

**사용 (SQL):**
```sql
FROM {{ source('ciq', 'sec_dprc') }}  -- ✅ 올바른 사용
FROM ciq.xpressfeed.sec_dprc           -- ❌ 하드코딩 금지
```

### 3.2 Ref 사용 규칙

**의존성 체인:**
```
source → staging → intermediate → marts
              ↓
            core (dimension)
```

**예시:**
```sql
-- Intermediate 모델에서 Staging 참조
FROM {{ ref('stg_us_sec_meta_base') }}  -- ✅ 올바른 사용

-- Marts 모델에서 Intermediate 참조
FROM {{ ref('int_us_simul_data_base') }}  -- ✅ 올바른 사용

-- ❌ 하드코딩 금지
FROM qraft_origin.staging.int_us_simul_data_base
```

## 4. Tags & Ownership

### 4.1 Tags 규칙

| Layer | Tags 형식 | 예시 |
|-------|----------|------|
| Staging | `['layer:staging', 'domain:{domain}']` | `['layer:staging', 'domain:us_sec_meta']` |
| Intermediate | `['layer:intermediate', 'domain:{domain}', 'team:{team}']` | `['layer:intermediate', 'domain:index', 'team:ML Platform (T)']` |
| Core | `['layer:core', 'domain:dimension']` | `['layer:core', 'domain:dimension']` |
| Marts | `['layer:mart', 'domain:{domain}', 'team:{team}']` | `['layer:mart', 'domain:us_simul_data', 'team:Strategy (T)']` |

**중요:**
- Intermediate/Marts는 반드시 팀명 포함
- 형식: `layer:값`, `domain:값`, `team:값`

### 4.2 Ownership (_models.yml)

```yaml
models:
  - name: us_simul_data
    description: |
      US Simulation Data 최종 마트 테이블
      
    meta:
      owner: "urn:li:corpGroup:ML+Platform+%28T%29"  # Business Owner
      technical_owner: "urn:li:corpGroup:ML+Platform+%28T%29"  # Technical Owner
      datahub:
        domain: "urn:li:domain:USSimulation"
      data_product: "us_backtesting_data"
      external_source: "Snowflake Marketplace - Capital IQ Xpressfeed"
    
    config:
      materialized: incremental
      incremental_strategy: delete+insert
      unique_key: ["datadate", "gvkey", "iid"]
      tags: ["layer:mart", "domain:us_simul_data", "team:Strategy (T)"]
```

**DataHub 메타데이터 매핑:**
- `meta.owner` → Business Owner (DataHub)
- `meta.technical_owner` → Technical Owner (DataHub)
- `meta.datahub.domain` → Domain (DataHub)
- `config.tags` → Tags (DataHub)

## 5. DataHub 통합

### 5.1 URN Encoding 문제 (Trial & Error)

**증상:**
- DBT의 tags와 owners가 DataHub에 중복 생성됨
- Keycloak 그룹: `ML+Platform+%28T%29`
- DBT 그룹: `ML Platform %28T%29`
- 동일한 그룹이 2개로 생성됨

**원인:**
DataHub의 DBT connector가 사용하는 URL 인코딩 방식이 Keycloak OIDC와 불일치:
- **Keycloak OIDC**: `quote_plus` (공백→`+`, 괄호→`%28%29`)
- **DBT Connector**: `UrnEncoder` (공백→` `, 괄호→`%28%29`)

**시도 1: DBT Connector 설정 변경 (실패)**
- DataHub DBT connector는 URL 인코딩 방식을 변경할 수 없음
- 소스 코드 수정 필요

**시도 2: Runtime Patch (성공)**

**패치 코드 (dbt_urn_encoding_patch.py):**
```python
from urllib.parse import quote_plus
from datahub.emitter import mce_builder

# Tag URN 패치
def make_tag_urn_no_encoding(tag: str) -> str:
    """
    태그 URN을 생성하되 URL 인코딩하지 않음
    
    Original: urn:li:tag:team%3AML%20Platform%20%28T%29
    Patched:  urn:li:tag:team:ML Platform (T)
    """
    return f"urn:li:tag:{tag}"

mce_builder.make_tag_urn = make_tag_urn_no_encoding

# Group URN 패치
def make_group_urn_keycloak_style(groupname: str) -> str:
    """
    그룹 URN을 Keycloak quote_plus 인코딩 방식으로 생성
    
    Original (UrnEncoder): urn:li:corpGroup:ML Platform %28T%29
    Patched (quote_plus):  urn:li:corpGroup:ML+Platform+%28T%29
    """
    if groupname and groupname.startswith(("urn:li:corpGroup:", "urn:li:corpuser:")):
        return groupname
    else:
        return f"urn:li:corpGroup:{quote_plus(groupname)}"

mce_builder.make_group_urn = make_group_urn_keycloak_style
```

**적용 방법:**
```bash
# entrypoint-actions.sh
python3 /tmp/setup/apply_dbt_patches.py

# 또는 ingestion recipe에서
import dbt_urn_encoding_patch  # 자동으로 monkey patch 적용
```

**결과:**
- Keycloak, Airflow, DBT 모두 동일한 URN 사용
- 그룹 중복 제거
- Tags 통합

### 5.2 Owner Type Detection

**문제:**
- 팀 그룹(`ML Platform (T)`)도 `corpuser`로 처리됨
- 개인과 팀을 구분할 수 없음

**해결:**
```python
def determine_owner_type(owner_name: str):
    """
    (T) suffix로 팀 그룹 판별
    
    ML Platform (T) → corpGroup
    John Doe → corpuser
    """
    if "(T)" in owner_name:
        return "corpGroup"
    else:
        return "corpuser"
```

**결과:**
- 팀 owner는 `corpGroup`으로 정상 처리
- 개인 owner는 `corpuser`로 처리

## 6. YML 파일 관리 규칙

### 6.1 _models.yml 위치

```
models/
├── core/_models.yml                    # 모든 core 모델 정의
├── staging/{domain}/_models.yml        # 도메인별 staging 모델
├── intermediate/{domain}/_models.yml   # 도메인별 intermediate 모델
└── marts/{domain}/_models.yml          # 도메인별 marts 모델
```

### 6.2 필수 업데이트 시점

1. ✅ **새 모델 생성 시**: 해당 폴더의 `_models.yml`에 모델 정의 추가
2. ✅ **모델 이름 변경 시**: `_models.yml`의 name 필드 업데이트
3. ✅ **모델 이동 시** (레이어 변경):
   - 기존 레이어의 `_models.yml`에서 제거
   - 새 레이어의 `_models.yml`에 추가
   - Dependencies 섹션 업데이트
4. ✅ **ref() 의존성 변경 시**: Dependencies 필드 업데이트
5. ✅ **컬럼 추가/삭제 시**: columns 섹션 업데이트

### 6.3 _models.yml 템플릿

```yaml
version: 2

models:
  - name: int_us_simul_data_base
    description: |
      모델 설명 (한글 가능)
      
      **Lineage:**
      - source → staging → int_us_simul_data_base
      
      **로직:**
      - 주요 변환 로직 1
      - 주요 변환 로직 2
      
      **Dependencies:** {{ ref('stg_us_sec_meta_base') }}
      
      **Materialization:**
      - Type: incremental (delete+insert)
      - Unique Key: [datadate, gvkey, iid]
      - Physical Table: qraft_origin.staging.int_us_simul_data_base
    
    config:
      materialized: incremental
      incremental_strategy: delete+insert
      unique_key: ['datadate', 'gvkey', 'iid']
      schema: staging
      alias: int_us_simul_data_base
      tags: ['layer:intermediate', 'domain:us_simul_data', 'team:Strategy (T)']
    
    columns:
      - name: datadate
        description: 데이터 기준일
        tests:
          - not_null
      
      - name: gvkey
        description: Global Company Key
        tests:
          - not_null
```

## 7. Multi-Database 지원

### 7.1 dbt_project.yml 설정

```yaml
models:
  qraft:
    # Staging: 기본 qraft_origin
    staging:
      +database: qraft_origin
      +schema: staging
      
      # Core/Flex 관련만 qraft_automation
      core:
        +database: qraft_automation
    
    # Intermediate: 기본 qraft_origin
    intermediate:
      +database: qraft_origin
      +schema: intermediate
    
    # Marts: 기본 qraft_origin
    marts:
      +database: qraft_origin
      +schema: mart
    
    # Core: 기본 qraft_origin
    core:
      +database: qraft_origin
      +schema: core
      
      # dim_flex만 qraft_automation.employee
      dim_flex:
        +database: qraft_automation
        +schema: employee
```

### 7.2 Cross-Database 참조

```sql
-- qraft_origin → qraft_automation 참조
FROM {{ ref('dim_flex') }}  -- DBT가 자동으로 qraft_automation.employee.dim_flex로 변환

-- qraft_automation → qraft_origin 참조
FROM {{ ref('stg_us_sec_meta_base') }}  -- qraft_origin.staging.stg_us_sec_meta_base
```

**핵심:**
- DBT가 `dbt_project.yml` 설정 기반으로 자동 변환
- 하드코딩 불필요
- Database 변경 시 yml만 수정

## 8. Airflow Cosmos 통합

### 8.1 Cosmos DBT Operator

```python
# DAG에서 DBT 모델 실행
from airflow.providers.astronomer.cosmos import DbtDagRunOperator

dbt_task = DbtDagRunOperator(
    task_id="transform_data",
    project_dir="/opt/airflow/dbt/qraft",
    profiles_dir="/opt/airflow/dbt/qraft",
    profile="qraft",
    target="dev",
    select=["tag:layer:intermediate"],  # Tag 기반 선택
    vars={
        "datadate": "{{ ds }}",
        "pre_date": "{{ macros.ds_add(ds, -1) }}"
    },
    full_refresh=False,
)
```

### 8.2 Asset (Dataset) 자동 생성

**Airflow 3.x + Cosmos:**
- Cosmos task가 실행되면 자동으로 Asset (Dataset) 생성
- Task naming: `transform_data.{model_name}.run`
- Asset URI: `dbt://{database}.{schema}.{model_name}`

**예시:**
```
Task: transform_data.int_us_simul_data_base.run
→ Asset: dbt://qraft_origin.intermediate.int_us_simul_data_base
```

**DataHub에서 확인:**
- Airflow DAG → DBT 모델 lineage 자동 연결
- Asset outlet으로 표시

## 9. Trial & Error

### 9.1 URN Encoding 불일치

**증상:**
- Keycloak, Airflow, DBT에서 동일한 팀명이 서로 다른 URN으로 생성
- DataHub에 중복 그룹 표시

**시도:**
1. **DBT Connector 설정 변경** (실패)
   - 설정 옵션 없음

2. **소스 코드 수정** (거부)
   - DataHub 버전 업그레이드 시 패치 사라짐
   - 유지보수 어려움

3. **Runtime Monkey Patch** (성공)
   - `mce_builder.make_tag_urn` 함수 교체
   - `mce_builder.make_group_urn` 함수 교체
   - DataHub 재시작 시에도 항상 적용

**해결:**
```python
# entrypoint-actions.sh에서 자동 적용
python3 /tmp/setup/apply_dbt_patches.py
```

### 9.2 _models.yml 누락으로 인한 DataHub 메타데이터 누락

**증상:**
- DBT 모델은 생성되었지만 DataHub에 메타데이터 없음
- Owner, Tags, Description 누락

**원인:**
- 모델 생성 후 `_models.yml` 업데이트 누락
- DataHub는 `_models.yml`의 meta 필드만 읽음

**해결:**
- 모델 생성 체크리스트에 `_models.yml` 업데이트 필수화
- Pre-commit hook으로 `_models.yml` 누락 검증

### 9.3 Incremental 모델 Full Refresh 오류

**증상:**
- `dbt run --full-refresh` 실행 시 `pre_date` 변수 오류

**원인:**
```sql
{% if is_incremental() %}
    datadate IN ('{{ pre_date }}', '{{ datadate }}')
{% else %}
    -- Full refresh에서는 pre_date 사용하지 않음
    datadate BETWEEN '{{ var('start_date', '1900-01-01') }}' AND '{{ datadate }}'
{% endif %}
```

**교훈:**
- `pre_date`는 incremental 모드에서만 사용
- Full refresh에서는 `start_date` ~ `datadate` 범위 사용

## 10. 성능 최적화

### 10.1 Partition Pruning

```sql
-- ❌ 비효율적 (Full table scan)
FROM {{ source('ciq', 'sec_dprc') }}
WHERE datadate = '2025-11-30'

-- ✅ 효율적 (Partition pruning)
FROM {{ source('ciq', 'sec_dprc') }}
WHERE
    {% if is_incremental() %}
        datadate IN ('{{ pre_date }}', '{{ datadate }}')  -- 2일치만 스캔
    {% else %}
        datadate BETWEEN '{{ var('start_date') }}' AND '{{ datadate }}'
    {% endif %}
```

### 10.2 Window Function 최적화

```sql
-- Window function 계산 후 필터링
WITH temp_simul AS (
    SELECT
        datadate,
        gvkey,
        iid,
        prccd / ajexdi AS price2,
        LEAD(price2, 1) OVER(PARTITION BY gvkey_iid ORDER BY datadate DESC) AS price1,
        price2 / price1 - 1 AS pr
    FROM temp_sp
)

SELECT *
FROM temp_simul
WHERE
    {% if is_incremental() %}
        datadate = '{{ datadate }}'  -- Window 계산 후 현재 날짜만 반환
    {% endif %}
```

**핵심:**
- Window function은 이전 날짜 데이터 필요 → `pre_date` 포함하여 조회
- 최종 결과는 `datadate`만 반환 → 중복 방지

## 11. 버전 관리

**DBT 프로젝트 버전:**
- Version: 1.0.0
- DBT Core: 1.8+
- Snowflake Connector: dbt-snowflake 1.8+

**주요 변경 이력:**
- 2025-11: DataHub URN 패치 적용
- 2025-10: Multi-database 지원 추가
- 2025-09: Incremental materialization 도입
- 2025-08: 4-layer 아키텍처 확립

## 📎 Related

### Projects 배경 (Why)
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/Airflow-3.0-업그레이드-배경|Airflow-3.0-업그레이드-배경]] - Cosmos DBT 통합 배경

### Technology (Core Concepts)
- [[DBT]] - DBT 기본 개념 및 Qraft 적용 사례
- [[Snowflake]] - Snowflake Data Warehouse

### Technology (Related Implementation)
- [[Airflow-3.0-구현]] - Cosmos DBT 통합 구현
- [[DataHub]] - DBT-DataHub 메타데이터 연동
- [[Snowflake-RBAC-가이드]] - Snowflake 권한 관리

### Projects (실제 사용)
- [[02-Areas/크래프트테크놀로지스/Projects/Active/qraft-data-platform-통합프로젝트|qraft-data-platform-통합프로젝트]] - Data Platform 전체 아키텍처
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/데이터-거버넌스-전략-수립|데이터-거버넌스-전략-수립]] - 거버넌스 전략

---

**작성일:** 2025-11-30  
**카테고리:** #Technology #DBT #DataTransformation #DataWarehouse  
**태그:** #DBT #Snowflake #Incremental #DataHub #Cosmos
