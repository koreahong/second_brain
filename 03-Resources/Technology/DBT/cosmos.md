---
title: "cosmos"
source: notion
notion_id: 270c6d43-3b4d-804e-92d5-f7f45e60a37b
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: []
링크: []
최종편집시각: "2025-09-26T01:35:00.000Z"
제목: ""
상위 항목: ["26dc6d43-3b4d-80f7-a162-ed9945c8906b"]
PARA: "Resource"
tags: ["레퍼런스", "notion-import"]
---

- cosmos는 dbt model을 task 단위로 쪼개서 dag를 구성해주는 라이브러리임.
### dbt operator vs cosmos

cosmos가 dbt 프로젝트를 읽고 엮으로 task 단위로 파싱해주는 것

🔖 [https://medium.com/daangn/dbt%EC%99%80-airflow-%EB%8F%84%EC%9E%85%ED%95%98%EB%A9%B0-%EB%A7%88%EC%A3%BC%ED%95%9C-7%EA%B0%80%EC%A7%80-%EB%AC%B8%EC%A0%9C%EB%93%A4-61250a9904ab](https://medium.com/daangn/dbt%EC%99%80-airflow-%EB%8F%84%EC%9E%85%ED%95%98%EB%A9%B0-%EB%A7%88%EC%A3%BC%ED%95%9C-7%EA%B0%80%EC%A7%80-%EB%AC%B8%EC%A0%9C%EB%93%A4-61250a9904ab)

### dbt project → cosmos

```python
import os
from datetime import datetime

from airflow import DAG
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
import pendulum

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="airflow_db",
        profile_args={"schema": "public"},
    ),
)

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        "dbt_test",
    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/.local/bin/dbt",
    ),
    # normal dag parameters
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="my_cosmos_dag",
    default_args={"retries": 2},
)

my_cosmos_dag
```

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/f85880c5-9b08-4b88-96b4-755e98d72f21/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663DX25NOA%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T020657Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQCPAHkjKeUF%2FOlRicJlUhEnHSh1lltOVxjUpcGH%2FhgBhwIgDOPotU99ZMW9T4r4Erw%2Fc%2FWDlD1GyHXx1yorfWFCX7gqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDEYu03wuoq1mGOXH7CrcAwO8ZfJOqkdCJukFh1gF%2FGhgsQ%2FgOtrAJr3%2Bm60pxp0N8uahLZPaZlvt3Dr48d6M9LBDHOZSx4Cw5FHgnl95HqOVaOLlt%2FTFTiFjV15mspNjSo%2FJRPAGJd46MBwGrNASJ76cV9l%2FNHnn1J5r7gsbWE%2FSzJPPWwHtKzeqGwdYuTRTGe08a4cVE2SCTNE1M6ZVIRQdMxCU%2BzlBnp4kmkcyQpVZdk7zLFjf6%2BfWjZDCgyJs65%2Bkas1k0VLVRqhtPS2WrwFNmGlDmcFQS74f4HMng4uELeJXac41fLO1Ab2HgeHqv3PlrJZVlZNiGY2B9FjQs0tNT1ZuchzSaCYYrgdNqcKpSlxeeVgNNMniYjHGyuKOQOBbmbd8StWh7iteigIHnYWUb%2BAeGwZmvMEE3VBpAWehTSEzrbuAlGDxLoaMxsOj8Itr5mHGezfgVav5C1vGrGptm9U5nH%2BKsqPFma2bc%2Fm7%2BSDgdz8sIdvI39nDGSz3jtK62zDs01yBJBnn5PWXfQKJH8r9nk4o9LznEmqf%2FMuGEJIOCkw%2BsDhSXf6fQ%2BTsDwU%2BUR3%2FdfSteWuNXKeGSVLO3Lkf9zhnG7hwsK8IDQRyIIpRI5AcEtqxflzLJu3LknSY6rrzWgg6BTpRMM6FqckGOqUBA%2B82pz3VOM6c5z4VTHpasaLCin%2BKZ9x6zCNWiZ4GDG%2FmYPxinn%2BtgE56vlwn305IciqHr6wztz5L37rdIe6580j1XxfB%2BFOLDNW3j2akT224i4eNFBgNAyn3gI4658%2BkadQoz4CvOgNRzY4MAa3JaFV1%2F4Y%2BnF%2BrurLvEOJSAd%2FYIccdlG1fq%2Fq3hdAuDC1Vw8DHJxynVzWpr%2FjexmhuogPp5KWb&X-Amz-Signature=60aa95f3853a432d996f7a0722bdc680ea5d315efd3963413dcc75e01e9095fb&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

🔖 [https://www.astronomer.io/docs/learn/airflow-dbt/](https://www.astronomer.io/docs/learn/airflow-dbt/)

dbtdag와 dbttaskgroup은 taskgroup은 dag안에서 task로 취급해서 다른 task와 관계를 맺을 수 있고 Dbtdag는 dbt를 dag단위로 생성하는 것

