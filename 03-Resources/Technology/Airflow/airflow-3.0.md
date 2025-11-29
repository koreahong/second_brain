---
title: airflow 3.0
type: resource
tags:
- pipeline
- datahub
- dbt
- airflow
- technology
- python
- aws
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

## Asset 개념

### 1. Asset 업데이트 기준

- Task 실행 성공 + outlets=[Asset(...)] 선언
  → 해당 Asset이 새로 갱신됐다고 Airflow가 기록

- 즉, “파일이 실제로 수정되었는지”를 감지하는 게 아니라,
  “이 Task가 성공적으로 돌았으니 이 Asset은 최신 버전이다” 라고 보는 것

예시:

```python
dag1_asset = Asset("s3://dag1/output_1.txt")

with DAG(...):
    BashOperator(
        task_id="producing_task_1",
        bash_command="echo hello > /tmp/output.txt && aws s3 cp /tmp/output.txt s3://dag1/output_1.txt",
        outlets=[dag1_asset],
    )

```

➡️ 위 Task가 성공하면, Airflow DB(Event Log)에

s3://dag1/output_1.txt Asset이 “2025-09-16 12:00 UTC에 갱신됨” 이라고 기록됨.

---

### 2. Inlet이 반응하는 기준

소비자 쪽(inlets or schedule=[Asset(...)])은 Airflow가 기록한 Asset 갱신 이벤트를 기반으로 실행됩니다.

예시:

```python
with DAG(
    dag_id="asset_consumes_1",
    schedule=[dag1_asset],  # <-- 이 Asset이 업데이트되면 DAG 실행
    ...
):
    BashOperator(
        task_id="consuming_1",
        bash_command="echo consuming asset1",
    )

```

➡️ 동작 흐름:

1. producing_task_1 실행 성공 → Asset Event 기록됨
1. Airflow Scheduler가 dag1_asset 갱신 이벤트 감지
1. asset_consumes_1 DAG 자동 Trigger
---

### 3. 물리적 파일 변경 vs Airflow 이벤트

- Airflow는 기본적으로 **파일 변경 감시(File Watcher)**를 하지 않음
- 대신 자기 DAG 실행 기록을 신뢰함
- 만약 실제 파일 변경 여부를 반영하고 싶다면 → Sensor Operator를 함께 사용해야 함
예시 (S3KeySensor 조합):

```python
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

s3_sensor = S3KeySensor(
    task_id="check_s3_file",
    bucket_key="dag1/output_1.txt",
    bucket_name="dag1",
    poke_interval=60,
    timeout=600,
)

```

---

### 4. 정리

- outlets=[Asset(...)] → Task 성공 = Asset 갱신 이벤트 기록
- inlets / schedule=[Asset(...)] → 그 이벤트를 보고 DAG/Task 실행
- 실제 파일 업데이트 검증까지 하고 싶다면 → Sensor를 추가해서 보강해야 함
## 코드 유닛

- airflow 2.0에서 파일당 한개의 dag만을 정의해서 파일 = dag였던 유닛과 다르게, airflow 3.0은 한 파일에서 한 파이프라인 전부를 정의할 수 있는 형태로 진행됨.
- 한 파일에서 한 파이프라인을 작성하면 그 것에 대한 정보들이 낯개로 올라옴. ⇒ 코드가 같게 보임, 이런 부분이 살짝 불편할듯
<details>
<summary>코드 예시</summary>

```python
from __future__ import annotations

# [START asset_def]
import pendulum

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG, Asset
from airflow.timetables.assets import AssetOrTimeSchedule
from airflow.timetables.trigger import CronTriggerTimetable

dag1_asset = Asset("s3://dag1/output_4.txt", extra={"hi": "bye"})
dag2_asset = Asset("s3://dag2/output_4.txt", extra={"hi": "bye"})
dag3_asset = Asset("s3://dag3/output_5.txt", extra={"hi": "bye"})

with DAG(
    dag_id="asset_produces_3",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule="@daily",
    tags=["produces", "asset-scheduled"],
) as dag1:
    # [START task_outlet]
    BashOperator(outlets=[dag1_asset], task_id="producing_task_3", bash_command="sleep 5")
    # [END task_outlet]

with DAG(
    dag_id="asset_produces_4",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=None,
    tags=["produces", "asset-scheduled"],
) as dag2:
    BashOperator(outlets=[dag2_asset], task_id="producing_task_4", bash_command="sleep 5")

# [START dag_dep]
with DAG(
    dag_id="asset_consumes_3",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[dag1_asset],
    tags=["consumes", "asset-scheduled"],
) as dag3:
    # [END dag_dep]
    BashOperator(
        outlets=[Asset("s3://consuming_3_task/asset_other.txt")],
        task_id="consuming_3",
        bash_command="sleep 5",
    )

with DAG(
    dag_id="asset_consumes_3_and_4",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[dag1_asset, dag2_asset],
    tags=["consumes", "asset-scheduled"],
) as dag4:
    BashOperator(
        outlets=[Asset("s3://consuming_4_task/asset_other_unknown.txt")],
        task_id="consuming_4",
        bash_command="sleep 5",
    )

with DAG(
    dag_id="asset_consumes_3_never_scheduled",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[
        dag1_asset,
        Asset("s3://unrelated/this-asset-doesnt-get-triggered"),
    ],
    tags=["consumes", "asset-scheduled"],
) as dag5:
    BashOperator(
        outlets=[Asset("s3://consuming_4_task/asset_other_unknown.txt")],
        task_id="consuming_3",
        bash_command="sleep 5",
    )

with DAG(
    dag_id="asset_consumes_unknown_never_scheduled",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[
        Asset("s3://unrelated/asset3.txt"),
        Asset("s3://unrelated/asset_other_unknown.txt"),
    ],
    tags=["asset-scheduled"],
) as dag6:
    BashOperator(
        task_id="unrelated_task",
        outlets=[Asset("s3://unrelated_task/asset_other_unknown.txt")],
        bash_command="sleep 5",
    )

with DAG(
    dag_id="consume_3_and_4_with_asset_expressions",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=(dag1_asset & dag2_asset),
) as dag5:
    BashOperator(
        outlets=[Asset("s3://consuming_4_task/asset_other_unknown.txt")],
        task_id="consume_3_and_4_with_asset_expressions",
        bash_command="sleep 5",
    )
with DAG(
    dag_id="consume_3_or_4_with_asset_expressions",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=(dag1_asset | dag2_asset),
) as dag6:
    BashOperator(
        outlets=[Asset("s3://consuming_4_task/asset_other_unknown.txt")],
        task_id="consume_3_or_4_with_asset_expressions",
        bash_command="sleep 5",
    )
with DAG(
    dag_id="consume_3_or_both_4_and_3_with_asset_expressions",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=(dag1_asset | (dag2_asset & dag3_asset)),
) as dag7:
    BashOperator(
        outlets=[Asset("s3://consuming_4_task/asset_other_unknown.txt")],
        task_id="consume_3_or_both_4_and_3_with_asset_expressions",
        bash_command="sleep 5",
    )
with DAG(
    dag_id="conditional_asset_and_time_based_timetable_1",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=AssetOrTimeSchedule(
        timetable=CronTriggerTimetable("0 1 * * 3", timezone="UTC"), assets=(dag1_asset & dag2_asset)
    ),
    tags=["asset-time-based-timetable"],
) as dag8:
    BashOperator(
        outlets=[Asset("s3://asset_time_based/asset_other_unknown.txt")],
        task_id="conditional_asset_and_time_based_timetable_1",
        bash_command="sleep 5",
    )
# [END asset_def]

```

</details>

## dbt 작성

## datahub 연결

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

