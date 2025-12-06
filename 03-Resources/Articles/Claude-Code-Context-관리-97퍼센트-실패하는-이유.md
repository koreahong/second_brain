---
tags:
  - article
  - reading
  - claude-code
  - context-management
  - orchestration
  - multi-agent
  - architecture
  - token-optimization
created: '2025-12-04T05:27:00.000Z'
updated: '2025-12-07T00:00:00.000Z'
title: Claude Code Context 관리 - 97%가 실패하는 이유
type: article
notion_id: 2bfc6d43-3b4d-804a-bda2-e664ea651efb
company: MEDIUM
period: '2025-12-04T00:00:00.000Z'
applied_in: MCP-아키텍처와-데이터-거버넌스-최적화
connection_quality: high
has_real_world_application: true
---

<!--
Notion 원본: https://www.notion.so/2bfc6d433b4d804abda2e664ea651efb
원본 소스: https://medium.com/@ichigoSan/i-accidentally-made-claude-45-smarter-heres-how-23ad0bf91ccf
마이그레이션 날짜: 2025-12-07
-->

# Claude Code Context 관리 - 97%가 실패하는 이유

## 📌 주요 이슈 요약

💡 이 글의 핵심 메시지 3가지

- **Context Window Death Spiral**: 구현 세부사항이 73% 차지하면서 아키텍처 요구사항이 밀려남
- **4-Layer Orchestra Architecture**: Orchestrator → Context Hub → Specialists → Integration 구조로 89% 정확도 유지
- **실측 성과**: WebSocket 시스템을 3일만에 구축 (기존 2~3주 소요)

## 🌍 배경 및 맥락

**실제 사건**: 9명의 시니어 엔지니어가 72시간 동안 OAuth 모듈 디버깅

**문제의 본질**:
- Agent가 OAuth 플로우를 17번 재작성
- 3.2M 토큰의 순환 수정
- 3번째 응답부터 프로젝트 요구사항 망각
- JWT → OAuth → 세션 기반 → 다시 JWT (완전히 다른 스키마)

**근본 원인**: 구현 노이즈 누적으로 아키텍처 플랜이 context window 밖으로 밀려남

## 📝 주요 내용 요약

### 3가지 실패 모드

#### 1. Context Window Death Spiral
**증상**:
- 완벽한 이해로 시작 → 5분 후 제외한 npm 패키지 제안
- 10분 후 방금 만든 인터페이스 재작성

**원인 분석**:
- 구현 세부사항이 첫 2,000 토큰 내 73% 차지
- 아키텍처 요구사항이 attention threshold 이하로 하락
- 아키텍처 영향력 < 30% → 구현 drift 불가피

#### 2. Permission Interrupt Cascade
**문제**:
- 파일 수정마다 permission 요청
- 5번째 인터럽트쯤 구현 전략 상실
- 각 재시작마다 미묘하게 다른 context 로드 → 큰 아키텍처 위반으로 연쇄

#### 3. Agent Collision Syndrome
**혼란 상황**:
- Agent A: DB 스키마 리팩토링
- Agent B: 구 스키마 기준 쿼리 작성
- Agent C: Agent B 가정 기반 API 업데이트
- 결과: 지수적으로 증가하는 호환 불가능한 구현

### 4-Layer Orchestra Architecture

#### Layer 1: Orchestrator Agent (절대 코드 작성 안 함)

**역할**: 복잡한 요청 분해 + 전문가 조율

```yaml
---
name: orchestrator
description: 다중 파일 작업 시 필수 사용
---

절대 코드를 작성하지 않는 순수 orchestration agent
책임:
1. 복잡도 및 의존성 분석
2. 원자적/병렬 가능 작업으로 분해
3. 적절한 전문가에게 할당
4. 진행 모니터링 및 Agent 간 의존성 처리
5. 결과를 일관된 결과물로 합성
```

**효과**: 아키텍처 플랜이 context window 앞쪽에서 최대 영향력 유지

#### Layer 2: Context Management System

**핵심 개념**: 각 subagent가 자체 context에서 작동 → 메인 대화 오염 방지

```python
class AgentContextHub:
    def __init__(self):
        self.project_state = {
            'architecture': {},    # 고수준 결정
            'dependencies': {},    # Agent 간 의존성
            'completions': {},     # 완료 작업
            'interfaces': {},      # 계약 정의
            'conflicts': []        # 발견된 불일치
        }
```

**토큰 절감**: 60~70% 감소하면서 아키텍처 일관성 유지

#### Layer 3: Specialized Execution Agents

**전문화의 이점**:
- Backend Specialist: Node.js 20+, Express, PostgreSQL, Prisma만 집중
- Frontend Specialist: React 18+, TypeScript, Tailwind만 집중

**Context 격리 사례**:
```bash
# Specialist가 받는 최소 context
claude --agent backend-specialist \
  --context-from hub:interfaces \
  --task "WebSocket 연결 핸들러 구현"

# Context 구성:
# - 인터페이스 정의: 300 토큰
# - 프로젝트 규칙: 200 토큰
# - 특정 작업 요구사항: 150 토큰
# 총 650 토큰 vs 전체 프로젝트 context 15,000+ 토큰
```

#### Layer 4: Integration Validation Layer

**자동 검증**:
- 타입 시그니처 일치 검사
- API 계약 검증
- Race condition 탐지
- 동기화 누락 지점 제안

### 실제 구현: WebSocket 시스템 3일 완성

**전통적 방식**: 시니어 개발자 1명, 2~3주, 지속적인 context switching

**Orchestrated 방식**: 개발자 2명 + agent orchestra, 3일, zero 아키텍처 drift

#### Day 1: 아키텍처 및 병렬 구현

**6개 Agent 동시 작업**:

**Track 1 - Backend (3 agents)**:
- WebSocket server (room 관리)
- PostgreSQL schema (문서, 작업, presence)
- Redis pub/sub (작업 브로드캐스팅)

**Track 2 - Frontend (2 agents)**:
- React 협업 에디터 (OT 엔진)
- Redux store (작업 및 presence)

**Track 3 - Algorithm (1 agent)**:
- Operational transformation merge

#### Day 2: 통합 및 테스트

**Integration Validator 발견 3가지 이슈**:
1. 타입 불일치: `userId: string` vs `user_id: number`
2. Race condition: 동시 작업이 문서 상태 손상 가능
3. 누락된 에러 핸들러: WebSocket 재연결 미구현

**자동 수정 제안 및 적용**

#### Day 3: 성능 최적화

**Performance Specialist 최적화**:
- 작업 배칭 (매 키 입력 → 100ms 간격) → 70% 메시지 감소
- WebSocket 압축 → 60% 대역폭 감소
- Connection pooling → 45ms 지연 개선

**최종 지표**:
- 평균 지연: 47ms (요구사항: <100ms) ✓
- 동시 사용자: 100+ 테스트 (요구사항: 50+) ✓
- 테스트 커버리지: 92%, 147 테스트 케이스 ✓
- 아키텍처 drift: Zero ✓

### Advanced Orchestration Patterns

#### 1. Wave-Based Deployment
**개념**: Context 한계를 관리하면서 병렬성 유지

```python
class WaveOrchestrator:
    def deploy_waves(self, tasks):
        # Context budget 기반 작업 배치
        # Wave 1: 핵심 인프라
        # Wave 2: 비즈니스 로직
        # Wave 3: UI 및 통합
```

#### 2. Progressive Context Summarization
**장기 세션 대응**:
- 구현 세부사항 → 인터페이스만 압축
- 디버깅 세션 → 최종 수정만 압축
- 탐색 과정 → 결정사항만 압축

#### 3. Agent Lifecycle Management
**Spawn 조건**: 
- 복잡도 > 5 파일
- 병렬 작업 가능
- 전문성 필요

**Terminate 조건**:
- 3회 연속 잘못된 제안
- Context 사용량 > 85% + 품질 저하
- 순환 수정 감지 (A→B→A 패턴)

## 💡 시사점 및 인사이트

### 내게 주는 교훈

**Context는 제한된 자원**: 토큰은 무한하지 않음. 전략적 배분 필요

**Orchestration ≠ 더 많은 Agent**: 아키텍처 무결성을 유지하면서 구현을 병렬화하는 것

**복잡도 한계선 존재**:
- 단일 Agent: 10~15 파일 수정이 한계
- Orchestrated: 50+ Agent로 전체 앱 재작성 가능

**토큰 경제학**:
- 단일 Agent: 500,000+ 토큰 (부분 성공)
- Orchestrated: 110,000 토큰 (완전 성공)
- 효율 개선: 78% 토큰 절감 + 100% 완료율

### 업무 적용 가능성

**Qraft 데이터 플랫폼 개발**:
1. **Orchestrator**: 복잡한 DBT 마이그레이션 분해
2. **Context Hub**: Airflow DAG 간 의존성 관리
3. **Specialist Agents**: Snowflake/DBT/Airflow 각각 전문 Agent
4. **Integration Validator**: 데이터 계약 자동 검증

**마이크로서비스 마이그레이션 사례**:
- 전통적 시도: 3일 만에 347개 충돌 커밋, 아키텍처 혼란
- Orchestrated: 4일 만에 완료 (예상 3주)
  - 12 agents 병렬 작업
  - 94% 테스트 커버리지
  - Zero breaking changes

### 의문점 & 추가 탐구

- **한국어 프로젝트**: 한글 주석/문서에서 Context 관리 효율은?
- **데이터 파이프라인**: DBT 모델 수백 개 동시 관리 시 Wave 전략은?
- **비용 분석**: 토큰 절감 vs API 호출 증가 trade-off

## 🔗 관련 자료

- **GitHub**: [claude-code-tresor](https://github.com/alirezarezvani/claude-code-tresor)
- **관련 아티클**: Multi-Agent Orchestration, Context Management
- **관련 기술**: Claude Code, Agent Architecture, Context Window Optimization

---

## 📎 Related

### 실제 적용 사례 (같은 시기)
**2025년 12월 - 크래프트테크놀로지스 MCP 구축**
- [[30-Flow/Life-Insights/Personal/MCP-아키텍처와-데이터-거버넌스-최적화|MCP 아키텍처 인사이트]] (2025-12-02)
  - 이 아티클의 4-Layer Orchestra 개념을 **실제로 적용**한 사례
  - 토큰 사용량 폭발 문제 → 중앙 Orchestrator Agent로 해결
  - dbt/Airflow/DataHub 전문 Agent 구조 → Layer 3 Specialist 패턴 적용
  - 계층적 위임 아키텍처 Mental Model 형성

### Projects
- 크래프트테크놀로지스 MCP 환경 구축 (예정)
- LSEG CDC 프로젝트 (예정)

### Knowledge
- Claude Code Orchestrator 아키텍처
- Multi-agent 패턴
- Context Management 전략
