---
title: Keycloak-Airflow 인증 개념
type: resource
tags:
  - keycloak
  - airflow
  - sso
  - authentication
  - jwt
  - oidc
  - auth-manager
  - rbac
created: '2025-11-30'
updated: '2025-11-30'
aliases:
  - Keycloak Airflow Authentication Concept
status: evergreen
maturity: 3
---
# Keycloak-Airflow 인증 개념

## 📌 개요

Airflow 3.x와 Keycloak SSO를 통합한 인증 시스템의 기본 개념과 아키텍처를 설명합니다.

## 🎓 핵심 개념

### Keycloak이란?

오픈소스 Identity and Access Management (IAM) 솔루션

**주요 기능:**
- **SSO (Single Sign-On)**: 한 번 로그인하면 여러 애플리케이션 접근
- **OAuth 2.0 / OpenID Connect**: 표준 프로토콜 지원
- **사용자/그룹/역할 관리**: 중앙화된 권한 관리

### JWT (JSON Web Token)

Keycloak이 발급하는 인증 토큰

```json
{
  "sub": "user-id",
  "email": "user@qraft.ai",
  "groups": ["/airflow/ML Platform (T)"],
  "realm_access": {
    "roles": ["airflow", "user"]
  },
  "exp": 1704067200
}
```

**구조:**
```
Header.Payload.Signature
```

### Auth Manager (Airflow 3.x)

Airflow의 인증/권한 시스템 플러그인 인터페이스

**종류:**
- 기본: FAB (Flask App Builder) Auth Manager
- Keycloak: 공식 Keycloak Auth Manager (Airflow 3.0+)
- 커스텀: CustomKeycloakAuthManager (이 프로젝트)

**주요 메서드:**
- `is_logged_in()`: 로그인 여부
- `is_authorized_dag()`: DAG 접근 권한
- `get_authorized_dag_ids()`: 접근 가능한 DAG 목록
- `is_authorized_configuration()`: Admin 설정 권한

## 🏗️ 아키텍처

### 전체 구조

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Browser   │─────▶│   Keycloak   │◀────▶│  Snowflake  │
│             │◀─────│  (Auth Server)│      │  (직원정보)  │
└─────────────┘      └──────────────┘      └─────────────┘
       │                     │                      │
       │ 1. Login           │ 2. JWT Token         │
       ▼                     ▼                      │
┌────────────────────────────────────────┐          │
│         Airflow Webserver              │          │
│  ┌──────────────────────────────────┐  │          │
│  │ CustomKeycloakAuthManager        │  │          │
│  │                                  │  │          │
│  │  3. JWT 디코드 → 그룹 추출      │  │          │
│  │  4. DAG team 태그 확인          │  │          │
│  │  5. 권한 매칭 → 접근 허용/거부  │  │          │
│  └──────────────────────────────────┘  │          │
└────────────────────────────────────────┘          │
                    ▲                                │
                    │ 매일 새벽 1시                 │
                    │                                │
            ┌───────────────────┐                    │
            │ sync_keycloak_    │───────────────────┘
            │ groups DAG        │  5. 그룹/멤버 동기화
            └───────────────────┘
```

### 인증 흐름

#### Step 1: 사용자 로그인

1. 사용자가 Airflow UI 접속 (http://localhost:8080)
2. CustomKeycloakAuthManager가 Keycloak 로그인 페이지로 리다이렉트
3. 사용자가 Keycloak에서 이메일/비밀번호 입력
4. Keycloak가 JWT Access Token 발급
   - Token 안에 포함된 정보:
     - `groups`: ["/airflow/ML Platform (T)", "/airflow/AI Product (T)"]
     - `realm_access.roles`: ["airflow", "user"]
     - `email`: "user@qraft.ai"

#### Step 2: JWT 토큰 디코딩 및 그룹 추출

```
JWT Token
    ↓
JWT 디코드 (서명 검증 없이 - 이미 Keycloak에서 인증됨)
    ↓
groups 클레임 추출: ["/airflow/ML Platform (T)", "/airflow/AI Product (T)"]
    ↓
경로에서 마지막 부분만 추출: ["ML Platform (T)", "AI Product (T)"]
    ↓
역할(roles)도 함께 추출: ["airflow", "user"]
    ↓
최종 사용자 그룹: ["ML Platform (T)", "AI Product (T)", "airflow", "user"]
```

#### Step 3: DAG 접근 권한 확인

```
DAG 접근 요청
    ↓
Admin 확인? → Yes → 모든 권한 허용
    ↓ No
DELETE 메서드? → Yes → 거부 (Admin만 가능)
    ↓ No
DAG의 team 태그 추출: ["team:ML Platform (T)"]
    ↓
Team 태그 없음? → Yes → 모든 인증된 사용자 접근 가능
    ↓ No
사용자 그룹과 DAG 팀 매칭
    ↓
매칭됨? → Yes → 접근 허용
    ↓ No
접근 거부
```

### DAG UI 필터링 원리

일반 사용자가 DAG 목록을 볼 때의 처리 과정:

```
1. DB에서 모든 DAG 조회 (DagModel)
    ↓
2. Admin? → Yes → 모든 DAG 반환
    ↓ No
3. 각 DAG의 team 태그 확인
    ↓
4. 팀 태그 없음? → 사용자에게 표시
    ↓
5. 사용자 그룹과 매칭? → Yes → 사용자에게 표시
    ↓ No
6. 해당 DAG 숨김
```

**결과:** 사용자는 자신이 접근 가능한 DAG만 UI에서 볼 수 있음

### 자동 동기화 시스템

**목적:** Snowflake 직원 정보와 Keycloak 그룹을 자동으로 동기화

**실행 주기:** 매일 새벽 1시 (KST)

**동작 흐름:**

```
1. Snowflake에서 재직 직원 조회 (use_yn='Y')
   ↓
2. Keycloak Admin API 인증
   ↓
3. Keycloak에서 현재 그룹 구조 및 멤버 조회
   ↓
4. 변경사항 비교 및 반영:
   A. 신규 그룹 생성 (Snowflake에 있지만 Keycloak에 없는 department)
   B. 신규 멤버 추가 (신규 입사자)
   C. 퇴사자 제거 (Snowflake에 없지만 Keycloak에 있는 사용자)
   D. 팀 이동 처리 (이전 그룹 제거 + 새 그룹 추가)
   ↓
5. 통계 로깅 (신규 그룹, 멤버 추가, 멤버 제거, 팀 이동)
```

**동기화 예시:**

Snowflake 데이터:
- user1@qraft.ai | ML Platform (T)
- user2@qraft.ai | AI Product (T)  ← 이전에는 ML Platform (T)
- user3@qraft.ai | QT Dev (T)      ← 신규 입사

Keycloak 현재 상태:
- user1@qraft.ai | ML Platform (T)
- user2@qraft.ai | ML Platform (T)
- user4@qraft.ai | ML Platform (T)  ← 퇴사

동기화 결과:
- ✅ user2: ML Platform (T) 제거 → AI Product (T) 추가 (팀 이동)
- ✅ user3: 사용자 생성 + QT Dev (T) 추가 (신규)
- ✅ user4: ML Platform (T) 제거 (퇴사)

## 🔐 권한 정책

### Admin 판별 로직

Admin 조건 (OR):
1. `airflow` 역할 보유
2. `ML Platform (T)` 그룹 소속

**Admin 권한:**
- 모든 DAG 조회, 트리거, 수정, 삭제
- Admin 설정 접근
- 모든 사용자 정보 조회

**일반 사용자 권한:**
- 팀 태그와 매칭되는 DAG만 조회, 트리거, 수정
- 삭제는 불가

### DAG 접근 제어 규칙

| 상황 | 결과 |
|------|------|
| Admin 사용자 | 모든 DAG 접근 가능 |
| DAG에 team 태그 없음 | 모든 인증된 사용자 접근 가능 |
| DAG team 태그와 사용자 그룹 매칭 | 조회, 트리거, 수정 가능 (삭제는 Admin만) |
| 매칭 안됨 | 접근 거부 (UI에 표시 안됨) |

## 📊 Keycloak 그룹 구조

```
qraft (Realm)
└── airflow (Parent Group)
    ├── ML Platform (T)          # Admin 권한 그룹
    ├── AI Tech Lab (T)
    ├── AI Product (T)
    ├── AI Research (T)
    ├── QT Dev (T)
    ├── ATS Dev (T)
    ├── DL Dev (P)
    ├── DL TF (T)
    ├── HFT (T)
    ├── MFT (T)
    ├── APS (T)
    ├── Wealth Solution (T)
    ├── Product Strategy (T)
    ├── Strategic Planning (T)
    ├── Strategy (T)
    ├── Business Solution (D)
    ├── Business Administration (D)
    ├── Client Coverage (T)
    ├── HR (T)
    ├── Accounting (T)
    ├── Legal & Compliance (T)
    ├── Risk Managemnet (T)
    ├── AI Trading Solution (D)
    ├── QRAFT (HQ)
    └── QRAFT APAC (C)
```

총 25개 팀

## 🔄 시스템 특징

### 장점

1. **중앙화된 권한 관리**: Keycloak에서 한 곳에서 모든 권한 관리
2. **자동 동기화**: Snowflake 직원 정보 변경 시 자동 반영
3. **팀 기반 권한**: DAG에 `team:` 태그만 추가하면 자동 권한 제어
4. **SSO 통합**: 한 번 로그인으로 여러 시스템 접근 가능

### 제약사항

1. **팀 단위 권한**: 개별 사용자 단위 세밀한 권한은 불가 (향후 개선 필요)
2. **DELETE 권한**: Admin만 가능 (일반 사용자는 불가)
3. **하드코딩된 매핑**: TEAM_MAPPING이 코드에 하드코딩 (향후 개선 필요)

---

## 📎 Related

### Projects 배경 (Why)
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/Keycloak-SSO-도입-배경|Keycloak-SSO-도입-배경]] - 왜 Keycloak SSO를 도입했는가

### Technology (Core Concepts)
- [[Keycloak-OIDC-인증]] - OIDC 프로토콜 상세 설명
- [[Airflow]] - Airflow 기본 개념

### Technology (Implementation)
- [[Keycloak-Airflow-구현]] - CustomKeycloakAuthManager 실제 코드 구현
- [[Airflow-3.0-구현]] - Airflow 3.0 플랫폼과의 통합

### Operational (Usage)
- [[Keycloak-Airflow-운영가이드]] - 설정 방법, DAG 태깅, 문제 해결

### Projects (실제 사용)
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/팀별-데이터-격리-체계|팀별-데이터-격리-체계]] - 팀별 권한 격리 전략

---

## 📚 참고 자료

- Keycloak 공식 문서: https://www.keycloak.org/docs/latest/
- Airflow Auth Manager: https://airflow.apache.org/docs/apache-airflow/stable/security/auth-manager.html
- Airflow Keycloak Provider: https://airflow.apache.org/docs/apache-airflow-providers-keycloak/

---

**Metadata:**
