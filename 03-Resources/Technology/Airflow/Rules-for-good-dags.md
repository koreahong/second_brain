---
title: Rules for good dags
type: resource
tags:
- airflow
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

[https://www.astronomer.io/docs/learn/dag-best-practices?tab=good-practice#treat-your-dag-file-like-a-config-file](https://www.astronomer.io/docs/learn/dag-best-practices?tab=good-practice#treat-your-dag-file-like-a-config-file)

---

1. 멱등성 확인
  -  특정 연산이나 작업이 여러 번 수행되더라도 결과가 동일하게 유지되는 특성
  결과: ⇒>> 동일한 조건, 환경에 있다는 전제하에, 언제 돌려도 같은 Dag의 결과는 동일하게 나와야 함.

1. Retries 설정
  - 분산환경에서 공유 호스트에서 작동하기 때문에, 이러한 환경의 이유로 좀비 프로세스가 생길 수 있음
  결과: ⇒>> retries를 최소 2로 설정해서, 위의 경우로 방지할 수 있게 조치

1. keep tasks atomic
  - tasks간의 MECE가 유지돼야 함.
  결과: ⇒>> 각 tasks의 역할범위의 합이 DAG의 역할 범위안에 있어야 함.

1. airflow에서 자체 제공하는 template 값들을 사용
  - dag 스크립트안에 특히 시간과 관련된 함수를 별도로 선언해서 사용 X
  결과: ⇒>> airflow context 사용

1. record를 필터링하는 기준 세우기
  결과: ⇒>> update_dt나 incremetal_id 등 같은 데이터의 시간을 확인할 수 있는 컬럼을 활용해서 멱등성 유지

1. top-level 코드 작성 주의
  - 함수나 API로 외부값을 추출하는 함수는 주의를 해야함. 30초마다 dag 코드를 구문분석하기 때문에, 이러한 것들은 30초마다 실행됨. 커넥션이나 쿼리로 값을 추출하는 경우 성능이슈가 발생할 수 잇음
  결과: ⇒>> 호출해서 값을 받아와야 하는 것들도 task로 따로 만들어서 사용

1. dag 스크립트 안에서는 모든 값들을 호출하는 형태로 구성돼야 함.
  - dag 스크립트 안에 쿼리나 다른 코드들이 많이 있으면, 유지보수 하기가 어렵다. config 파일처럼, airflow 외적 파일, 코드, 값들은 호출하는 형태로 진행
  결과: ⇒>> template_searchpath와 같은 dag의 tamplate를 지정하는 설정값 사용하기

1. airflow 서버 부하 방지
  - 되도록이면 airflow는 오케스트라 역할만 하게 설계. 데이터 전처리 모델링 등 같은 작업은 별도의 서버에서 처리

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

