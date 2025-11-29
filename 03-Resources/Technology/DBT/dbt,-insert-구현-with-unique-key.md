---
title: dbt, insert 구현 with unique key
type: resource
tags:
- dbt
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

## 개념

- config에 incremental 설정은 unique_key의 존재유무에 따라 다르게 작동함.
## 목적

- DBT 쿼리를 더욱 효율적으로 작성하기 위함
## 서칭내용

## incremental 설정

- incremental_strategy의 기본은 ‘append’
- merge = delete+insert 설정은 서로 같음
- table에 unique 설정이 없더라도 unique_key를 사용할 수 있음. 
  - unique_key를 설정하지 않고 진행시에 
겹치는 데이터가 있으면 error 발생함
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

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

