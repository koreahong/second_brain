---
title: alembic ini 설정
type: resource
tags:
- Alembic
- DB
---

## 개념

- alembic.ini 파일을 활용한 다중 database 처리
## 목적

- database 마다 alembic 버전관리를 따로 해야함
## 서칭내용

```sql
-- alembic.ini 파일

아래 [ ] 로 감싼 부분은 커스터마이징한 부분임.
대상 스키마로 정의한 내용이고, 각 스키마마다 version_locations 디렉토리에
파일 버전이 생성된다.

[aace_mart]
schema_name = aace_mart
script_location = alembic
version_locations = alembic/aace_mart

[cafe24_api]
schema_name = cafe24_api
script_location = alembic
version_locations = alembic/cafe24_api

[aivelabs_sv]
schema_name = cafe24_api
script_location = alembic
version_locations = alembic/aivelabs_sv
```

alembic.ini 파일의 내용은 context.config(from alembic import context)로 가져올 수 있음