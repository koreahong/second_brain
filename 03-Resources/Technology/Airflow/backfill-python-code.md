---
title: "backfill python code"
source: notion
notion_id: 0ebdd095-1f9b-4f20-983c-8ce01af18fe0
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["Airflow"]
링크: []
최종편집시각: "2025-09-13T03:53:00.000Z"
제목: ""
상위 항목: ["26dc6d43-3b4d-80f7-a162-ed9945c8906b"]
날짜: "2024-02-23"
PARA: "Resource"
tags: ["레퍼런스", "Airflow", "notion-import"]
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

