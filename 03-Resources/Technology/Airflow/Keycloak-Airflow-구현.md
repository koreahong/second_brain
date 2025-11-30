---
title: Keycloak-Airflow 구현
type: resource
tags:
  - keycloak
  - airflow
  - implementation
  - custom-auth-manager
  - sync-dag
  - python
  - code
created: '2025-11-30'
updated: '2025-11-30'
aliases:
  - Keycloak Airflow Implementation
status: evergreen
maturity: 3
---
# Keycloak-Airflow 구현

## 📌 핵심 요약 (TL;DR)

### 무엇을 구현했나?

- Airflow 3.x에 Keycloak SSO 인증 통합
- DAG의 team 태그 기반으로 자동 권한 제어
- Snowflake 직원 정보와 Keycloak 그룹 자동 동기화

### 주요 기능

1. **커스텀 Auth Manager**: DAG에 `team:ML Platform (T)` 태그만 추가하면 해당 팀만 접근 가능
2. **자동 그룹 동기화**: 매일 새벽 1시 Snowflake ↔ Keycloak 자동 동기화 (신규 입사, 퇴사, 팀 이동)
3. **역할 기반 권한**: Admin은 모든 권한, 팀 멤버는 조회/트리거/수정 가능 (삭제 불가)

### 파일 구조

```
plugins/airflow_keycloak/
├── custom_keycloak_auth_manager.py  # 핵심 인증 로직
├── setup_keycloak_groups.py         # 초기 설정 스크립트
└── README.md

dags/core/
└── sync_keycloak_groups.py          # 자동 동기화 DAG
```

---

## 🔧 주요 컴포넌트

### 1. TEAM_MAPPING

**위치:** `custom_keycloak_auth_manager.py:44-72`

```python
TEAM_MAPPING = {
    "ML Platform (T)": "ML Platform (T)",
    "AI Tech Lab (T)": "AI Tech Lab (T)",
    "AI Product (T)": "AI Product (T)",
    "AI Research (T)": "AI Research (T)",
    "QT Dev (T)": "QT Dev (T)",
    "ATS Dev (T)": "ATS Dev (T)",
    "DL Dev (P)": "DL Dev (P)",
    "DL TF (T)": "DL TF (T)",
    "HFT (T)": "HFT (T)",
    "MFT (T)": "MFT (T)",
    "APS (T)": "APS (T)",
    "Wealth Solution (T)": "Wealth Solution (T)",
    "Product Strategy (T)": "Product Strategy (T)",
    "Strategic Planning (T)": "Strategic Planning (T)",
    "Strategy (T)": "Strategy (T)",
    "Business Solution (D)": "Business Solution (D)",
    "Business Administration (D)": "Business Administration (D)",
    "Client Coverage (T)": "Client Coverage (T)",
    "HR (T)": "HR (T)",
    "Accounting (T)": "Accounting (T)",
    "Legal & Compliance (T)": "Legal & Compliance (T)",
    "Risk Managemnet (T)": "Risk Managemnet (T)",
    "AI Trading Solution (D)": "AI Trading Solution (D)",
    "QRAFT (HQ)": "QRAFT (HQ)",
    "QRAFT APAC (C)": "QRAFT APAC (C)",
}
```

**역할:** DAG의 team 태그와 Keycloak 그룹을 매핑

- **Key**: DAG 태그 값 (예: `team:ML Platform (T)`에서 추출)
- **Value**: Keycloak 그룹명
- 현재는 1:1 매핑이지만, 다르게 설정도 가능

**확장 예시:**

```python
TEAM_MAPPING = {
    "ml-platform": "ML Platform (T)",  # DAG에는 짧은 이름
    "ai-product": "AI Product (T)",
}
```

### 2. ADMIN_ROLES & ADMIN_GROUPS

**위치:** `custom_keycloak_auth_manager.py:74-78`

```python
ADMIN_ROLES = ["airflow"]
ADMIN_GROUPS = ["ML Platform (T)"]
```

**역할:** 전체 Admin 권한 부여 조건

- `airflow` 역할 보유자 → Admin
- `ML Platform (T)` 그룹 소속 → Admin

---

## 💻 핵심 코드 구현

### 1. JWT 토큰 디코딩 및 그룹 추출

**위치:** `custom_keycloak_auth_manager.py:498-556`

```python
def _get_user_groups(self, user) -> list[str]:
    """
    JWT 토큰에서 사용자 그룹 추출
    
    Returns:
        ["ML Platform (T)", "AI Product (T)", "airflow", "user"]
    """
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

**핵심 로직:**
1. JWT 토큰 디코드 (Keycloak에서 이미 인증했으므로 서명 검증 스킵)
2. `groups` 클레임에서 그룹 경로 추출
3. 경로에서 실제 그룹명만 파싱 (`/airflow/ML Platform (T)` → `ML Platform (T)`)
4. Realm roles도 함께 추출 (`airflow`, `user` 등)

### 2. DAG 접근 권한 확인

**위치:** `custom_keycloak_auth_manager.py:80-175`

```python
def is_authorized_dag(self, method: str, access_entity: DagAccessEntity, user):
    """
    DAG 접근 권한 확인
    
    Args:
        method: HTTP 메서드 (GET, POST, PUT, DELETE)
        access_entity: DAG 엔티티 정보
        user: 사용자 객체
    
    Returns:
        True: 접근 허용, False: 접근 거부
    """
    # 1. Admin 확인
    if self._is_admin(user):
        return True  # Admin은 모든 권한
    
    # 2. DELETE 메서드는 Admin만 허용
    if method == "DELETE":
        log.warning(f"{user.email} attempted DELETE (admin only)")
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
    
    log.warning(f"{user.email} denied access to {dag_id}")
    return False  # 매칭 안되면 접근 거부
```

**핵심 로직:**
1. Admin 사용자는 무조건 허용
2. DELETE는 Admin만 가능
3. DAG의 `team:` 태그 추출
4. 팀 태그 없으면 모두 접근 가능
5. 사용자 그룹과 DAG 팀 매칭 확인

### 3. Admin 판별 로직

**위치:** `custom_keycloak_auth_manager.py:611-628`

```python
def _is_admin(self, user) -> bool:
    """
    Admin 권한 확인
    
    Returns:
        True: Admin, False: 일반 사용자
    """
    user_roles = self._get_user_roles(user)
    user_groups = self._get_user_groups(user)
    
    # Admin 조건 1: airflow 역할 보유
    is_admin_role = "airflow" in user_roles
    
    # Admin 조건 2: ML Platform (T) 그룹 소속
    is_admin_group = "ML Platform (T)" in user_groups
    
    return is_admin_role or is_admin_group
```

**핵심 로직:**
- Admin 조건은 OR 관계 (둘 중 하나만 만족하면 Admin)
- `airflow` 역할 보유 또는 `ML Platform (T)` 그룹 소속

### 4. DAG UI 필터링

**위치:** `custom_keycloak_auth_manager.py:384-464`

```python
def get_authorized_dag_ids(self, user):
    """
    사용자가 접근 가능한 DAG ID 목록 반환
    
    Returns:
        set: 접근 가능한 DAG ID 집합
    """
    # 1. DB에서 모든 DAG 조회 (DagModel)
    all_dags = session.query(DagModel).all()
    
    # 2. Admin이면 모든 DAG 반환
    if self._is_admin(user):
        return {dag.dag_id for dag in all_dags}
    
    # 3. 일반 사용자: 각 DAG의 태그 확인
    authorized_dag_ids = set()
    user_groups = self._get_user_groups(user)
    
    for dag_model in all_dags:
        dag_id = dag_model.dag_id
        
        # DAG의 team 태그 추출
        dag_tags = session.query(DagTag.name).filter(
            DagTag.dag_id == dag_id
        ).all()
        dag_teams = [
            tag.name.replace("team:", "")
            for tag in dag_tags
            if tag.name.startswith("team:")
        ]
        
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

**핵심 로직:**
1. DB에서 모든 DAG 조회
2. Admin은 전체 반환
3. 일반 사용자는 각 DAG의 `team:` 태그 확인
4. 사용자 그룹과 매칭되는 DAG만 필터링
5. **결과:** UI에는 접근 가능한 DAG만 표시

---

## 🔄 자동 동기화 DAG 구현

### DAG 정보

**파일:** `dags/core/sync_keycloak_groups.py`

**실행 주기:** 매일 새벽 1시 (KST)
- Schedule: `"0 10 * * *"` (UTC 10시 = KST 19시)
- 수정 필요하면 `"0 16 * * *"`로 변경 (UTC 16시 = KST 01시)

### 주요 함수

#### 1. get_snowflake_employees()

```python
def get_snowflake_employees():
    """
    Snowflake에서 재직 직원 조회
    
    Returns:
        {
            "ML Platform (T)": [
                {"email": "user1@qraft.ai", "name": "User 1"}
            ]
        }
    """
    query = """
        SELECT department, email, name
        FROM qraft_automation.employee.dim_flex
        WHERE use_yn = 'Y'
    """
    
    # Snowflake 연결 및 쿼리 실행
    hook = SnowflakeHook(snowflake_conn_id="snowflake-account-etl")
    results = hook.get_records(query)
    
    # Department별로 그룹화
    employees_by_dept = defaultdict(list)
    for department, email, name in results:
        employees_by_dept[department].append({
            "email": email,
            "name": name
        })
    
    return dict(employees_by_dept)
```

#### 2. get_keycloak_access_token()

```python
def get_keycloak_access_token():
    """
    Keycloak Admin API 인증
    
    Returns:
        str: Access token
    """
    from airflow.models import Variable
    
    client_secret = Variable.get("keycloak_client_secret")
    
    response = requests.post(
        f"{KEYCLOAK_SERVER_URL}/realms/{REALM}/protocol/openid-connect/token",
        data={
            "grant_type": "client_credentials",
            "client_id": "admin-cli",
            "client_secret": client_secret,
        },
    )
    
    return response.json()["access_token"]
```

#### 3. get_keycloak_groups_and_members()

```python
def get_keycloak_groups_and_members(token):
    """
    Keycloak에서 현재 그룹 구조 및 멤버 조회
    
    Returns:
        {
            "groups": {
                "ML Platform (T)": {"id": "group-id-1"},
            },
            "members": {
                "ML Platform (T)": ["user1@qraft.ai", "user2@qraft.ai"]
            }
        }
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    # airflow parent group 조회
    parent_group_id = _get_or_create_parent_group(token)
    
    # Child groups 조회
    groups_response = requests.get(
        f"{KEYCLOAK_SERVER_URL}/admin/realms/{REALM}/groups/{parent_group_id}/children",
        headers=headers
    )
    
    groups = {}
    members = {}
    
    for group in groups_response.json():
        group_name = group["name"]
        group_id = group["id"]
        
        groups[group_name] = {"id": group_id}
        
        # 각 그룹의 멤버 조회
        members_response = requests.get(
            f"{KEYCLOAK_SERVER_URL}/admin/realms/{REALM}/groups/{group_id}/members",
            headers=headers
        )
        
        members[group_name] = [
            user["email"] for user in members_response.json()
        ]
    
    return {"groups": groups, "members": members}
```

#### 4. sync_groups_and_members()

```python
def sync_groups_and_members(token, sf_employees, kc_data):
    """
    Snowflake ↔ Keycloak 동기화
    
    변경사항:
    - 신규 그룹 생성
    - 신규 멤버 추가
    - 퇴사자 제거
    - 팀 이동 처리
    """
    stats = {
        "new_groups": 0,
        "members_added": 0,
        "members_removed": 0,
        "team_changes": 0,
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    parent_group_id = _get_or_create_parent_group(token)
    
    # A. 신규 그룹 생성
    for department in sf_employees.keys():
        if department not in kc_data["groups"]:
            _create_group(token, parent_group_id, department)
            stats["new_groups"] += 1
            log.info(f"Created new group: {department}")
    
    # B. 신규 멤버 추가 & C. 퇴사자 제거 & D. 팀 이동
    for department, employees in sf_employees.items():
        group_id = kc_data["groups"][department]["id"]
        current_members = set(kc_data["members"].get(department, []))
        sf_members = {emp["email"] for emp in employees}
        
        # B. 신규 멤버 추가
        to_add = sf_members - current_members
        for email in to_add:
            user_id = _get_or_create_user(token, email, employees)
            _add_user_to_group(token, user_id, group_id)
            stats["members_added"] += 1
            log.info(f"Added {email} to {department}")
        
        # C. 퇴사자 제거
        to_remove = current_members - sf_members
        for email in to_remove:
            user_id = _get_user_id_by_email(token, email)
            if user_id:
                _remove_user_from_group(token, user_id, group_id)
                stats["members_removed"] += 1
                log.info(f"Removed {email} from {department}")
    
    return stats
```

**핵심 로직:**
1. **신규 그룹 생성**: Snowflake에 있지만 Keycloak에 없는 department
2. **신규 멤버 추가**: 신규 입사자 → Keycloak 사용자 생성 + 그룹 추가
3. **퇴사자 제거**: Keycloak에 있지만 Snowflake에 없는 사용자 → 그룹에서 제거
4. **팀 이동**: 자동 감지 (같은 이메일이 다른 department에 있으면 이전 그룹 제거 + 새 그룹 추가)

---

## 🔍 Keycloak API 호출 헬퍼 함수

### _create_group()

```python
def _create_group(token, parent_group_id, group_name):
    """그룹 생성"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{KEYCLOAK_SERVER_URL}/admin/realms/{REALM}/groups/{parent_group_id}/children",
        headers=headers,
        json={"name": group_name}
    )
    response.raise_for_status()
```

### _get_or_create_user()

```python
def _get_or_create_user(token, email, employees):
    """사용자 조회 또는 생성"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # 기존 사용자 조회
    user_id = _get_user_id_by_email(token, email)
    if user_id:
        return user_id
    
    # 신규 사용자 생성
    name = next(emp["name"] for emp in employees if emp["email"] == email)
    response = requests.post(
        f"{KEYCLOAK_SERVER_URL}/admin/realms/{REALM}/users",
        headers=headers,
        json={
            "email": email,
            "username": email,
            "firstName": name,
            "enabled": True,
        }
    )
    response.raise_for_status()
    
    return _get_user_id_by_email(token, email)
```

### _add_user_to_group()

```python
def _add_user_to_group(token, user_id, group_id):
    """사용자를 그룹에 추가"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(
        f"{KEYCLOAK_SERVER_URL}/admin/realms/{REALM}/users/{user_id}/groups/{group_id}",
        headers=headers
    )
    response.raise_for_status()
```

### _remove_user_from_group()

```python
def _remove_user_from_group(token, user_id, group_id):
    """사용자를 그룹에서 제거"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(
        f"{KEYCLOAK_SERVER_URL}/admin/realms/{REALM}/users/{user_id}/groups/{group_id}",
        headers=headers
    )
    response.raise_for_status()
```

---

## 📎 Related

### Projects 배경 (Why)
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/Keycloak-SSO-도입-배경|Keycloak-SSO-도입-배경]] - 왜 Keycloak SSO를 도입했는가

### Technology (Core Concepts)
- [[Keycloak-Airflow-인증-개념]] - Keycloak, JWT, Auth Manager 개념
- [[Keycloak-OIDC-인증]] - OIDC 프로토콜 상세

### Operational (Usage)
- [[Keycloak-Airflow-운영가이드]] - 환경 변수 설정, DAG 태깅 방법, 문제 해결

### Technology (Related Implementation)
- [[Airflow-3.0-구현]] - Airflow 3.0 플랫폼 구현 상세
- [[Airflow]] - Airflow 기본 개념

### Projects (실제 사용)
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/팀별-데이터-격리-체계|팀별-데이터-격리-체계]] - 팀별 권한 격리 전략

---

**Metadata:**
