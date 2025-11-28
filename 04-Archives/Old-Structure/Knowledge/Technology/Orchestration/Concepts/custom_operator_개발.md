---
title: custom operator 개발
created: 2024-06-11
tags: ["reference", "migrated", "resource", "airflow"]
PARA: Resource
구분: ["Airflow"]
---

# custom operator 개발

## 📝 내용

너무 좋은데 러닝 커브가 있다는게 단점이에요.

그리고 custom operator 만들어달라는 요구가 들어오는 것도 무서워요.

'우리팀만' 사용하면 airflow 2.0의 taskflow api로 멋있게 만들겠지만

구축 후 운영을 고려한다면 python operator 보다는 custom operator만 오픈하는 것을 추천합니다.

custom opreator 만들고 .output으로 값 호출

add >> multiply >> use_cat_fact_hook(multiply.output)

## 🏷️ 분류

- **PARA**: Resource
- **구분**: Airflow

## 🔗 연결

**Hub**: [[_HUB_Data_Engineering]], [[_HUB_Python]]

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
