---
title: ref source 차이
type: resource
tags:
  - dbt
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

## 개념

- source와 ref 둘다 데이터 Lineage를 생성함
- source는 쿼리 순서에 상관 없음. ref는 ref를 하는 순서에 따라서 자동으로 쿼리의 순서가 정해져서 실행됨.
## 목적

- DBT Lineage 자동 생성 확인

---

## 📎 Related

### Technology

- [[dbt|DBT]] - DBT 개요 및 Qraft 적용 사례
- [[DataHub|DataHub]] - DBT Lineage 추적

