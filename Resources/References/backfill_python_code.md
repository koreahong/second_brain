---
title: backfill python code
created: 2024-02-23
tags: ["reference", "migrated", "resource", "airflow"]
PARA: Resource
구분: ["Airflow"]
---

# backfill python code

## 📝 내용

```python

import os

import pandas as pd

date_list = sorted(

    [

        date.strftime("%Y%m%d")

        for date in pd.date_range("2023-01-01", "2024-04-01", freq="MS")

    ],

    reverse=True,

)

date_list = sorted(date_list)



for date in date_list:

    os.system(

        # f"airflow dags backfill --reset-dagruns -s {date} -e {date} -y step3_monthly_cv_seg_backfill"

        f"airflow dags trigger -e {date} step3_monthly_cv_seg_backfill"

    )

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
