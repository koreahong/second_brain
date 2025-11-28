---
title: personalize
created: 2024-08-07
tags: ["reference", "migrated", "resource", "aws"]
PARA: Resource
구분: ["AWS"]
---

# personalize

## 📝 내용

# Neurons

# References

aws personalize는 추천테마가 3가지가 있음

- e-commerce: 상품 - 유저

- video: 콘텐츠-유저, 넷플릭스 같은 콘텐츠 추천

- custom: 도메인 종속 X, 사용자가 모든 컬럼 결정

레시피: aws가 개발한 알고리즘

솔루션: 데이터 셋 * 레시피 ⇒ 학습된 모델

캠페인: 솔루션을 실제로 사용할 수 있게 배포한 것

평가지표

- HR@10 (Hit Rate at 10): 추천된 상위 10개의 아이템 중 사용자가 실제로 상호작용한 아이템의 비율입니다.

- ARHR@10 (Average Reciprocal Hit Rate at 10): 상위 10개의 아이템 중 사용자 상호작용 아이템의 위치에 기반한 평균 역순 점수입니다.

- NDCG@10 (Normalized Discounted Cumulative Gain at 10): 추천된 상위 10개의 아이템의 순서에 따른 가중치를 부여하여 모델의 성능을 평가한 점수입니다.

- Precision@10: 추천된 상위 10개의 아이템 중 실제로 사용자가 상호작용한 아이템의 비율입니다.

- Coverage@10: 전체 아이템 중 추천된 아이템의 비율입니다.

## 🏷️ 분류

- **PARA**: Resource
- **구분**: AWS

## 🔗 연결

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
