---
title: data medaillon
type: resource
tags:
- anger
- pipeline
- anxiety
- data
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

## 📌 Medallion Architecture: What, Why, How 요약

### 1. What (무엇인가?)

- Medallion Architecture = 레이어 기반 데이터 구조
- 데이터를 Bronze → Silver → Gold 단계로 점차 정제 및 가공
- 각 레이어는 서로 다른 목적과 품질 수준을 가짐
---

### 2. Why (왜 필요한가?)

- 데이터 품질 문제 해결:
  - 원본 데이터를 그대로 쓰면 품질 불안정 → 신뢰성 문제
  - 중복/결측/이상치 제거 후에야 분석과 AI/ML에 활용 가능
- 투명성:
  - 각 단계별로 데이터가 어떻게 변환되는지 추적(Lineage) 가능
- 유연성:
  - 원본(Bronze)을 보존하기 때문에, 필요 시 새로운 규칙으로 재처리 가능
- 효율성:
  - 최종 사용자(분석가, BI, 데이터 사이언티스트)는 Gold 레이어만 활용 → 생산성↑
---

### 3. How (어떻게 구현하는가?)

### 🥉 Bronze Layer

- 역할: 원천(raw) 데이터를 그대로 저장
- 특징: 최소 가공, 보존성 강조
- 예시: API dump, 로그, 센서 데이터, CSV 파일
### 🥈 Silver Layer

- 역할: 브론즈 데이터를 정제하고 구조화
- 작업:
  - 중복 제거, 결측값 처리
  - 스키마 표준화
  - 다른 소스와 조인
- 결과: 신뢰할 수 있는 단일 소스(Cleaned & Standardized Data)
### 🥇 Gold Layer

- 역할: 비즈니스 친화적인 데이터
- 작업:
  - 집계(Aggregation)
  - KPI 계산
  - 머신러닝 학습용 Feature Store 준비
- 결과: BI 보고서, 대시보드, 모델 학습에 바로 쓰이는 데이터
---

### 4. 실무적 Best Practice

- 파이프라인 자동화:
  - Delta Lake, Apache Spark, Databricks Workflow 활용
- 거버넌스 통합:
  - 각 레이어별 데이터 접근 제어, 품질 규칙 관리
- 유스케이스:
  - 금융(거래 로그 → 고객 행동 분석)
  - 리테일(구매 데이터 → 추천 모델)
  - 제조업(센서 데이터 → 예지 보수 모델)
---

## ✅ 한 줄 요약

Medallion Architecture는 데이터를 Bronze(원본) → Silver(정제) → Gold(비즈니스 최적화) 단계로 점진적으로 가공하여 품질, 신뢰성, 재사용성을 보장하는 데이터 아키텍처 패턴입니다.

- What: 레이어드 아키텍처
- Why: 데이터 품질·투명성·효율성 확보
- How: 단계별 가공 (Raw → Clean → BI/ML)

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

