---
title: DataHub 커스텀 구현 상세
type: technical-implementation
tags:
  - datahub
  - custom-implementation
  - airflow
  - dbt
  - keycloak
  - 크래프트테크놀로지스
created: '2025-11-30'
updated: '2025-11-30'
status: active
project: qraft-data-platform
---

# DataHub 커스텀 구현 상세

## 📋 개요

**프로젝트**: [[qraft-data-platform-통합프로젝트|Qraft Data Platform]]
**구현 기간**: 2025-11-22 ~ 2025-11-27
**목적**: Airflow 3.x 및 Keycloak OIDC 통합을 위한 DataHub 커스텀 구현

## 🎯 구현 배경

### 문제점
1. **Airflow 3.x 비호환**: DataHub 공식 Airflow plugin이 Airflow 2.x만 지원
2. **Keycloak 통합**: URN 인코딩 불일치로 그룹 중복 생성
3. **메타데이터 누락**: DBT meta 필드가 DataHub owner로 매핑되지 않음

### 해결 방향
- Custom Airflow Source 개발
- Runtime Patch를 통한 DBT URN 통일
- Domain Pattern Mapping으로 플랫폼 간 통합

## 🏗️ 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│              DataHub Ingestion Layer                      │
│                                                            │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Custom    │  │     DBT      │  │   Snowflake     │  │
│  │   Airflow   │  │   Patches    │  │    Standard     │  │
│  │   Source    │  │  (Runtime)   │  │   Connector     │  │
│  └──────┬──────┘  └──────┬───────┘  └────────┬────────┘  │
│         │                │                   │             │
│         │  ┌─────────────▼──────────────┐    │             │
│         │  │  URN Encoding Unification  │    │             │
│         │  │  (Keycloak OIDC + quote)   │    │             │
│         │  └─────────────┬──────────────┘    │             │
│         │                │                   │             │
└─────────┼────────────────┼───────────────────┼─────────────┘
          │                │                   │
          ▼                ▼                   ▼
┌──────────────────────────────────────────────────────────┐
│                  DataHub GMS (Storage)                    │
│  ✅ 통일된 URN으로 그룹 중복 없음                           │
│  ✅ Airflow-DBT-Snowflake 메타데이터 연결                  │
└──────────────────────────────────────────────────────────┘
```

## 🔧 구현 #1: Custom Airflow Source

### 배경: Airflow 3.x Plugin 비호환

**문제**:
```
공식 acryl-datahub-airflow-plugin:
- Airflow 2.7-2.9.x만 지원
- Airflow 3.x serialized_dag 구조 변경 대응 못함
- OpenLineage 구버전 패키지 사용 (deprecated)
```

**기술적 배경**:
- Airflow 2.7부터: OpenLineage가 외부 패키지 → 네이티브 provider로 전환
- 구버전: `openlineage-airflow` (brittle, deprecated)
- 신버전: `apache-airflow-providers-openlineage` (stable)
- DataHub 플러그인이 구버전 사용으로 Airflow 3.x 비호환

### 해결책: REST API 기반 Custom Connector

**구현 위치**: `infrastructure/datahub/custom_sources/airflow/`

**파일 구조**:
```
airflow/
├── __init__.py                  # Package 초기화
├── config.py                    # Configuration (Keycloak, Domain Mapping 등)
├── auth.py                      # Keycloak OIDC 인증 클라이언트
├── api_client.py                # Airflow REST API v2 클라이언트
├── metadata_db_client.py        # Airflow metadata DB 직접 쿼리
├── metadata_utils.py            # 메타데이터 변환 (URN 생성, sanitization)
├── airflow_source.py            # 메인 Source 클래스
└── README.md                    # 상세 문서
```

**주요 기능**:

#### 1. Keycloak OIDC 인증 (`auth.py`)
```python
class AirflowAuthClient:
    def acquire_token(self):
        # Keycloak token endpoint 호출
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.config.keycloak_client_id,
            "client_secret": self.config.keycloak_client_secret
        }
        # Bearer token 획득
        # → Airflow API 호출 시 Authorization 헤더에 포함
```

#### 2. Airflow 3.x Task Lineage 추출 (`metadata_db_client.py`)
**문제**: Airflow 3.x serialized_dag 구조 변경
- Task 데이터가 `__var/__type` 구조로 저장됨
- `upstream_task_ids` 필드 없음, `downstream_task_ids`만 존재

**해결**:
```python
def get_task_dependencies(dag_id: str):
    # serialized_dag에서 task_dict 추출
    for task_id, task_data in tasks.items():
        task = task_data.get("__var", {})  # ← Airflow 3.x 구조
        downstream_ids = task.get("downstream_task_ids", [])

        # Downstream → Upstream 역변환
        for down_id in downstream_ids:
            task_deps[down_id]["upstream"].append(task_id)
```

**결과**: Task 간 lineage가 DataHub에 표시됨
- `dataJobInputOutput` 메트릭: 17 → 79 증가

#### 3. Asset (Dataset) Lineage & Metadata 상속 (`airflow_source.py`)
**기능**: Airflow 3.x Asset이 부모 DAG의 tags/owner 상속

**구현**:
```python
# airflow_source.py:600-630
def _process_asset(dag_id, asset_uri, is_inlet):
    # Asset URN 생성
    dataset_urn = make_dataset_urn(platform, name, env)

    # 부모 DAG의 tags 상속 (600-618)
    dag_tags = self._dag_tags_cache.get(dag_id, [])
    for tag in dag_tags:
        tag_urn = make_tag_urn(tag)  # Keycloak OIDC 형식 (quote_plus)
        dataset_tags.append(tag_urn)

    # 부모 DAG의 owner 상속 (620-630)
    dag_owners = self._dag_owners_cache.get(dag_id, [])
    for owner in dag_owners:
        owner_urn = make_group_urn(owner)  # (T) suffix → corpGroup
        dataset_owners.append(owner_urn)
```

**상속 규칙**:
- 하나의 Asset을 여러 DAG가 생성 → 모든 DAG의 tags/owners 합침 (deduplicate)
- Keycloak OIDC URN 인코딩 (`quote_plus`)으로 일관성 보장

#### 4. Domain Pattern Mapping (`metadata_utils.py:387-410`)
**목적**: Airflow-DBT-Snowflake 간 Domain 통합

**설정 예시**:
```yaml
domain_pattern_mapping:
  # Portfolio rebalancing DAGs
  ".*rebalancing.*": "urn:li:domain:Portfolio"
  ".*port_.*": "urn:li:domain:Portfolio"

  # Index data DAGs
  ".*index.*": "urn:li:domain:Index"
  ".*qqq.*": "urn:li:domain:Index"
```

**구현**:
```python
def extract_domain(dag_id: str, config) -> Optional[str]:
    for pattern, domain_urn in config.domain_pattern_mapping.items():
        if re.match(pattern, dag_id):
            return domain_urn  # 첫 번째 매칭 반환
    return None
```

**Cross-Platform 일관성**:
| Domain | Airflow DAG Pattern | DBT Model | Snowflake Schema |
|--------|---------------------|-----------|------------------|
| Portfolio | `.*rebalancing.*` | `port_*` | `mart.port_*` |
| Index | `.*index.*` | `index_*` | `invesco.*` |

#### 5. Cosmos DBT Outlet 추론 (`airflow_source.py`)
**목적**: Airflow Cosmos task → DBT 모델 자동 연결

**동작 원리**:
```python
# Cosmos task 이름 패턴
task_id = "transform_data.stg_us_sec_meta_base.run"

# 패턴 파싱
group_id = "transform_data"
model_name = "stg_us_sec_meta_base"
operation = "run"

# Schema 매핑 (prefix 기반)
cosmos_schema_mapping = {
    "stg_": "qraft_origin.staging",
    "int_": "qraft_origin.intermediate",
    "vw_": "qraft_origin.mart"
}

# → DBT URN 생성
dbt_urn = "dbt:qraft_origin.staging.stg_us_sec_meta_base"
```

**결과**:
```
Airflow Task                              → DataHub Dataset
────────────────────────────────────────────────────────────
transform_data.stg_us_sec_meta_base.run   → dbt:qraft_origin.staging.stg_us_sec_meta_base
transform_data.dim_holiday.run            → dbt:qraft_origin.core.dim_holiday
```

## 🔧 구현 #2: DBT Custom Patches

### 배경: Keycloak OIDC URN 불일치

**문제**:
```
Keycloak:  urn:li:corpGroup:ML+Platform+%28T%29  (quote_plus)
DBT:       urn:li:corpGroup:ML Platform (T)      (공백 그대로)
Airflow:   urn:li:corpuser:ML Platform (T)       (user로 잘못)

→ Groups 페이지에 중복 그룹 3개 생성!
→ Owner 매핑 실패!
```

**Root Cause**:
- Keycloak: `urllib.parse.quote_plus()` 사용
- DBT: DataHub `UrnEncoder.encode_string()` 사용 (다른 규칙)
- Airflow: 모든 owner를 user로 처리

### 해결책: Runtime Patch

**구현 위치**: `infrastructure/datahub/environments/local/entrypoint-actions.sh`

**패치 방식**: 컨테이너 시작 시 `sed` 명령으로 DataHub 내부 파일 수정

#### Patch 1: Tag URL Encoding (`entrypoint-actions.sh:45-64`)
```bash
# Before (DataHub 기본)
def make_tag_urn(tag_name):
    return f"urn:li:tag:{UrnEncoder.encode_string(tag_name)}"
    # → "team:ML Platform (T)" (공백 그대로)

# After (Patch 적용)
def make_tag_urn(tag_name):
    from urllib.parse import quote_plus
    return f"urn:li:tag:{quote_plus(tag_name)}"
    # → "team:ML+Platform+%28T%29" (Keycloak OIDC와 동일)
```

**패치 명령**:
```bash
sed -i 's/UrnEncoder\.encode_string(tag_str)/quote_plus(tag_str)/' \
    /usr/local/lib/python3.10/site-packages/datahub/emitter/mce_builder.py
```

#### Patch 2: Owner Group URN (`entrypoint-actions.sh:66-86`)
```bash
# Before
def make_group_urn(group_name):
    return f"urn:li:corpGroup:{UrnEncoder.encode_string(group_name)}"
    # → "urn:li:corpGroup:ML Platform (T)"

# After
def make_group_urn(group_name):
    from urllib.parse import quote_plus
    return f"urn:li:corpGroup:{quote_plus(group_name)}"
    # → "urn:li:corpGroup:ML+Platform+%28T%29"
```

#### Patch 3: Owner Type Detection (`entrypoint-actions.sh:88-97`)
```python
# Before (DBT default)
owner_type = OwnershipTypeClass.TECHNICAL_OWNER  # 항상 TECHNICAL

# After (Patch)
if owner_str.endswith(" (T)"):
    owner_type = OwnershipTypeClass.BUSINESS_OWNER  # 팀 그룹
    entity_type = "corpGroup"  # ← Key 변경!
else:
    owner_type = OwnershipTypeClass.TECHNICAL_OWNER
    entity_type = "corpuser"
```

#### Patch 4: DBT Meta Mapping (Configuration)
**파일**: `infrastructure/datahub/environments/common/ingestion/dbt_qraft.yml`

```yaml
source:
  type: dbt
  config:
    # Meta Mapping 활성화
    enable_meta_mapping: true
    meta_mapping:
      business_owner:
        match: "^owner$"
        operation: "add_owner"
        config:
          owner_type: "corpGroup"  # 팀 그룹으로
      technical_owner:
        match: "^technical_owner$"
        operation: "add_owner"
        config:
          owner_type: "corpGroup"
```

**DBT 모델 예시**:
```yaml
# models/_models.yml
models:
  - name: fct_market_data
    meta:
      owner: "Strategy (T)"           # → BUSINESS_OWNER (corpGroup)
      technical_owner: "ML Platform (T)"  # → TECHNICAL_OWNER (corpGroup)
```

### 검증 방법

**패치 적용 확인**:
```bash
docker logs datahub-actions | grep "patch"
# ✅ DBT tag URL encoding patch applied (quote_plus)
# ✅ Owner group URL encoding patch applied (quote_plus)
# ✅ DBT owner group patch applied
```

**URN 일관성 테스트**:
```python
from datahub.emitter.mce_builder import make_group_urn, make_tag_urn

# 모두 동일한 인코딩
assert make_group_urn("ML Platform (T)") == "urn:li:corpGroup:ML+Platform+%28T%29"
assert make_tag_urn("team:ML Platform (T)") == "urn:li:tag:team:ML+Platform+%28T%29"
```

## 🔧 구현 #3: Dataset URN Sanitization

### 배경: URN Validation 실패

**문제**:
```
GMS 로그: Invalid urn: urn:li:dataset:(urn:li:dataPlatform:snowflake,QRAFT_ORIGIN/MART/VW_SECURITY,LOCAL)

원인:
1. env="LOCAL" → DataHub가 인식 못함 (DEV/PROD/QA만 허용)
2. 대문자, 하이픈, 공백 → URN validation 실패
```

### 해결책: Sanitization

**구현 위치**: `custom_sources/airflow/metadata_utils.py:177-211`

```python
def _sanitize_dataset_name(name: str, platform: str) -> str:
    """
    DataHub URN validation을 통과하도록 dataset name 정제
    """
    # 1. 소문자 변환
    name = name.lower()

    # 2. 플랫폼별 처리
    if platform == "snowflake":
        # QRAFT_ORIGIN/MART/TABLE → qraft_origin.mart.table
        name = name.replace("/", ".")
    elif platform in ["s3", "file"]:
        # nas-quant/path/file.txt → nas_quant.path.file.txt
        name = name.replace("/", ".")

    # 3. 특수문자 제거
    name = re.sub(r"[^a-z0-9._]", "_", name)  # 허용: [a-z0-9._]
    name = re.sub(r"_+", "_", name)  # 중복 밑줄 제거
    name = name.strip("_")  # 앞뒤 밑줄 제거

    return name
```

**변환 예시**:
```
Before                                → After
─────────────────────────────────────────────────────────────
QRAFT_ORIGIN/MART/VW_SECURITY        → qraft_origin.mart.vw_security
nas-quant/short-term/lseg/file.txt   → nas_quant.short_term.lseg.file.txt
PCAP_TPEX_-_Stocks                   → pcap_tpex_stocks
```

**env 변경**:
```yaml
# 모든 ingestion recipe
config:
  env: "DEV"  # LOCAL → DEV 변경 (DataHub 인식 가능)
```

## 📊 구현 결과

### Before vs After

| 메트릭 | Before | After | 개선 |
|--------|--------|-------|------|
| **Airflow Assets 수집** | 0개 | 38개 | ✅ 100% |
| **Task Lineage** | 17개 | 79개 | +362% |
| **Groups 중복** | 3개 (Keycloak, DBT, Airflow) | 1개 | ✅ 통일 |
| **Owner 매핑 실패** | 100% | 0% | ✅ 해결 |
| **Domain 자동 할당** | 수동 | 자동 (pattern) | ✅ 자동화 |

### URN 일관성 보장

**통일 전**:
```
Keycloak → urn:li:corpGroup:ML+Platform+%28T%29
DBT      → urn:li:corpGroup:ML Platform (T)
Airflow  → urn:li:corpuser:ML Platform (T)

→ 3개의 다른 엔티티 생성!
```

**통일 후**:
```
Keycloak → urn:li:corpGroup:ML+Platform+%28T%29
DBT      → urn:li:corpGroup:ML+Platform+%28T%29  ← Patch 적용
Airflow  → urn:li:corpGroup:ML+Platform+%28T%29  ← (T) 감지

→ 1개로 통일! Owner 매핑 성공!
```

## 🔗 관련 문서

### 프로젝트
- [[qraft-data-platform-통합프로젝트|Qraft Data Platform]] - 메인 프로젝트
- [[DataHub-시행착오-해결과정|DataHub 시행착오 해결 과정]] - 문제 해결 기록
- [[Git-Subtree-마이그레이션|Git Subtree 마이그레이션]] - 구조 변경

### 기술 문서
- [[DataHub|DataHub - 메타데이터 관리]] - DataHub 개요
- [[Keycloak]] - SSO 통합 인증
- [[Airflow|Airflow]] - 파이프라인 오케스트레이션

### 프로젝트 저장소 문서
- `infrastructure/datahub/custom_sources/airflow/README.md` - Custom Airflow Source 상세
- `infrastructure/datahub/custom_sources/dbt/README.md` - DBT Patches 상세
- `infrastructure/datahub/docs/DESIGN_DECISIONS.md` - 설계 결정 및 히스토리

---

**구현 완료**: 2025-11-27
**버전**: v1.2.0
**구현자**: ML Platform Infrastructure Team
