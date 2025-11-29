---
title: "top level code jinja"
source: notion
notion_id: c75a730a-9499-442f-a40e-bbe4698e66bf
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["Airflow"]
링크: []
최종편집시각: "2024-10-20T07:15:00.000Z"
제목: ""
상위 항목: []
날짜: "2024-06-12"
PARA: "Resource"
tags: ["레퍼런스", "Airflow", "notion-import"]
---

https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html

```plain text
templated_command = textwrap.dedent(
"""{% for i in range(5) %}    echo "{{ ds }}"    echo "{{ macros.ds_add(ds, 7)}}"{% endfor %}""")
```

