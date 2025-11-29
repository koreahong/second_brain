---
title: top level code jinja
type: resource
tags:
- airflow
---

https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html

```plain text
templated_command = textwrap.dedent(
"""{% for i in range(5) %}    echo "{{ ds }}"    echo "{{ macros.ds_add(ds, 7)}}"{% endfor %}""")
```