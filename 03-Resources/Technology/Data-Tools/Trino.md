---
title: Trino
type: resource
tags:
  - trino
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

## 🔹 Trino

- 엔진 본연의 역할: 단순히 SQL을 여러 데이터 소스에 분산 처리해서 결과를 내는 것
- 데이터 가속화/캐시: 기본 제공 ❌
  - 매번 쿼리할 때마다 → Iceberg/Parquet 파일을 직접 읽음
  - 속도를 높이려면 외부에 따로 캐시 계층(예: materialized view, Presto-on-Spark, Alluxio)이나 데이터 레이아웃 최적화(파티션 설계, 파일 크기 튜닝)를 해야 함
- 👉 즉, “빠르게 해주는” 기능은 사용자가 직접 세팅해야 함
---

## 🔹 Dremio

- 엔진 + 플랫폼 성격이라서
- Reflections라는 기능이 있음 → 일종의 자동 materialized view
  - 자주 쓰는 쿼리 결과를 미리 요약/저장해두고, 다음에 같은 쿼리(or 비슷한 패턴)가 오면 캐시된 데이터로 빠르게 응답
  - 사용자는 그냥 SQL만 날리면 되고, 내부적으로 Reflections가 알아서 대체 실행
- 👉 리서처/분석가 입장에서는 “쿼리 속도가 눈에 띄게 빨라지는 효과”
---

## ✅ 요약

- Trino: 쿼리 가속화 기능 없음 → 매번 원본 데이터 읽음 → 대신 오픈소스 + 확장성 강점
- Dremio: Reflections로 캐시/요약을 자동 관리 → 같은 쿼리는 훨씬 빠르게 응답
---

👉 그래서 리서처 중심 조직에서는 “아무것도 안 해도 빠른 게 좋다” → Dremio 유리

👉 엔지니어링 팀이 있고 “우리가 직접 최적화할게” → Trino 유리

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

