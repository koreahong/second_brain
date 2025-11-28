---
title: data medaillon
created: 2025-11-28
tags: ["reference", "migrated", "resource"]
PARA: Resource
구분: []
---

# data medaillon

## 📝 내용

## 📌 Medallion Architecture: What, Why, How 요약

### 1. What (무엇인가?)

- Medallion Architecture = 레이어 기반 데이터 구조

- 데이터를 Bronze → Silver → Gold 단계로 점차 정제 및 가공

- 각 레이어는 서로 다른 목적과 품질 수준을 가짐

### 2. Why (왜 필요한가?)

- 데이터 품질 문제 해결:

- 투명성:

- 유연성:

- 효율성:

### 3. How (어떻게 구현하는가?)

### 🥉 Bronze Layer

- 역할: 원천(raw) 데이터를 그대로 저장

- 특징: 최소 가공, 보존성 강조

- 예시: API dump, 로그, 센서 데이터, CSV 파일

### 🥈 Silver Layer

- 역할: 브론즈 데이터를 정제하고 구조화

- 작업:

- 결과: 신뢰할 수 있는 단일 소스(Cleaned & Standardized Data)

### 🥇 Gold Layer

- 역할: 비즈니스 친화적인 데이터

- 작업:

- 결과: BI 보고서, 대시보드, 모델 학습에 바로 쓰이는 데이터

### 4. 실무적 Best Practice

- 파이프라인 자동화:

- 거버넌스 통합:

- 유스케이스:

## ✅ 한 줄 요약

Medallion Architecture는 데이터를 Bronze(원본) → Silver(정제) → Gold(비즈니스 최적화) 단계로 점진적으로 가공하여 품질, 신뢰성, 재사용성을 보장하는 데이터 아키텍처 패턴입니다.

- What: 레이어드 아키텍처

- Why: 데이터 품질·투명성·효율성 확보

- How: 단계별 가공 (Raw → Clean → BI/ML)

## 🏷️ 분류

- **PARA**: Resource
- **구분**: 없음

## 🔗 연결

**Hub**: [[_HUB_Learning]], [[_HUB_Data_Architecture]]

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
