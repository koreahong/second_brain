---
title: backfill python code
type: resource
tags:
- airflow
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

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

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

