---
title: 'airflow, grafana 연동'
type: resource
tags:
  - airflow
  - grafana
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

## 개념

- grafana는 서버 리소스 및 사용자 정의 지표를 대시보드로 보여주는 서비스임
## 목적

- airflow에서 보여주는 대시보드에 더해서 전체적인 뷰로 dag를 관리하기 위함
## 서칭내용

1. grafana에 log를 전달하는 구조
  1. airflow에서 statsd 라이브러리를 활용해서 metrics 데이터를 생성
  1. metrics데이터를 export
  1. export한 데이터를 파라메타우스로 모니터링 서버에서 가져감
  1. 파라메타우스와 grafana 연결해서 데이터 import
  1. import한 데이터를 대시보드에 사용
1. airflow 설정
  1. airflow.cfg 설정
    ```sql
    [metrics]
    statsd_on = True
    statsd_host = statsd-exporter ## airflow와 같은 docker network를 사용하는 컨테이너 지정
    statsd_port = 8125
    statsd_prefix = airflow
    ```

  1. docker compose 수정
    ```sql
    RUN pip install 'apache-airflow[statsd]'
    ```

  1. statsd-exporter 컨테이너 생성
    ```sql
    FROM prom/statsd-exporter:latest
    
    COPY ./statsd_mapping.yaml /opt/statsd_mapping.yaml
    
    
    sudo docker build -t statsd-exporter -f statsd_dockerfile . && \
    sudo docker run -d --name statsd-exporter --network=ubuntu_default -p 9102:9102 -p 9125:9125 -p 9125:9125/udp statsd-exporter --statsd.listen-udp=:9125 --web.listen-address=:9102 --log.level=debug --statsd.mapping-config=/opt/statsd_mapping.yaml
    ```

  1. airflow 재설치

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

