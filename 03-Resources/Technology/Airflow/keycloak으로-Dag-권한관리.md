---
title: keycloak으로 Dag 권한관리
type: resource
---

# Airflow Keycloak 인증 & 권한 관리 시스템

## 📌 핵심 요약 (TL;DR)

### 무엇을 했나?

- Airflow 3.x에 Keycloak SSO 인증 통합
- DAG의 team 태그 기반으로 자동 권한 제어
- Snowflake 직원 정보와 Keycloak 그룹 자동 동기화
### 주요 기능

1. 커스텀 Auth Manager: DAG에 team:ML Platform (T) 태그만 추가하면 해당 팀만 접근 가능
1. 자동 그룹 동기화: 매일 새벽 1시 Snowflake ↔ Keycloak 자동 동기화 (신규 입사, 퇴사, 팀 이동)
1. 역할 기반 권한: Admin은 모든 권한, 팀 멤버는 조회/트리거/수정 가능 (삭제 불가)
### 파일 구조

```plain text
plugins/airflow_keycloak/
├── custom_keycloak_auth_manager.py  # 핵심 인증 로직
├── setup_keycloak_groups.py         # 초기 설정 스크립트
└── README.md

dags/core/
└── sync_keycloak_groups.py          # 자동 동기화 DAG

```

---

## 🏗️ 아키텍처 & 작동 원리

### 1. 전체 구조

```plain text
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

### 2. 인증 흐름 (상세)

### Step 1: 사용자 로그인

```plain text
1. 사용자가 Airflow UI 접속 (http://localhost:8080)
2. CustomKeycloakAuthManager가 Keycloak 로그인 페이지로 리다이렉트
3. 사용자가 Keycloak에서 이메일/비밀번호 입력
4. Keycloak가 JWT Access Token 발급
   - Token 안에 포함된 정보:
     * groups: ["/airflow/ML Platform (T)", "/airflow/AI Product (T)"]
     * realm_access.roles: ["airflow", "user"]
     * email: "user@qraft.ai"

```

### Step 2: JWT 토큰 디코딩 및 그룹 추출

```python
# custom_keycloak_auth_manager.py:498-556
def _get_user_groups(self, user) -> list[str]:
    # JWT 토큰 디코드 (서명 검증 없이 - 이미 Keycloak에서 인증됨)
    decoded = jwt.decode(user.access_token, options={"verify_signature": False})

    # 1. groups 클레임 추출
    groups = decoded.get("groups", [])
    # 예: ["/airflow/ML Platform (T)", "/airflow/AI Product (T)"]

    # 2. 경로에서 마지막 부분만 추출
    normalized_groups = [group.split("/")[-1] for group in groups]
    # 결과: ["ML Platform (T)", "AI Product (T)"]

    # 3. 역할(roles)도 함께 반환
    realm_roles = decoded.get("realm_access", {}).get("roles", [])
    # 예: ["airflow", "user"]

    return normalized_groups + realm_roles
    # 최종: ["ML Platform (T)", "AI Product (T)", "airflow", "user"]

```

### Step 3: DAG 접근 권한 확인

```python
# custom_keycloak_auth_manager.py:80-175
def is_authorized_dag(self, method: str, access_entity: DagAccessEntity, user):
    # 1. Admin 확인
    if self._is_admin(user):
        return True  # Admin은 모든 권한

    # 2. DELETE 메서드는 Admin만 허용
    if method == "DELETE":
        log.warning("DELETE is restricted to admins only")
        return False

    # 3. DAG의 team 태그 추출
    dag_teams = self._get_dag_teams(dag_id)
    # 예: DAG에 tags=["team:ML Platform (T)"] → ["ML Platform (T)"]

    # 4. Team 태그 없으면 모든 인증된 사용자 접근 가능
    if not dag_teams:
        return True

    # 5. 사용자 그룹과 DAG 팀 매칭
    user_groups = self._get_user_groups(user)
    # 예: ["ML Platform (T)", "AI Product (T)", "airflow"]

    for team in dag_teams:
        mapped_group = self.TEAM_MAPPING.get(team)
        if mapped_group in user_groups:
            return True  # 매칭되면 접근 허용

    return False  # 매칭 안되면 접근 거부

```

### 3. 권한 정책 (상세)

Admin 판별 로직:

```python
# custom_keycloak_auth_manager.py:611-628
def _is_admin(self, user) -> bool:
    user_roles = self._get_user_roles(user)
    user_groups = self._get_user_groups(user)

    # Admin 조건 1: airflow 역할 보유
    is_admin_role = "airflow" in user_roles

    # Admin 조건 2: ML Platform (T) 그룹 소속
    is_admin_group = "ML Platform (T)" in user_groups

    return is_admin_role or is_admin_group

```

### 4. DAG UI 필터링 동작 원리

일반 사용자가 DAG 목록을 볼 때:

```python
# custom_keycloak_auth_manager.py:384-464
def get_authorized_dag_ids(self, user):
    # 1. DB에서 모든 DAG 조회 (DagModel)
    all_dags = session.query(DagModel).all()

    # 2. Admin이면 모든 DAG 반환
    if self._is_admin(user):
        return {dag.dag_id for dag in all_dags}

    # 3. 일반 사용자: 각 DAG의 태그 확인
    authorized_dag_ids = set()
    user_groups = self._get_user_groups(user)

    for dag_model in all_dags:
        # DAG의 team 태그 추출
        dag_tags = session.query(DagTag.name).filter(DagTag.dag_id == dag_id).all()
        dag_teams = [tag.replace("team:", "") for tag in dag_tags if tag.startswith("team:")]

        # 팀 태그 없으면 모두 접근 가능
        if not dag_teams:
            authorized_dag_ids.add(dag_id)
            continue

        # 사용자 그룹과 매칭
        for team in dag_teams:
            if self.TEAM_MAPPING.get(team) in user_groups:
                authorized_dag_ids.add(dag_id)
                break

    return authorized_dag_ids
    # 결과: 사용자가 접근 가능한 DAG ID 목록만 반환
    # UI에는 이 목록의 DAG만 표시됨

```

### 5. 자동 동기화 시스템

DAG: sync_keycloak_groups (dags/core/sync_keycloak_groups.py)

실행 주기: 매일 새벽 1시 (KST) - schedule="0 10 * * *" (UTC 10시 = KST 19시... 수정 필요하면 0 16 * * *로 변경)

동작 흐름:

```plain text
1. get_snowflake_employees()
   ↓ Snowflake에서 재직 직원 조회 (use_yn='Y')
   ↓ SELECT department, email, name FROM dim_flex WHERE use_yn='Y'

2. get_keycloak_access_token()
   ↓ Keycloak Admin API 인증
   ↓ Client: airflow-keycloak-client
   ↓ Secret: Airflow Variable 'keycloak_client_secret'

3. get_keycloak_groups_and_members(token)
   ↓ Keycloak에서 현재 그룹 구조 조회
   ↓ GET /admin/realms/qraft/groups/{parent_id}
   ↓ 각 그룹의 멤버 목록 조회

4. sync_groups_and_members(token, sf_employees, kc_data)
   ↓ 변경사항 비교 및 반영

   A. 신규 그룹 생성
      - Snowflake에 있지만 Keycloak에 없는 department
      - POST /admin/realms/qraft/groups/{parent_id}/children

   B. 신규 멤버 추가
      - 신규 입사자: Keycloak 사용자 생성 + 그룹 추가
      - POST /admin/realms/qraft/users (사용자 생성)
      - PUT /admin/realms/qraft/users/{user_id}/groups/{group_id}

   C. 퇴사자 제거
      - Snowflake에 없지만 Keycloak 그룹에 있는 사용자
      - DELETE /admin/realms/qraft/users/{user_id}/groups/{group_id}
      - (사용자 계정은 유지, 그룹에서만 제거)

   D. 팀 이동 처리
      - 이전 그룹에서 제거 + 새 그룹에 추가
      - 자동으로 감지 (같은 이메일이 다른 department)

5. 통계 로깅
   - 신규 그룹: N개
   - 멤버 추가: N명
   - 멤버 제거: N명 (퇴사)
   - 팀 이동: N명

```

예시 시나리오:

```plain text
Snowflake 데이터:
  - user1@qraft.ai | ML Platform (T)
  - user2@qraft.ai | AI Product (T)  ← 이전에는 ML Platform (T)
  - user3@qraft.ai | QT Dev (T)      ← 신규 입사

Keycloak 현재 상태:
  - user1@qraft.ai | ML Platform (T)
  - user2@qraft.ai | ML Platform (T)
  - user4@qraft.ai | ML Platform (T)  ← 퇴사

동기화 결과:
  ✅ user2: ML Platform (T) 제거 → AI Product (T) 추가 (팀 이동)
  ✅ user3: 사용자 생성 + QT Dev (T) 추가 (신규)
  ✅ user4: ML Platform (T) 제거 (퇴사)

```

---

## ⚙️ 설정 방법

### 1. 환경 변수 설정 (.env)

```bash
# Keycloak Auth Manager 활성화
AIRFLOW__CORE__AUTH_MANAGER=plugins.airflow_keycloak.custom_keycloak_auth_manager.CustomKeycloakAuthManager

# Keycloak 서버 정보
AIRFLOW__KEYCLOAK_AUTH_MANAGER__SERVER_URL=https://auth.qraft.ai
AIRFLOW__KEYCLOAK_AUTH_MANAGER__REALM=qraft
AIRFLOW__KEYCLOAK_AUTH_MANAGER__CLIENT_ID=airflow-keycloak-client
AIRFLOW__KEYCLOAK_AUTH_MANAGER__CLIENT_SECRET=<client-secret>

```

중요: AUTH_MANAGER 경로는 plugins/airflow_keycloak/가 아닌 Docker 컨테이너 내부 경로 기준입니다.

### 2. Airflow Variable 설정

```bash
# DAG에서 사용하는 Keycloak Admin API Secret
airflow variables set keycloak_client_secret "<admin-cli-secret>"

```

또는 .env.variables 파일에:

```bash
AIRFLOW_VAR_KEYCLOAK_CLIENT_SECRET=<admin-cli-secret>

```

### 3. Keycloak 클라이언트 설정

Realm: qraft

Client 1: airflow-keycloak-client (인증용)

- Client Protocol: openid-connect
- Access Type: confidential
- Valid Redirect URIs: http://localhost:8080/*
- Web Origins: http://localhost:8080
Client 2: admin-cli (DAG 동기화용)

- Service Accounts Enabled: On
- Authorization Enabled: On
- Service Account Roles:
  - realm-management: manage-users, manage-groups, view-users
### 4. 초기 그룹 설정

```bash
# 1. 데이터 확인만
docker exec qraft_airflow-airflow-apiserver-1 \
  python /opt/airflow/plugins/airflow_keycloak/setup_keycloak_groups.py --check

# 2. 실제 Keycloak에 그룹 생성
docker exec qraft_airflow-airflow-apiserver-1 \
  python /opt/airflow/plugins/airflow_keycloak/setup_keycloak_groups.py --setup

```

스크립트 동작:

1. Snowflake qraft_automation.employee.dim_flex 테이블에서 department 조회
1. Parent group airflow 생성 (없을 경우)
1. 각 department를 Child group으로 생성
1. 직원 이메일을 각 그룹에 멤버로 추가
---

## 🎯 DAG 태깅 가이드

### 기본 사용법

```python
from airflow.decorators import dag
import pendulum

@dag(
    dag_id="my_team_dag",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    schedule="0 9 * * *",
    tags=[
        "vendor:snowflake",
        "from:s3",
        "to:snowflake",
        "team:ML Platform (T)",  # ← 이 태그로 권한 제어!
        "datatype:core",
    ],
)
def my_team_dag():
    ...

```

결과:

- ML Platform (T) 그룹 멤버만 이 DAG를 UI에서 볼 수 있음
- 조회, 트리거, 수정 가능
- 삭제는 Admin만 가능
### 여러 팀 허용

```python
tags=[
    "team:ML Platform (T)",
    "team:AI Product (T)",
    # OR 조건: 둘 중 하나라도 속하면 접근 가능
]

```

### 공용 DAG (모든 사람 접근 가능)

```python
tags=[
    "vendor:airflow",
    "datatype:core",
    # team 태그 없음 → 모든 인증된 사용자 접근 가능
]

```

---

## 🔍 주요 컴포넌트 설명

### TEAM_MAPPING

custom_keycloak_auth_manager.py:44-72

```python
TEAM_MAPPING = {
    "ML Platform (T)": "ML Platform (T)",
    "AI Tech Lab (T)": "AI Tech Lab (T)",
    "AI Product (T)": "AI Product (T)",
    # ... 총 25개 팀
}

```

역할: DAG의 team 태그와 Keycloak 그룹을 매핑

- Key: DAG 태그 값
- Value: Keycloak 그룹명
- 현재는 1:1 매핑이지만, 다르게 설정도 가능
확장 예시:

```python
TEAM_MAPPING = {
    "ml-platform": "ML Platform (T)",  # DAG에는 짧은 이름, Keycloak은 정식 명칭
    "ai-product": "AI Product (T)",
}

```

### ADMIN_ROLES & ADMIN_GROUPS

custom_keycloak_auth_manager.py:74-78

```python
ADMIN_ROLES = ["airflow"]
ADMIN_GROUPS = ["ML Platform (T)"]

```

역할: 전체 Admin 권한 부여 조건

- airflow 역할 보유자 → Admin
- ML Platform (T) 그룹 소속 → Admin
Admin 권한 추가 방법:

1. Keycloak에서 사용자에게 airflow 역할 할당
1. Snowflake dim_flex에서 department를 'ML Platform (T)'로 변경
---

## 🔧 문제 해결

### 1. "Permission denied" 오류

증상: DAG는 보이는데 트리거 버튼이 비활성화

원인: 사용자가 해당 DAG의 팀 그룹에 속하지 않음

해결:

```bash
# 1. 사용자의 그룹 확인
# Keycloak Admin Console → Users → 사용자 선택 → Groups

# 2. DAG의 team 태그 확인
# Airflow UI → DAGs → 해당 DAG → Code → tags 확인

# 3. 그룹 추가 (2가지 방법)
# 방법 A: Keycloak에서 직접 추가
# Keycloak Admin Console → Groups → 해당 그룹 → Members → Add member

# 방법 B: Snowflake에서 department 변경 후 동기화 대기
# UPDATE qraft_automation.employee.dim_flex
# SET department = 'ML Platform (T)'
# WHERE email = 'user@qraft.ai'
# (다음날 새벽 1시 자동 동기화)

```

### 2. DAG 목록이 안 보임

증상: 로그인은 되는데 DAG 목록이 비어있음

원인: 모든 DAG에 team 태그가 있고, 사용자가 어느 팀에도 속하지 않음

해결:

```bash
# 로그 확인
docker logs qraft_airflow-airflow-apiserver-1 | grep "get_authorized_dag_ids"

# 예상 로그:
# User user@qraft.ai groups: []  ← 그룹이 비어있음!

# 해결: Admin 권한 부여
# Keycloak Admin Console → Users → user@qraft.ai
# Role Mapping → Assign role → airflow

```

### 3. 동기화 DAG 실패

증상: sync_keycloak_groups DAG가 실패

로그 확인:

```bash
docker logs qraft_airflow-airflow-apiserver-1 | grep "sync_keycloak_groups"

```

주요 오류:

A. Keycloak Client Secret 없음

```plain text
airflow.exceptions.AirflowException: Variable keycloak_client_secret does not exist

```

해결:

```bash
airflow variables set keycloak_client_secret "<your-secret>"

```

B. Snowflake 연결 실패

```plain text
Connection 'snowflake-account-etl' not found

```

해결: config/init_connections.py에서 연결 확인

C. Keycloak API 권한 없음

```plain text
403 Forbidden: Insufficient permissions

```

해결: admin-cli 클라이언트에 manage-users, manage-groups 역할 추가

### 4. "Keycloak scope error" 로그

증상: 로그에 scope 관련 경고가 많이 나옴

원인: Airflow 공식 KeycloakAuthManager가 권한 체크 시 Keycloak API를 호출하는데, scope 설정 불일치

해결: 이미 해결됨 (코드에서 우회 처리)

```python
# custom_keycloak_auth_manager.py:116-118
# Keycloak 기본 권한 체크는 scope 오류로 인해 스킵
# 사용자가 이미 로그인했다면 Keycloak 인증은 완료된 것으로 간주
log.debug(f"Bypassing parent authorization check for user {user}")

```

---

## 📊 Keycloak 그룹 구조

```plain text
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

총 25개 팀 (custom_keycloak_auth_manager.py:46-72)

---

## 🎓 개념 정리

### Keycloak이란?

오픈소스 Identity and Access Management (IAM) 솔루션

- SSO (Single Sign-On): 한 번 로그인하면 여러 애플리케이션 접근
- OAuth 2.0 / OpenID Connect: 표준 프로토콜 지원
- 사용자/그룹/역할 관리: 중앙화된 권한 관리
### JWT (JSON Web Token)

Keycloak이 발급하는 인증 토큰

```plain text
Header.Payload.Signature

Payload 예시:
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

### Auth Manager (Airflow 3.x)

Airflow의 인증/권한 시스템 플러그인 인터페이스

- 기본: FAB (Flask App Builder) Auth Manager
- Keycloak: 공식 Keycloak Auth Manager (Airflow 3.0+)
- 커스텀: CustomKeycloakAuthManager (이 프로젝트)
주요 메서드:

- is_logged_in(): 로그인 여부
- is_authorized_dag(): DAG 접근 권한
- get_authorized_dag_ids(): 접근 가능한 DAG 목록
- is_authorized_configuration(): Admin 설정 권한
---

## 📚 참고 자료

- Keycloak 공식 문서: https://www.keycloak.org/docs/latest/
- Airflow Auth Manager: https://airflow.apache.org/docs/apache-airflow/stable/security/auth-manager.html
- Airflow Keycloak Provider: https://airflow.apache.org/docs/apache-airflow-providers-keycloak/
---

## 🔄 향후 개선 방향

1. DAG 레벨 세분화
  - 현재: 팀 단위 전체 접근
  - 개선: 특정 DAG만 읽기 전용, 특정 사용자만 트리거 등
1. Keycloak Attribute 활용
  - 사용자 속성 (직급, 부서코드 등)을 권한 정책에 반영
1. Audit Log
  - 누가 어떤 DAG를 실행했는지 Keycloak에 기록
1. Dynamic Team Mapping
  - 하드코딩된 TEAM_MAPPING을 Airflow Variable이나 DB로 이동
---

이 문서를 기반으로 다른 개발자가 시스템을 이해하고 유지보수할 수 있습니다!