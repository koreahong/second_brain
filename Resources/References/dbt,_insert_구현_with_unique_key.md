---
title: dbt, insert 구현 with unique key
created: 2025-11-28
tags: ["reference", "migrated", "resource", "dbt"]
PARA: Resource
구분: ["DBT"]
---

# dbt, insert 구현 with unique key

## 📝 내용

## 개념

- config에 incremental 설정은 unique_key의 존재유무에 따라 다르게 작동함.

## 목적

- DBT 쿼리를 더욱 효율적으로 작성하기 위함

## 서칭내용

## incremental 설정

- incremental_strategy의 기본은 ‘append’

- merge = delete+insert 설정은 서로 같음

- table에 unique 설정이 없더라도 unique_key를 사용할 수 있음. 

## 중복 데이터 갱신

- config에 unique_key 설정

## 중복 데이터 Skip

```sql
아래와 같이 코드를 작성하는 경우
증분 데이터가 있을 경우에는 목적이 되는 테이블에서 확인하여 
따로 처리를 할 수 있음

해당 코드가 있을 경우에는 config에 설정이 어떻든
중복되는 데이터는 갱신되지 않음

{% if is_incremental() %}
WHERE (t1.a, t1.b) NOT IN (
    SELECT a, b FROM {{ this }}
)
{% endif %}
```

### 예제코드

```bash
{{ config(
    materialized='incremental',
    pre_hook="
		SET TIME ZONE 'Asia/Seoul';
	",
	unique_key=['a', 'b']
) }}

select t1.a, t1.b, current_timestamp as etltime
from {{ source('temp1', 'tt1') }} t1 
    inner join {{ source('temp2', 'tt2') }} t2
		on t1.a = t2.a
			and t1.b = t2.b
-- {% if is_incremental() %}
-- WHERE (t1.a, t1.b) NOT IN (
--     SELECT a, b FROM {{ this }}
-- )
```

## 🏷️ 분류

- **PARA**: Resource
- **구분**: DBT

## 🔗 연결

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
