---
title: dbt 명령어
type: resource
---

```sql
cd /Users/qraft_hongjinyoung/qraft_airflow/dbt/snowflake && dbt run --project-dir . --profiles-dir ../profiles --target dev --profile snowflake --select +us_sec_meta --vars '{"datadate": "2025-10-20"}'
```