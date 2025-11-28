---
title: airflow 아키텍쳐 및 세팅
created: 2024-06-13
tags: ["reference", "migrated", "resource", "airflow"]
PARA: Resource
구분: ["Airflow"]
---

# airflow 아키텍쳐 및 세팅

## 📝 내용

# 레퍼런스

https://tech.socarcorp.kr/data/2021/06/01/data-engineering-with-airflow.html

https://tech.socarcorp.kr/data/2022/11/09/advanced-airflow-for-databiz.html

https://blog.doctor-cha.com/buliding-local-airflow-and-apply-vault

https://engineering.linecorp.com/ko/blog/data-engineering-with-airflow-k8s-1

https://engineering.linecorp.com/ko/blog/data-engineering-with-airflow-k8s-2

https://amazelimi.tistory.com/entry/Airflow-KubernetesExecutor-vs-CeleryExecutor-LIM

https://airflow.apache.org/docs/apache-airflow/stable/concepts/overview.html

https://airflow.apache.org/docs/apache-airflow/stable/executor/kubernetes.html

https://happycloud-lee.tistory.com/3

https://velog.io/@sms8377/Celery-Python-Celery란

https://velog.io/@wnguswn7/Redis란-무엇일까-Redis의-특징과-사용-시-주의점

# 내용

구조는 거의 비슷하지만 worker는 항상 리소스를 점유하지 않는다. airflow가 스케쥴링된 DAG를 실행하기 위해는 쿠버네티스에게 worker pod 생성을 요청한다. (이때 pod의 리소스를 제한 할 수도 있다.)이후 생성한 pod(worker)에 task를 할당하고, task를 완료한 후에는 리소스를 다시 반납한다. 즉 유동적으로 리소스를 사용할 수 있다.

Airflow는 실시간 처리가 아닌 배치 처리를 위한 workflow engine이고 그렇기 때문에 분명 스케쥴이 돌지 않는 시간이 존재한다. 대부분의 운영 환경에서 DAG Job이 도는 시간 보다는 Idle 상태로 worker가 리소스를 점유하고 있는 시간이 더 길 것이라고 생각한다.

쿠버네티스 executor는 동적으로 worker pod를 생성해서 task를 실행한다. 그런데 여기서 라이브러리 종속성 문제가 발생하게 된다. 하나의 쿠버네티스 클러스터 내에서 하나의 에어플로우를 운영할 때 Spark2, 3 버전을 둘 다 사용해야 하는 경우를 예로 들 수 있다.

Helm은 컨테이너를 쉽게 설치할 수 있도록 돕는 툴

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
