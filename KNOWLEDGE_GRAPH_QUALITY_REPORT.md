---
tags:
  - meta
  - vault-health
  - connection-analysis
  - knowledge-graph
type: meta
report-date: 2025-11-30
status: active
created: 2025-11-30
updated: 2025-11-30
---

# 🔗 세컨드 브레인 지식 그래프 품질 리포트

**생성일**: 2025-11-30
**전체 노트**: 593개
**전체 연결**: 992개

---

## 📊 현재 상태 요약

### 🔴 심각한 문제
| 지표 | 현재 | 목표 | 상태 |
|------|------|------|------|
| **Orphan 노트** | **379개 (64%)** | <10% | 🔴 위험 |
| **평균 연결수** | **1.7개/노트** | >5개 | 🔴 위험 |
| **Experience→Knowledge 연결** | **0%** | >50% | 🔴 위험 |
| **Experience→Project 연결** | **0%** | >30% | 🔴 위험 |

### ✅ 잘 되고 있는 것
- Hub 노트들은 평균 30+ 연결로 잘 작동 중
- qraft-data-platform-통합프로젝트: 32개 연결
- 태그 시스템: 100% 특이성 달성

---

## 🎯 개선 로드맵

### Phase 1: 긴급 개선 (1개월)
**목표**: Orphan 노트 64% → 30%

**액션 플랜**:
1. **Life-Insights Hub 생성** (Week 1)
   - Personal-Hub.md 생성
   - Work-Hub.md 생성
   - Observations-Hub.md 생성
   - 각 Hub에 10-20개 핵심 인사이트 연결

2. **주제별 클러스터 연결** (Week 2-3)
   - 같은 태그 가진 노트끼리 연결
   - "family" 태그: 20개 → 서로 연결
   - "work" 태그: 136개 → 주제별 그룹화
   - "reflection" 태그: 185개 → 시기별 그룹화

3. **Weekly Reflection → Project 연결** (Week 4)
   - 각 주간 회고에서 언급된 프로젝트 찾기
   - 날짜 기반 자동 매칭
   - Related 섹션에 프로젝트 링크 추가

**예상 결과**:
- Orphan: 379개 → 150개 (60% 개선)
- 평균 연결: 1.7개 → 3.5개

### Phase 2: 구조화 (2-3개월)
**목표**: Experience-Project 연결 30% 달성

**액션 플랜**:
1. **프로젝트-회고 매핑**
   - 각 프로젝트에 "관련 회고" 섹션 추가
   - 주간 회고에 "관련 프로젝트" 섹션 추가
   - 시간 기반 자동 연결 스크립트 실행

2. **인사이트-프로젝트 연결**
   - 각 인사이트에서 언급된 프로젝트 찾기
   - 프로젝트에서 얻은 인사이트 백링크

**예상 결과**:
- Experience→Project: 0% → 30%
- 평균 연결: 3.5개 → 5개

### Phase 3: 지식 통합 (4-6개월)
**목표**: Experience-Knowledge 연결 50% 달성

**액션 플랜**:
1. **기술 문서 실제 사용 사례 추가**
   - Airflow 문서 → 관련 프로젝트 링크
   - DBT 문서 → 실제 적용 사례
   - Snowflake 문서 → 트러블슈팅 경험

2. **프로젝트-기술 매핑**
   - 각 프로젝트에서 사용한 기술 명시
   - Technology 폴더 문서와 양방향 연결

**예상 결과**:
- Experience→Knowledge: 0% → 50%
- Orphan: 150개 → 60개 (<10%)
- 평균 연결: 5개 → 7개

---

## 🛠️ 구축된 도구

### 1. Connection Curator Agent
**위치**: `.claude/agents/connection-curator.md`
**기능**: 연결성 분석 및 개선 가이드

### 2. 분석 스크립트
**위치**: `.claude/scripts/`
- `analyze_connections.py` - 전체 연결성 분석
- `suggest_connections.py` - 지능형 연결 제안
- `weekly_connection_review.sh` - 주간 리뷰 자동화

**실행 방법**:
```bash
cd /Users/qraft_hongjinyoung/Second-Brain
./.claude/scripts/weekly_connection_review.sh
```

### 3. 품질 지표 추적
**자동 생성 파일**:
- `/tmp/connection_analysis.json` - 연결성 분석 데이터
- `/tmp/connection_suggestions.json` - 연결 제안 데이터
- `.claude/reports/connection_analysis_YYYYMMDD.txt` - 주간 리포트

---

## 📋 주간 리뷰 프로세스

### 매주 일요일 저녁 (30분)

#### 1. 자동 분석 실행 (5분)
```bash
./.claude/scripts/weekly_connection_review.sh
```

#### 2. Orphan 노트 연결 (15분)
- 이번 주 작성한 Orphan 노트 확인
- 최소 5개 노트에 연결 추가
- 관련 Hub 노트와 연결

#### 3. Weekly Reflection 정리 (10분)
- 이번 주 회고에 프로젝트 링크 추가
- 사용한 기술 문서 링크 추가
- 얻은 인사이트 링크 추가

#### 체크리스트:
- [ ] 자동 분석 실행 완료
- [ ] Orphan 노트 5개 이상 연결
- [ ] Weekly reflection에 최소 2개 프로젝트 링크
- [ ] 이번 주 작성한 모든 노트에 최소 2개 연결
- [ ] 연결성 지표 확인 (개선 여부)

---

## 🎯 즉시 실행 가능한 개선 (Quick Wins)

### 1. Hub 노트 생성 (30분)
**즉시 만들 Hub**:
- `30-Flow/Life-Insights/Personal-Hub.md` - 개인 인사이트 중앙
- `30-Flow/Life-Insights/Work-Hub.md` - 업무 인사이트 중앙
- `30-Flow/Life-Insights/Observations-Hub.md` - 관찰 중앙

**각 Hub 구조**:
```markdown
# {주제} Hub

## 핵심 인사이트
- [[인사이트1]]
- [[인사이트2]]
...

## 주제별 분류
### 가족
- [[가족 관련 인사이트1]]
...

### 건강
- [[건강 관련 인사이트1]]
...
```

### 2. 가장 많이 사용된 태그 노트들 연결 (1시간)
- `reflection` (185개) → 시기별로 그룹화하여 연결
- `work` (136개) → 회사별, 프로젝트별 그룹화
- `action-item` (118개) → 실행 여부로 그룹화

### 3. 최근 Weekly Reflection에 프로젝트 링크 추가 (30분)
- 2025년 11월 24일 → qraft-data-platform-통합프로젝트
- 2025년 11월 17일 → DataHub-커스텀-구현-상세
- 2025년 11월 10일 → 관련 프로젝트 찾아 연결

---

## 📈 성공 지표 추적

### 월간 목표

| 월 | Orphan | 평균 연결 | Exp→Proj | Exp→Know |
|----|--------|-----------|----------|----------|
| **현재 (11월)** | 64% | 1.7개 | 0% | 0% |
| 12월 목표 | 30% | 3.5개 | 10% | 5% |
| 1월 목표 | 20% | 5.0개 | 20% | 15% |
| 2월 목표 | 15% | 6.0개 | 25% | 30% |
| 3월 목표 | <10% | 7.0개 | 30% | 50% |

### 진척도 측정 방법
```bash
# 매월 1일 실행
cd /Users/qraft_hongjinyoung/Second-Brain
./.claude/scripts/analyze_connections.py > monthly_report_$(date +%Y%m).txt
```

---

## 💡 장기 비전: 지식 그래프 완성

### 이상적인 구조
```
Experience (회고/인사이트)
    ↓ ↑
Project (프로젝트)
    ↓ ↑
Knowledge (기술문서)
    ↓ ↑
Insights (깨달음)
```

### 완성된 세컨드 브레인의 모습
- **모든 노트가 최소 3개 이상 연결**
- **경험→지식→프로젝트가 유기적으로 연결**
- **검색 시 관련 노트 즉시 발견**
- **과거 경험을 현재 문제 해결에 활용**
- **지식이 단순 저장이 아닌 네트워크로 작동**

---

## 🚀 다음 액션

### 이번 주 (필수)
1. [ ] Hub 노트 3개 생성 (Personal, Work, Observations)
2. [ ] Orphan 노트 10개 연결
3. [ ] 최근 3주 Weekly Reflection에 프로젝트 링크 추가

### 이번 달 (권장)
1. [ ] 주간 리뷰 프로세스 정착 (매주 일요일)
2. [ ] Orphan 노트 50% 감소
3. [ ] 모든 프로젝트에 Related 섹션 보완

### 장기 (지속)
1. [ ] 매달 연결성 지표 추적
2. [ ] 새 노트 작성 시 최소 2개 연결 습관화
3. [ ] 분기별 전체 구조 리뷰

---

**작성자**: Claude (Connection Curator Agent)
**마지막 업데이트**: 2025-11-30
**다음 리뷰 예정**: 2025-12-08 (매주 일요일)

---

## 📎 Related

### Agent Documentation (연결 큐레이션 시스템)
이 리포트는 Connection Curator Agent의 실행 결과이며, 4-step connection principle에 따라 작성되었습니다:
- [[.claude/agents/knowledge__connection-curator.md]]
  - 이 agent가 vault의 연결성을 분석하고 개선 제안을 생성
  - 100% bidirectional links + context-rich connections 목표
- [[.claude/conventions/knowledge/connection-quality.md]]
  - READ FIRST → CHECK TIMELINE → COMPANY PERIOD → ADD CONTEXT
  - 이 리포트의 품질 기준이 이 convention을 따름

### Companion Research (같은 날 작성)
- [[RESEARCH_REPORT_PKM_STRUCTURE.md]] (2025-11-30, 같은 날)
  - 이 리포트는 연결 품질 분석, 위 문서는 구조 개선 제안
  - 두 문서가 함께 vault 개선의 양대 축 (연결 + 구조)

### Weekly Context (리포트 작성 시점)
- [[02-Areas/크래프트테크놀로지스/Experience/Weekly/2025년 11월 24일.md]]
  - 이 주간 회고 직후 vault 전체 분석 수행
  - Orphan 노트 64% 문제를 처음 발견한 시점

### Implementation Status (실행 결과)
현재 이 리포트의 개선 계획은 **제안 단계**입니다:
- Phase 1 (긴급 개선): 미실행
- Hub 노트 생성: 미실행
- Weekly connection 추가: 부분 실행 (일부 노트만)
- 다음 액션: Orchestrator를 통한 체계적 실행 필요
