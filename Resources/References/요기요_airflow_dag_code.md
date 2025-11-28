---
title: 요기요 airflow dag code
created: 2024-05-03
tags: ["reference", "migrated", "resource", "airflow"]
PARA: Resource
구분: ["Airflow"]
---

# 요기요 airflow dag code

## 📝 내용

```python

"""
만다라트 월간 DAG
"""

import sys
import os
from pathlib import Path

HOMEPATH = Path(__file__).parent.parent.absolute()

sys.path.append(f"{HOMEPATH}")

from common.python_script_common import *
from common.airflow_script_common import *

KST_TZ = pendulum.timezone("Asia/Seoul")


default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 3, 1, tzinfo=KST_TZ),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id=Path(__file__).absolute().stem,
    default_args=default_args,
    description="만다라트",
    schedule_interval="00 9 * * *",
    catchup=False,
)
def mandalart_monthly():

    job_group = datetime.now().strftime("%Y%m%d%H%M%S")

    start = DummyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule=TriggerRule.ONE_SUCCESS)
    resource_available = DummyOperator(task_id="resource_available")
    resource_unavailable = DummyOperator(task_id="resource_unavailable")

    @task.branch
    def check_resource_table(**context):

        target_date = pd.date_range(
            end=context["logical_date"] - pd.offsets.MonthEnd(1), periods=1, freq="M"
        )[0].strftime("%Y-%m-%d")

        update_resource(target_date)

        with bigquery.Client() as bq_client:

            query = f"""
                select
                    if(check_shinhan_yn = 'Y', 1, 0) +
                    if(check_order_yn = 'Y', 1, 0) +
                    if(etl_done = 'N', 1, 0) as source_check
                from kpmg-data-375303.ad_hoc.mandalart_monthly_source_table_check
                where target_date = '{target_date}'
            """

            query_job = bq_client.query(query)
            check_etl_done = query_job.to_dataframe()

            if (check_etl_done.source_check == 3).all():
                return "resource_available"
            else:
                return "resource_unavailable"

    @task_group(group_id="group")
    def level_group(stage: str, level: str):
        f"""{stage} {level} group"""

        query_paths = get_query_files(
            f"/opt/rgpkorea-finance-KPMG/mandalart_process_files/{stage}/{level}/*.sql"
        )

        # check python path between Windows(local) and Linux
        try:
            check_python = subprocess.check_output("where python", shell=True)
            python_path = "python"
        except:
            python_path = "/home/K202212010/miniconda/envs/test/bin/python"

        # create task list
        task_list = []
        for query_path in query_paths:
            task_list.append(
                BashOperator(
                    task_id=f"{query_path.split('/')[-1][:-4]}",
                    bash_command="{python_path} /opt/rgpkorea-finance-KPMG/mandalart_process_files/mandalart_monthly_{stage}.py -p {query_path} -e {execution_date} -g {job_group}".format(
                        python_path=python_path,
                        stage=stage,
                        query_path=query_path,
                        execution_date="{{data_interval_end.add(days=-1).strftime('%Y-%m-%d')}}",
                        job_group=job_group,
                    ),
                )
            )

        task_chain = chain(*task_list)

    @task
    def update_source_table(**context):

        target_date = pd.date_range(
            end=context["logical_date"] - pd.offsets.MonthEnd(1), periods=1, freq="M"
        )[0].strftime("%Y-%m-%d")

        with bigquery.Client() as bq_client:

            query = f"""
                MERGE kpmg-data-375303.ad_hoc.mandalart_monthly_source_table_check old
                USING   (
                        SELECT
                            '{target_date}' as target_date,
                            'Y' as etl_done,
                            current_timestamp() as check_time,
                    ) new_data
                ON old.target_date = new_data.target_date
                WHEN NOT MATCHED THEN
                    INSERT(etl_done, check_time)
                    VALUES(new_data.etl_done, new_data.check_time)
            """

            query_job = bq_client.query(query)
            query_job.result()

    branch = check_resource_table()

    start >> branch
    branch >> resource_available
    branch >> resource_unavailable >> end

    group_list = [resource_available]

    group_list.append(
        level_group.override(group_id=f"속성계산_lv0_group")("속성계산", "lv0")
    )
    for level in ["lv0", "lv1", "lv2", "lv3"]:
        group_list.append(
            level_group.override(group_id=f"지표계산_{level}_group")("지표계산", level)
        )

    update = update_source_table()

    group_list += [update]
    group_list += [end]

    chain(*group_list)


mandalart_monthly()

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
