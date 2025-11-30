---
title: taskflow 공부
type: resource
tags:
  - airflow
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

[https://www.astronomer.io/docs/learn/airflow-decorators?tab=traditional#how-to-use-airflow-decorators](https://www.astronomer.io/docs/learn/airflow-decorators?tab=traditional#how-to-use-airflow-decorators)

[https://www.astronomer.io/blog/apache-airflow-taskflow-api-vs-traditional-operators/](https://www.astronomer.io/blog/apache-airflow-taskflow-api-vs-traditional-operators/)

---

taskflow api는 쉽고 간결하게 사용할 수 있게 하고
task간의 데이터를 송수신하는 것을 간단하게 하는 것

taskflow는 airflow를 pythonic하게 사용할 수 있게 하는 것

기본 문법은 함수선언 + @task 데코레이션을 사용하면된다.
함수를 선언 후 호출함으로 taskflow를 등록함과 동시에 함수 리턴값을 받을 수 있음

![[Pasted image 20240302221035.png]]

```python
from airflow.decorators import dag, task
from airflow.providers.http.operators.http import SimpleHttpOperator
from pendulum import datetime, duration
import json

# Define body of POST request for the API call to trigger another DAG
date = "{{ execution_date }}"
request_body = {"execution_date": date}
json_body = json.dumps(request_body)

@task
def print_task_type(task_type):
	"""
	Example function to call before and after downstream DAG.
	"""
	print(f"The {task_type} task has completed.")
	print(request_body)

default_args = {
"owner": "airflow",
"depends_on_past": False,
"email_on_failure": False,
"email_on_retry": False,
"retries": 1,
"retry_delay": duration(minutes=5),
}

@dag(
	start_date=datetime(2021, 1, 1),
	max_active_runs=1,
	schedule="@daily",
	catchup=False,
)
def api_dag_taskflow():
	start_task = print_task_type("starting")

	api_trigger_dependent_dag = SimpleHttpOperator(
		task_id="api_trigger_dependent_dag",
		http_conn_id="airflow-api",
		endpoint="/api/v1/dags/dependent-dag/dagRuns",
		method="POST",
		headers={"Content-Type": "application/json"},
		data=json_body,
	)

	end_task = print_task_type("ending")

	start_task >> api_trigger_dependent_dag >> end_task

api_dag_taskflow()

```

---

실습

목표, 기존과 비교해서 어떻게 사용하는게 서로 좋은지 확인

### 도커에 에어플로우 설치

sla는 스케쥴이된 시간에 돌아가야 찍힘
sla callback은 더 해봐야 할듯
xcom은 taskflow api를 활용하면 return에 찍어서 바로 받으면 됨
proccess는 일일히 작성해야 하는 듯

```python
from __future__ import annotations

import json

import pendulum

import time

from airflow import DAG

import datetime

from airflow.operators.python import PythonOperator

from airflow.decorators import dag

from airflow.decorators import task

from airflow.decorators import task_group

from airflow.utils.task_group import TaskGroup

from airflow.operators.dummy_operator import DummyOperator

from airflow.operators.postgres_operator import PostgresOperator

from airflow.hooks.base_hook import BaseHook

from airflow.utils.edgemodifier import Label

import random

from airflow.providers.postgres.hooks.postgres import PostgresHook

from psycopg2 import extras

from sqlalchemy import create_engine

def sla_callback(dag, task_list, blocking_task_list, slas, blocking_tis):

    print(

        "The callback arguments are: ",

        {

            "dag": dag,

            "task_list": task_list,

            "blocking_task_list": blocking_task_list,

            "slas": slas,

            "blocking_tis": blocking_tis,

        },

    )

@dag(

    schedule="@hourly",

    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),

    catchup=False,

    sla_miss_callback=sla_callback,

    default_args={"email": "jimmy@aivelabs.com"},

    tags=["test"],

)

def test_():

    """

    ### TaskFlow API Tutorial Documentation

    This is a simple data pipeline example which demonstrates the use of

    the TaskFlow API using three simple tasks for Extract, Transform, and Load.

    Documentation that goes along with the Airflow TaskFlow API tutorial is

    located

    [here](<https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html>)

    """

    @task(sla=datetime.timedelta(seconds=1))

    def sleep_20():

        """Sleep for 20 seconds"""

        time.sleep(2)

    @task(sla=datetime.timedelta(seconds=0))

    def sleep_30():

        """Sleep for 20 seconds"""

        time.sleep(2)

    sleep_20() >> sleep_30()

    sql_query = """

        SELECT crawling_yn, ctgr_mclas_id

        FROM crawling_mart.crawling_target_info_temp

        limit 1

    """

    # taskflow api를 활용하면 객체 타입이 json으로 변환이 안됨

    postgres_task = PostgresOperator(

        task_id="execute_sql_query",

        sql=sql_query,

        postgres_conn_id="aivelabs_db",

        autocommit=True,  # 필요에 따라 설정

        max_active_tis_per_dag=1,  # 동시에 실행할 작업 수 설정

        # pool='your_postgres_pool',  # 연결 풀 지정, 필요에 따라 설정

        # params={'param_name': 'param_value'},  # 쿼리에 전달할 파라미터 설정

        # priority_weight=2,  # 작업 우선순위 설정

        do_xcom_push=True,  # XCom에 결과값 저장 여부 설정

    )

    @task.branch(task_id="branching_task_id")

    def random_choice():

        result = random.choice([1, 2])

        print(result)

        if result == 1:

            return "branch_task1"

        else:

            return "branch_task2"

    branch_task = random_choice()

    postgres_task >> branch_task

    branch_task1 = DummyOperator(

        task_id='branch_task1',

    )

    branch_task2 = DummyOperator(

        task_id='branch_task2',

    )

    branch_task >> Label("return 1") >> branch_task1

    branch_task >> Label("return 2") >> branch_task2

    @task_group(group_id='first_group')

    def group_1():

        '''task_group 데커레이터를 이용한 첫 번째 그룹입니다.'''

        @task(task_id='group1_inner_function1')

        def group1_inner_func1(**kwargs):

            print('첫 번째 TaskGroup 내 첫 번째 task입니다.')

            return {'ad': 'ad'}

        @task(task_id='group1_inner_function2')

        def group1_inner_func2(**kwargs):

            print('첫 번째 TaskGroup 내 첫 번째 task입니다.')

            return {'ad': 'ad'}

        group1_inner_func1() >> group1_inner_func2()

    branch_task1 >>  group_1()

    @task_group(group_id='second_group', tooltip='두 번째 그룹입니다.')

    def group_2():

        @task(task_id='group2_inner_function1')

        def group2_inner_function1(**kwargs):

            print('두 번째 TaskGroup 내 첫 번째 task입니다.')

            return {'ad': 'ad'}

        @task(task_id='group2_inner_function2')

        def group2_inner_function2(**kwargs):

            print('두 번째 TaskGroup 내 첫 번째 task입니다.')

            return {'ad': 'ad'}

        group2_inner_function1() >> group2_inner_function2()

    branch_task2 >> group_2()

test = test_()

```

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

