---
title: Trino
created: 2025-11-28
tags: ["reference", "migrated", "resource", "trino"]
PARA: Resource
구분: ["Trino"]
---

# Trino

## 📝 내용

## 🔹 Trino

- 엔진 본연의 역할: 단순히 SQL을 여러 데이터 소스에 분산 처리해서 결과를 내는 것

- 데이터 가속화/캐시: 기본 제공 ❌

- 👉 즉, “빠르게 해주는” 기능은 사용자가 직접 세팅해야 함

## 🔹 Dremio

- 엔진 + 플랫폼 성격이라서

- Reflections라는 기능이 있음 → 일종의 자동 materialized view

- 👉 리서처/분석가 입장에서는 “쿼리 속도가 눈에 띄게 빨라지는 효과”

## ✅ 요약

- Trino: 쿼리 가속화 기능 없음 → 매번 원본 데이터 읽음 → 대신 오픈소스 + 확장성 강점

- Dremio: Reflections로 캐시/요약을 자동 관리 → 같은 쿼리는 훨씬 빠르게 응답

👉 그래서 리서처 중심 조직에서는 “아무것도 안 해도 빠른 게 좋다” → Dremio 유리

👉 엔지니어링 팀이 있고 “우리가 직접 최적화할게” → Trino 유리

## 🏷️ 분류

- **PARA**: Resource
- **구분**: Trino

## 🔗 연결

**Hub**: [[_HUB_Database]], [[_HUB_Analytics]], [[_HUB_Data_Architecture]]

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
