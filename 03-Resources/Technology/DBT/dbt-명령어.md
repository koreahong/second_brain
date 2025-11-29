---
title: "dbt 명령어"
source: notion
notion_id: 27dc6d43-3b4d-808b-b7ef-cbd84bb998c4
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: []
링크: []
최종편집시각: "2025-10-24T08:05:00.000Z"
제목: ""
상위 항목: ["267c6d43-3b4d-808e-bd36-d3f92b10fdd7"]
PARA: "Resource"
tags: ["레퍼런스", "notion-import"]
---

```sql
cd /Users/qraft_hongjinyoung/qraft_airflow/dbt/snowflake && dbt run --project-dir . --profiles-dir ../profiles --target dev --profile snowflake --select +us_sec_meta --vars '{"datadate": "2025-10-20"}'
```

