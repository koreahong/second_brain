---
title: Keycloak OIDC 인증
type: technical-implementation
tags:
  - keycloak
  - oidc
  - sso
  - authentication
  - jwt
created: '2025-11-30'
updated: '2025-11-30'
status: evergreen
---
# Keycloak OIDC 인증

## 📋 개요

Keycloak은 오픈소스 IAM(Identity and Access Management) 솔루션으로, OIDC(OpenID Connect) 및 SAML 2.0 프로토콜을 지원합니다.

**크래프트테크놀로지스 적용:**
- Airflow, DataHub SSO 통합 인증
- Service Account 기반 M2M 인증
- Keycloak 그룹 → 플랫폼 역할 자동 매핑

## 🔐 OIDC 인증 플로우

### 사용자 SSO 인증 (Authorization Code Flow)

```
┌──────────┐                                   ┌──────────┐
│  Browser │                                   │ Keycloak │
└──────────┘                                   └──────────┘
     │                                                │
     │  1. /login 접속                                │
     │──────────────────────────────────────────────>│
     │                                                │
     │  2. 로그인 페이지 반환                         │
     │<──────────────────────────────────────────────│
     │                                                │
     │  3. ID/PW 입력                                 │
     │──────────────────────────────────────────────>│
     │                                                │
     │  4. Authorization Code 발급                   │
     │<──────────────────────────────────────────────│
     │                                                │
┌──────────┐                                   ┌──────────┐
│ Airflow  │                                   │ Keycloak │
└──────────┘                                   └──────────┘
     │                                                │
     │  5. Code로 Token 교환                          │
     │──────────────────────────────────────────────>│
     │                                                │
     │  6. Access Token + Refresh Token              │
     │<──────────────────────────────────────────────│
     │                                                │
     │  7. Token으로 사용자 정보 조회                 │
     │──────────────────────────────────────────────>│
     │                                                │
     │  8. UserInfo (email, groups, etc.)            │
     │<──────────────────────────────────────────────│
```

### Service Account 인증 (Client Credentials Flow)

```
┌──────────┐                                   ┌──────────┐
│ Airflow  │                                   │ Keycloak │
│  (DAG)   │                                   │          │
└──────────┘                                   └──────────┘
     │                                                │
     │  1. Client ID + Secret 전송                    │
     │──────────────────────────────────────────────>│
     │                                                │
     │  2. Service Account Token (JWT)               │
     │<──────────────────────────────────────────────│
     │                                                │
┌──────────┐                                   ┌──────────┐
│ Airflow  │                                   │ DataHub  │
└──────────┘                                   └──────────┘
     │                                                │
     │  3. API 호출 (Bearer Token)                    │
     │──────────────────────────────────────────────>│
     │                                                │
     │  4. Token 검증 (Keycloak Public Key)           │
     │                                        (DataHub)│
     │                                                │
     │  5. 응답                                        │
     │<──────────────────────────────────────────────│
```

## 🔧 Airflow Keycloak 통합

### Custom Auth Manager 구현

```python
# plugins/airflow_keycloak/auth_manager.py

from airflow.auth.managers.base_auth_manager import BaseAuthManager
from flask import redirect, request, session
import requests

class KeycloakAuthManager(BaseAuthManager):
    def __init__(self):
        self.keycloak_url = os.getenv("KEYCLOAK_SERVER_URL")
        self.realm = os.getenv("KEYCLOAK_REALM")
        self.client_id = os.getenv("KEYCLOAK_CLIENT_ID")
        self.client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET")
        
        # OIDC 엔드포인트
        self.authorization_endpoint = f"{self.keycloak_url}/realms/{self.realm}/protocol/openid-connect/auth"
        self.token_endpoint = f"{self.keycloak_url}/realms/{self.realm}/protocol/openid-connect/token"
        self.userinfo_endpoint = f"{self.keycloak_url}/realms/{self.realm}/protocol/openid-connect/userinfo"
    
    def get_url_login(self, **kwargs) -> str:
        """로그인 페이지 URL 생성"""
        redirect_uri = request.url_root.rstrip('/') + '/oauth-authorized/keycloak'
        
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": "openid profile email"
        }
        
        return f"{self.authorization_endpoint}?{urlencode(params)}"
    
    def oauth_callback(self):
        """OAuth 콜백 처리"""
        # 1. Authorization Code 받기
        code = request.args.get('code')
        if not code:
            raise AirflowException("No authorization code received")
        
        # 2. Code를 Token으로 교환
        redirect_uri = request.url_root.rstrip('/') + '/oauth-authorized/keycloak'
        
        token_response = requests.post(
            self.token_endpoint,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        )
        
        token_data = token_response.json()
        access_token = token_data["access_token"]
        
        # 3. Access Token으로 사용자 정보 조회
        userinfo_response = requests.get(
            self.userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        userinfo = userinfo_response.json()
        
        # 4. JIT Provisioning (사용자 자동 생성/업데이트)
        user = self._get_or_create_user(userinfo)
        
        # 5. Keycloak 그룹 → Airflow 역할 매핑
        self._sync_user_roles(user, userinfo.get("groups", []))
        
        # 6. 세션 생성
        session["user_id"] = user.id
        session["access_token"] = access_token
        
        return redirect("/")
    
    def _get_or_create_user(self, userinfo: dict):
        """JIT Provisioning: 최초 로그인 시 사용자 자동 생성"""
        username = userinfo.get("preferred_username")
        email = userinfo.get("email")
        
        # DB에서 사용자 조회
        user = session.query(User).filter_by(username=username).first()
        
        if not user:
            # 신규 사용자 생성
            user = User(
                username=username,
                email=email,
                first_name=userinfo.get("given_name"),
                last_name=userinfo.get("family_name"),
                active=True
            )
            session.add(user)
            session.commit()
        
        return user
    
    def _sync_user_roles(self, user, keycloak_groups: List[str]):
        """Keycloak 그룹 → Airflow 역할 매핑"""
        # 기존 역할 삭제
        user.roles = []
        
        # TEAM_MAPPING (환경변수에서 로드)
        team_mapping = json.loads(os.getenv("KEYCLOAK_TEAM_MAPPING", "{}"))
        # 예: {"ml-platform-admin": "Admin", "qraft-ml-platform (T)": "User"}
        
        for group in keycloak_groups:
            if group in team_mapping:
                role_name = team_mapping[group]
                role = session.query(Role).filter_by(name=role_name).first()
                
                if role:
                    user.roles.append(role)
        
        # 기본 역할: Public (그룹 없음)
        if not user.roles:
            public_role = session.query(Role).filter_by(name="Public").first()
            user.roles.append(public_role)
        
        session.commit()
```

### DAG 접근 제어

```python
# plugins/airflow_keycloak/auth_manager.py (계속)

def is_authorized_dag(self, method: str, details: DagDetails, user) -> bool:
    """DAG 접근 권한 검증"""
    dag_id = details.id
    
    # DAG의 team 태그 추출
    dag = DagBag().get_dag(dag_id)
    team_tags = [tag for tag in dag.tags if tag.startswith("team:")]
    
    if not team_tags:
        # team 태그 없음 → Public (모두 접근 가능)
        return True
    
    # team:ML Platform (T) → "ML Platform (T)"
    required_team = team_tags[0].replace("team:", "")
    
    # 사용자 그룹 확인
    user_groups = self._get_user_groups(user)
    
    # Admin은 모든 DAG 접근 가능
    if "ml-platform-admin" in user_groups:
        return True
    
    # 팀 그룹 일치 확인
    if required_team in user_groups:
        return True
    
    # Public 태그는 모두 접근 가능
    if required_team == "Public":
        return True
    
    return False
```

### Service Account Token 발급

```python
# dags/common/keycloak_client.py

import requests
from airflow.models import Variable

def get_service_account_token() -> str:
    """Keycloak Service Account Token 발급"""
    
    keycloak_url = Variable.get("keycloak_server_url")
    realm = Variable.get("keycloak_realm")
    client_id = Variable.get("keycloak_sa_client_id")
    client_secret = Variable.get("keycloak_sa_client_secret")
    
    token_endpoint = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/token"
    
    response = requests.post(
        token_endpoint,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
    )
    
    token_data = response.json()
    return token_data["access_token"]

# DAG에서 사용
@task
def call_datahub_api(**kwargs):
    token = get_service_account_token()
    
    response = requests.post(
        "http://datahub:8080/api/graphql",
        headers={"Authorization": f"Bearer {token}"},
        json={"query": "..."}
    )
    
    return response.json()
```

## 🔧 DataHub Keycloak 통합

### OIDC 설정

```yaml
# docker-compose.yaml

services:
  datahub-frontend:
    environment:
      # OIDC 활성화
      AUTH_OIDC_ENABLED: "true"
      AUTH_OIDC_CLIENT_ID: "datahub"
      AUTH_OIDC_CLIENT_SECRET: "${KEYCLOAK_CLIENT_SECRET}"
      AUTH_OIDC_DISCOVERY_URI: "https://keycloak.example.com/realms/qraft/.well-known/openid-configuration"
      AUTH_OIDC_REDIRECT_URI: "https://datahub.example.com/callback/oidc"
      
      # JIT Provisioning
      AUTH_OIDC_JIT_PROVISIONING_ENABLED: "true"
      AUTH_OIDC_PRE_PROVISIONING_REQUIRED: "false"
      
      # 그룹 매핑
      AUTH_OIDC_GROUPS_CLAIM: "groups"
      AUTH_OIDC_EXTRACT_GROUPS_ENABLED: "true"
```

### Owner 기반 접근 제어

DataHub에서는 **Owner** 기반으로 엔티티 수정 권한을 제어합니다:

```yaml
# policies/owner_only_edit.yaml

id: owner-only-edit-policy
name: Owner Only Edit
description: Only owners can modify entities
type: METADATA
state: ACTIVE
actors:
  users: []
  groups: []
  resourceOwners: true  # Owner만 허용
privileges:
  - EDIT_ENTITY
  - DELETE_ENTITY
resources:
  type: dataset
  allResources: true
```

**적용 효과:**
- Keycloak 그룹 `Strategy (T)` → DataHub Owner `urn:li:corpGroup:Strategy (T)`
- `Strategy (T)` 그룹 멤버만 해당 Dataset 수정 가능

## ⚠️ 트라이 에러

### 문제 1: URN 인코딩 불일치

**증상:**
```
DataHub UI에서 동일한 그룹이 3개로 표시됨:
- Strategy Team
- Strategy+Team
- Strategy%20Team
```

**원인:**
- Keycloak OIDC: `quote_plus()` 사용 → `Strategy+Team`
- DBT: `UrnEncoder.encode_string()` → `Strategy%20Team`
- Airflow: Owner를 User로 처리 → `Strategy Team`

**해결:**
```bash
# entrypoint-actions.sh (DataHub Actions 컨테이너)

# DBT 소스 패치: UrnEncoder → quote_plus
sed -i 's/UrnEncoder\.encode_string(tag_str)/quote_plus(tag_str)/' \
    /usr/local/lib/python3.10/site-packages/datahub/emitter/mce_builder.py

# Owner 타입 변경: corpuser → corpGroup
sed -i 's/make_user_urn(owner)/make_group_urn(owner)/' \
    /usr/local/lib/python3.10/site-packages/datahub/ingestion/source/dbt/dbt_core.py
```

**결과:**
- 중복 그룹 3개 → 1개로 통합
- Owner URN 일관성 확보

### 문제 2: Redirect URI 불일치

**증상:**
```
Error: Invalid parameter: redirect_uri
```

**원인:**
Keycloak Client 설정의 Redirect URI와 실제 콜백 URL이 다름

**해결:**
```python
# Airflow 콜백 URL
redirect_uri = request.url_root.rstrip('/') + '/oauth-authorized/keycloak'
# → http://localhost:8082/oauth-authorized/keycloak

# Keycloak Admin Console → Clients → airflow-web → Settings
# Valid Redirect URIs에 추가:
#   - http://localhost:8082/oauth-authorized/keycloak
#   - https://airflow.example.com/oauth-authorized/keycloak
```

### 문제 3: Token 만료 처리

**증상:**
```
401 Unauthorized: Token expired
```

**원인:**
- Access Token 만료 시간: 1시간
- 장시간 작업 중 Token 만료

**해결:**
```python
def get_service_account_token_with_refresh() -> str:
    """Token 캐싱 및 자동 갱신"""
    
    # 1. 캐시 확인
    cached_token = redis_client.get("sa_token")
    if cached_token:
        # 만료 5분 전이면 갱신
        exp = jwt.decode(cached_token, options={"verify_signature": False})["exp"]
        if exp - time.time() > 300:  # 5분 여유
            return cached_token
    
    # 2. 새 토큰 발급
    response = requests.post(
        token_endpoint,
        data={"grant_type": "client_credentials", ...}
    )
    
    token = response.json()["access_token"]
    
    # 3. 캐시 저장 (55분)
    redis_client.setex("sa_token", 3300, token)
    
    return token
```

### 문제 4: 그룹 매핑 누락

**증상:**
```
사용자 로그인 성공했지만 "Public" 역할만 부여됨
```

**원인:**
Keycloak User에 그룹이 없거나, `groups` claim이 Token에 포함되지 않음

**해결:**
```yaml
# Keycloak Admin Console → Client Scopes → profile → Mappers

# 1. Groups Mapper 추가
Name: groups
Mapper Type: Group Membership
Token Claim Name: groups
Full group path: OFF  # 그룹명만 반환 (경로 제외)
Add to ID token: ON
Add to access token: ON
Add to userinfo: ON
```

**검증:**
```python
# Airflow 로그인 시 로그 확인
log.info(f"User {username} groups: {userinfo.get('groups', [])}")
# → ['ml-platform-admin', 'qraft-ml-platform (T)']
```

## 📎 Related

### Projects 배경 (Why)
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/Keycloak-SSO-도입-배경|Keycloak-SSO-도입-배경]] - 왜 Keycloak SSO를 도입했는가

### Technology (Core Concepts)
- [[Keycloak-Airflow-인증-개념]] - Airflow Keycloak 인증 개념

### Technology (Related Implementation)
- [[Keycloak-Airflow-구현]] - Airflow Custom Auth Manager 구현
- [[Keycloak-Airflow-운영가이드]] - Keycloak 운영 방법
- [[Airflow-3.0-구현]] - Airflow 3.0 플랫폼 통합

### Projects (실제 사용)
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/팀별-데이터-격리-체계|팀별-데이터-격리-체계]] - 팀별 권한 격리 전략
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/DataHub-도입|DataHub-도입]] - DataHub OIDC 설정

---

**작성일**: 2025-11-30
**카테고리**: Authentication & Authorization
**태그**: #keycloak #oidc #sso #authentication
