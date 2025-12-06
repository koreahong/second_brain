---
notion_id: 2bdc6d43-3b4d-80f9-9a8e-c417026a4623
content_type: Insight
created: "2025-12-02T02:52:00.000Z"
updated: "2025-12-05T12:32:00.000Z"
company: 크레프트테크놀로지스
period: 2025-12-01
category:
  - Reflection
---

# Untitled

MCP - dbt, airflow, context7, snowflake등 활용

MCP 세팅하여, claude code를 통한 개발 및 유지보수 환경을 최적화

agent, hook 등에 대한 아키텍쳐 구현

각 agent를 관리하는 중앙 agent를 만들고, 각 분야의 expert agent 생성 → 토큰 사용량 줄이고, 효율 Up

jira, confluence 문서 자동화 구축

---

LSEG snowflake 데이터 CDC
사용자 1명으로 계약해서 사원들이 원천을 보면 안되고 CDC한 자체 테이블을 바라보게 해야함. 매일 1000개 테이블 마이그레이션 프로세스 추가.

작년에는 해당 문제로 인해서 20명분 이상의 비용지출을 추가로 해서 손실이 많이 발생함.

원본에 대한 key column 중심으로 dbt delete+insert 증분형태로 작성. 

데이터계약 제약조건 컴플라이언스를 지켜야 하는 상황임

---

