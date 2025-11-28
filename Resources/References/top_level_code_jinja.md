---
title: top level code jinja
created: 2024-06-12
tags: ["reference", "migrated", "resource", "airflow"]
PARA: Resource
구분: ["Airflow"]
---

# top level code jinja

## 📝 내용

https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html

```plain text
templated_command = textwrap.dedent(
"""{% for i in range(5) %}    echo "{{ ds }}"    echo "{{ macros.ds_add(ds, 7)}}"{% endfor %}""")
```

## 🏷️ 분류

- **PARA**: Resource
- **구분**: Airflow

## 🔗 연결

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
