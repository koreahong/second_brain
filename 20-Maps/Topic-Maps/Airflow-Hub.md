---
type: hub
status: evergreen
tags:
  - hub
  - airflow
  - orchestration
  - data-engineering
created: '2025-11-30'
updated: '2025-11-30'
maturity: 80
---
# Airflow Hub

> Central hub for all Apache Airflow orchestration knowledge and experience

## 🎯 Core Concepts

Apache Airflow is the backbone of data pipeline orchestration at Qraft, managing workflow automation, scheduling, and monitoring.

### Key Learning Areas
- [[03-Resources/Technology/Airflow/Airflow|Airflow Overview]]
- [[03-Resources/Technology/Airflow/airflow-기본개념(책)|Airflow 기본개념]]
- [[03-Resources/Technology/Airflow/airflow-아키텍쳐-및-세팅|Airflow 아키텍쳐 및 세팅]]
- [[03-Resources/Technology/Airflow/taskflow-공부|TaskFlow API]]

### Best Practices
- [[03-Resources/Technology/Airflow/Rules-for-good-dags|Rules for Good DAGs]]
- [[03-Resources/Technology/Airflow/top-level-code-jinja|Top-level Code & Jinja]]
- [[03-Resources/Technology/Airflow/partial|Partial Functions]]

## 📚 Resources (Technical Notes)

### Infrastructure & Setup
- [[03-Resources/Technology/Airflow/AWS-airflow-설치|AWS Airflow 설치]]
- [[03-Resources/Technology/Airflow/airflow-3.0|Airflow 3.0 Upgrade]]
- [[03-Resources/Technology/Airflow/airflow-ecs에-적용|Airflow on ECS]]
- [[03-Resources/Technology/Airflow/worker-분리|Worker 분리]]

### Development Patterns
- [[03-Resources/Technology/Airflow/airflow-pipeline-ingestion|Pipeline Ingestion]]
- [[03-Resources/Technology/Airflow/custom-operator-개발|Custom Operator 개발]]
- [[03-Resources/Technology/Airflow/ecs-operator--사용법|ECS Operator 사용법]]
- [[03-Resources/Technology/Airflow/ecs-operator-란|ECS Operator 개념]]
- [[03-Resources/Technology/Airflow/backfill-python-code|Backfill Python Code]]

### Integrations
- [[03-Resources/Technology/Airflow/airflow,-grafana-연동|Airflow-Grafana 연동]]
- [[03-Resources/Technology/Airflow/keycloak으로-Dag-권한관리|Keycloak DAG 권한관리]]
- [[03-Resources/Technology/Airflow/airflow-plugin|Airflow Plugin]]
- [[03-Resources/Technology/Airflow/ingestion-생성|DataHub Ingestion]]

### Example DAGs
- [[03-Resources/Technology/Airflow/nepa-airflow-dag-code|NEPA Airflow DAG]]
- [[03-Resources/Technology/Airflow/요기요-airflow-dag-code|요기요 Airflow DAG]]

## 💼 Projects (Applied Experience)

### Infrastructure Projects
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/airflow-3.0,-dbt-local-test|Airflow 3.0 & DBT Local Test]]
- [[02-Areas/크래프트테크놀로지스/Projects/03-인프라구축-Infrastructure/dag권한-관리|DAG 권한 관리]]

### Team Support
- [[02-Areas/크래프트테크놀로지스/Projects/05-팀지원-Support/MFT팀-배치-작업|MFT팀 배치 작업]]

## 🔍 Weekly Reflections

### Recent Work
- [[02-Areas/크래프트테크놀로지스/Experience/Weekly/2025년-11월-24일|2025년 11월 24일]] - DataHub 론칭, Airflow-DBT 연결
- [[02-Areas/크래프트테크놀로지스/Experience/Weekly/2025년-11월-17일|2025년 11월 17일]] - Airflow 레포 분리, 3.1.3 버전 사용
- [[02-Areas/크래프트테크놀로지스/Experience/Weekly/2025년-9월-29일|2025년 9월 29일]] - Data pipeline 개발 체계

## 🔗 Related Hubs
- [[20-Maps/Topic-Maps/Data-Governance-Hub|Data Governance Hub]] - DataHub integration
- [[20-Maps/Topic-Maps/Qraft-Work-Hub|Qraft Work Hub]] - Project context

## 📊 Statistics
- Total resources: 22 technical notes
- Active projects: 3
- Weekly mentions: 3 recent reflections
- Last updated: 2025-11-30

---

## 🎓 Learning Path

1. **Beginner**: Start with Airflow 기본개념 → 아키텍쳐 세팅
2. **Intermediate**: Study TaskFlow API → Custom Operators → Best Practices
3. **Advanced**: ECS integration → Worker 분리 → Multi-environment management
4. **Expert**: Keycloak integration → DataHub ingestion → Full automation

## 🚀 Current Focus
- Airflow 3.x migration
- Keycloak-based DAG access control
- DataHub metadata integration
- Environment separation (local/dev/prod)
