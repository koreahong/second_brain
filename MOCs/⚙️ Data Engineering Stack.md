---
created: 2025-11-28
type: moc
tags: [moc, technology, data-engineering, stack]
---

# ⚙️ Data Engineering Stack

> 데이터 엔지니어링 기술 스택 전체 맵

## 🗺️ Technology Map

### 🔄 Orchestration
- **Airflow** ⭐ (Main)
  - [[Knowledge/Technology/Airflow/아키텍처]]
  - [[Knowledge/Technology/Airflow/RBAC-설계]]
  - [[Knowledge/Technology/Airflow/Operators]]
  - Used in: [[Actions/Work/Qraft/Projects/dag권한 관리]]

### 🐍 Programming
- **Python** ⭐
  - [[Knowledge/Technology/Python/Decorators]]
  - [[Knowledge/Technology/Python/비동기-프로그래밍]]
  - [[Knowledge/Technology/Python/SQLAlchemy]]

- **SQL** ⭐
  - [[Knowledge/Technology/SQL/쿼리-최적화]]
  - [[Knowledge/Technology/SQL/윈도우-함수]]
  - [[Knowledge/Technology/SQL/파티셔닝]]

### ☁️ Cloud & Storage
- **Snowflake**
  - [[Knowledge/Technology/DataPlatform/Snowflake-권한관리]]
  - [[Knowledge/Technology/DataPlatform/Snowflake-파티셔닝]]

- **MinIO**
  - [[Knowledge/Technology/Cloud/MinIO-아키텍처]]
  - Used in: [[Actions/Work/Qraft/Projects/MinIO 적재 - 호출 테스트]]

- **AWS**
  - [[Knowledge/Technology/Cloud/AWS-Lambda]]
  - [[Knowledge/Technology/Cloud/AWS-SQS]]
  - [[Knowledge/Technology/Cloud/AWS-RDS-Proxy]]

### 🗄️ Databases
- **PostgreSQL**
  - [[Knowledge/Technology/SQL/PostgreSQL-파티셔닝]]
  - [[Knowledge/Technology/SQL/PostgreSQL-타입]]

### 🔧 DevOps & Tools
- **GitLab CI/CD**
  - [[Knowledge/Technology/DataPlatform/GitLab-CICD]]
  - Used in: [[Actions/Work/Qraft/Projects/gitlab ci cd 세팅]]

- **Docker**
  - [[Knowledge/Technology/DataPlatform/Docker-이미지-작성]]

- **DBT**
  - [[Knowledge/Technology/DataPlatform/DBT-로컬-테스트]]
  - Used in: [[Actions/Work/Qraft/Projects/airflow 3.0, dbt local test]]

### 🔐 Security & Auth
- **Keycloak**
  - [[Knowledge/Technology/Cloud/Keycloak-권한설정]]
  - Used in: [[Actions/Work/Qraft/Projects/jira, keycloak 권한 자동화]]

## 📚 Core Concepts

### Architecture Patterns
- [[Knowledge/Concepts/데이터-레이크하우스]]
- [[Knowledge/Concepts/이벤트-드리븐-아키텍처]]
- [[Knowledge/Patterns/마이크로서비스-패턴]]

### Data Engineering
- [[Knowledge/Concepts/데이터-거버넌스]]
- [[Knowledge/Concepts/데이터-품질-관리]]
- [[Knowledge/Concepts/데이터-리니지]]
- [[Knowledge/Concepts/파이프라인-설계-패턴]]

### Best Practices
- [[Knowledge/Patterns/권한-설계-패턴]]
- [[Knowledge/Patterns/CI-CD-파이프라인]]
- [[Knowledge/Patterns/데이터-마이그레이션-전략]]

## 🎯 프로젝트별 기술 활용

### Airflow Projects
```
dag권한 관리 ─→ Airflow RBAC + Keycloak
HFT lseg dag ─→ Airflow + SFTP + Batch Processing
airflow 3.0   ─→ Airflow Upgrade + DBT
```

### Data Pipeline Projects
```
원천 데이터 적재 ─→ Python + MinIO + Snowflake
Invesco 크롤링 ─→ Python + Selenium + Airflow
flex master    ─→ SQL + Data Modeling
```

### Infrastructure Projects
```
gitlab ci cd ─→ GitLab + Docker + Automation
권한 자동화   ─→ Keycloak + Jira + Python
```

## 📈 숙련도

### ⭐⭐⭐ Expert
- Airflow
- Python
- SQL
- PostgreSQL

### ⭐⭐ Proficient
- Snowflake
- MinIO
- AWS (Lambda, SQS)
- Docker

### ⭐ Working Knowledge
- DBT
- Keycloak
- GitLab CI/CD

## 🔗 관련 MOC
- [[MOCs/💼 Qraft Experience]] - 실제 사용 경험
- [[MOCs/🚀 Career Journey 2025]] - 면접 준비

## 📝 학습 로드맵

### 현재 학습 중
- [ ] Airflow 3.0 신기능
- [ ] DBT 고급 기법
- [ ] Iceberg + DataHub

### 다음 학습 목표
- [ ] Kubernetes
- [ ] Kafka
- [ ] Spark

---

**마지막 업데이트**: 2025-11-28
**Total Technologies**: 15+ tools/frameworks