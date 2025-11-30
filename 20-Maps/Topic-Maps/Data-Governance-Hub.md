---
type: hub
status: evergreen
tags:
  - hub
  - data-governance
  - datahub
  - metadata
  - compliance
created: '2025-11-30'
updated: '2025-11-30'
maturity: 85
---
# Data Governance Hub

> Central hub for data governance, metadata management, and organizational data strategy

## 🎯 Core Concepts

Data governance at Qraft focuses on establishing transparency, quality, and compliance through modern tools like DataHub while respecting team autonomy.

### Foundational Principles
- **Visibility over Control**: Catalog and lineage before standardization
- **Non-invasive Approach**: Mirror and track rather than force integration
- **Compliance-driven**: CFO/Risk/Audit as strategic framing
- **Progressive Integration**: Inventory → Quality → Standards

### Key Framework
- [[03-Resources/Data-Governance/Data-Governance|Data Governance Strategy]]

## 📚 Resources (Knowledge Base)

### Strategic Guidelines
- [[03-Resources/Data-Governance/Data-Governance|크래프트 데이터 거버넌스 방향성]]
  - Top-down justification (compliance, risk)
  - Research team resistance management
  - Phased implementation approach

### Architecture Patterns
- [[03-Resources/Data-Governance/Architecture-Patterns/]] - Governance architecture designs

### Access Control
- [[03-Resources/Data-Governance/Access-Control/]] - Permission and security patterns

## 💼 Projects (Applied Experience)

### Active Governance Initiatives
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/iceberg-+-datahub|Iceberg + DataHub]] - Metadata catalog implementation
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/ERD-작성|ERD 작성]] - Data modeling documentation
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/데이터벤토-관리-방안|데이터 벤토 관리 방안]] - Data product management
- [[02-Areas/크래프트테크놀로지스/Projects/07-거버넌스-Governance/원천-네이밍-룰-정하기|원천 네이밍 룰]] - Source naming conventions

### Infrastructure Integration
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/dag권한-관리|DAG 권한 관리]] - Keycloak-based access control

## 🔍 Weekly Reflections

### DataHub Launch & Integration
- [[02-Areas/크래프트테크놀로지스/Experience/Weekly/2025년-11월-24일|2025년 11월 24일]]
  - DataHub 론칭
  - Airflow-DBT-DB 연결
  - Tag/Domain 관리 고려사항
  - Data product vs purchased data 구분

- [[02-Areas/크래프트테크놀로지스/Experience/Weekly/2025년-11월-17일|2025년 11월 17일]]
  - DataHub-Keycloak 권한 연동
  - 팀별 Database 및 Airflow 권한 분리

### Organizational Challenges
- [[02-Areas/크래프트테크놀로지스/Experience/Weekly/2025년-11월-10일|2025년 11월 10일]]
  - Keycloak 도입 배경 (팀간 데이터 가시성 격리)
  - 조직 체계 붕괴와 거버넌스 컨센서스 부재

## 🔗 Related Hubs
- [[20-Maps/Topic-Maps/Airflow-Hub|Airflow Hub]] - Pipeline orchestration
- [[20-Maps/Topic-Maps/Qraft-Work-Hub|Qraft Work Hub]] - Organizational context

## 📊 Statistics
- Core strategy documents: 1
- Active projects: 5
- Weekly reflections: 3
- Architecture patterns: 2 subdirectories
- Last updated: 2025-11-30

---

## 🎓 Implementation Phases

### Phase 1: Data Inventory (Non-invasive)
- Catalog existing data sources per team
- Document pipeline patterns (batch/realtime)
- Identify ownership and purpose
- No code changes required

### Phase 2: Catalog & Lineage
- DataHub ingestion setup
- Connect Snowflake, Postgres, Airflow
- Automated documentation
- Visibility without control

### Phase 3: Data Quality Rules
- Great Expectations integration
- DBT test implementation
- Critical datasets first (risk/finance)
- Slack alerting

### Phase 4: Common Datasets & Standards
- Shared dimension tables
- Naming conventions
- Tag/domain taxonomy
- Data product definitions

## 🚀 Current Focus (2025 Q4)

### DataHub Launch
- ✅ Airflow-DBT-DB integration
- ✅ Keycloak permission sync
- ⏳ Tag/Domain management strategy
- ⏳ Data product taxonomy

### Access Control
- ✅ Team-based database separation
- ✅ DAG connection variable isolation
- ✅ Kubernetes environment management
- ⏳ Asset visibility rules (public vs team-owned)

### Key Decisions Needed
1. Clear terminology and standards
2. Team tag vs public asset distinction
3. Purchased data (raw) vs processed data classification
4. Metadata inheritance from DAG to tasks/assets

## 💡 Strategic Insights

### What Works
- Framing as "compliance & audit" not "control"
- Offering time savings through catalog search
- Maintaining team autonomy while tracking lineage
- Progressive rollout starting with non-critical systems

### What to Avoid
- Forcing immediate standardization
- Modifying legacy pipelines directly
- Centralization without buy-in
- One-size-fits-all governance policies

### Success Metrics
- % of data sources cataloged
- Mean time to find data source (reduced)
- Data quality rule coverage
- Audit trail completeness
