---
title: "nepa airflow dag code"
source: notion
notion_id: c2bd9fa6-b263-4dfd-9f08-ff7103c48692
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

#airflow-chain #airflow-branch

정리

- step별로 나눠서 디렉토리 정리
- 디렉토리에서 .py, .sql을 찾아서 실행
- bash operator만 사용해서 쿼리를 실행하던지, 파이썬 스크립트를 실행하는지 두 개의 경우로만 컨트롤
- 다른 사람들이 작성한 스크립트 등등을 연결시키기만 하면 되서 dag따로 스크립트따로 작성할 수 있다는 장점이 있음.
- dag 작성하는 사람은 스크립트 단위로 돌아가게 파일 만들어 주세요라고 요청할 수 있고, 스크립트 짜는 사람은 자기가 짠 코드가 cli에서 돌아가는지만 체크하면되서 서로 편리함
```python
import os
import sys

home_path = "/opt/airflow/scripts"
file_paths = "/opt/airflow/sql/step2"

sys.path.append(home_path)

from airflow_common import *

def decide_branch(**kwargs):

    execution_date = kwargs["execution_date"].strftime("%d")

    print(execution_date)

    if execution_date == "01":

        return "trigger_step3_monthly"

    else:

        return "trigger_step3_daily"

default_args = {

    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "email": ["ethan@aivelabs.com"],
}

dag = DAG(
    "step2",
    default_args=default_args,
    start_date=datetime(2024, 2, 12, tzinfo=korean_time_zone),
    description="step2 - create master table",
    schedule_interval=None,
    max_active_runs=1,
    concurrency=1,
    tags=["step2"],
)

file_paths = sorted(
    [
        file_name
        for file_name in glob(f"{file_paths}/**", recursive=True)
        if (".sh" in file_name or ".sql" in file_name)
    ]
)

start = DummyOperator(task_id="start", dag=dag)
end = EmptyOperator(task_id="end", trigger_rule="none_failed_min_one_success")

branching_task = BranchPythonOperator(
    task_id="branching_task",
    python_callable=decide_branch,
    provide_context=True,
    dag=dag,
)

trigger_step3_monthly = TriggerDagRunOperator(
    task_id="trigger_step3_monthly",
    trigger_dag_id="step3_monthly",
    dag=dag,
)


trigger_step3_daily = TriggerDagRunOperator(
    task_id="trigger_step3_daily",
    trigger_dag_id="step3_daily",
    dag=dag,
)



check_status_all_done = EmptyOperator(
    task_id="check_status_all_done", trigger_rule=TriggerRule.ALL_DONE, dag=dag
)

task_list = chain(
    *(
        [start]
        + [
            (
                PythonOperator(
                    task_id=f"{file_path.split('/')[-1][:-4]}",
                    python_callable=execute_sql_postgres,
                    op_kwargs={
                        "query_path": f"{file_path}",
                        "execution_date": "{{ execution_date.in_timezone('Asia/Seoul').add(days=0).strftime('%Y%m%d')}}",
                    },
                    dag=dag,
                )
                if ".sql" in file_path
                else BashOperator(
                    task_id=f"{file_path.split('/')[-1][:-3]}",
                    bash_command=f"bash {file_path} "
                    + "{{ execution_date.in_timezone('Asia/Seoul').add(days=0).strftime('%Y%m%d')}}",
                    dag=dag,
                )
            )
            for file_path in file_paths
        ]
        + [branching_task]
    )
)

branching_task >> trigger_step3_monthly >> check_status_all_done
branching_task >> trigger_step3_daily >> check_status_all_done

check_status_all_done >> end

```

---

taskflow

#airflow-taskflow

task 이름 변경은 테스크생성함수.override(task_id="변경할태스트명")

```python
import os

import sys



home_path = "/opt/airflow/scripts"

file_paths = "/opt/airflow/sql/tableau/step0"



sys.path.append(home_path)



from airflow_common import *



tables_config = conf.tables_config_tableau



file_paths = sorted(

    [

        file_name

        for file_name in glob(f"{file_paths}/**", recursive=True)

        if (".sh" in file_name or ".sql" in file_name)

    ]

)




@dag(

    schedule_interval="0 7 1 * *",

    start_date=datetime(2024, 4, 15, tzinfo=korean_time_zone),

    catchup=False,

    # sla_miss_callback=sla_callback,

    max_active_runs=1,

    concurrency=1,

    default_args={"email": "lucas@aivelabs.com"},

    tags=["tableau_step0_monthly"],

)

def tableau_step0_monthly():



    start = DummyOperator(task_id="start")

    end = DummyOperator(task_id="end")



    task_list = [start]



    # crtbatch -> mktbidb

    @task

    def execute_query(query_path, destination_table):

        source_hook = PostgresHook(postgres_conn_id="crt_bat_stg")

        destination_hook = PostgresHook(postgres_conn_id="tableau")



        # make tables in crtbatch

        source_query = open(query_path, "r").read()

        source_records = source_hook.get_records(source_query)



        if source_records:

            destination_hook.run(sql=f"truncate table {destination_table}")

            destination_hook.insert_rows(destination_table, source_records)



    for file_path in file_paths:

        task_name = f"{file_path.replace('.sql', '')}".split(".")[-1]



        if "KPI_1_new_cus_info" in file_path:

            destination_table = "aivelabs_sv.new_cus_info"

        elif "KPI_2_cus_daily_purchase" in file_path:

            destination_table = "aivelabs_sv.cus_daily_purchase"

        elif "KPI_3_retention_cal" in file_path:

            destination_table = "aivelabs_sv.retention_cal"

        elif "cus_bought_monthly" in file_path:

            destination_table = "aivelabs_sv.cus_bought_monthly"



        globals()[task_name] = execute_query.override(task_id=f"{task_name}")(

            file_path, destination_table

        )

        task_list.append(globals()[task_name])

```

