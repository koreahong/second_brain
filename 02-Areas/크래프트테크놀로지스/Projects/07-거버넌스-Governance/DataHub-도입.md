---
tags:
  - projects
  - datahub
  - metadata
  - governance
  - qraft
created: '2025-11-30'
updated: '2025-11-30'
status: 운영중
team: ML Platform (T)
period: 2025-09 ~ 2025-11
company: 크래프트테크놀로지스
---
# DataHub 도입

## 📋 Overview

**기간**: 2025년 9월 ~ 11월  
**주도**: ML Platform (T)  
**배경**: 메타데이터 관리 플랫폼 필요  
**결과**: DataHub 구축, 85% Lineage 커버리지

---

## 🎯 도입 배경

### 문제 상황

[[데이터-거버넌스-전략-수립|거버넌스 전략]]의 핵심 과제:

1. **Data Ownership 불명확**
   - "이 테이블 누가 소유하나?" → 1시간 이상 추적
   - Slack DM으로 물어보기 → 담당자 퇴사하면 끝

2. **데이터 의존성 파악 불가**
   - "이 DAG 건드리면 어디에 영향 가나?" → 알 수 없음
   - 실수로 다른 팀 파이프라인 중단 위험

3. **메타데이터 분산**
   - Airflow: DAG 메타데이터
   - DBT: 데이터 모델 메타데이터
   - Snowflake: 테이블 스키마
   - Confluence: 수동 문서 (outdated)
   → **통합된 카탈로그 필요**

4. **검색 불가**
   - "OHLCV 데이터 어디 있지?" → Snowflake 직접 뒤지기
   - 중복 테이블 생성 (같은 데이터를 모르고 재생성)

### CFO 요구사항

> "팀별로 누가 무슨 데이터 쓰는지 한눈에 보고 싶다"

**구체적 요구**:
- 벤더 비용 검토 시 → 실제 사용 팀 즉시 파악
- 데이터 중복 발견 → 비용 절감
- 팀별 데이터 격리 → 무단 접근 방지

---

## 🔍 플랫폼 비교

### 후보 평가

| 항목 | DataHub | Amundsen | Apache Atlas | OpenMetadata |
|------|---------|----------|--------------|--------------|
| **Lineage** | ⭐⭐⭐⭐⭐ Asset 기반 | ⭐⭐⭐ Table 레벨 | ⭐⭐⭐⭐ Hive 중심 | ⭐⭐⭐⭐ Table 레벨 |
| **API** | ⭐⭐⭐⭐⭐ GraphQL | ⭐⭐⭐ REST | ⭐⭐⭐ REST | ⭐⭐⭐⭐ REST |
| **OIDC 지원** | ⭐⭐⭐⭐⭐ | ❌ | ⭐⭐ 복잡 | ⭐⭐⭐⭐ |
| **커뮤니티** | ⭐⭐⭐⭐⭐ LinkedIn | ⭐⭐⭐ Lyft | ⭐⭐ Apache | ⭐⭐⭐ 성장 중 |
| **커스터마이징** | ⭐⭐⭐⭐⭐ Plugin 자유 | ⭐⭐⭐ | ⭐⭐ 제한적 | ⭐⭐⭐⭐ |
| **UI/UX** | ⭐⭐⭐⭐⭐ 직관적 | ⭐⭐⭐⭐ | ⭐⭐ 복잡 | ⭐⭐⭐⭐ |
| **Snowflake 지원** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Airflow 3.x** | ⭐⭐⭐ Custom 가능 | ❌ | ❌ | ⭐⭐ |

### 선정 이유: DataHub

**1. 강력한 Lineage (Asset 기반)**
- Airflow Asset → Snowflake Table → DBT Model 전체 추적
- Column-level lineage 지원 (향후 확장)
- Graph 시각화 우수

**2. GraphQL API**
- 자동화 스크립트 작성 용이
- Bootstrap 자동화 (`bootstrap_datahub.py`)
- 정책 자동 적용 (`apply_policies.py`)

**3. Keycloak OIDC 통합**
- 표준 OIDC 프로토콜
- Group 자동 동기화
- JIT Provisioning 지원

**4. 활발한 커뮤니티**
- LinkedIn의 지속적 투자
- Slack 커뮤니티 활성 (답변 빠름)
- 주간 릴리스

**5. Plugin 확장성**
- Airflow 3.x Custom Source 개발 가능
- DBT URN Encoding Patch 적용 가능
- Python SDK 제공

### 탈락 이유

**Amundsen**:
- ❌ OIDC 미지원 (자체 인증만)
- ❌ Airflow 3.x 미지원
- ⚠️ 커뮤니티 활동 감소

**Apache Atlas**:
- ❌ Hadoop 중심 (Snowflake 지원 약함)
- ❌ UI/UX 복잡
- ❌ OIDC 설정 복잡

**OpenMetadata**:
- ✅ 좋은 대안
- ⚠️ 커뮤니티 규모 작음
- ⚠️ Airflow 3.x 지원 불확실

---

## 🏗️ 아키텍처

### 전체 구조

```
┌─────────────────────────────────────────────────┐
│                   Keycloak                       │
│              (SSO, Group 관리)                   │
└────────────┬────────────────────────────────────┘
             │ OIDC
             ↓
┌─────────────────────────────────────────────────┐
│                  DataHub GMS                     │
│           (GraphQL API, Metadata Storage)        │
└──────┬──────────────────────────────────────────┘
       │
       ├─ DataHub Actions (Ingestion)
       │    ├── Airflow Source (Custom)
       │    ├── DBT Source (S3 Manifest)
       │    └── Snowflake Source
       │
       └─ Frontend (React)
            - Search
            - Lineage
            - Ownership
```

### Domain 구조

**10개 Domain** (bootstrap 시 자동 생성):

```python
# bootstrap_datahub.py
DOMAINS = [
    {"id": "Core", "name": "Core", 
     "description": "핵심 차원 테이블 (dim_ticker, dim_holiday)"},
    
    {"id": "Index", "name": "Index",
     "description": "지수 구성 데이터 (QQQ, SPY)"},
    
    {"id": "Futures", "name": "Futures",
     "description": "선물 데이터 (OHLCV)"},
    
    {"id": "Employee", "name": "Employee",
     "description": "직원 정보"},
    
    {"id": "FRED", "name": "FRED",
     "description": "연준 경제 지표"},
    
    {"id": "USSimulation", "name": "US Simulation",
     "description": "US 백테스팅 데이터"},
    
    {"id": "Portfolio", "name": "Portfolio",
     "description": "포트폴리오 구성"},
    
    {"id": "Marketplace", "name": "Marketplace",
     "description": "Snowflake Marketplace (CIQ, QA)",
     "parent": "External"},
    
    {"id": "Vendor", "name": "Vendor Data",
     "description": "벤더 직접 수집 (LSEG, FactSet)",
     "parent": "External"},
    
    {"id": "External", "name": "External Sources",
     "description": "외부 데이터"},
]
```

**Domain 할당 로직**:
- DBT: `_models.yml` → `meta.datahub.domain`
- Airflow: `tags` → `domain:index` → DataHub Domain
- Snowflake: Table 이름 기반 매핑

### Metadata Ingestion Flow

```
1. Source 시스템에서 메타데이터 추출
   ├── Airflow: PostgreSQL serialized_dag 테이블 직접 쿼리
   ├── DBT: S3 manifest.json 다운로드
   └── Snowflake: INFORMATION_SCHEMA 쿼리

2. DataHub 형식으로 변환
   ├── URN 생성 (quote_plus 통일)
   ├── Owner 판별 ((T) suffix → corpGroup)
   └── Tag 매핑 (Airflow → DataHub)

3. GMS로 전송
   ├── GraphQL mutation
   └── Kafka (내부 처리)

4. 검색 인덱싱
   └── Elasticsearch
```

---

## 🛠️ 구현 과정

### Phase 1: 환경 구성 (2025년 10월 1주)

**Docker Compose 구성**:
```yaml
# infrastructure/datahub/environments/local/docker-compose.yml
services:
  datahub-gms:
    image: acryldata/datahub-gms-service:v0.13.0
    environment:
      - EBEAN_DATASOURCE_USERNAME=datahub
      - EBEAN_DATASOURCE_PASSWORD=datahub
      - KAFKA_BOOTSTRAP_SERVER=broker:29092
      - ELASTICSEARCH_HOST=elasticsearch
      
  datahub-frontend:
    image: acryldata/datahub-frontend-react:v0.13.0
    environment:
      - DATAHUB_GMS_HOST=datahub-gms
      - AUTH_OIDC_ENABLED=true
      - AUTH_OIDC_CLIENT_ID=datahub
      - AUTH_OIDC_DISCOVERY_URI=http://keycloak:8080/realms/qraft/.well-known/openid-configuration
      
  datahub-actions:
    image: acryldata/datahub-actions:head
    volumes:
      - ./entrypoint-actions.sh:/entrypoint-actions.sh
      - ../common/ingestion:/etc/datahub/ingestion
    entrypoint: /entrypoint-actions.sh
```

**Key Decisions**:
- Full image 사용 (slim 버전은 Snowflake plugin 없음)
- Runtime Patch (`entrypoint-actions.sh`)로 URN 통일
- Local/Dev 모두 `env="DEV"` (URN validation 이슈)

### Phase 2: Bootstrap (2025년 10월 2주)

**자동화 스크립트**:
```bash
# infrastructure/datahub/environments/common/setup/run_all.sh
#!/bin/bash
set -e

echo "🚀 DataHub Bootstrap 시작..."

# 1. Domain/Group 생성
python bootstrap_datahub.py --all

# 2. Keycloak 그룹 동기화
python apply_groups.py

# 3. OIDC 설정
python apply_oidc.py

# 4. Access Policies
python apply_policies.py

# 5. Ingestion Sources
python apply_ingestion_sources.py

echo "✅ Bootstrap 완료"
```

**Domain 생성 로직** ([bootstrap_datahub.py](../../../qraft_data_platform/infrastructure/datahub/environments/common/setup/bootstrap_datahub.py)):
```python
def domain_exists(self, domain_id: str) -> bool:
    """Domain 존재 여부 확인 (properties까지 확인)"""
    query = """
    query getDomain($urn: String!) {
      domain(urn: $urn) {
        urn
        properties { name }
      }
    }
    """
    urn = f"urn:li:domain:{domain_id}"
    result = self.execute_graphql_safe(query, {"urn": urn})
    
    domain = result.get("data", {}).get("domain")
    # URN만 있고 properties 없으면 phantom domain
    return domain is not None and domain.get("properties") is not None
```

**Issue 해결**: Phantom Domain 문제 ([[03-Resources/Technology/DataHub/Phantom-Domain-이슈|상세]])
- `docker-compose down -v` 후에도 URN stub 남음
- Properties 확인으로 완전 삭제 여부 판별

### Phase 3: Custom Sources (2025년 10월 3-4주)

**Airflow 3.x Connector 개발**:

Built-in Airflow source는 Airflow 2.x 전용 → Custom 개발 필요

**주요 기능**:
1. **Serialized DAG Parsing** (Airflow 3.x 구조 대응)
2. **Task Lineage 추출** (downstream → upstream 역변환)
3. **Owner Type 판별** (`(T)` suffix → corpGroup)
4. **Dataset URN Sanitization** (대문자/하이픈 제거)

[[Airflow-3.0-구현|기술 상세]], [[03-Resources/Technology/Airflow/Custom-Airflow-Source|구현 코드]]

**DBT URN Patch**:

DataHub DBT connector는 `UrnEncoder`로 인코딩 → Keycloak (`quote_plus`)와 불일치

**해결**:
```bash
# entrypoint-actions.sh (런타임 패치)
sed -i 's/from datahub.emitter.mce_builder import make_group_urn/from urllib.parse import quote_plus\ndef make_group_urn(group): return f"urn:li:corpGroup:{quote_plus(group)}"/g' \
    /usr/local/lib/python3.10/site-packages/datahub/ingestion/source/dbt/dbt_common.py
```

[[03-Resources/Technology/DataHub/URN-Encoding-통일|상세]]

### Phase 4: Access Control (2025년 11월 1주)

**Owner 기반 정책**:
```python
# apply_policies.py
POLICIES = [
    {
        "name": "Owner Full Access",
        "description": "Owner는 모든 작업 가능",
        "type": "METADATA",
        "actors": {"owners": True},
        "privileges": ["EDIT_ENTITY", "EDIT_ENTITY_TAGS", "DELETE_ENTITY"],
    },
    {
        "name": "All Users View Access",
        "description": "모든 사용자는 조회 가능",
        "type": "METADATA",
        "actors": {"allUsers": True},
        "privileges": ["VIEW_ENTITY_PAGE"],
    },
]
```

**Keycloak Group 동기화**:
```python
# apply_groups.py
def sync_keycloak_groups():
    """Keycloak Group → DataHub corpGroup"""
    groups = keycloak.get_groups()  # (T) suffix 포함
    
    for group in groups:
        urn = f"urn:li:corpGroup:{quote_plus(group['name'])}"
        datahub.create_group(urn, group)
```

### Phase 5: Ingestion 자동화 (2025년 11월 2주)

**Ingestion Sources 등록**:
```yaml
# environments/common/ingestion/dbt_qraft.yml
source:
  type: dbt
  config:
    manifest_path: s3://qraft-dbt-artifacts/manifest.json
    catalog_path: s3://qraft-dbt-artifacts/catalog.json
    env: DEV
    
    owner_extraction_pattern: "^urn:li:corpGroup:(.+)"
    
sink:
  type: datahub-rest
  config:
    server: http://datahub-gms:8080
```

**Schedule**:
- Airflow: 매 6시간 (변경 빈번)
- DBT: 매일 1회 (artifact S3 업로드 후)
- Snowflake: 주 1회 (스키마 변경 드묾)

---

## 📊 성과

### Lineage 커버리지

| Source | Datasets | Lineage Edges | Coverage |
|--------|----------|---------------|----------|
| **Airflow** | 38 Assets | 79 Task deps | 85% |
| **DBT** | 127 Models | 245 ref() deps | 90% |
| **Snowflake** | 89 Tables/Views | - | - |
| **Total** | 254 | 324 | **85%** |

### 검색 성능

**Before (Snowflake 직접 쿼리)**:
```sql
-- "OHLCV 데이터" 찾기
SHOW TABLES LIKE '%OHLCV%';  -- 수십 개 테이블
-- 하나씩 DESCRIBE로 스키마 확인
-- 실제 사용처 찾기 위해 Airflow 코드 검색
-- 소요 시간: 20-30분
```

**After (DataHub)**:
```
1. 검색창: "OHLCV"
2. Filters: Domain=Futures
3. 클릭 → Lineage 탭
   → 이 테이블 읽는 DAG 즉시 확인
   → Owner: HFT (T)
소요 시간: 5초
```

### Owner Lookup

| 항목 | Before | After |
|------|--------|-------|
| "이 테이블 누가 소유?" | Slack DM → 1시간+ | DataHub 검색 → 5초 |
| "이 DAG 건드려도 되나?" | 코드 읽고 추측 | Owner 확인 → DM |
| "벤더 비용 누가 쓰나?" | 추적 불가 | Tag 필터 → 즉시 |

---

## 🔗 관련 문서

### Projects
- [[데이터-거버넌스-전략-수립]]: 전체 전략
- [[팀별-데이터-격리-체계]]: Access Control 구현
- [[데이터-카탈로그-구축]]: 검색 및 Discovery
- [[메타데이터-자동-수집-체계]]: Ingestion 자동화

### Technology
- [[03-Resources/Technology/DataHub/DataHub-개념]]: 핵심 개념
- [[03-Resources/Technology/DataHub/DataHub-MCP-Server]]: MCP 서버 및 AI Agent 통합
- [[03-Resources/Technology/DataHub/Custom-Sources]]: Airflow/DBT Connector
- [[03-Resources/Technology/DataHub/URN-Encoding-통일]]: URN 일관성
- [[03-Resources/Technology/DataHub/Bootstrap-자동화]]: Domain 자동 생성

### Weekly (실제 경험)
- [[2025년 10월 27일]]: 거버넌스 중요성 인식 (팀 간 협업 어려움)
- [[2025년 11월 24일]]: DataHub 론칭, Keycloak 권한 관리 완료

---

## 📝 교훈

### ✅ 잘한 점

1. **대안 철저 비교**: 4개 플랫폼 PoC → 정량적 비교
2. **Bootstrap 자동화**: 수동 설정 제로 → 재구축 쉬움
3. **Custom Source**: Airflow 3.x 대응 → 벤더 독립성
4. **Runtime Patch**: 패키지 재빌드 없이 URN 통일

### ⚠️ Trial & Error

1. **Phantom Domain**: URN만 체크 → Properties까지 확인으로 수정
2. **URN Validation**: env="LOCAL" 미지원 → env="DEV"로 변경
3. **Slim Image**: Snowflake plugin 없음 → Full image 사용
4. **Task Lineage**: Airflow 3.x 구조 변경 → Custom parsing 구현

### 🔮 향후 계획

1. **Column-level Lineage**: DBT ref() → 컬럼 추적
2. **Data Quality**: Great Expectations 통합
3. **Cost Tracking**: 벤더별 사용량 대시보드
4. **Glossary**: 비즈니스 용어 정의
5. **DataHub MCP 통합**: AI Agent로 자동 데이터 발견 및 영향도 분석 ([[DataHub-MCP-Server|상세]])

---

**작성일**: 2025-11-30  
**작성자**: ML Platform (T)  
**상태**: ✅ 운영 중, 85% Lineage 커버리지
