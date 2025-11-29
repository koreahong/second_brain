---
title: "kafka 개념"
source: notion
notion_id: 16fc6d43-3b4d-8013-a441-ea82064e084f
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["Kafka"]
링크: ["https://velog.io/@holicme7/Apache-Kafka-%EC%B9%B4%ED%94%84%EC%B9%B4%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80"]
최종편집시각: "2025-09-13T03:50:00.000Z"
제목: ""
상위 항목: ["26dc6d43-3b4d-80ef-9be9-e48bcd32d4d5"]
PARA: "Resource"
tags: ["레퍼런스", "Kafka", "notion-import"]
---

## 개념

- 성능과 기능이 좋은 큐라 할 수 있다.
## 목적

- 데이터 파이프라인을 더 안정적으로 운용할 수 있는 방안 모색
## 서칭내용

- kafka는 실시간 스트리밍에 최적화 되어 있음
- 자체 서버를 가지고 운영하는 것
- 탄생배경: 대량의 데이터를 안정적이고 실시간으로 처리할 수 있도록 설계되었습다. 카프카는 주로 대량의 이벤트 스트림 데이터를 처리하고 여러 시스템 간에 데이터를 신속하게 전송하는 데 사용됩니다.
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/abf8c10b-3985-4ff3-882a-17adfa698aa6/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466YYHI45RR%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015708Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIBvA5%2BPFFeDxz23lVEx%2BFp2M9Or2886E7NJL7v2C%2FbByAiAMnoWW4EdS%2Fucd2df93L5vzSric32%2Bb5LYETaOOpKVxyqIBAjC%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMd8doc1glBpZL%2F82oKtwDVzAp0A3tI3JwUmElRP4n0ekyve%2FxW4aoxbRlUocFVZ1D62jwQAJ4MQvcMu8eaPr66snZM0hT%2BpFn8j1jbdkkGo%2BnrG2GblYkixJ%2FTFFjeh3bIeoHpulCqX8HFK2CKTHVRql6fuk%2BcDYr9Jc2oU%2FvADPS4pynkNMoy%2F6YT%2BeSkr7LM3hGQGtRpYlyosfxq79pDrcwOlNI%2FqExuqVlX0ttVXMxHrtv9LPBxr%2BpALxliGqM3aZgem%2BoyLsCXAPDCrcu8tLKZ%2FZp%2BQyCiVAO9gnyJE4JpAM0x8VFZ%2BPnuA5d9XxTKGw%2BMlwGjzGOSmS528RC7%2BIjG3zYFYON1BvEZf9kzeyAail2czxue%2BNQFRL3jj7uMBT2UapamCgO2tkKIdj%2BVP%2B8ffncg13LilKh4uSo9KHkBtyw21KH4Jqn0oWh%2BxNFqA7caV%2FPZHffbFTW1XvLfbPRdDRMdfmYKF725qAPSFsAxpenazbaTPx%2F9obojZiGFYBqx7WwqjI9evOY9s0KnC7Z9M4pa%2B5kbJHBnd5G5GyZ4UkIYfYzwZf0WvZNY7rTjerWBFgrqSW5mu7z3qD56TFXphCIt4bSIZzshbq24OnNUlQ0ttXLnffyXKwZ1SvI6rF4RRnliuU6MlYwk4OpyQY6pgG40zvyDFW0pHQFrUeK%2BvMRGCvGnX0%2Bs3uolxpUxtcJ9oNsfXf4i143d6c8U1460gUAzKnDsjMrrPYSv4AqEgoVqabw%2Bg8OzQmQcrkQA8fTDYoG7dKIVElJx%2BLxmcgYBoAuvSqBoIKe9jQW%2Fc6WJpfuNJ3TIW7c6R4Q6JhREoOjSmZf3OpKVZNzdiAV1Hq2Pfz1rUWNP2FgjLDEobSd1swVuSJFKpiL&X-Amz-Signature=74c7eb3e00bd25eff032630278bfe3f434c626ef66b91c43686173ef750474f3&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/3b6ff51e-0279-493e-a420-3da3e21cfb3e/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466YYHI45RR%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015708Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIBvA5%2BPFFeDxz23lVEx%2BFp2M9Or2886E7NJL7v2C%2FbByAiAMnoWW4EdS%2Fucd2df93L5vzSric32%2Bb5LYETaOOpKVxyqIBAjC%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMd8doc1glBpZL%2F82oKtwDVzAp0A3tI3JwUmElRP4n0ekyve%2FxW4aoxbRlUocFVZ1D62jwQAJ4MQvcMu8eaPr66snZM0hT%2BpFn8j1jbdkkGo%2BnrG2GblYkixJ%2FTFFjeh3bIeoHpulCqX8HFK2CKTHVRql6fuk%2BcDYr9Jc2oU%2FvADPS4pynkNMoy%2F6YT%2BeSkr7LM3hGQGtRpYlyosfxq79pDrcwOlNI%2FqExuqVlX0ttVXMxHrtv9LPBxr%2BpALxliGqM3aZgem%2BoyLsCXAPDCrcu8tLKZ%2FZp%2BQyCiVAO9gnyJE4JpAM0x8VFZ%2BPnuA5d9XxTKGw%2BMlwGjzGOSmS528RC7%2BIjG3zYFYON1BvEZf9kzeyAail2czxue%2BNQFRL3jj7uMBT2UapamCgO2tkKIdj%2BVP%2B8ffncg13LilKh4uSo9KHkBtyw21KH4Jqn0oWh%2BxNFqA7caV%2FPZHffbFTW1XvLfbPRdDRMdfmYKF725qAPSFsAxpenazbaTPx%2F9obojZiGFYBqx7WwqjI9evOY9s0KnC7Z9M4pa%2B5kbJHBnd5G5GyZ4UkIYfYzwZf0WvZNY7rTjerWBFgrqSW5mu7z3qD56TFXphCIt4bSIZzshbq24OnNUlQ0ttXLnffyXKwZ1SvI6rF4RRnliuU6MlYwk4OpyQY6pgG40zvyDFW0pHQFrUeK%2BvMRGCvGnX0%2Bs3uolxpUxtcJ9oNsfXf4i143d6c8U1460gUAzKnDsjMrrPYSv4AqEgoVqabw%2Bg8OzQmQcrkQA8fTDYoG7dKIVElJx%2BLxmcgYBoAuvSqBoIKe9jQW%2Fc6WJpfuNJ3TIW7c6R4Q6JhREoOjSmZf3OpKVZNzdiAV1Hq2Pfz1rUWNP2FgjLDEobSd1swVuSJFKpiL&X-Amz-Signature=70856e6d1586ec07842bbce6e2e329b6ffd38d64ff991ca1d662741c17985067&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

- 카프카를 선택하면 좋을 때:
  - 실시간 데이터 스트리밍과 높은 처리 속도가 필요한 경우
  - 복잡한 데이터 파이프라인을 구축해야 할 때
  - 로그 수집 및 분석, 이벤트 소싱 등 고급 데이터 처리가 필요할 때
  - 오픈 소스 솔루션을 선호하고 직접 관리할 수 있는 인프라가 있을 때
- AWS SQS를 선택하면 좋을 때:
  - 간단한 메시지 큐잉과 작업 분배가 필요한 경우
  - AWS 생태계를 주로 사용하고 관리형 서비스를 선호할 때
  - 초기 설정과 운영이 간단한 솔루션이 필요할 때
  - 메시지의 순서 보장이 필요하지만, FIFO 큐로 충분할 때
  - 
### 데이터 처리 과정: 상세 타임라인

1. Producer 데이터 생성:
  - API 요청 또는 로그 생성 등의 작업으로 데이터가 생성됩니다.
  - 데이터를 특정 토픽에 전송하며, 각 메시지에는 **키(Key)**가 포함될 수 있습니다.
1. Partition 선택 및 데이터 전송:
  - 프로듀서는 데이터가 저장될 파티션을 선택합니다.
    - 키가 있으면 해싱(Hashing) 기반으로 파티션 선택.
    - 키가 없으면 Round Robin 방식으로 파티션 분배.
1. Broker 데이터 저장:
  - 선택된 브로커가 데이터를 수신하여 디스크에 저장합니다.
  - 데이터는 **로그 세그먼트(log segment)**라는 파일 단위로 관리됩니다.
  - 복제를 통해 다른 브로커에 데이터를 복사하여 장애에 대비합니다.
1. Consumer 데이터 읽기:
  - 컨슈머는 특정 토픽을 구독하여 데이터를 읽습니다.
  - 컨슈머 그룹 내에서 파티션을 나눠 병렬로 처리합니다.
1. Consumer 데이터 처리:
  - 데이터를 읽어 애플리케이션에서 처리(예: 데이터베이스 저장, 분석 등)합니다.
  - 처리된 데이터는 Ack(확인 신호)를 보내 처리 완료를 알립니다.
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/07b43113-fe9f-4804-80f9-7a19791b2871/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466YYHI45RR%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015708Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIBvA5%2BPFFeDxz23lVEx%2BFp2M9Or2886E7NJL7v2C%2FbByAiAMnoWW4EdS%2Fucd2df93L5vzSric32%2Bb5LYETaOOpKVxyqIBAjC%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMd8doc1glBpZL%2F82oKtwDVzAp0A3tI3JwUmElRP4n0ekyve%2FxW4aoxbRlUocFVZ1D62jwQAJ4MQvcMu8eaPr66snZM0hT%2BpFn8j1jbdkkGo%2BnrG2GblYkixJ%2FTFFjeh3bIeoHpulCqX8HFK2CKTHVRql6fuk%2BcDYr9Jc2oU%2FvADPS4pynkNMoy%2F6YT%2BeSkr7LM3hGQGtRpYlyosfxq79pDrcwOlNI%2FqExuqVlX0ttVXMxHrtv9LPBxr%2BpALxliGqM3aZgem%2BoyLsCXAPDCrcu8tLKZ%2FZp%2BQyCiVAO9gnyJE4JpAM0x8VFZ%2BPnuA5d9XxTKGw%2BMlwGjzGOSmS528RC7%2BIjG3zYFYON1BvEZf9kzeyAail2czxue%2BNQFRL3jj7uMBT2UapamCgO2tkKIdj%2BVP%2B8ffncg13LilKh4uSo9KHkBtyw21KH4Jqn0oWh%2BxNFqA7caV%2FPZHffbFTW1XvLfbPRdDRMdfmYKF725qAPSFsAxpenazbaTPx%2F9obojZiGFYBqx7WwqjI9evOY9s0KnC7Z9M4pa%2B5kbJHBnd5G5GyZ4UkIYfYzwZf0WvZNY7rTjerWBFgrqSW5mu7z3qD56TFXphCIt4bSIZzshbq24OnNUlQ0ttXLnffyXKwZ1SvI6rF4RRnliuU6MlYwk4OpyQY6pgG40zvyDFW0pHQFrUeK%2BvMRGCvGnX0%2Bs3uolxpUxtcJ9oNsfXf4i143d6c8U1460gUAzKnDsjMrrPYSv4AqEgoVqabw%2Bg8OzQmQcrkQA8fTDYoG7dKIVElJx%2BLxmcgYBoAuvSqBoIKe9jQW%2Fc6WJpfuNJ3TIW7c6R4Q6JhREoOjSmZf3OpKVZNzdiAV1Hq2Pfz1rUWNP2FgjLDEobSd1swVuSJFKpiL&X-Amz-Signature=83d5f6069dd4dc1445b16683ced063f909b793fda8feada02d08d7f79584a9e1&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

### 카프카 구성 요소

Topic

- 각각의 메시지를 목적에 맞게 구분할 때 사용한다.
- 메시지를 전송하거나 소비할 때 Topic을 반드시 입력한다.
- Consumer는 자신이 담당하는 Topic의 메시지를 처리한다.
- 한 개의 토픽은 한 개 이상의 파티션으로 구성된다.
Partition

- 분산 처리를 위해 사용된다.
- Topic 생성 시 partition 개수를 지정할 수 있다. (파티션 개수 변경 가능. *추가만 가능)
- 파티션이 1개라면 모든 메시지에 대해 순서가 보장된다.
- 파티션 내부에서 각 메시지는 offset(고유 번호)로 구분된다.
- 파티션이 여러개라면 Kafka 클러스터가 라운드 로빈 방식으로 분배해서 분산처리되기 때문에 순서 보장 X
- 파티션이 많을 수록 처리량이 좋지만 장애 복구 시간이 늘어난다.
Offset

- 컨슈머에서 메세지를 어디까지 읽었는지 저장하는 값
- 컨슈머 그룹의 컨슈머들은 각각의 파티션에 자신이 가져간 메시지의 위치 정보(offset) 을 기록
- 컨슈머 장애 발생 후 다시 살아나도, 전에 마지막으로 읽었던 위치에서부터 다시 읽어들일 수 있다.
Producer

- 메시지를 만들어서 카프카 클러스터에 전송한다.
- 메시지 전송 시 Batch 처리가 가능하다.
- key값을 지정하여 특정 파티션으로만 전송이 가능하다.
- 전송 acks값을 설정하여 효율성을 높일 수 있다.
- ACKS=0 -> 매우 빠르게 전송. 파티션 리더가 받았는 지 알 수 없다.
- ACKS=1 -> 파티션 리더가 받았는지 확인. 기본값
- ACKS=ALL -> 파티션 리더 뿐만 아니라 팔로워까지 메시지를 받았는 지 확인
Consumer

- 카프카 클러스터에서 메시지를 읽어서 처리한다.
- 메세지를 Batch 처리할 수 있다.
- 한 개의 컨슈머는 여러 개의 토픽을 처리할 수 있다.
- 메시지를 소비하여도 메시지를 삭제하지는 않는다. (Kafka delete policy에 의해 삭제)한 번 저장된 메시지를 여러번 소비도 가능하다.
- 컨슈머는 컨슈머 그룹에 속한다.
- 한 개 파티션은 같은 컨슈머그룹의 여러 개의 컨슈머에서 연결할 수 없다.
Broker

- 실행된 카프카 서버를 말한다.
- 프로듀서와 컨슈머는 별도의 애플리케이션으로 구성되는 반면, 브로커는 카프카 자체이다.
- Broker(각 서버)는 Kafka Cluster 내부에 존재한다.
- 서버 내부에 메시지를 저장하고 관리하는 역할을 수행한다.
Zookeeper

- 분산 애플리케이션 관리를 위한 코디네이션 시스템
- 분산 메시지큐의 메타 정보를 중앙에서 관리하는 역할
