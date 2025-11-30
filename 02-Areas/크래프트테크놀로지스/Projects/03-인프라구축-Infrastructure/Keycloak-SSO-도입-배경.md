---
title: Keycloak SSO 도입 배경
type: project-background
tags:
  - qraft
  - keycloak
  - sso
  - authentication
  - project
company: 크래프트테크놀로지스
period: 2025-10 ~ 2025-11
status: completed
created: '2025-11-30'
updated: '2025-11-30'
---
# Keycloak SSO 도입 배경

## 📋 프로젝트 개요

**기간**: 2025년 10월 ~ 2025년 11월  
**담당**: ML Platform Infrastructure Team  
**목적**: 데이터 플랫폼 전체의 통합 인증 체계 구축

## 🎯 도입 배경

### 기존 문제점

#### 1. 플랫폼별 계정 관리의 혼란

**상황 (2025년 9월):**
크래프트테크놀로지스에서 운영하는 데이터 플랫폼:
- Airflow (DAG 관리)
- DataHub (메타데이터 관리)
- Superset (BI 대시보드)
- Jupyter Hub (노트북)
- GitLab (코드 관리)

**문제:**
```
사용자당 5개의 계정 관리:
- Airflow: airflow_user1 / password1
- DataHub: datahub_user1 / password2
- Superset: superset_user1 / password3
- Jupyter Hub: jupyter_user1 / password4
- GitLab: gitlab_user1 / password5
```

**실제 불편 사례:**
1. **신규 팀원 온보딩:**
   - 5개 플랫폼 × 계정 생성 = 1시간 소요
   - 각 플랫폼별 비밀번호 전달 (Slack DM) → 보안 위험

2. **퇴사자 계정 삭제:**
   - 5개 플랫폼에서 일일이 삭제
   - 종종 누락 발생 → 보안 위험

3. **비밀번호 분실:**
   - 사용자: "어느 플랫폼 비밀번호인지 기억 안 나요"
   - 관리자: 5곳 모두 리셋

#### 2. 권한 관리의 어려움

**팀별 접근 제어 요구사항:**

크래프트테크놀로지스 조직 구조:
```
Financial Markets Division
├── Strategy Team        # 주식 전략
├── HFT Team            # 고빈도 거래
└── MFT Team            # 멀티팩터

AI & ML Division
├── ML Platform Team    # 데이터 인프라
└── AI Product Team     # AI 제품 개발
```

**기존 문제:**
```python
# Airflow: DAG 파일 소유권으로 제어 (팀별 구분 불가)
# DataHub: Owner 수동 할당 (자동화 불가)
# Superset: Role 기반 (팀 개념 없음)
```

**실제 사고 사례 (2025년 9월):**
- Strategy 팀원이 HFT DAG 실수로 수정
- 원인: Airflow에서 팀별 접근 제어 불가
- 영향: HFT 데이터 파이프라인 1시간 중단

#### 3. 감사 로그 부재

**규제 요구사항:**
- 금융 데이터 사용 이력 추적 필요
- "누가, 언제, 무엇을" 했는지 기록

**기존 문제:**
```
Q: "Strategy 팀의 홍길동님이 11월 15일에 어떤 데이터를 조회했나요?"
A: "알 수 없습니다. 각 플랫폼 로그를 일일이 확인해야 합니다."

- Airflow 로그: DAG 실행 기록만 (사용자 정보 부정확)
- DataHub 로그: 조회 이력 없음
- Superset 로그: 쿼리 실행 기록만
```

### 비즈니스 요구사항

#### 1. 빠른 온보딩/오프보딩

**목표:**
- 신규 팀원 온보딩: 1시간 → **5분**
- 퇴사자 오프보딩: 1시간 → **즉시**

**인사팀 요청사항:**
- "Flex(인사 시스템)에서 입사/퇴사 처리 시 자동으로 계정 생성/삭제"

#### 2. 팀별 데이터 격리

**CFO 요청사항 (2025년 9월):**
- "각 팀은 자기 팀 DAG만 볼 수 있어야 합니다"
- "Strategy 팀 데이터를 HFT 팀이 볼 수 없어야 합니다"

**구체적 시나리오:**
```
Strategy 팀:
- DAG: strategy_* (접근 가능)
- DAG: hft_* (접근 불가)
- Dataset: STRATEGY.* (접근 가능)
- Dataset: HFT.* (접근 불가)

ML Platform 팀 (Admin):
- 모든 DAG 접근 가능
- 모든 Dataset 접근 가능
```

#### 3. 보안 강화

**CTO 요청사항:**
- MFA (Multi-Factor Authentication) 도입
- 비밀번호 정책 강화 (12자 이상, 특수문자 포함)
- 세션 타임아웃 (1시간)

## 💡 해결 방안: Keycloak SSO

### 왜 Keycloak인가?

**비교 검토 (2025년 10월):**

| 솔루션 | 장점 | 단점 | 선택 |
|--------|------|------|------|
| **Keycloak** | ✅ 오픈소스<br>✅ OIDC/SAML 지원<br>✅ 그룹 기반 권한<br>✅ Self-hosted | ❌ 초기 설정 복잡 | ✅ **선택** |
| Okta | ✅ SaaS (관리 불필요)<br>✅ 엔터프라이즈 기능 | ❌ 월 $5/user (60명 = $300/월)<br>❌ 벤더 종속 | ❌ |
| Auth0 | ✅ 개발자 친화적<br>✅ 빠른 통합 | ❌ 월 $240 (10,000 MAU 기준)<br>❌ 비싼 Add-on | ❌ |
| AWS Cognito | ✅ AWS 통합<br>✅ 저렴 | ❌ 그룹 기능 제한적<br>❌ OIDC 설정 복잡 | ❌ |
| 자체 구현 | ✅ 완전한 제어 | ❌ 개발 시간 3개월<br>❌ 유지보수 부담 | ❌ |

**선택 이유:**
1. **비용**: 오픈소스 (무료)
2. **유연성**: 그룹 기반 권한 매핑 지원
3. **표준**: OIDC 표준 준수 → 모든 플랫폼과 통합 가능
4. **Self-hosted**: 금융 데이터 외부 유출 방지

### 구현 방식

**Keycloak 구조:**
```
Keycloak Server
├── Realm: qraft
│   ├── Users (Flex에서 동기화)
│   ├── Groups
│   │   ├── ml-platform-admin (Admin)
│   │   ├── Strategy (T)
│   │   ├── HFT (T)
│   │   ├── MFT (T)
│   │   └── ...
│   └── Clients
│       ├── airflow-web (OIDC)
│       ├── datahub (OIDC)
│       └── airflow-service-account (Service Account)
```

**통합 방식:**

1. **Airflow:**
   - Custom Auth Manager 개발
   - Keycloak 그룹 → Airflow 역할 자동 매핑
   - DAG `team:` 태그와 그룹 매칭

2. **DataHub:**
   - OIDC SSO 설정
   - JIT Provisioning (최초 로그인 시 자동 계정 생성)
   - Owner 기반 접근 제어

3. **Service Account:**
   - Airflow → DataHub API 호출 시 사용
   - Client Credentials Flow

## 📊 도입 효과

### Before vs After

| 지표 | Before | After | 개선율 |
|------|--------|-------|--------|
| **계정 수 (사용자당)** | 5개 | 1개 | **-80%** |
| **온보딩 시간** | 1시간 | 5분 | **-92%** |
| **오프보딩 시간** | 1시간 | 즉시 | **-100%** |
| **비밀번호 분실 문의** | 월 15건 | 월 0건 | **-100%** |
| **팀별 DAG 격리** | 불가 | 가능 | ✅ |
| **감사 로그** | 부분적 | 통합 | ✅ |

### 구체적 개선 사례

#### 사례 1: 신규 팀원 온보딩

**Before (2025년 9월):**
```
1. 인사팀 → ML Platform 팀에 Slack 메시지
2. ML Platform 팀: 5개 플랫폼 계정 생성 (30분)
3. 각 플랫폼별 비밀번호 Slack DM 전달 (15분)
4. 신규 팀원: 5개 플랫폼 로그인 및 비밀번호 변경 (15분)
총 1시간 소요
```

**After (2025년 11월):**
```
1. 인사팀: Flex에서 입사 처리
2. Flex → Keycloak 자동 동기화 (Webhook)
3. 신규 팀원: Keycloak 로그인 → 모든 플랫폼 SSO
총 5분 소요
```

#### 사례 2: 팀별 DAG 격리

**Before:**
```python
# Strategy 팀원도 HFT DAG 수정 가능
# → 실수로 수정 → 장애 발생
```

**After:**
```python
# DAG 정의
@dag(
    dag_id="hft_futures_arbitrage",
    tags=["team:HFT (T)", ...]
)

# Airflow Auth Manager가 자동 체크
def is_authorized_dag(user, dag_id):
    required_team = "HFT (T)"  # DAG tag에서 추출
    user_groups = ["Strategy (T)"]  # Keycloak에서 조회
    
    return required_team in user_groups  # False → 접근 거부
```

**결과:**
- Strategy 팀원: HFT DAG **UI에서 보이지 않음**
- 실수로 수정 불가능

#### 사례 3: 퇴사자 계정 즉시 삭제

**Before:**
```
퇴사자 A씨 (2025년 9월 25일 퇴사)
- 9월 27일: Airflow 계정 아직 활성화
- 10월 2일: GitLab 계정 아직 활성화
- 보안팀 지적: "즉시 삭제하세요"
```

**After:**
```
퇴사자 B씨 (2025년 11월 15일 퇴사)
- 11월 15일 17:00: Flex에서 퇴사 처리
- 11월 15일 17:01: Keycloak 계정 비활성화 (Webhook)
- 11월 15일 17:01: 모든 플랫폼 즉시 로그아웃
```

## 🚨 도입 과정의 시행착오

### 시행착오 1: Flex 동기화 실패

**문제 (2025년 10월):**
- Flex API 연동 → Keycloak 사용자 동기화 실패
- 원인: Flex API Rate Limit (1req/sec)
- 증상: 60명 동기화 → 60초 소요, 종종 타임아웃

**해결:**
```python
# Before: 순차 처리
for user in flex_users:
    keycloak.create_user(user)  # 1초씩 걸림

# After: Batch API 사용
keycloak.batch_create_users(flex_users)  # 한번에 처리
```

**교훈:**
- 외부 API 연동 시 Rate Limit 사전 확인 필수

### 시행착오 2: 그룹명 불일치

**문제:**
```
Flex: "ML Platform"
Keycloak: "ML Platform (T)"  # (T)는 Team 의미
Airflow DAG tag: "team:ML Platform (T)"

→ 불일치로 권한 매핑 실패
```

**해결:**
1. **Flex → Keycloak 동기화 시 자동 변환:**
```python
def sync_flex_to_keycloak():
    flex_team = "ML Platform"
    keycloak_group = f"{flex_team} (T)"  # (T) 자동 추가
```

2. **DAG 컨벤션 문서화:**
```markdown
# convention-dag.md
- team 태그는 Flex 공식 팀명 + " (T)" 필수
- 예: "team:ML Platform (T)"
- 대소문자, 공백, 괄호 모두 정확히 일치해야 함
```

### 시행착오 3: 사용자 저항

**문제 (2025년 10월 초):**
- 기존 사용자: "새로운 로그인 방식 불편해요"
- "이전처럼 Airflow 직접 로그인하면 안 되나요?"

**해결:**
1. **점진적 마이그레이션:**
   - 1주차: ML Platform 팀만 (5명)
   - 2주차: Strategy 팀 추가 (10명)
   - 3주차: 전체 적용 (60명)

2. **교육 자료 제공:**
   - Confluence: "Keycloak SSO 사용 가이드"
   - Slack 공지: "1계정으로 모든 플랫폼 접근 가능"
   - 비디오 튜토리얼 (2분)

3. **피드백 수렴:**
   - Slack 채널: #data-platform-feedback
   - 개선 사항 즉시 반영

**결과:**
- 3주 후: 사용자 만족도 85% → "편리하다"

## 🔗 관련 문서

### 기술 문서
- [[Keycloak-OIDC-인증]] - 기술 구현 상세

### 프로젝트 문서
- [[qraft-data-platform-통합프로젝트]] - 전체 프로젝트 개요
- [[통합-인증-체계-구축]] - SSO 프로젝트 전체

### 기술 스택
- [[Keycloak]] - Keycloak 개념
- [[OIDC]] - OIDC 프로토콜

---

**작성일**: 2025-11-30
**담당자**: ML Platform Infrastructure Team
**상태**: ✅ 완료 (운영 중)
