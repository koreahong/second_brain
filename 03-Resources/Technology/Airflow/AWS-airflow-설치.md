---
title: AWS airflow 설치
type: resource
tags:
  - airflow
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

1. docker-compose.yaml 다운로드
  ```javascript
  curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.1/docker-compose.yaml'
  ```

1. docker-compose 기본세팅값 변경
  ```javascript
  수정:
  AIRFLOW__CORE__LOAD_EXAMPLES: 'true'
  
  기존:
  AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
  
  
  -------------------------------------------------------
  
  수정:
  build .
  
  기존:
  # build .
  
  ```

1. airflow meta DB 세팅하기
  ```sql
  aivelabs 계정으로
  CREATE USER airflow WITH PASSWORD 'airflow' CREATEDB CREATEROLE;
  
  airflow 계정으로
  CREATE SCHEMA airflow;
  
  ```

1. 서버에 docker 설치
  ```sql
  sudo apt-get install docker.io
  sudo apt-get install docker-compose
  ```

1. docker compose 실행
  ```sql
  접속확인
  http://aice-front-dev.s3-website.ap-northeast-2.amazonaws.com:8080 
  ```

1. 용량증설
  ```sql
  sudo growpart /dev/xvda 1
  
  sudo resize2fs /dev/root
  ```

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

