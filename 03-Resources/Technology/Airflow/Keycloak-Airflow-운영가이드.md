---
title: Keycloak-Airflow 운영가이드
type: resource
tags:
  - keycloak
  - airflow
  - operations
  - setup
  - troubleshooting
  - dag-tagging
  - monitoring
created: '2025-11-30'
updated: '2025-11-30'
aliases:
  - Keycloak Airflow Operational Guide
status: evergreen
maturity: 3
---
# Keycloak-Airflow 운영가이드

## 📌 개요

Keycloak-Airflow 인증 시스템의 설정, 사용, 운영 방법을 안내합니다.

---

## ⚙️ 초기 설정

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

**중요:** 
- `AUTH_MANAGER` 경로는 `plugins/airflow_keycloak/`가 아닌 Docker 컨테이너 내부 경로 기준입니다.
- `CLIENT_SECRET`은 Keycloak Admin Console에서 확인할 수 있습니다.

### 2. Airflow Variable 설정

```bash
# DAG에서 사용하는 Keycloak Admin API Secret
airflow variables set keycloak_client_secret "<admin-cli-secret>"
```

또는 `.env.variables` 파일에:

```bash
AIRFLOW_VAR_KEYCLOAK_CLIENT_SECRET=<admin-cli-secret>
```

### 3. Keycloak 클라이언트 설정

**Realm:** `qraft`

#### Client 1: airflow-keycloak-client (인증용)

```yaml
Client ID: airflow-keycloak-client
Client Protocol: openid-connect
Access Type: confidential
Valid Redirect URIs: http://localhost:8080/*
Web Origins: http://localhost:8080
```

#### Client 2: admin-cli (DAG 동기화용)

```yaml
Client ID: admin-cli
Service Accounts Enabled: On
Authorization Enabled: On

Service Account Roles:
  - realm-management: manage-users, manage-groups, view-users
```

**Service Account Roles 추가 방법:**
1. Keycloak Admin Console → Clients → admin-cli
2. Service Account Roles 탭
3. Client Roles → realm-management 선택
4. `manage-users`, `manage-groups`, `view-users` 추가

### 4. 초기 그룹 설정

#### Step 1: 데이터 확인만 (Dry Run)

```bash
docker exec qraft_airflow-airflow-apiserver-1 \
  python /opt/airflow/plugins/airflow_keycloak/setup_keycloak_groups.py --check
```

**출력 예시:**
```
Snowflake employees found:
  - ML Platform (T): 5 members
  - AI Product (T): 3 members
  - QT Dev (T): 2 members

Groups to create:
  - ML Platform (T)
  - AI Product (T)
  - QT Dev (T)

Members to add:
  - user1@qraft.ai → ML Platform (T)
  - user2@qraft.ai → AI Product (T)
  ...
```

#### Step 2: 실제 Keycloak에 그룹 생성

```bash
docker exec qraft_airflow-airflow-apiserver-1 \
  python /opt/airflow/plugins/airflow_keycloak/setup_keycloak_groups.py --setup
```

**스크립트 동작:**
1. Snowflake `qraft_automation.employee.dim_flex` 테이블에서 department 조회
2. Parent group `airflow` 생성 (없을 경우)
3. 각 department를 Child group으로 생성
4. 직원 이메일을 각 그룹에 멤버로 추가

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

**결과:**
- ML Platform (T) 그룹 멤버만 이 DAG를 UI에서 볼 수 있음
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

### 태그 네이밍 규칙

| 태그 형식 | 의미 | 예시 |
|----------|------|------|
| `team:<팀명>` | 접근 권한 제어 | `team:ML Platform (T)` |
| `vendor:<벤더>` | 데이터 소스 | `vendor:snowflake`, `vendor:s3` |
| `from:<출처>` | 데이터 입력 | `from:s3`, `from:api` |
| `to:<목적지>` | 데이터 출력 | `to:snowflake`, `to:datahub` |
| `datatype:<타입>` | 데이터 유형 | `datatype:core`, `datatype:raw` |

---

## 🔧 운영 방법

### 1. Admin 권한 부여

#### 방법 A: Keycloak에서 직접 역할 할당

1. Keycloak Admin Console → Users → 사용자 선택
2. Role Mapping 탭 → Assign role
3. `airflow` 역할 선택 → Assign

#### 방법 B: Snowflake에서 department 변경

```sql
UPDATE qraft_automation.employee.dim_flex
SET department = 'ML Platform (T)'
WHERE email = 'user@qraft.ai';
```

**참고:** 다음날 새벽 1시 자동 동기화 실행 후 반영됨

### 2. 사용자 그룹 변경 (팀 이동)

#### 방법 A: Keycloak에서 직접 변경

1. Keycloak Admin Console → Groups → 이전 그룹 → Members
2. 해당 사용자 선택 → Leave
3. 새 그룹 → Members → Add member → 사용자 추가

#### 방법 B: Snowflake에서 변경 (권장)

```sql
UPDATE qraft_automation.employee.dim_flex
SET department = 'AI Product (T)'
WHERE email = 'user@qraft.ai';
```

**장점:**
- Snowflake가 Source of Truth
- 자동 동기화로 일관성 유지
- 퇴사자 자동 제거

### 3. 동기화 DAG 수동 실행

```bash
# Airflow UI에서 sync_keycloak_groups DAG 트리거
# 또는 CLI에서:
airflow dags trigger sync_keycloak_groups
```

**실행 후 로그 확인:**

```bash
docker logs qraft_airflow-airflow-apiserver-1 | grep "sync_keycloak_groups"
```

**출력 예시:**
```
[2025-11-30] Sync completed:
  - New groups: 0
  - Members added: 2 (user3@qraft.ai, user4@qraft.ai)
  - Members removed: 1 (user5@qraft.ai)
  - Team changes: 1 (user2@qraft.ai: ML Platform → AI Product)
```

---

## 🔍 문제 해결

### 1. "Permission denied" 오류

**증상:** DAG는 보이는데 트리거 버튼이 비활성화

**원인:** 사용자가 해당 DAG의 팀 그룹에 속하지 않음

**해결:**

```bash
# 1. 사용자의 그룹 확인
# Keycloak Admin Console → Users → 사용자 선택 → Groups

# 2. DAG의 team 태그 확인
# Airflow UI → DAGs → 해당 DAG → Code → tags 확인

# 3-A. Keycloak에서 직접 그룹 추가
# Keycloak Admin Console → Groups → 해당 그룹 → Members → Add member

# 3-B. Snowflake에서 department 변경 후 동기화 대기
UPDATE qraft_automation.employee.dim_flex
SET department = 'ML Platform (T)'
WHERE email = 'user@qraft.ai';
# (다음날 새벽 1시 자동 동기화)
```

### 2. DAG 목록이 안 보임

**증상:** 로그인은 되는데 DAG 목록이 비어있음

**원인:** 모든 DAG에 team 태그가 있고, 사용자가 어느 팀에도 속하지 않음

**로그 확인:**

```bash
docker logs qraft_airflow-airflow-apiserver-1 | grep "get_authorized_dag_ids"
```

**예상 로그:**
```
User user@qraft.ai groups: []  ← 그룹이 비어있음!
```

**해결:** Admin 권한 부여

```bash
# Keycloak Admin Console → Users → user@qraft.ai
# Role Mapping → Assign role → airflow
```

### 3. 동기화 DAG 실패

**증상:** `sync_keycloak_groups` DAG가 실패

**로그 확인:**

```bash
docker logs qraft_airflow-airflow-apiserver-1 | grep "sync_keycloak_groups"
```

#### A. Keycloak Client Secret 없음

**오류:**
```
airflow.exceptions.AirflowException: Variable keycloak_client_secret does not exist
```

**해결:**
```bash
airflow variables set keycloak_client_secret "<your-secret>"
```

#### B. Snowflake 연결 실패

**오류:**
```
Connection 'snowflake-account-etl' not found
```

**해결:** `config/init_connections.py`에서 연결 확인

```python
# Snowflake 연결 확인
airflow connections get snowflake-account-etl
```

#### C. Keycloak API 권한 없음

**오류:**
```
403 Forbidden: Insufficient permissions
```

**해결:** `admin-cli` 클라이언트에 `manage-users`, `manage-groups` 역할 추가

1. Keycloak Admin Console → Clients → admin-cli
2. Service Account Roles 탭
3. Client Roles → realm-management
4. `manage-users`, `manage-groups` 추가

### 4. "Keycloak scope error" 로그

**증상:** 로그에 scope 관련 경고가 많이 나옴

**원인:** Airflow 공식 KeycloakAuthManager가 권한 체크 시 Keycloak API를 호출하는데, scope 설정 불일치

**해결:** 이미 해결됨 (코드에서 우회 처리)

```python
# custom_keycloak_auth_manager.py:116-118
# Keycloak 기본 권한 체크는 scope 오류로 인해 스킵
# 사용자가 이미 로그인했다면 Keycloak 인증은 완료된 것으로 간주
log.debug(f"Bypassing parent authorization check for user {user}")
```

---

## 📊 모니터링

### 1. 로그인 성공/실패 확인

```bash
docker logs qraft_airflow-airflow-apiserver-1 | grep "User.*logged in"
docker logs qraft_airflow-airflow-apiserver-1 | grep "Login failed"
```

### 2. 권한 체크 로그 확인

```bash
docker logs qraft_airflow-airflow-apiserver-1 | grep "is_authorized_dag"
```

**출력 예시:**
```
[2025-11-30] User user@qraft.ai authorized for DAG my_team_dag
[2025-11-30] User user2@qraft.ai denied access to another_dag
```

### 3. 동기화 통계 확인

```bash
docker logs qraft_airflow-airflow-apiserver-1 | grep "Sync completed"
```

---

## 🔄 향후 개선 방향

### 1. DAG 레벨 세분화

**현재:** 팀 단위 전체 접근

**개선 방향:**
- 특정 DAG만 읽기 전용
- 특정 사용자만 트리거 가능
- 개별 사용자 단위 권한

**예시:**
```python
tags=[
    "team:ML Platform (T):read-only",
    "user:admin@qraft.ai:trigger",
]
```

### 2. Keycloak Attribute 활용

**개선 방향:**
- 사용자 속성 (직급, 부서코드 등)을 권한 정책에 반영
- 동적 권한 부여 (직급에 따라 자동으로 권한 변경)

**예시:**
```python
# 매니저 이상만 Production DAG 접근
if user.attributes.get("position") in ["Manager", "Director"]:
    return True
```

### 3. Audit Log

**개선 방향:**
- 누가 어떤 DAG를 실행했는지 Keycloak에 기록
- 권한 변경 이력 추적
- 보안 감사 지원

### 4. Dynamic Team Mapping

**현재:** 하드코딩된 TEAM_MAPPING

**개선 방향:**
- Airflow Variable이나 DB로 이동
- UI에서 매핑 관리
- 팀 추가 시 코드 수정 불필요

**예시:**
```python
# Airflow Variable에서 동적 로드
TEAM_MAPPING = Variable.get("team_mapping", deserialize_json=True)
```

---

## 📎 Related

### Projects 배경 (Why)
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/Keycloak-SSO-도입-배경|Keycloak-SSO-도입-배경]] - 왜 Keycloak SSO를 도입했는가

### Technology (Core Concepts)
- [[Keycloak-Airflow-인증-개념]] - Keycloak, JWT, Auth Manager 개념
- [[Keycloak-OIDC-인증]] - OIDC 프로토콜 상세

### Technology (Implementation)
- [[Keycloak-Airflow-구현]] - CustomKeycloakAuthManager 실제 코드 구현
- [[Airflow-3.0-구현]] - Airflow 3.0 플랫폼 구현

### Projects (실제 사용)
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/팀별-데이터-격리-체계|팀별-데이터-격리-체계]] - 팀별 권한 격리 전략

---

## 📚 참고 자료

- Keycloak 공식 문서: https://www.keycloak.org/docs/latest/
- Airflow Auth Manager: https://airflow.apache.org/docs/apache-airflow/stable/security/auth-manager.html
- Airflow Keycloak Provider: https://airflow.apache.org/docs/apache-airflow-providers-keycloak/
- Keycloak Admin REST API: https://www.keycloak.org/docs-api/latest/rest-api/index.html

---

**Metadata:**
