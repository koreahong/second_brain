---
title: cosmos
created: 2025-11-28
tags: ["reference", "migrated", "resource"]
PARA: Resource
구분: []
---

# cosmos

## 📝 내용

- cosmos는 dbt model을 task 단위로 쪼개서 dag를 구성해주는 라이브러리임.

### dbt operator vs cosmos

cosmos가 dbt 프로젝트를 읽고 엮으로 task 단위로 파싱해주는 것

### dbt project → cosmos

```python
import os
from datetime import datetime

from airflow import DAG
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
import pendulum

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="airflow_db",
        profile_args={"schema": "public"},
    ),
)

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        "dbt_test",
    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/.local/bin/dbt",
    ),
    # normal dag parameters
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="my_cosmos_dag",
    default_args={"retries": 2},
)

my_cosmos_dag
```

dbtdag와 dbttaskgroup은 taskgroup은 dag안에서 task로 취급해서 다른 task와 관계를 맺을 수 있고 Dbtdag는 dbt를 dag단위로 생성하는 것

## 🏷️ 분류

- **PARA**: Resource
- **구분**: 없음

## 🔗 연결

**Hub**: [[_HUB_Data_Engineering]], [[_HUB_Database]], [[_HUB_Python]]

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
