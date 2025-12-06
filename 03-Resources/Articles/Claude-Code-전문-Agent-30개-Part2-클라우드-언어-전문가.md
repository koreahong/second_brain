---
tags:
  - article
  - reading
  - claude-code
  - subagents
  - cloud-architecture
  - specialized-agents
created: 2025-12-04T05:32:00.000Z
updated: 2025-12-04T05:35:00.000Z
title: Claude Code 전문 Agent 30개 Part 2 - 클라우드/언어 전문가
type: article
notion_id: 2bfc6d43-3b4d-8045-b5d5-e5fd03375bd8
company: MEDIUM
period: 2025-12-04T00:00:00.000Z
---

<!--
Notion 원본: https://www.notion.so/2bfc6d433b4d8045b5d5e5fd03375bd8
원본 소스: https://medium.com/@ichigoSan/i-accidentally-made-claude-45-smarter-heres-how-23ad0bf91ccf
마이그레이션 날짜: 2025-12-07
-->

# Claude Code 전문 Agent 30개 Part 2 - 클라우드/언어 전문가

## 📌 주요 이슈 요약

💡 이 글의 핵심 메시지 3가지

- **클라우드 전문가 Agent**: AWS/GCP/Azure 각각의 전문가로 월 $228,000 비용 절감 사례
- **언어별 심화 Agent**: Python/Go/Rust/TypeScript 전문가로 성능 95% 향상
- **도메인 전문가**: Blockchain/ML/Gaming/IoT 등 특수 분야 전문성 제공

## 🌍 배경 및 맥락

**Part 1에서 다룬 것**: 15개 핵심 개발 Agent (Frontend, Backend, QA, Security 등)

**Part 2의 목적**: 특수 시나리오를 위한 15개 전문 Agent 추가

**실제 문제**:
- AWS 청구서 $45,000/월 → 최적화 필요
- Python 파이프라인 4시간 → 실시간 필요
- 스마트 컨트랙트 취약점 → $2M 손실 위험

## 📝 주요 내용 요약

### 클라우드 전문가 (3개 Agent)

#### 16. AWS Solutions Architect
**실제 사례**: $45,000/월 → $26,000/월 (42% 절감, 연간 $228,000 절감)

**최적화 발견**:
- RDS 인스턴스 over-provisioned (CPU 12% 사용률)
- Reserved Instances 미사용
- CloudFront CDN 없이 EC2에서 직접 static asset 제공
- S3 lifecycle 정책 없음 (로그 영구 저장)

#### 17. GCP Cloud Engineer  
**실제 사례**: BigQuery 비용 $8,000/월 → $1,800/월 (78% 절감)

**최적화 내용**:
- 테이블 파티셔닝 (scan 95% 감소)
- Clustering 추가
- SELECT * 대신 필요 컬럼만 선택
- Materialized views 구현

#### 18. Azure DevOps Specialist
**실제 사례**: 온프레미스 $15,000/월 → Azure $6,300/월 (58% 절감)

**하이브리드 마이그레이션**:
- Azure Functions로 배치 작업 이전
- AKS로 컨테이너화
- Azure AD 통합

### 언어 전문가 (4개 Agent)

#### 19. Python Expert
**실제 사례**: 데이터 파이프라인 4시간 → 12분 (95% 단축)

**최적화 기법**:
- asyncio로 50,000 API 호출 병렬화
- pandas → polars (10배 빠름)
- 멀티프로세싱 CPU 계산
- 배치 DB writes (1,000개씩)

#### 20. Go Systems Programmer
**실제 사례**: Node.js 8GB 메모리 → Go 800MB (90% 감소)

**성능 향상**:
- Response time: 2,000ms → 45ms
- Throughput: 5,000 req/s → 50,000 req/s
- 서버 12대 → 3대

#### 21. Rust Performance Engineer
**실제 사례**: 브라우저 이미지 처리 15초 → 800ms (95% 단축)

**WebAssembly 활용**:
- Rust로 이미지 처리 알고리즘 작성
- WASM으로 컴파일
- 메모리 사용량 85% 감소

#### 22. TypeScript Architect
**실제 사례**: 프로덕션 버그 주 3~4개 → 0.3개 (90% 감소)

**Strict TypeScript**:
- any 타입 제거
- Branded types로 ID 혼용 방지
- Discriminated unions

### 고급 운영 (2개 Agent)

#### 23. Kubernetes Operator
**실제 사례**: Uptime 99.2% → 99.99%

**K8s 최적화**:
- Resource limits 설정
- HPA (Horizontal Pod Autoscaler)
- Pod Disruption Budgets
- Istio service mesh

#### 24. Blockchain Developer
**실제 사례**: $2M 유동성 스마트 컨트랙트 취약점 발견

**발견한 치명적 이슈**:
- Reentrancy 취약점 (컨트랙트 drain 가능)
- Integer overflow
- 접근 제어 누락
- Front-running 취약점
- Unchecked external calls

### 도메인 전문가 (6개 Agent)

#### 25. ML/AI Engineer
**실제 사례**: 모델 배포 6주 → 2시간 (99% 단축)

**MLOps 파이프라인**:
- 자동 학습, 검증, 배포
- 실시간 drift detection
- Gradual rollout + 자동 rollback

#### 26-30. 기타 전문가
- **Game Developer**: 모바일 게임 로드 12초 → 2.3초, 평점 2.1 → 4.5
- **IoT Systems Engineer**: 50,000 IoT 트래커 배터리 3일 → 21일
- **GraphQL Specialist**: 12~15 API 호출 → 1개 통합 쿼리
- **Observability Engineer**: MTTD 45분 → 90초, MTTR 4~6시간 → 15분
- **GitOps Automation**: 배포 3~4시간 → 5분, 실패율 25% → 0.8%

## 💡 시사점 및 인사이트

### 내게 주는 교훈

**전문화의 힘**: Generic AI보다 specialized agent가 domain-specific 문제에서 훨씬 효과적

**ROI 계산**:
- AWS 최적화: 1회 분석으로 연간 $228,000 절감
- 스마트 컨트랙트 감사: $2M 손실 방지
- MLOps 자동화: 배포 시간 99% 단축

**전문 지식의 가치**: 
- 시니어 아키텍트 vs 제너럴리스트 차이
- 클라우드별 특화 기능 활용 (AWS vs GCP vs Azure)
- 언어별 최적화 패턴 (Go goroutines, Rust ownership, Python async)

### 업무 적용 가능성

**Qraft 데이터 플랫폼**:
- **AWS Architect**: Snowflake + Redshift 비용 최적화
- **Python Expert**: Airflow DAG 실행 시간 단축
- **K8s Operator**: DataHub 배포 안정성 향상
- **Observability Engineer**: 데이터 파이프라인 모니터링 강화

**우선순위**:
1. AWS Solutions Architect (비용 절감 즉시 효과)
2. Python Expert (데이터 파이프라인 최적화)
3. Observability Engineer (장애 대응 시간 단축)

### 의문점 & 추가 탐구

- **한국 클라우드 환경**: AWS Seoul 리전 최적화 패턴은?
- **데이터 엔지니어링 특화**: Snowflake/DBT/Airbyte 전문 Agent 필요
- **비용 모니터링**: 클라우드 비용 최적화 자동화 가능?

## 🔗 관련 자료

- **Part 1**: [Claude Code SubAgents 30개 Part 1](Claude-Code-전문-Agent-30개-Part1-핵심-개발자.md)
- **관련 기술**: AWS, GCP, Azure, Kubernetes, Python, Go, Rust, TypeScript
- **GitHub**: [claude-code-tresor](https://github.com/alirezarezvani/claude-code-tresor)

---

## 📎 Related

### Projects
- [[02-Areas/크래프트테크놀로지스/Projects]] - 클라우드 비용 최적화 프로젝트

### Knowledge
- [[03-Resources/Technology/AWS]] - AWS 아키텍처 패턴
- [[03-Resources/Technology/Kubernetes]] - K8s 운영
- [[03-Resources/Data-Governance]] - MLOps 및 관측성

### Insights
- [[30-Flow/Life-Insights/Personal/Untitled]] - MCP 아키텍처 최적화
