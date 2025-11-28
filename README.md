---
created: 2025-11-28
updated: 2025-11-28
---

# 🧠 DAE Second Brain

**Data Analytics Engineer를 위한 지식 네트워크 시스템**

---

## 철학

**"지식(Knowledge) + 경험(Experience) + 결과(Pattern) = 네트워크"**

각 주제마다 외부 지식, 실제 경험, 그 결과물이 연결된 지식 네트워크를 구축합니다.

---

## 📁 폴더 구조

```
DAE-Second-Brain/
├── Knowledge/              # 주제별 지식 체계
│   ├── Data-Management/    # 데이터 관리
│   │   ├── Data-Governance/
│   │   ├── Data-Quality/
│   │   ├── Data-Modeling/
│   │   └── Data-Lineage/
│   ├── Data-Architecture/  # 데이터 아키텍처
│   │   ├── Data-Mesh/
│   │   ├── Data-Lakehouse/
│   │   └── Streaming/
│   ├── Technology/         # 기술 스택
│   │   ├── Orchestration/       # Airflow
│   │   ├── Transformation/      # DBT
│   │   ├── Storage/             # PostgreSQL, BigQuery, etc
│   │   ├── Infrastructure/      # K8s, Docker, AWS
│   │   ├── CI-CD/
│   │   └── Languages/           # Python, SQL
│   ├── Analytics/          # 분석
│   │   ├── Product-Analytics/
│   │   ├── Web-Analytics/
│   │   └── Marketing-Analytics/
│   ├── Personal/           # 개인 주제
│   │   ├── Well-being/
│   │   ├── Investment/
│   │   └── Learning/
│   └── Career/             # 커리어
│       ├── Certifications/
│       ├── Interview/
│       ├── Portfolio/
│       └── Learning-Path/
│
├── Experiences/            # 회사/프로젝트별 경험
│   ├── Qraft/
│   ├── Coupang/
│   └── Companies/
│
├── Projects/               # 프로젝트
│   ├── Active/
│   └── Completed/
│
└── Templates/              # 노트 템플릿
    ├── concept-note.md
    ├── experience-note.md
    ├── pattern-note.md
    ├── hub-note.md
    └── project-note.md
```

---

## 🗂️ 노트 타입

각 주제는 **Concepts/Experiences/Patterns** 3개 폴더로 구성:

### 📚 Concept (개념)
외부 학습, 공부한 내용, 이론
- 책, 강의, 문서에서 학습한 내용
- 기술 개념 정리
- 참고 자료 모음

### 💼 Experience (경험)
실제 작업 경험, 트러블슈팅, 시행착오
- 프로젝트 경험 기록
- 문제 해결 과정
- 배운 점과 개선사항

### 🎯 Pattern (패턴)
반복 사용 가능한 패턴, 베스트 프랙티스
- 재사용 가능한 코드
- 검증된 베스트 프랙티스
- 팀 표준 가이드

### 🏢 Hub (허브)
주제별 지식 네트워크 연결점 (MOC - Map of Content)
- 특정 주제의 모든 노트 연결
- 학습 로드맵
- 빠른 참조

---

## 🎯 주요 Hub

### Data Engineering
- [[Airflow-Hub|🚀 Airflow]] - 워크플로우 오케스트레이션 (22개 노트)
- DBT - 데이터 변환
- Great Expectations - 데이터 품질

### Technology Stack

#### Languages
- [[Python-Hub|🐍 Python]] - 메인 프로그래밍 언어 (15개 노트)
- SQL - 데이터 쿼리

#### Infrastructure
- Kubernetes - 컨테이너 오케스트레이션
- Docker - 컨테이너화
- AWS - 클라우드 인프라

#### Storage
- PostgreSQL - RDBMS
- BigQuery - 데이터 웨어하우스
- Snowflake - 클라우드 DW

### Analytics
- Product Analytics (AARRR, 퍼널)
- Web Analytics (웹로그 분석)
- Marketing Analytics (CRM)

---

## 🏷️ 메타데이터 시스템

```yaml
---
type: [concept|experience|pattern|hub]
domain: [data-engineering|data-architecture|analytics]
topic: airflow
tags: [orchestration, dag, production]
status: [learning|practicing|mastered]
created: 2025-11-28
updated: 2025-11-28
---
```

---

## 🚀 시작하기

### 새 노트 작성하기
1. 적절한 폴더 찾기 (예: `Knowledge/Technology/Orchestration`)
2. 노트 타입 결정 (Concept/Experience/Pattern)
3. 템플릿 사용 (`Templates/` 참고)
4. 메타데이터 작성
5. 관련 Hub에 연결

### 학습 플로우 예시: Airflow 배우기
1. **Concept**: `Airflow 기본 개념` - 외부 자료 학습
2. **Experience**: `Airflow ECS 배포` - 실제 적용하며 경험 기록
3. **Pattern**: `좋은 DAG 작성 규칙` - 재사용 가능한 패턴 정리
4. **Hub**: `Airflow Hub` - 모든 노트 연결

---

## 📊 현재 상태

### 통계 (2025-11-28)
- **총 노트**: 113개
- **Concepts**: ~60개
- **Experiences**: ~20개
- **Patterns**: ~30개
- **Hubs**: 2개 (Airflow, Python)
- **삭제된 빈 파일**: 34개

### 최근 마이그레이션
- **2025-11-28**: Notion → Obsidian 완료 (156개 파일)
- **2025-11-28**: 새 지식 네트워크 구조 설계 및 적용
- **2025-11-28**: 파일 자동 분류 및 이동 완료

---

## 🔗 연결 원칙

### 양방향 링크
Concept ↔ Experience ↔ Pattern ↔ Hub

### 수평적 연결
비슷한 주제끼리 (Airflow ↔ DBT ↔ PostgreSQL)

### 수직적 연결
상위 개념 → 하위 구현 (이론 → 실습 → 적용)

---

## 🎓 DAE 학습 로드맵

### 신입 DAE (0-2년)
1. **기초**: SQL, Python, Git
2. **파이프라인**: Airflow 기본
3. **변환**: DBT 기초
4. **인프라**: Docker, 기본 AWS
5. **심화**: 대규모 데이터 처리

### 시니어 DAE (3-5년)
1. **아키텍처**: Data Mesh, Medallion
2. **성능**: 최적화, 스케일링
3. **품질**: Data Quality, Lineage
4. **거버넌스**: 권한 관리, 보안
5. **리더십**: 팀 빌딩, 기술 전파

---

## 📚 참고 문서

- [[KNOWLEDGE_STRUCTURE_DESIGN|📐 Knowledge Structure Design]] - 상세 설계 문서
- [[MIGRATION_SUMMARY|📦 Migration Summary]] - 마이그레이션 요약
- [Templates](Templates/) - 노트 템플릿 모음

---

## 🔧 플러그인

- **Dataview**: 통계 및 동적 쿼리
- **Templater**: 템플릿 자동화
- **Obsidian Git**: Git 자동 동기화
- **Tag Wrangler**: 태그 관리

---

*Last Updated: 2025-11-28*
*Version: 2.0 (Knowledge Network Structure)*
*Total Notes: 113개*

## 📚 Documentation

### 구조 및 가이드

- [[PARA-BRAIN-STRUCTURE.md|PARA + Brain 구조 설명]]
- [[RESTRUCTURE_SUMMARY.md|재구조화 요약]]
- [[CAREER_STRUCTURE.md|커리어 구조 가이드]]
- [[RECOMMENDED_PLUGINS.md|추천 플러그인]]
- [[QUICK_START.md|빠른 시작 가이드]]
- [[KNOWLEDGE_STRUCTURE_DESIGN.md|Knowledge 구조 설계]]
- [[MIGRATION_SUMMARY.md|마이그레이션 요약]]

### Vault 관리 및 자동화

- [[VAULT_MANAGEMENT_GUIDE.md|Vault 관리 가이드]] - Second Brain 유지보수 가이드
- [[second_brain_report.md|Second Brain Health Report]] - 현재 상태 분석 리포트
- [[SECOND_BRAIN_ACTION_PLAN.md|액션 플랜]] - 개선 작업 계획
- [[.claude/agents/second-brain-curator.md|Second Brain Curator Agent]] - 자동 큐레이션 에이전트

---
