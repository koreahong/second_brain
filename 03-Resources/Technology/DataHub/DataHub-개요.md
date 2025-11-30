---
title: DataHub - 메타데이터 관리 플랫폼
type: technology
tags:
  - datahub
  - metadata
  - data-catalog
  - data-governance
  - data-lineage
  - 크래프트테크놀로지스
created: '2025-11-30'
updated: '2025-11-30'
status: active
company: 크래프트테크놀로지스
project: qraft-data-platform
---

# DataHub - 메타데이터 관리 플랫폼

## 📋 개요

DataHub는 LinkedIn에서 개발한 오픈소스 메타데이터 관리 플랫폼으로, 데이터 디스커버리, 거버넌스, 리니지 추적을 지원합니다.

**공식 사이트**: https://datahubproject.io/

**크래프트테크놀로지스 적용 배경**:
- 2025년 11월 DataHub 론칭 ([[2025년-11월-24일|2025년 11월 24일 회고]] 참조)
- Airflow, DBT, Snowflake 메타데이터 통합 관리
- 전사 데이터 거버넌스 체계 구축
- [[qraft-data-platform-통합프로젝트|Qraft Data Platform 통합 프로젝트]]의 핵심 컴포넌트

## 🎯 주요 기능

### 1. 데이터 카탈로그
- **데이터셋 검색**: 통합 검색으로 모든 데이터 자산 탐색
- **메타데이터 관리**: 스키마, 컬럼, 타입, 설명 등
- **비즈니스 용어**: Glossary를 통한 용어 정의
- **태그 관리**: 데이터 분류 및 필터링

### 2. 데이터 리니지
- **자동 리니지 추적**: Airflow, DBT, Snowflake 등에서 자동 수집
- **컬럼 레벨 리니지**: 필드 간 의존성 추적
- **Impact Analysis**: 변경 영향도 분석
- **시각화**: 그래프 형태로 데이터 흐름 표시

### 3. 데이터 거버넌스
- **도메인 관리**: 비즈니스 영역별 데이터 그룹핑
- **소유권 관리**: 데이터셋별 Owner 및 Team 할당
- **접근 제어**: Role 기반 권한 관리
- **Policy 엔진**: 자동화된 거버넌스 규칙

### 4. 통합 인증
- **OIDC/SSO**: Keycloak, Okta 등과 통합
- **RBAC**: Role-Based Access Control
- **Team 기반 권한**: 그룹별 접근 제어

## 🏗️ 아키텍처

### 주요 컴포넌트

```
┌─────────────────────────────────────────┐
│             Frontend (React)            │
├─────────────────────────────────────────┤
│          GMS (GraphQL/REST API)         │
├─────────────────────────────────────────┤
│      MAE (Metadata Audit Events)        │
├─────────────────────────────────────────┤
│    Storage (MySQL/PostgreSQL/Neo4j)     │
└─────────────────────────────────────────┘
           ↑
           │ Ingestion
           │
┌──────────┴───────────┐
│  Source Systems:     │
│  - Airflow           │
│  - DBT               │
│  - Snowflake         │
│  - etc.              │
└──────────────────────┘
```

### 메타데이터 모델
- **Entity**: Dataset, Chart, Dashboard, Pipeline, Task 등
- **Aspect**: 엔티티의 속성 (Schema, Ownership, Tags 등)
- **Relationship**: 엔티티 간 관계 (Lineage, Membership 등)

## 💻 Qraft 구현 상세

### 환경 구성
- **로컬**: `http://localhost:9002`
- **개발**: `https://datahub-dev.qraft.ai`
- **프로덕션**: `https://datahub.qraft.ai`

### 통합된 Source Systems
1. **Airflow**
   - DAG 메타데이터
   - Task 의존성 및 리니지
   - 실행 통계
   - Keycloak 인증 통합 (Custom Source)

2. **DBT**
   - 모델 메타데이터
   - 컬럼 레벨 리니지
   - 테스트 결과
   - Tag URL 인코딩 (Custom Patches)

3. **Snowflake**
   - 테이블/뷰 스키마
   - 데이터 프로필
   - 사용 통계

### 커스텀 구현

#### 1. Airflow Custom Source
**목적**: Keycloak 인증이 적용된 Airflow API 호출

**구현**: `infrastructure/datahub/custom_sources/airflow/`
- Bearer Token 기반 인증
- DAG, Task 메타데이터 수집
- Domain Pattern Mapping

#### 2. DBT Custom Patches
**목적**: DBT Tag URL 인코딩 및 Keycloak 통합

**구현**: `infrastructure/datahub/custom_sources/dbt/`
- Tag 이름 URL 인코딩 해결
- Meta 필드 매핑 개선
- Keycloak 인증 통합

#### 3. Domain Pattern Mapping
**목적**: Airflow ↔ DBT ↔ Snowflake 간 도메인 자동 매핑

**매핑 규칙**:
```python
{
    "airflow_dag_tag": "dbt_meta_domain",
    "dbt_meta_domain": "snowflake_schema",
    "pattern": "team-based"
}
```

**예시**:
- Airflow DAG tag: `team:strategy`
- → DBT meta domain: `strategy`
- → Snowflake schema: `strategy_*`

### 메타데이터 관리 프로세스

#### Ingestion 워크플로우
```bash
# 1. DBT manifest 생성
cd infrastructure/airflow/teams/qraft/dbt
dbt docs generate --target prod

# 2. S3 업로드
aws s3 cp target/manifest.json s3://qraft-origin/metadata/dbt/

# 3. DataHub Ingestion 실행
# UI → Ingestion → dbt_qraft → Execute
```

#### Owner 업데이트
```bash
cd infrastructure/datahub/environments/common/maintenance
python fix_owners.py --owners-only
```

#### Tag 동기화
```bash
python sync_tags.py
```

## 🔧 주요 설정

### Ingestion Source 구성

#### DBT Source
```yaml
source:
  type: dbt
  config:
    manifest_path: "s3://qraft-origin/metadata/dbt/qraft/dev/target/manifest.json"
    catalog_path: "s3://qraft-origin/metadata/dbt/qraft/dev/target/catalog.json"
    target_platform: "snowflake"
    load_schemas: true
    enable_meta_mapping: true
```

#### Airflow Source
```yaml
source:
  type: airflow-custom
  config:
    airflow_url: "http://airflow-webserver:8080"
    auth_type: "keycloak"
    enable_domain_mapping: true
```

### Domain 구조
```
Financial Markets (D)
├── Strategy (T)
├── HFT (T)
└── MFT (T)

AI Products (D)
└── AI Product (T)

Public Data (D)
└── Public datasets
```

### Tag 체계
- **팀 태그**: `team:strategy`, `team:hft`
- **기술 태그**: `dbt`, `airflow`, `snowflake`
- **도메인 태그**: `financial`, `ai`, `public`
- **데이터 타입**: `raw`, `processed`, `mart`

## 📊 사용 사례

### 1. 데이터 디스커버리
**시나리오**: 전략팀이 사용하는 마켓 데이터 찾기

**방법**:
1. 검색창에 "market" 입력
2. 도메인 필터: "Financial Markets"
3. 태그 필터: "team:strategy"
4. 결과: 관련 데이터셋, DBT 모델, Airflow DAG

### 2. 리니지 추적
**시나리오**: 특정 리포트 오류 원인 파악

**방법**:
1. 문제 데이터셋 검색
2. "Lineage" 탭 선택
3. Upstream 추적으로 원천 데이터까지 확인
4. 각 단계별 변환 로직 검토

### 3. Impact Analysis
**시나리오**: 스키마 변경 영향도 분석

**방법**:
1. 변경할 테이블 검색
2. "Lineage" 탭에서 Downstream 확인
3. 영향받는 DBT 모델, Airflow DAG 파악
4. 관련 팀에 사전 공지

### 4. 메타데이터 품질 관리
**시나리오**: Owner가 없는 데이터셋 찾기

**GraphQL Query**:
```graphql
{
  search(
    input: {
      type: DATASET,
      query: "*",
      filters: [
        { field: "hasOwner", value: "false" }
      ]
    }
  ) {
    searchResults {
      entity {
        urn
        ... on Dataset {
          name
        }
      }
    }
  }
}
```

## 🚨 트러블슈팅

### 1. Ingestion 실패
**증상**: DBT ingestion이 실패함

**원인**:
- S3 권한 부족
- manifest.json 파싱 오류
- Network 연결 실패

**해결**:
```bash
# 로그 확인
docker logs datahub-actions

# S3 권한 확인
aws s3 ls s3://qraft-origin/metadata/dbt/

# Manifest 검증
python -m json.tool target/manifest.json
```

### 2. Tag가 보이지 않음
**증상**: DBT Tag가 DataHub에 표시되지 않음

**원인**: URL 인코딩 이슈

**해결**:
```bash
# Custom DBT Patch 적용 확인
cd infrastructure/datahub/custom_sources/dbt
cat README.md  # 패치 적용 가이드

# 메타데이터 수정 스크립트 실행
cd infrastructure/datahub/environments/common/maintenance
python fix_dbt_metadata.py
```

### 3. Keycloak 로그인 실패
**증상**: DataHub 로그인 시 401 오류

**원인**:
- Realm 설정 오류
- Client Secret 불일치
- Redirect URI 미등록

**해결**:
```bash
# Keycloak 설정 확인
cat infrastructure/datahub/environments/common/setup/KEYCLOAK.md

# 브라우저 캐시 삭제
# Realm: qraft, Client: datahub 확인
```

### 4. Lineage 누락
**증상**: Airflow → DBT 리니지가 표시되지 않음

**원인**:
- URN 불일치
- Domain Mapping 실패

**해결**:
```bash
# URN 확인
# Airflow Task URN과 DBT Model URN이 일치하는지 검증

# Domain Mapping 로그 확인
docker logs datahub-actions | grep "domain"
```

## 📚 참고 자료

### 🌐 공식 문서
- **DataHub Docs**: https://datahubproject.io/docs
- **API Reference**: https://datahubproject.io/docs/api/graphql
- **Metadata Model**: https://datahubproject.io/docs/metadata-modeling

### 📂 크래프트 프로젝트 저장소 문서 (qraft_data_platform)
- **Setup Guide**: `infrastructure/datahub/docs/SETUP.md`
- **Usage Guide**: `infrastructure/datahub/docs/USAGE.md`
- **Team Guide**: `infrastructure/datahub/docs/TEAM_GUIDE.md`
- **Troubleshooting**: `infrastructure/datahub/docs/TROUBLESHOOTING.md`
- **Design Decisions**: `infrastructure/datahub/docs/DESIGN_DECISIONS.md`

### 🛠 커스텀 구현 (크래프트 특화)
- **Airflow Source**: `infrastructure/datahub/custom_sources/airflow/README.md` - Keycloak 인증 통합
- **DBT Patches**: `infrastructure/datahub/custom_sources/dbt/README.md` - URL 인코딩 패치
- **Maintenance Scripts**: `infrastructure/datahub/environments/common/maintenance/README.md` - 메타데이터 관리

## 🔗 관련 문서 (세컨드브레인)

### 📋 프로젝트
- [[qraft-data-platform-통합프로젝트|Qraft Data Platform 통합 프로젝트]] - 메인 프로젝트
- [[iceberg-+-datahub|Iceberg + DataHub]] - Iceberg 통합 계획
- [[ERD-작성|ERD 작성]] - 데이터 모델링

### 🏛 거버넌스 & 품질
- [[Qraft-Data-Governance-Framework|크래프트 데이터 거버넌스 프레임워크]] - 전사 거버넌스 체계
- [[Data-Quality-Management|데이터 품질 관리 프로세스]] - 품질 검증
- [[데이터-거버넌스|Data Governance]] - 거버넌스 개념
- [[데이터벤토-관리-방안|데이터 벤더 관리 방안]] - 데이터 카탈로그 전략
- [[원천-네이밍-룰-정하기|원천 네이밍 룰 정하기]] - 네이밍 컨벤션

### 🔧 통합 기술 스택
- [[Airflow|Airflow]] - 데이터 파이프라인 오케스트레이션
- [[DBT|DBT]] - 데이터 변환 및 품질 관리
- [[Keycloak]] - SSO 통합 인증
- [[PostgreSQL|PostgreSQL]] - 메타데이터 저장소
- [[Snowflake]] - 데이터 웨어하우스

### 📅 관련 회고
- [[2025년-11월-24일|2025년 11월 24일]] - DataHub 론칭 주간 회고

## 💡 Best Practices

### 메타데이터 작성
1. **설명 작성**: 모든 데이터셋에 명확한 설명 추가
2. **Owner 할당**: 반드시 Owner와 Team 지정
3. **Tag 사용**: 일관된 태그 체계로 분류
4. **Domain 배치**: 비즈니스 영역별 도메인 할당

### Ingestion 관리
1. **스케줄링**: 주기적으로 메타데이터 동기화
2. **검증**: Ingestion 후 반드시 검증
3. **모니터링**: 실패 알림 설정
4. **버전 관리**: manifest.json 버전 관리

### 거버넌스
1. **정기 리뷰**: 월간 메타데이터 품질 검토
2. **Owner 관리**: 팀 이동 시 Owner 업데이트
3. **Policy 자동화**: 반복 작업은 Policy로 자동화
4. **교육**: 팀원 대상 사용법 교육

## 🎓 학습 포인트

### 메타데이터 관리의 중요성
- 데이터 디스커버리 시간 단축
- 데이터 품질 향상
- 협업 효율성 증대
- 컴플라이언스 준수

### 리니지 추적의 가치
- 영향도 분석 가능
- 디버깅 시간 단축
- 변경 관리 용이
- 데이터 신뢰도 향상

### 도메인 기반 접근
- 비즈니스 컨텍스트 명확화
- 팀별 데이터 소유권 확립
- 거버넌스 정책 적용 용이

---

**Last Updated**: 2025-11-30
**Maintained by**: ML Platform Infrastructure Team
