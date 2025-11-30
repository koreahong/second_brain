---
title: postgres / snowflake 권한관리 (리다이렉트)
date: '2025-10-10'
type: project
status: redirect
tags:
  - postgres
  - snowflake
  - sql
  - aws
  - redirect
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
maturity: 0
---

# ⚠️ 문서가 분리되었습니다

이 문서는 응집도 개선을 위해 **주제별** 3개의 문서로 분리되었습니다.

---

## 📚 새로운 문서 구조

### 1. Storage Integration (S3 연결)
**[[03-Resources/Technology/Snowflake/Snowflake-Storage-Integration|Snowflake Storage Integration]]**

다음을 알고 싶다면:
- S3와 Snowflake를 어떻게 연결하는가?
- File Format, Storage Integration, External Stage 생성 방법은?
- LIST vs DIRECTORY 차이는?

### 2. RBAC 개념 및 패턴
**[[03-Resources/Technology/Snowflake/Snowflake-RBAC-가이드|Snowflake RBAC 가이드]]**

다음을 알고 싶다면:
- Snowflake RBAC는 무엇인가?
- Domain-based Role을 어떻게 설계하는가?
- 사용자 및 권한 관리 방법은?

### 3. 실제 적용 (Alembic Migration)
**[[Snowflake-권한-마이그레이션]]**

다음을 알고 싶다면:
- qraft_origin 데이터베이스의 실제 RBAC 구현 코드는?
- Alembic Migration으로 어떻게 권한을 관리하는가?
- Upgrade/Downgrade 코드는?

---

## 🔗 빠른 링크

| 목적 | 문서 |
|------|------|
| S3 연결 | [[03-Resources/Technology/Snowflake/Snowflake-Storage-Integration\|Storage Integration]] |
| RBAC 개념 | [[03-Resources/Technology/Snowflake/Snowflake-RBAC-가이드\|RBAC 가이드]] |
| 실제 적용 | [[Snowflake-권한-마이그레이션\|권한 마이그레이션]] |

---

## 📎 Related

### Related Projects
- [[원천-데이터-적재-파이프라인-개발]] - 데이터 파이프라인 인프라
- [[jira,-keycloak-권한-자동화]] - 통합 권한 관리 자동화
