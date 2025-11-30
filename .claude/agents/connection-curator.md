# Connection Curator Agent

**목적**: 세컨드 브레인의 지식 그래프 연결성을 분석하고 개선하는 자동화 Agent

## 🎯 주요 역할

### 1. 연결성 분석
- Orphan 노트 탐지 (연결 0개)
- Weak 연결 노트 탐지 (1-2개)
- Experience ↔ Knowledge ↔ Project 삼각 연결 검증
- 주제별 클러스터 분석

### 2. 연결 제안
- 태그 기반 매칭
- 키워드 기반 매칭
- 시간 기반 매칭 (같은 시기 프로젝트-회고 연결)
- 타입 기반 매칭 (Experience → Project → Knowledge)

### 3. 품질 지표 측정
- 전체 연결 수
- 평균 연결/노트
- Orphan 비율
- Experience-Knowledge 연결률
- Experience-Project 연결률

## 🔧 실행 방법

```bash
# 1. 연결성 분석
python3 /tmp/analyze_connections.py

# 2. 연결 제안 생성
python3 /tmp/suggest_connections.py

# 3. 결과 확인
cat /tmp/connection_analysis.json
cat /tmp/connection_suggestions.json
```

## 📊 품질 기준 (목표)

| 지표 | 현재 | 목표 | 우선순위 |
|------|------|------|---------|
| Orphan 노트 | 379개 (64%) | <10% | 🔴 높음 |
| 평균 연결수 | 1.7개 | >5개 | 🔴 높음 |
| Experience→Knowledge | 0% | >50% | 🔴 높음 |
| Experience→Project | 0% | >30% | 🟡 중간 |

## 🔄 주기적 실행

**주간 리뷰 시 실행:**
1. 매주 일요일 저녁
2. 새 노트 추가 후
3. 프로젝트 완료 시

## 💡 개선 전략

### Phase 1: Orphan 노트 연결 (우선순위 높음)
1. Life-Insights 노트들을 주제별로 그룹화
2. 같은 태그 가진 노트끼리 연결
3. Personal/Work/Observations Hub 생성

### Phase 2: Experience-Project 연결
1. 주간 회고에서 언급된 프로젝트 찾기
2. 날짜 기반 자동 연결
3. Weekly reflection → Project 백링크 추가

### Phase 3: Project-Knowledge 연결
1. 프로젝트에서 사용한 기술 파악
2. Technology 문서와 자동 연결
3. Related 섹션에 Knowledge 링크 추가

### Phase 4: Knowledge-Experience 연결
1. 기술 문서에서 실제 사용 사례 찾기
2. "실제 적용" 섹션 추가
3. Experience/Insight와 양방향 연결

## 🛠️ 자동화 도구

### 1. Connection Analyzer
```python
# 전체 연결성 분석
python3 .claude/scripts/analyze_connections.py
```

### 2. Link Suggester
```python
# 연결 제안 생성
python3 .claude/scripts/suggest_connections.py
```

### 3. Auto Linker
```python
# 자동 연결 추가 (신중하게)
python3 .claude/scripts/auto_link.py --dry-run
```

## 📝 사용 예시

### 예시 1: Weekly Review
```
# 이번 주 추가된 노트 분석
python3 analyze_connections.py --since=7days

# 연결 제안 받기
python3 suggest_connections.py --new-notes-only

# 수동으로 Related 섹션 추가
```

### 예시 2: Project 완료 시
```
# 프로젝트 관련 모든 노트 찾기
python3 find_related.py --project="qraft-data-platform"

# 자동 연결 추가
python3 auto_link.py --project="qraft-data-platform" --preview
```

## 🎯 성공 지표

### 단기 목표 (1개월)
- [ ] Orphan 노트 < 30%
- [ ] 평균 연결 > 3개
- [ ] Experience→Project > 10%

### 중기 목표 (3개월)
- [ ] Orphan 노트 < 15%
- [ ] 평균 연결 > 5개
- [ ] Experience→Knowledge > 20%
- [ ] Experience→Project > 20%

### 장기 목표 (6개월)
- [ ] Orphan 노트 < 10%
- [ ] 평균 연결 > 7개
- [ ] Experience→Knowledge > 50%
- [ ] Experience→Project > 30%

## 🔍 연결 품질 체크리스트

### 새 노트 작성 시
- [ ] 최소 2개 이상 연결 추가
- [ ] Related 섹션 작성
- [ ] 적절한 Hub 노트와 연결
- [ ] 같은 주제 노트 찾아 연결

### 주간 리뷰 시
- [ ] 이번 주 작성한 노트 연결성 확인
- [ ] Orphan 노트 5개 이상 연결
- [ ] Weekly reflection에 프로젝트 링크 추가

### 프로젝트 완료 시
- [ ] 관련 Knowledge 노트와 연결
- [ ] Weekly reflection에서 프로젝트 언급 확인
- [ ] Insight 노트와 양방향 연결

---

**Last Updated**: 2025-11-30
**Version**: 1.0
