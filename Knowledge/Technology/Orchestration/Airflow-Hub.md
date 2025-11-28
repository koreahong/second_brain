---
type: hub
domain: data-engineering
topic: airflow
tags: [moc, orchestration, workflow, dag]
created: 2025-11-28
updated: 2025-11-28
---

# Airflow Hub

Apache Airflow 관련 모든 지식, 경험, 패턴을 연결하는 허브

## 개요

Airflow는 데이터 파이프라인 오케스트레이션 도구로, DAG(Directed Acyclic Graph)를 통해 워크플로우를 관리합니다.

---

## 📚 개념 (Concepts)

학습한 이론과 기본 개념

- [[AWS_airflow_설치|AWS Airflow 설치]]
- [[airflow,_grafana_연동|Airflow Grafana 연동]]
- [[airflow_기본개념(책)|Airflow 기본 개념 (책)]]
- [[airflow_아키텍쳐_및_세팅|Airflow 아키텍처 및 세팅]]
- [[backfill_python_code|Backfill Python 코드]]
- [[cosmos|Cosmos]]
- [[custom_operator_개발|Custom Operator 개발]]
- [[logs_s3_연결_|Logs S3 연결]]
- [[taskflow_공부|TaskFlow 공부]]
- [[경로설정|경로 설정]]
- [[기존_서비스와_연결(airflow,_postgresql)|기존 서비스와 연결]]
- [[외부_저장소_마운트|외부 저장소 마운트]]
- [[쿠버네티스|Kubernetes]]
- [[클러스터란|클러스터란]]

---

## 💼 경험 (Experiences)

실제 작업 경험과 트러블슈팅

- [[airflow_ecs에_적용|Airflow ECS 배포 경험]]

---

## 🎯 패턴 (Patterns)

반복 사용 가능한 베스트 프랙티스

- [[Rules_for_good_dags|좋은 DAG 작성 규칙]]
- [[TypeB_CRM_서비스_구축|TypeB CRM 서비스 구축]]
- [[airflow_3.0|Airflow 3.0]]
- [[keycloak으로_Dag_권한관리|Keycloak으로 DAG 권한 관리]]
- [[nepa_airflow_dag_code|네파 Airflow DAG 코드]]
- [[top_level_code_jinja|Top Level Code Jinja]]
- [[요기요_airflow_dag_code|요기요 Airflow DAG 코드]]

---

## 🚀 관련 프로젝트

- [[Qraft 데이터 파이프라인]]
- TypeB CRM 서비스
- 네파 데이터 파이프라인
- 요기요 데이터 파이프라인

---

## 🔗 관련 주제

### Transformation
- [[DBT-Hub|DBT]] - 데이터 변환 도구

### Storage
- [[PostgreSQL-Hub|PostgreSQL]] - 메타스토어 및 데이터베이스
- [[BigQuery-Hub|BigQuery]] - 데이터 웨어하우스

### Infrastructure
- [[Kubernetes-Hub|Kubernetes]] - 컨테이너 오케스트레이션
- [[Docker-Hub|Docker]] - 컨테이너화
- [[AWS-Hub|AWS]] - ECS, S3, Lambda 등

### Languages
- [[Python-Hub|Python]] - Airflow 개발 언어

---

## 📈 학습 로드맵

### 초급
- [ ] Airflow 기본 개념 이해
- [ ] DAG 작성 기초
- [ ] Operator 종류 파악
- [ ] TaskFlow API 학습

### 중급
- [ ] Custom Operator 개발
- [ ] Airflow 아키텍처 이해
- [ ] 성능 최적화
- [ ] Backfill 처리

### 고급
- [ ] Kubernetes Executor 활용
- [ ] 대규모 파이프라인 설계
- [ ] 모니터링 및 알람 구축
- [ ] 권한 관리 (Keycloak)

---

## 🔖 빠른 참조

### 자주 사용하는 명령어
```bash
# Airflow 시작
airflow webserver
airflow scheduler

# DAG 테스트
airflow dags test <dag_id> <execution_date>

# Backfill
airflow dags backfill <dag_id> -s <start_date> -e <end_date>
```

### 핵심 원칙
1. **멱등성(Idempotency)**: DAG는 여러 번 실행해도 같은 결과
2. **Atomic Tasks**: Task는 원자적으로 동작
3. **Template 활용**: execution_date 등 활용
4. **Top-level Code 주의**: DAG 파일 로딩 시 실행되는 코드 최소화

---

*Last Updated: 2025-11-28*
*Status: active*
*Total Notes: 22개 (Concepts: 14, Experiences: 1, Patterns: 7)*
