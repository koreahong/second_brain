---
title: "sqlalchemy type 주의사항"
source: notion
notion_id: 157c6d43-3b4d-8058-a9e8-eda24773fe8a
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: []
링크: []
최종편집시각: "2024-12-09T15:16:00.000Z"
제목: ""
상위 항목: []
tags: ["레퍼런스", "notion-import"]
---

## 개념

- 개념에 대해서 한 줄로 작성하되, 반드시 내가 스스로 정리한 말로 작성할 것
## 목적

- 개념이 필요하게 된 배경을 작성할 것
## 서칭내용

- timestamptz 타입에는 null이 들어가는 경우에 NaT로 변환이 되서 error가 발생하는 경우가 있음
그럴 경우에는 text 타입으로 컬럼을 설정하고, 사용할때 ::timestamptz를 붙여서 사용하는게 좋음
