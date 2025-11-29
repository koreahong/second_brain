---
title: "AWS airflow 설치"
source: notion
notion_id: 90f727d7-18db-4a09-9f23-5488ea095468
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["Airflow"]
링크: []
최종편집시각: "2025-09-13T03:53:00.000Z"
제목: ""
상위 항목: ["26dc6d43-3b4d-80f7-a162-ed9945c8906b"]
날짜: "2024-06-10"
PARA: "Resource"
tags: ["레퍼런스", "Airflow", "notion-import"]
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

