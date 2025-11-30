---
title: keycloak으로 Dag 권한관리 (리다이렉트)
type: resource
tags:
  - keycloak
  - airflow
  - rbac
  - access-control
  - dag-permissions
  - sso
  - redirect
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: redirect
maturity: 0
---

# ⚠️ 문서가 분리되었습니다

이 문서는 응집도 개선을 위해 **개념-구현-운영** 3개의 문서로 분리되었습니다.

---

## 📚 새로운 문서 구조

### 1. 개념 이해 (Why & What)
**[[Keycloak-Airflow-인증-개념]]**

다음을 알고 싶다면:
- Keycloak, JWT, Auth Manager가 무엇인가?
- 전체 아키텍처와 인증 흐름은 어떻게 되는가?
- 왜 이렇게 동작하는가?

### 2. 코드 구현 (How - Technical)
**[[Keycloak-Airflow-구현]]**

다음을 알고 싶다면:
- CustomKeycloakAuthManager 실제 코드는?
- JWT 디코딩, DAG 권한 체크는 어떻게 구현했는가?
- sync_keycloak_groups DAG 코드는?

### 3. 운영 가이드 (How - Usage)
**[[Keycloak-Airflow-운영가이드]]**

다음을 알고 싶다면:
- 환경 변수 설정 방법은?
- DAG에 team 태그를 어떻게 추가하는가?
- 문제가 생겼을 때 어떻게 해결하는가?

---

## 🔗 빠른 링크

| 목적 | 문서 |
|------|------|
| 시스템 이해 | [[Keycloak-Airflow-인증-개념\|개념]] |
| 코드 분석 | [[Keycloak-Airflow-구현\|구현]] |
| 실제 사용 | [[Keycloak-Airflow-운영가이드\|운영가이드]] |

---

## 📎 Related

### Projects 배경 (Why)
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/Keycloak-SSO-도입-배경|Keycloak-SSO-도입-배경]] - 왜 Keycloak을 도입했는가

### Related Technology
- [[Airflow-3.0-구현]] - Airflow 3.0 Custom Auth Manager와의 통합
