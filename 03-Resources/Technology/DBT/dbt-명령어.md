---
title: dbt 명령어
type: resource
tags:
  - dbt
  - airflow
  - snowflake
  - technology
  - sql
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

```sql
cd /Users/qraft_hongjinyoung/qraft_airflow/dbt/snowflake && dbt run --project-dir . --profiles-dir ../profiles --target dev --profile snowflake --select +us_sec_meta --vars '{"datadate": "2025-10-20"}'
```

---

## 📎 Related

### Technology

- [[dbt|DBT]] - DBT 개요 및 Qraft 적용 사례

### Insights

