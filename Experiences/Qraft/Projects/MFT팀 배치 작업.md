---
type: qraft-experience
category: projects
title: MFT팀 배치 작업
imported: 2025-11-28
notion_id: 271c6d43-3b4d-807e-9f34-da2e73bf1f12
---

# MFT팀 배치 작업





### 원천 파악

- 원천 - 테이블 정의서


### alembic 구성

- data modeling
- 원천 → stage


### 배치개발

- airflow






krx_stocks는 매일 수정주가를 반영해야하는데 이는 모든 raw데이터가 대상임.

현재 1000만 raw정도 되고 이를 매일 업데이트 하기 위해서 성능 최적화가 필요함.



alembic / sqlalchemy 수정

- daily 추가
- raw 테이블 파티셔닝 추가
- stocks mv 생성


stocks raw에 데이터 넣기 



daily → raw 배치 확인하기



휴장체크를 어떻게 하지? → 화-토 배치 주기 설정



