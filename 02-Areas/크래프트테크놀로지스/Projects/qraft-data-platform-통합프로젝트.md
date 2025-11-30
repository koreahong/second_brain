---
title: Qraft Data Platform 통합 프로젝트
type: project
tags:
  - 크래프트테크놀로지스
  - data-platform
  - infrastructure
  - data-governance
  - metadata
  - data-quality
  - airflow
  - datahub
  - dbt
  - alembic
created: '2025-11-30'
updated: '2025-11-30'
status: active
priority: high
project_type: infrastructure
start_date: '2025-08-01'
company: 크래프트테크놀로지스
---

# Qraft Data Platform 통합 프로젝트

## 📋 프로젝트 개요

**회사**: 크래프트테크놀로지스 (Qraft Technologies)
**기간**: 2025년 8월 ~ 현재 (진행 중)
**역할**: Data Analytics Engineer
**팀**: ML Platform Infrastructure Team

크래프트테크놀로지스의 데이터 플랫폼 중앙 통합 저장소로, 전사 데이터 파이프라인과 거버넌스를 관리하는 핵심 인프라 프로젝트입니다.

**프로젝트 저장소**: `~/qraft_data_platform`

**배경**:
- 2025년 8월 입사 후 데이터 인프라 전반 재구축
- 팀별로 분산된 데이터 파이프라인 통합 관리 필요
- 메타데이터 관리 및 데이터 거버넌스 체계 부재
- 데이터 품질 관리 프로세스 정립 필요

## 🎯 핵심 목표

1. **데이터 파이프라인 통합 관리** - Airflow 기반 팀별 DAG 관리
2. **메타데이터 관리** - DataHub를 통한 데이터 카탈로그 및 리니지 관리
3. **데이터 거버넌스** - 권한, 품질, 표준화 정책 수립
4. **데이터 품질 관리** - DBT 기반 데이터 검증 및 테스트
5. **인프라 자동화** - CI/CD, 권한 자동화, 환경 관리

## 🏗️ 아키텍처 구조

```
qraft_data_platform/
├── infrastructure/
│   ├── airflow/teams/  # 팀별 Airflow 프로젝트 (Git Subtree)
│   ├── datahub/        # DataHub 메타데이터 관리
│   └── alembic/        # DB 마이그레이션
├── .claude/            # 공유 개발 컨벤션
└── .git-workflow/      # Git Subtree 워크플로우
```

## 🔧 주요 컴포넌트

### 1. Airflow (데이터 파이프라인)
- **역할**: 팀별 데이터 파이프라인 오케스트레이션
- **구성**: Git Subtree로 팀별 레포 통합 관리
- **환경**: local, dev, prod 환경 분리
- **인증**: Keycloak SSO 통합
- **관련 문서**: `infrastructure/airflow/teams/qraft/`

### 2. DataHub (메타데이터 & 거버넌스)
- **역할**: 데이터 카탈로그, 리니지, 검색, 거버넌스
- **주요 기능**:
  - Airflow - DBT - Snowflake 메타데이터 통합
  - 데이터 리니지 추적
  - 도메인 및 태그 관리
  - 팀별 권한 관리
- **커스텀 구현**:
  - Airflow Custom Source (Keycloak 인증 통합)
  - DBT Custom Patches (URL 인코딩, Tag 매핑)
  - Domain Pattern Mapping (플랫폼 간 도메인 통합)
- **관련 문서**: `infrastructure/datahub/docs/`

### 3. DBT (데이터 변환 & 품질)
- **역할**: SQL 기반 데이터 변환 및 품질 검증
- **계층 구조**: Raw → Intermediate → Mart → Analytics
- **품질 관리**:
  - DBT Tests (데이터 검증)
  - Great Expectations 통합 계획
  - 메타데이터 자동 생성
- **관련 문서**: `infrastructure/airflow/teams/qraft/dbt/`

### 4. Alembic (DB 마이그레이션)
- **역할**: PostgreSQL 스키마 버전 관리
- **대상**: Airflow, DataHub 메타데이터 DB
- **관련 문서**: `infrastructure/alembic/`

### 5. Keycloak (통합 인증)
- **역할**: SSO 인증 및 권한 관리
- **적용 범위**: Airflow, DataHub, Jira
- **자동화**: Python 스크립트를 통한 권한 동기화

## 📊 데이터 거버넌스 구현

### 메타데이터 관리
- **도구**: DataHub
- **관리 항목**:
  - 데이터셋 정의 및 설명
  - 컬럼 레벨 메타데이터
  - 비즈니스 용어 및 태그
  - 소유자 및 팀 정보
  - 데이터 리니지 (Airflow → DBT → Snowflake)

### 네이밍 컨벤션
- **원천 데이터**: 벤더사 기준 명명 규칙 정립 필요
- **DBT 모델**: Prefix 기반 레이어 구분
  - `raw_`: 원천 데이터
  - `int_`: 중간 테이블
  - `fct_`, `dim_`: Fact/Dimension
  - `vw_`: 뷰
- **관련 노트**: [[원천-네이밍-룰-정하기]]

### 권한 관리
- **플랫폼별 권한**:
  - Airflow: DAG 단위 권한 (Keycloak 연동)
  - Snowflake: Role 기반 접근 제어
  - DataHub: 도메인/태그 기반 권한
- **자동화**:
  - Keycloak ↔ Airflow/DataHub 권한 동기화
  - 신규 팀원 자동 권한 부여
- **관련 노트**: [[dag권한-관리]], [[jira,-keycloak-권한-자동화]]

### 데이터 품질 관리
- **현재 구현**: DBT Tests
- **계획**: Great Expectations 통합
- **검증 항목**:
  - 스키마 검증
  - Null 체크
  - Unique 제약
  - 참조 무결성
  - 비즈니스 규칙

## 🔄 개발 워크플로우

### Git Subtree 전략
- **목적**: 팀별 레포를 중앙 레포에 통합
- **구조**: `infrastructure/airflow/teams/` 하위에 팀별 subtree
- **워크플로우**:
  1. 팀별 레포에서 독립 개발
  2. Subtree pull로 중앙 레포 동기화
  3. 통합 테스트 및 배포
- **관련 문서**: `.git-workflow/`

### CI/CD
- **도구**: GitLab CI
- **파이프라인**:
  - 코드 검증 (pre-commit hooks)
  - DBT 모델 테스트
  - DAG 문법 검증
  - 환경별 배포
- **관련 노트**: [[gitlab-ci-cd-세팅]]

### 개발 컨벤션
- **DAG 개발**: `.claude/convention-dag.md`
- **DBT 모델링**: `.claude/convention-dbt.md`
- **Git 워크플로우**: `.claude/convention-git.md`
- **Jira 연동**: `.claude/convention-jira.md`
- **문서화**: `.claude/convention-documentation.md`

## 🚀 구현 현황

### ✅ 완료된 작업
- [x] Airflow 3.0 로컬/개발 환경 구축
- [x] DataHub 초기 설정 및 Keycloak 인증 통합
- [x] Airflow-DBT-Snowflake 메타데이터 연동
- [x] Git Subtree 기반 팀별 레포 통합
- [x] 커스텀 Airflow Source 개발 (Keycloak 인증)
- [x] DBT Patches (URL 인코딩, Tag 매핑)
- [x] Domain Pattern Mapping 구현
- [x] 로컬 개발 환경 명령어 (`dkai`, `dkdh`)

### 🔄 진행 중
- [ ] DataHub 컨텐츠 채우기 (도메인, 태그 정립)
- [ ] 데이터 명명 규칙 표준화
- [ ] 데이터 품질 검증 프로세스 정립
- [ ] ERD 작성 및 관리
- [ ] Iceberg + DataHub 통합 검토

### 📋 계획
- [ ] Great Expectations 통합
- [ ] 데이터 카탈로그 자동 생성
- [ ] 데이터 품질 대시보드
- [ ] 자동화된 메타데이터 검증

## 🔗 관련 프로젝트

### 인프라 구축
- [[airflow-3.0,-dbt-local-test]]
- [[dag권한-관리]]
- [[gitlab-ci-cd-세팅]]
- [[jira,-keycloak-권한-자동화]]
- [[postgres--snowflake-권한관리]]
- [[원천-데이터-적재-파이프라인-개발]]

### 거버넌스
- [[iceberg-+-datahub]]
- [[ERD-작성]]
- [[데이터벤토-관리-방안]]
- [[원천-네이밍-룰-정하기]]

### 데이터 개발
- [[HFT-lseg-sftp-파일-배치-dag-개발]]
- [[Invesco-크롤링-데이터-개발]]
- [[flex-master-table-개발]]
- [[slickcharts-마이그레이션]]

## 📝 주간 회고 연결

### 2025년 11월 24일
- DataHub 론칭
- Airflow - DBT - DB 연결
- Local/Dev/Prod 환경 분리
- Keycloak 권한 관리
- DataHub 컨텐츠 채우기 (도메인/태그 관리)
- **링크**: [[2025년-11월-24일]]

## 🎓 학습 및 인사이트

### 데이터 거버넌스
1. **명확한 용어 정리 필요**: 데이터 셋, 도메인, 태그의 기준 명확화
2. **Public vs Team 데이터 구분**: 팀 태그가 없는 asset은 Public으로
3. **구매 vs 프로세싱 데이터**: Data Product 분류 기준 필요
4. **Owner 정책**: 구매한 원천 데이터는 Public owner

### 메타데이터 관리
- Airflow Tasks는 DAG 정보 상속
- DBT Tag는 URL 인코딩 이슈 (Custom Patch로 해결)
- Domain Pattern Mapping으로 플랫폼 간 통합

### 기술 스택
- **Airflow 3.0**: 안정성 및 성능 개선
- **DataHub**: 엔터프라이즈급 메타데이터 관리
- **DBT**: SQL 기반 데이터 변환 및 검증
- **Keycloak**: 통합 SSO 인증

## 📚 참고 문서

### 📂 프로젝트 저장소 문서 (qraft_data_platform)
- **Documentation Index**: `DOCUMENTATION_INDEX.md` - 전체 문서 인덱스
- **Claude Code Context**: `.claude/CLAUDE.md` - AI 컨텍스트 및 컨벤션
- **README**: `README.md` - 프로젝트 개요
- **신규 개발자**: `infrastructure/airflow/teams/qraft/CONTRIBUTING.md`
- **DataHub 사용**: `infrastructure/datahub/docs/USAGE.md`
- **DataHub 설정**: `infrastructure/datahub/docs/SETUP.md`
- **트러블슈팅**: 각 컴포넌트별 `TROUBLESHOOTING.md`

### 📖 세컨드브레인 문서 (본 vault)

#### 거버넌스 & 품질
- [[Qraft-Data-Governance-Framework|크래프트 데이터 거버넌스 프레임워크]] - 전사 거버넌스 체계
- [[Data-Quality-Management|데이터 품질 관리 프로세스]] - 품질 검증 및 모니터링

#### 기술 스택
- [[DataHub|DataHub - 메타데이터 관리]] - 메타데이터 플랫폼 상세
- [[Airflow|Airflow]] - 데이터 파이프라인 오케스트레이션
- [[DBT|DBT]] - 데이터 변환 및 테스트
- [[Keycloak]] - SSO 통합 인증
- [[PostgreSQL|PostgreSQL]] - 메타데이터 저장소
- [[Snowflake]] - 데이터 웨어하우스

#### 관련 기술 지식
- [[Data-Modeling-Best-Practices|데이터 모델링 Best Practices]]
- [[Git Subtree]] - 팀별 레포 통합 전략
- [[데이터-거버넌스|Data Governance]] - 거버넌스 개념

## 💡 다음 액션

1. **DataHub 컨텐츠 정립**
   - 도메인 및 태그 표준 정의
   - 팀별 데이터셋 분류
   - 용어집 작성

2. **데이터 품질 프로세스**
   - Great Expectations 도입 검토
   - 품질 검증 규칙 정의
   - 자동화된 품질 리포트

3. **네이밍 컨벤션**
   - 벤더사별 원천 데이터 네이밍 규칙
   - DBT 모델 네이밍 가이드
   - Snowflake 스키마/테이블 네이밍

4. **문서화**
   - ERD 작성 및 최신화
   - API 문서 자동 생성
   - 온보딩 가이드 보완

---

**프로젝트 담당**: ML Platform Infrastructure Team
**마지막 업데이트**: 2025-11-30
