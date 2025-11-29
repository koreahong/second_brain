---
title: top level code jinja
type: resource
tags:
- airflow
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html

```plain text
templated_command = textwrap.dedent(
"""{% for i in range(5) %}    echo "{{ ds }}"    echo "{{ macros.ds_add(ds, 7)}}"{% endfor %}""")
```

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

