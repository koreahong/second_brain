---
created: '2025-11-30'
updated: '2025-11-30'
tags:
  - Technology
  - Airflow
  - DataHub
  - Metadata
  - DataPlatform
related:
  - Keycloak-OIDC-인증
  - DBT-Incremental-구현
  - Airflow-3.0-업그레이드-배경
---
# Airflow 3.0 구현

## 개요

Apache Airflow 3.0으로 업그레이드하면서 주요 아키텍처 변경 사항을 적용하고, DataHub 메타데이터 수집을 위한 커스텀 REST API Connector를 개발했습니다.

**핵심 구현:**
- Custom REST API Connector (DataHub 연동)
- Asset-based lineage 시스템
- Serialized DAG 구조 파싱
- Metadata DB 직접 쿼리
- Keycloak OIDC 인증 통합

## 주요 기술 스택

- **Airflow 3.1.3** (3.0.6 → 3.1.3 업그레이드)
- **PostgreSQL** (Metadata DB)
- **DataHub** (메타데이터 카탈로그)
- **Keycloak OIDC** (인증)
- **Python 3.10+**
- **psycopg2** (DB 직접 쿼리)

## 1. Custom REST API Connector 구조

### 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                      DataHub Ingestion                       │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │          AirflowSource (airflow_source.py)            │  │
│  │  - DAG/Task 메타데이터 추출                            │  │
│  │  - Asset lineage 추출                                  │  │
│  │  - Task dependencies 추출                              │  │
│  │  - DataHub work units 생성                             │  │
│  └──────┬───────────────────────────────┬───────────────────┘  │
│         │                               │                       │
│  ┌──────▼──────────────────┐  ┌─────────▼─────────────────┐  │
│  │ AirflowAPIClient        │  │ AirflowMetadataDBClient   │  │
│  │ (api_client.py)         │  │ (metadata_db_client.py)   │  │
│  │ - REST API v2 호출      │  │ - serialized_dag 파싱     │  │
│  │ - Pagination 처리       │  │ - Task dependencies 추출  │  │
│  │ - Filtering 적용        │  │ - Asset outlets 추출      │  │
│  └──────┬──────────────────┘  └─────────┬─────────────────┘  │
│         │                               │                       │
│  ┌──────▼──────────────────┐            │                       │
│  │ AirflowAuthClient       │            │                       │
│  │ (auth.py)               │            │                       │
│  │ - Keycloak OIDC token   │            │                       │
│  │ - Basic Auth fallback   │            │                       │
│  └──────┬──────────────────┘            │                       │
└─────────┼─────────────────────────────────┼───────────────────────┘
          │                               │
          │ HTTP                          │ PostgreSQL
          ▼                               ▼
  ┌────────────────────┐     ┌──────────────────────┐
  │ Airflow REST API   │     │ Airflow Metadata DB  │
  │ (Keycloak 인증)    │     │ (PostgreSQL)         │
  └────────────────────┘     └──────────────────────┘
```

### 파일 구조

```
infrastructure/datahub/custom_sources/airflow/
├── __init__.py                  # Package 초기화
├── config.py                    # Configuration 클래스
├── auth.py                      # Keycloak OIDC 인증 클라이언트
├── api_client.py                # Airflow API v2 클라이언트
├── metadata_db_client.py        # Airflow metadata DB 직접 쿼리
├── metadata_utils.py            # 메타데이터 변환 유틸리티
└── airflow_source.py            # 메인 Source 클래스
```

## 2. 핵심 기술 구현

### 2.1 Serialized DAG 파싱 (Airflow 3.x 구조 변경 대응)

**문제:** Airflow 3.x에서 `serialized_dag` 테이블의 JSON 구조가 변경되어 기존 DataHub 플러그인이 작동하지 않음.

**Airflow 2.x 구조:**
```json
{
  "tasks": [
    {
      "task_id": "task1",
      "downstream_task_ids": ["task2"]
    }
  ]
}
```

**Airflow 3.x 구조:**
```json
{
  "dag": {
    "tasks": [
      {
        "__var": {
          "task_id": "task1",
          "downstream_task_ids": ["task2"]
        },
        "__type": "operator"
      }
    ]
  }
}
```

**구현 코드:**

```python
# metadata_db_client.py:129-166
def get_task_dependencies(self, dag_id: str) -> Dict[str, List[str]]:
    """
    Extract task dependencies from serialized DAG data
    """
    with self._get_connection() as conn:
        with conn.cursor() as cursor:
            # Query serialized DAG data (Airflow 3.x)
            query = """
                SELECT data
                FROM serialized_dag
                WHERE dag_id = %s
            """
            cursor.execute(query, (dag_id,))
            result = cursor.fetchone()
            
            dag_data = result["data"]
            if isinstance(dag_data, str):
                dag_data = json.loads(dag_data)
            
            # Airflow 3.x: tasks in "dag" wrapper with __var/__type
            if "dag" in dag_data:
                tasks = dag_data["dag"].get("tasks", [])
            else:
                tasks = dag_data.get("tasks", [])
            
            upstream_deps = {}
            downstream_info = {}
            
            for task in tasks:
                # Airflow 3.x uses __var to store actual task data
                if "__var" not in task:
                    continue
                
                task_var = task["__var"]
                task_id = task_var.get("task_id")
                
                # Initialize upstream deps
                upstream_deps[task_id] = []
                
                # Collect downstream info (will be inverted)
                downstream_task_ids = task_var.get("downstream_task_ids", [])
                downstream_info[task_id] = downstream_task_ids
            
            # Second pass: Invert downstream → upstream
            for task_id, downstream_ids in downstream_info.items():
                for downstream_id in downstream_ids:
                    if downstream_id in upstream_deps:
                        upstream_deps[downstream_id].append(task_id)
            
            return upstream_deps
```

**핵심:**
1. `__var` 키로 실제 task 데이터 추출
2. `downstream_task_ids`를 역순으로 변환하여 `upstream_deps` 생성
3. DataHub가 요구하는 형식 (task → upstream list) 제공

### 2.2 Asset Outlet 추출

**문제:** Airflow 3.x의 Asset (Dataset) outlet 정보가 REST API에 없음.

**해결:** Metadata DB 직접 쿼리 (`task_outlet_asset_reference` 테이블)

```python
# metadata_db_client.py:195-222
def get_task_outlets(self, dag_id: str) -> Dict[str, List[str]]:
    """
    Extract task outlets (Dataset outputs) from metadata DB
    """
    with self._get_connection() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    sd.dag_id,
                    tor.task_id,
                    a.uri
                FROM task_outlet_asset_reference tor
                JOIN asset a ON tor.asset_id = a.id
                JOIN serialized_dag sd ON tor.dag_id = sd.dag_id
                WHERE sd.dag_id = %s
            """
            cursor.execute(query, (dag_id,))
            results = cursor.fetchall()
            
            # Group outlets by task_id
            outlets = {}
            for row in results:
                task_id = row["task_id"]
                uri = row["uri"]
                
                if task_id not in outlets:
                    outlets[task_id] = []
                outlets[task_id].append(uri)
            
            return outlets
```

### 2.3 Cosmos DBT Outlet 추론

**문제:** Airflow Cosmos로 실행되는 DBT task는 명시적 outlet이 없음.

**해결:** Task 이름 패턴으로 DBT 모델 URN 추론

```python
# airflow_source.py:509-578
def _infer_cosmos_outlet(self, task_id: str) -> Optional[str]:
    """
    Infer dataset outlet URN from Cosmos DBT task name
    
    Cosmos task naming pattern: {group_id}.{model_name}.{run|test}
    Example: transform_data.stg_us_sec_meta_base.run
    """
    import re
    
    group_pattern = self.config.cosmos_task_group_pattern
    
    # Match Cosmos task pattern: {group}.{model}.run or {group}.{model}_run
    cosmos_pattern = rf"^{re.escape(group_pattern)}\.(.+?)(?:\.run|_run)$"
    match = re.match(cosmos_pattern, task_id)
    
    if not match:
        return None
    
    model_name = match.group(1)
    
    # Determine database.schema from mapping
    db_schema = None
    if self.config.cosmos_schema_mapping:
        # Check model prefix (sorted by longest first)
        for prefix, mapping in sorted(
            self.config.cosmos_schema_mapping.items(),
            key=lambda x: len(x[0]),
            reverse=True,
        ):
            if model_name.startswith(prefix):
                db_schema = mapping
                break
    
    # Fall back to default database.schema
    if not db_schema:
        db_schema = f"{self.config.cosmos_outlet_database}.{self.config.cosmos_outlet_schema}"
    
    # Build the dataset URN
    dataset_name = f"{db_schema}.{model_name}"
    
    # Platform: DBT (task→model→table) or direct to Snowflake
    platform = (
        "dbt"
        if self.config.cosmos_outlet_to_dbt
        else self.config.cosmos_outlet_platform
    )
    
    dataset_urn = make_dataset_urn(
        platform=platform, name=dataset_name, env=self.config.env
    )
    
    logger.info(
        f"Inferred Cosmos outlet: task '{task_id}' → {platform}:'{dataset_name}'"
    )
    return dataset_urn
```

**Schema Mapping 예시:**
```yaml
cosmos_schema_mapping:
  # Core dimension tables
  "dim_holiday": "qraft_origin.core"
  "dim_ticker": "qraft_origin.core"
  # Employee dimension tables
  "dim_flex": "qraft_automation.employee"
  "flex_": "qraft_automation.employee"
  # Layer-based mapping
  "int_": "qraft_origin.intermediate"
  "stg_": "qraft_origin.staging"
  "vw_": "qraft_origin.mart"
```

**결과:**
```
Task ID                              → Dataset URN
────────────────────────────────────────────────────────────
transform_data.dim_holiday.run       → dbt:qraft_origin.core.dim_holiday
transform_data.stg_us_sec_meta.run   → dbt:qraft_origin.staging.stg_us_sec_meta
transform_data.us_simul_data_run     → dbt:qraft_origin.mart.us_simul_data
```

### 2.4 Domain Pattern Mapping (Cross-Platform Integration)

**문제:** Airflow DAG, DBT 모델, Snowflake 테이블이 서로 다른 Domain에 속해 lineage 추적 어려움.

**해결:** DAG ID 패턴 기반 자동 Domain 할당

```python
# metadata_utils.py:387-410
def extract_domain(
    self, dag_id: str, domain_pattern_mapping: Dict[str, str]
) -> Optional[str]:
    """
    Extract domain from DAG ID using pattern mapping
    
    Args:
        dag_id: DAG identifier
        domain_pattern_mapping: Regex patterns → Domain URN mapping
    
    Returns:
        Domain URN or None
    """
    import re
    
    for pattern, domain_urn in domain_pattern_mapping.items():
        if re.search(pattern, dag_id, re.IGNORECASE):
            logger.debug(
                f"DAG '{dag_id}' matched pattern '{pattern}' → domain '{domain_urn}'"
            )
            return domain_urn
    
    logger.debug(f"DAG '{dag_id}' matched no domain patterns")
    return None
```

**설정 예시:**
```yaml
domain_pattern_mapping:
  # Portfolio rebalancing DAGs
  ".*rebalancing.*": "urn:li:domain:Portfolio"
  ".*port_.*": "urn:li:domain:Portfolio"
  # Index data DAGs
  ".*index.*": "urn:li:domain:Index"
  ".*qqq.*": "urn:li:domain:Index"
  # FRED economic data DAGs
  ".*fred.*": "urn:li:domain:FRED"
  # Employee data DAGs
  ".*flex.*": "urn:li:domain:Employee"
  # Security/Simul data DAGs
  ".*simul.*": "urn:li:domain:Security"
  # Core dimension DAGs
  ".*ticker.*": "urn:li:domain:Core"
```

**Cross-Platform 일관성:**

| Domain | Airflow DAG Pattern | DBT Model | Snowflake Schema |
|--------|---------------------|-----------|------------------|
| Portfolio | `.*rebalancing.*` | `port_*` | `mart.port_*` |
| Index | `.*index.*`, `.*qqq.*` | `index_*` | `invesco.*` |
| FRED | `.*fred.*` | FRED 모델 | `fred.*` |
| Employee | `.*flex.*` | `dim_flex*` | `employee.*` |
| Security | `.*simul.*` | `int_us_simul_*` | `mart.us_sec_*` |
| Core | `.*ticker.*`, `.*dim_.*` | `dim_*` | `core.*` |

### 2.5 Asset Metadata 상속 (Tags & Ownership)

**문제:** Asset은 DAG의 tags와 owner 정보를 자동으로 상속받아야 함.

**구현:**

```python
# airflow_source.py:620-732
def _extract_assets(self) -> Iterable[MetadataWorkUnit]:
    """Extract Airflow Assets with tag/owner inheritance"""
    
    for asset_data in self.api_client.get_assets():
        asset_uri = asset_data.get("uri", "unknown")
        asset_urn = self.transformer.make_asset_urn(asset_uri)
        
        # Get asset lineage to find producing DAGs
        events = self.api_client.get_asset_events(asset_uri)
        producing_dags = set()
        dag_tags_list = []
        dag_owners_list = []
        
        for event in events:
            dag_id = event.get("source_dag_id")
            if dag_id:
                producing_dags.add(dag_id)
        
        # Fetch DAG metadata for producing DAGs
        for dag_id in producing_dags:
            dag_data = self.api_client.get_dag(dag_id)
            if dag_data:
                # Extract tags from DAG
                tags = dag_data.get("tags", [])
                for tag in tags:
                    tag_name = tag.get("name") if isinstance(tag, dict) else str(tag)
                    if tag_name:
                        dag_tags_list.append(tag_name)
                
                # Extract owner from DAG
                owner = dag_data.get("owner") or dag_data.get("owners", [])
                if owner:
                    owners = [owner] if isinstance(owner, str) else owner
                    dag_owners_list.extend(owners)
        
        # Emit tags from producing DAGs
        if dag_tags_list:
            asset_tags = self.transformer.extract_tags({"tags": dag_tags_list})
            if asset_tags:
                yield self._make_workunit(
                    entity_urn=asset_urn,
                    aspect=asset_tags,
                    aspect_name="globalTags",
                )
        
        # Emit ownership (deduplicate owners)
        if dag_owners_list:
            unique_owners = list(dict.fromkeys(dag_owners_list))
            asset_ownership = self.transformer.extract_ownership(
                {"owner": unique_owners}
            )
            if asset_ownership:
                yield self._make_workunit(
                    entity_urn=asset_urn,
                    aspect=asset_ownership,
                    aspect_name="ownership",
                )
```

**핵심:**
1. Asset의 producing DAG들을 조회
2. 각 DAG의 tags와 owners를 수집
3. 중복 제거 후 Asset에 동일한 tags/ownership 적용
4. 하나의 Asset을 여러 DAG가 생성하는 경우, 모든 DAG의 tags/owners가 합쳐짐

### 2.6 DataProcessInstance (실행 이력 추적)

**문제:** DAG 실행 이력을 DataHub에 상세히 기록해야 함.

**구현:**

```python
# airflow_source.py:785-902
def _extract_dag_process_instances(self, dag_id: str):
    """Extract DAG runs as DataProcessInstance entities"""
    
    start_date, _ = self.api_client.get_execution_date_range()
    run_count = 0
    
    for dag_run in self.api_client.get_dag_runs(dag_id, start_date):
        if run_count >= self.config.process_instance_max_runs:
            break
        
        run_count += 1
        dag_run_id = dag_run.get("dag_run_id")
        state = dag_run.get("state", "unknown")
        
        # Create DataProcessInstance URN
        dag_urn = self.transformer.make_dag_urn(dag_id)
        instance_id = f"{dag_id}_{dag_run_id}"
        instance_urn = make_data_process_instance_urn(
            orchestrator=self.transformer.platform,
            id=instance_id,
            cluster=self.transformer.platform_instance or self.config.env,
        )
        
        # Properties
        properties = DataProcessInstancePropertiesClass(
            name=dag_run_id,
            externalUrl=self.transformer.make_dag_run_url(
                dag_id, dag_run_id, self.config.airflow_url
            ),
            customProperties={
                "dag_id": dag_id,
                "dag_run_id": dag_run_id,
                "state": state,
                "run_type": dag_run.get("run_type", "unknown"),
                "conf": str(dag_run.get("conf", {})),
            },
        )
        yield self._make_workunit(
            entity_urn=instance_urn,
            aspect=properties,
            aspect_name="dataProcessInstanceProperties",
        )
        
        # Relationships (link to parent DataFlow)
        relationships = DataProcessInstanceRelationshipsClass(
            parentTemplate=dag_urn,
        )
        yield self._make_workunit(
            entity_urn=instance_urn,
            aspect=relationships,
            aspect_name="dataProcessInstanceRelationships",
        )
        
        # Run Event with status
        start_ts = parse_airflow_timestamp(dag_run.get("start_date"))
        end_ts = parse_airflow_timestamp(dag_run.get("end_date"))
        
        # Map Airflow state to DataHub status
        status_map = {
            "success": DataProcessRunStatusClass.COMPLETE,
            "running": DataProcessRunStatusClass.STARTED,
            "failed": DataProcessRunStatusClass.COMPLETE,
            "queued": DataProcessRunStatusClass.STARTED,
        }
        run_status = status_map.get(state, DataProcessRunStatusClass.COMPLETE)
        
        # Result for completed runs
        result = None
        if state in ("success", "failed"):
            result_type = (
                DataProcessInstanceRunResultClass.SUCCESS
                if state == "success"
                else DataProcessInstanceRunResultClass.FAILURE
            )
            result = DataProcessInstanceRunResultClass(
                type=result_type,
                nativeResultType=state,
            )
        
        run_event = DataProcessInstanceRunEventClass(
            status=run_status,
            timestampMillis=start_ts or int(datetime.now().timestamp() * 1000),
            result=result,
        )
        yield self._make_workunit(
            entity_urn=instance_urn,
            aspect=run_event,
            aspect_name="dataProcessInstanceRunEvent",
        )
```

**추출 정보:**
- DAG Run ID, 상태 (success/failed/running)
- 실행 시작/종료 시간
- 실행 유형 (scheduled/manual/backfill)
- 실행 설정 (conf)
- Airflow UI 링크

## 3. Trial & Error

### 3.1 Task Lineage 미표시 문제

**증상:**
- DataHub UI에서 DAG 내부 task 간 연결선이 표시되지 않음
- Asset outlets만 표시됨 (17개 lineage)

**원인:**
- Airflow 3.x의 `serialized_dag` 구조 변경으로 REST API에서 `upstream_task_ids` 필드 누락
- DataHub가 task dependencies를 추출하지 못함

**시도:**
1. **REST API만 사용 (실패)**
   - `/api/v2/dags/{dag_id}/tasks` 응답에 `upstream_task_ids` 없음
   - Task dependencies 정보 부족

2. **Metadata DB 직접 쿼리 (성공)**
   - `serialized_dag` 테이블 직접 조회
   - `__var` 구조 파싱하여 `downstream_task_ids` 추출
   - 역순으로 변환하여 `upstream_deps` 생성

**해결:**
```python
# 1. Metadata DB 클라이언트 추가
self.metadata_db_client = AirflowMetadataDBClient(
    host=config.metadata_db_host,
    port=config.metadata_db_port,
    database=config.metadata_db_database,
    username=config.metadata_db_username,
    password=config.metadata_db_password,
)

# 2. DAG 처리 시 metadata DB 데이터 로드
self._load_metadata_db_data(dag_id)

# 3. Task lineage 구성 시 DB 데이터 우선 사용
upstream_task_ids = []
if dag_id in self._dag_dependencies_cache:
    upstream_task_ids = self._dag_dependencies_cache[dag_id].get(task_id, [])
```

**결과:**
- 17 (asset outlets만) → **79 (task deps + asset outlets)**
- Task 간 lineage 정상 표시

### 3.2 Cosmos DBT Outlet 버그

**증상:**
- `infer_cosmos_outlets: true` 설정 시 non-Cosmos task의 명시적 outlet이 무시됨
- Airflow metadata DB에는 outlet 존재하지만 DataHub에 연결 안 됨

**원인:**
```python
# 버그 코드 (airflow_source.py:377-387)
skip_explicit_outlets = False
if self.config.infer_cosmos_outlets:
    is_cosmos_task = bool(re.match(cosmos_pattern, task_id))
    skip_explicit_outlets = not is_cosmos_task  # ← 버그!
```

- Cosmos task가 아니면 명시적 outlet을 건너뛰는 로직
- Cosmos 추론이 명시적 outlet을 **대체**하는 것으로 잘못 구현됨

**해결:**
```python
# 수정된 코드
# Always extract explicit outlets from metadata DB for all tasks
# (Cosmos inference adds DBT outlets additionally, doesn't replace explicit ones)
if dag_id in self._dag_outlets_cache:
    outlet_uris = self._dag_outlets_cache[dag_id].get(task_id, [])
    for uri in outlet_uris:
        dataset_urn = self.transformer.make_asset_urn(uri)
        outlet_dataset_urns.append(dataset_urn)

# Infer Cosmos DBT outlets if enabled (ADDITIONAL, not replacement)
if self.config.infer_cosmos_outlets:
    cosmos_outlet = self._infer_cosmos_outlet(task_id)
    if cosmos_outlet:
        outlet_dataset_urns.append(cosmos_outlet)
```

**핵심:**
- Cosmos 추론은 **추가** 기능 (명시적 outlet **대체** 아님)
- 모든 task에서 명시적 outlet 먼저 추출
- Cosmos 패턴 매칭 시 DBT outlet **추가**로 덧붙임

### 3.3 Airflow 3.1 Cosmos 호환성 문제

**증상:**
- Airflow 3.0.6에서 Cosmos task 실행 시 import error
- `Cosmos requires Airflow >= 3.1.0`

**원인:**
- Cosmos 플러그인이 Airflow 3.1 이상 요구
- Asset URI 형식 변경 필요

**시도:**
1. **Cosmos 다운그레이드 (실패)**
   - 구버전 Cosmos는 Airflow 3.x 미지원

2. **Airflow 업그레이드 (성공)**
   - Airflow 3.0.6 → 3.1.3 업그레이드
   - `AIRFLOW__COSMOS__USE_DATASET_AIRFLOW3_URI_STANDARD=True` 설정
   - Asset URI: `dot notation` → `slash notation` 변경

**해결:**
```bash
# requirements.txt
apache-airflow==3.1.3
astronomer-cosmos==1.11.1

# .env
AIRFLOW__COSMOS__USE_DATASET_AIRFLOW3_URI_STANDARD=True
```

**결과:**
- Cosmos DBT task 정상 실행
- Asset lineage 자동 생성

### 3.4 Plugin Import 경로 문제

**증상:**
- `attempted relative import beyond top-level package`
- Airflow가 plugins 디렉토리를 제대로 인식하지 못함

**원인:**
- Plugins의 `__init__.py`에서 상대 import 사용
- Docker 볼륨 마운트 시 `__pycache__` stale bytecode 문제

**시도:**
1. **PYTHONPATH 추가 (부분 성공)**
   - `export PYTHONPATH=/opt/airflow/plugins:$PYTHONPATH`
   - 일부 import는 동작하지만 여전히 경고 로그

2. **절대 import로 변경 (성공)**
   ```python
   # Before (relative import)
   from .custom_keycloak_auth_manager import CustomKeycloakAuthManager
   
   # After (absolute import)
   from airflow_keycloak.custom_keycloak_auth_manager import CustomKeycloakAuthManager
   ```

3. **__pycache__ 자동 정리 (완전 해결)**
   ```dockerfile
   # Dockerfile
   RUN find /opt/airflow/plugins -type d -name "__pycache__" -exec rm -rf {} + || true
   ```

**결과:**
- Import 경고 로그 완전 제거
- Plugins 정상 로드

## 4. 환경별 설정

### Local 환경

```yaml
# airflow_local.yml
source:
  type: datahub_airflow_source.airflow_source.AirflowSource
  config:
    airflow_url: "http://host.docker.internal:8082"
    
    # Keycloak OIDC
    keycloak_server: "https://auth.qraft.ai"
    keycloak_realm: "qraft"
    keycloak_client_id: "data-pipeline-keycloak-client"
    keycloak_client_secret: "${AIRFLOW_VAR_KEYCLOAK_CLIENT_SECRET}"
    
    # Environment
    env: "LOCAL"
    platform_instance: "airflow-local"
    
    # Metadata DB
    metadata_db_enabled: true
    metadata_db_host: "host.docker.internal"
    metadata_db_port: 5432
    metadata_db_database: "airflow"
    metadata_db_username: "airflow"
    metadata_db_password: "${AIRFLOW__DATABASE__SQL_ALCHEMY_CONN_PASSWORD}"
    
    # Capture options
    capture_executions: true
    capture_executions_days: 7
    capture_assets: true
    
    # Advanced
    verify_ssl: false
    timeout: 30
```

### Prod 환경

```yaml
# airflow_prod.yml
source:
  type: datahub_airflow_source.airflow_source.AirflowSource
  config:
    airflow_url: "https://airflow.prod.qraft.ai"
    
    # Keycloak OIDC
    keycloak_server: "https://auth.qraft.ai"
    keycloak_client_secret: "${KEYCLOAK_CLIENT_SECRET_PROD}"
    
    # Environment
    env: "PROD"
    platform_instance: "airflow-prod"
    
    # Metadata DB
    metadata_db_enabled: true
    metadata_db_host: "postgres.prod.qraft.ai"
    
    # Capture options
    capture_executions_days: 30
    emit_process_instances: true
    process_instance_max_runs: 10
    
    # Advanced
    verify_ssl: true
    timeout: 45
    max_workers: 10

sink:
  type: datahub-rest
  config:
    server: "${DATAHUB_GMS_URL_PROD}"
    token: "${DATAHUB_ACCESS_TOKEN_PROD}"
```

## 5. 성능 최적화

### 5.1 Pagination 및 Caching

```python
# api_client.py:85-141
def _paginate(
    self, endpoint: str, params: Optional[Dict[str, Any]] = None, limit: int = 100
) -> Iterator[Dict[str, Any]]:
    """Paginate through API results"""
    params = params or {}
    offset = 0
    
    while True:
        params["limit"] = limit
        params["offset"] = offset
        
        response = self._request("GET", endpoint, params=params)
        data = response.json()
        
        # Handle different pagination response formats
        items = (
            data.get("dags")
            or data.get("dag_runs")
            or data.get("task_instances")
            or data.get("assets")
            or []
        )
        
        if not items:
            break
        
        for item in items:
            yield item
        
        # Check if there are more pages
        total_entries = data.get("total_entries", 0)
        if offset + limit >= total_entries:
            break
        
        offset += limit
```

### 5.2 Metadata DB 캐싱

```python
# airflow_source.py:132-134
# Cache for metadata DB data per DAG
self._dag_dependencies_cache: Dict[str, Dict[str, List[str]]] = {}
self._dag_outlets_cache: Dict[str, Dict[str, List[str]]] = {}

# airflow_source.py:392-424
def _load_metadata_db_data(self, dag_id: str) -> None:
    """Load metadata DB data for a DAG into cache"""
    if not self.metadata_db_client:
        return
    
    if dag_id in self._dag_dependencies_cache:
        return  # Already loaded
    
    try:
        # Load task dependencies
        dependencies = self.metadata_db_client.get_task_dependencies(dag_id)
        self._dag_dependencies_cache[dag_id] = dependencies
        
        # Load task outlets
        outlets = self.metadata_db_client.get_task_outlets(dag_id)
        self._dag_outlets_cache[dag_id] = outlets
        
    except Exception as e:
        logger.warning(f"Failed to load metadata DB data for DAG '{dag_id}': {e}")
        self._dag_dependencies_cache[dag_id] = {}
        self._dag_outlets_cache[dag_id] = {}
```

**효과:**
- DAG당 1번만 DB 쿼리
- Task 수백 개인 DAG도 빠르게 처리
- 메모리 사용량 최소화

## 6. 버전 히스토리

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.2.0 | 2025-11-27 | DataProcessInstance, Task log URL, Connection/Variable, SLA 추출 기능 추가 |
| 1.1.0 | 2025-11-27 | Domain Pattern Mapping 기능 추가 (Cross-Platform Integration) |
| 1.0.1 | 2025-11-26 | Cosmos DBT Outlet 추론 기능 추가, Asset outlet 버그 수정 |
| 1.0.0 | 2025-11-22 | 초기 릴리스 - Airflow 3.x REST API 기반 커넥터 |

## 📎 Related

### Projects 배경 (Why)
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/Airflow-3.0-업그레이드-배경|Airflow-3.0-업그레이드-배경]] - 왜 Airflow 3.0을 도입했는가
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/DataHub-커스텀-구현-상세|DataHub-커스텀-구현-상세]] - DataHub Custom Connector 프로젝트 배경

### Technology (Core Concepts)
- [[Airflow]] - Airflow 기본 개념 및 Qraft 적용 사례
- [[DataHub]] - DataHub 메타데이터 카탈로그

### Technology (Related Implementation)
- [[Keycloak-OIDC-인증]] - OIDC 인증 구현
- [[DBT-구현]] - DBT 통합 구현
- [[TransferPipeline-패턴]] - 데이터 전송 패턴

### Projects (실제 사용)
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/DataHub-도입|DataHub-도입]] - DataHub 도입 프로젝트
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/데이터-거버넌스-전략-수립|데이터-거버넌스-전략-수립]] - 거버넌스 전략

---

**작성일:** 2025-11-30  
**카테고리:** #Technology #Airflow #DataPlatform #Metadata  
**태그:** #Airflow3 #CustomConnector #DataHub #AssetLineage
