---
title: sqlalchemy type 주의사항
type: resource
tags:
  - technology
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

## 개념

- 개념에 대해서 한 줄로 작성하되, 반드시 내가 스스로 정리한 말로 작성할 것
## 목적

- 개념이 필요하게 된 배경을 작성할 것
## 서칭내용

- timestamptz 타입에는 null이 들어가는 경우에 NaT로 변환이 되서 error가 발생하는 경우가 있음
그럴 경우에는 text 타입으로 컬럼을 설정하고, 사용할때 ::timestamptz를 붙여서 사용하는게 좋음

---

## 📎 Related

### Technology

- [[ORM|ORM]] - ORM 개념
- [[postgres|PostgreSQL]] - SQLAlchemy가 사용하는 DB

