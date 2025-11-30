---
title: sqlalchemy 사용법
type: resource
tags:
  - python
  - technology
  - sql
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

## 개념

- sqlalchemy 사용법
## 목적

- 개념이 필요하게 된 배경을 작성할 것
## 서칭내용

- DB와 다른 이름으로 컬럼을 사용하고 싶을 경우
  ```sql
  discount_information_amount_discount = Column(
      "real column name on Database schema",
      Float,
      nullable=True,
      key="rename column name to use another name"
  )
  ```

  컬럼명에 특수기호가 들어갈 경우, “.” 과 같은, python에서 핸들링하기가 어려워짐.

  그럴 경우 key값에 python 코드로 핸들링할 경우를 별도로 이름을 지어줄 수 있다.

- default를 사용할 때 주의사항
  ```python
  ## default가 CURRENT_TIMESTAMP를 적용할 경우
  etltime = Column(
      Timestamp(timezone=True),
      nullable=True,
      server_default=text("CURRENT_TIMESTAMP"),
  )
  
  ## default가 CURRENT_TIMESTAMP를 문자 자체로 적용할 경우, 따옴표 추가
  etltime = Column(
      Timestamp(timezone=True),
      nullable=True,
      server_default=text("'CURRENT_TIMESTAMP'"),
  )
  ```

---

## 📎 Related

### Technology

- [[ORM|ORM]] - ORM 개념
- [[alembic|Alembic]] - SQLAlchemy와 함께 사용되는 마이그레이션 도구

