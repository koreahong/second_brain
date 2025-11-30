---
tags:
- anger
- pipeline
- achievement
- data
- datahub
- dbt
- project
- goal
created: '2025-11-30'
updated: '2025-11-30'
title: SECOND_BRAIN_AGENT_SYSTEM
aliases: []
---
# Second Brain Agent System Design

> 세컨드 브레인 전문가 관점에서 설계한 8-Agent 시스템  
> **설계일**: 2025-11-29  
> **버전**: 1.0  
> **기반**: PARA + Zettelkasten + CODE 사이클

---

## 🎯 설계 철학

### 핵심 원칙

**"Capture Everything, Organize Effortlessly, Connect Meaningfully, Express Confidently"**

1. **CODE 사이클**: Collect → Organize → Distill → Express
2. **워크플로우**: Capture → Clarify → Connect → Create
3. **품질 기준**: 노트당 평균 **8+ links**, atomic notes, evergreen status
4. **자동화 우선**: 인지 부하 최소화, 일관성 유지

### 연구 기반 목표

- **Knowledge Growth**: 주 5-10개 새 노트
- **Network Density**: 평균 8+ links per note
- **Retrieval Speed**: 30초 이내
- **Evergreen Ratio**: 30% 이상
- **Orphan Rate**: 5% 이하

---

## 🤖 8개 핵심 Agent

### 1. 📥 Capture Agent (포착 Agent)

**슬로건**: "모든 아이디어를 놓치지 않는다"

#### 책임
- Fleeting Notes 즉시 생성
- Daily Note에 빠른 추가
- 컨텍스트 자동 캡처 (시간, 위치, 관련 프로젝트)
- 임시 저장소(00-Inbox/) 관리

#### 트리거
- `/capture [내용]` 명령어
- Daily Note 작성 시 자동 지원
- 회의/작업 중 빠른 메모

#### 워크플로우
```
사용자 아이디어 발생
    ↓
Capture Agent 활성화
    ↓
Fleeting Note 생성 (템플릿 기반)
    ↓
00-Inbox/ 저장 + Daily Note 링크
    ↓
24시간 내 정리 알림 설정
```

#### 구현 기능
```yaml
Auto-capture:
  - 템플릿 기반 빠른 생성
  - 스크린샷 자동 첨부
  - 관련 프로젝트 자동 태그
  - 시간 기록 (review_by 설정)

Frontmatter:
  type: fleeting
  captured: {{timestamp}}
  context: {{current_project}}
  review_by: {{date+1day}}
  status: inbox
```

#### 예시
```markdown
사용자: "/capture Airflow XCom 1MB 제한 문제 해결 방법 찾음"

Capture Agent:
✅ Fleeting Note 생성: 00-Inbox/2025-11-29-1430-airflow-xcom.md
✅ Daily Note에 링크 추가
✅ #airflow 태그 추가
✅ 내일까지 정리 알림 설정
```

---

### 2. 🗂️ Organizer Agent (정리 Agent)

**슬로건**: "올바른 위치로 모든 것을 정리한다"

#### 책임
- Fleeting → Literature/Permanent 변환
- PARA 구조에 맞게 폴더 이동
- 자동 태그 부여 (기술, 도메인, 타입)
- Frontmatter 표준화

#### 트리거
- `/organize` 명령어
- 일일 정리 시간 (저녁 9시)
- Inbox가 10개 이상일 때 알림

#### 분류 규칙
```yaml
Literature Note:
  조건:
    - 출처 URL 있음
    - "문서", "책", "article" 언급
  위치: 03-Resources/

Permanent Note:
  조건:
    - 독립적 개념
    - 재사용 가능한 지식
    - 하나의 명확한 아이디어
  위치: 10-Zettelkasten/Permanent/

Project Note:
  조건:
    - 목표, 마감일 언급
    - 할 일 목록 포함
  위치: 01-Projects/ or 02-Areas/크래프트/Projects/

Experience Note:
  조건:
    - "회고", "배웠다", "느꼈다"
    - 주차 정보
  위치: 02-Areas/크래프트/Experience/Weekly/
```

#### 워크플로우
```
Fleeting Note (Inbox)
    ↓
콘텐츠 분석 (AI + 키워드)
    ↓
타입 판별 (Literature/Permanent/Project/Experience)
    ↓
이동 + 태그 + Frontmatter 업데이트
    ↓
사용자에게 결과 보고
```

#### 기존 Content Organizer 확장
- ✅ 마이그레이션 데이터 정리 (기존 기능)
- **신규**: 일상적인 노트 정리
- **신규**: 품질 검증 (atomic, clear idea)

---

### 3. 🔗 Linker Agent (연결 Agent)

**슬로건**: "지식 네트워크를 구축한다"

#### 책임
- 모든 노트에 **8+ meaningful links** 확보
- Semantic similarity 기반 추천
- Hub/MOC와 자동 연결
- 양방향 백링크 생성

#### 트리거
- 노트 생성/수정 시 자동
- `/connect [노트]` 명령어
- 주간 리뷰 시 orphan 노트 처리

#### 8+ Links 구성 전략
```yaml
연결 타입별 목표:
  Semantic similarity: 2-3개 (AI embedding)
  Same domain/tags: 2-3개
  Temporal (같은 주): 1-2개
  Hierarchical (Hub): 1개
  Hierarchical (MOC): 1개
  Related project: 1개
  ----------------------
  Total: 8-10개 ✅
```

#### 구현 알고리즘
```python
def auto_link(note):
    connections = []
    
    # 1. Semantic search (AI)
    similar = embedding_search(note.content, top_k=3)
    connections.extend(similar)
    
    # 2. Tag-based
    same_tags = find_by_tags(note.tags, limit=2)
    connections.extend(same_tags)
    
    # 3. Temporal
    same_week = find_by_date_range(note.created, window=7, limit=2)
    connections.extend(same_week)
    
    # 4. Hierarchical
    hub = find_hub(note.domain)
    moc = find_moc(note.domain)
    connections.extend([hub, moc])
    
    # 5. Contextual
    if note.project:
        connections.append(note.project)
    
    # 6. Quality filter
    filtered = [c for c in connections if relevance_score(note, c) > 0.7]
    
    return deduplicate(filtered)[:10]
```

#### 품질 관리
- Random links 방지 (relevance score > 0.7)
- 링크 설명 자동 생성 ("왜 연결되는가")
- 고아 노트(orphan) 주간 알림
- 양방향 백링크 자동 생성

---

### 4. 🌱 Curator Agent (큐레이터 Agent)

**슬로건**: "지식의 품질을 관리한다"

#### 책임
- Status 업그레이드 (seedling → budding → evergreen)
- Orphan 노트 발견 및 연결 촉진
- 품질 기준 검증
- 오래된 노트 재검토 알림

#### 트리거
- 매일 자동 실행 (새벽 6시)
- `/curate` 명령어
- Monthly 회고 시

#### Status 승격 기준
```yaml
Seedling (🌱) → Budding (🌿):
  요구사항:
    - 작성된 지 7일 이상
    - 내용 3단락 이상
    - Links 3개 이상
    - 명확한 아이디어 표현

Budding (🌿) → Evergreen (🌲):
  요구사항:
    - 작성된 지 30일 이상
    - Links 8개 이상
    - 실제 적용 사례 1개 이상
    - 타인이 읽고 이해 가능
    - 재사용 2회 이상
```

#### 일일 큐레이션 워크플로우
```python
def daily_curation():
    # 1. Seedling 검토
    seedlings = get_notes(status="seedling", age_days=7)
    for note in seedlings:
        if qualify_for_budding(note):
            promote(note, "budding")
            notify(f"🌿 {note.title} promoted!")
    
    # 2. Budding → Evergreen
    budding = get_notes(status="budding", age_days=30)
    for note in budding:
        if qualify_for_evergreen(note):
            promote(note, "evergreen")
            celebrate(f"🌲 {note.title} is evergreen!")
    
    # 3. Orphan 노트 발견
    orphans = find_notes(links_count__lt=3)
    if orphans:
        suggest_connections(orphans)
    
    # 4. Wilted 노트 (6개월+ 수정 없음)
    wilted = get_notes(updated__lt=180_days_ago)
    suggest_review(wilted)
```

#### Dashboard 생성
```markdown
# Knowledge Forest Health

🌱 Seedlings: 23개 (promotion 대상: 5개)
🌿 Budding: 45개 (evergreen 후보: 3개)
🌲 Evergreen: 78개
🍂 Wilted: 12개 (재검토 필요)

## 이번 주 성장
- 🌱→🌿: 8개
- 🌿→🌲: 2개

## Orphan Alert
[[노트1]], [[노트2]] - 연결 필요!
```

---

### 5. 💡 Synthesizer Agent (통합 Agent)

**슬로건**: "점을 연결하여 통찰을 만든다"

#### 책임
- MOC (Map of Content) 자동 생성
- Hub Note 업데이트
- 패턴 발견
- 새로운 영구 노트 제안

#### 트리거
- `/synthesize [주제]` 명령어
- 월간 리뷰 시
- 같은 domain 노트 10개 이상 축적 시

#### 워크플로우
```
같은 도메인 노트들 수집
    ↓
클러스터링 (AI)
    ↓
패턴 발견:
  - 공통 주제
  - 반복 키워드
  - 연결 밀도 높은 노드
    ↓
MOC/Hub 생성 또는 업데이트
    ↓
새로운 통찰 제안
```

#### MOC 자동 생성 예시
```markdown
사용자: "/synthesize airflow"

Synthesizer Agent:
✅ Airflow 관련 노트 23개 발견
✅ 3개 클러스터 감지:
   - 기본 개념 (8개)
   - Task 통신 (5개)
   - 고급 패턴 (10개)

✅ MOC 생성: 20-Maps/Airflow-Map.md
✅ Hub Notes 3개 생성
✅ 새로운 통찰 제안: 
   "XCom과 TaskFlow의 공통점" → Permanent Note로?
```

#### 패턴 발견
```yaml
예시 1:
  발견: "Airflow DAG", "DBT model", "Iceberg table"
  공통점: 모두 "선언적 정의" 패턴
  제안: "선언적 vs 명령적 파이프라인" Permanent Note

예시 2:
  발견: "OIDC 구현" 노트 3개 (Keycloak, DataHub, Airflow)
  제안: "OIDC 통합 패턴" Hub Note 생성
```

---

### 6. 📝 Reviewer Agent (회고 Agent)

**슬로건**: "성찰하고 개선한다"

#### 책임
- Daily/Weekly/Monthly 회고 템플릿 제공
- 성과 지표 자동 집계
- 학습 패턴 분석
- 다음 Focus 제안

#### 트리거
- 매일 저녁 9시 (Daily)
- 매주 금요일 (Weekly)
- 매월 마지막 일요일 (Monthly)
- `/review [period]` 명령어

#### Daily 회고 템플릿
```markdown
# {{date}} Daily Review

## 📊 오늘의 통계
- Captured: {{count}}개
- Organized: {{count}}개
- New Links: {{count}}개
- Permanent Notes: {{count}}개

## 🎯 오늘의 Focus
{{active_projects}}

## 💡 배운 것
{{new_permanent_notes}}

## 🔗 만든 연결
{{new_links_today}}

## 🌱 Growing
{{promotions}}

## 📅 내일
{{tomorrow_tasks}}
```

#### Weekly 회고 (자동 집계)
```markdown
# {{year}}-W{{week}} Weekly Review

## 📈 이번 주 성장
- Knowledge Growth:
  - New notes: {{count}}개
  - Permanent notes: {{count}}개
  - Links added: {{count}}개
  - Avg links/note: {{avg}} (목표: 8+)

- Network Health:
  - Orphan notes: {{count}}개
  - Evergreen promoted: {{count}}개

## 🎯 주요 성과
{{top_achievements}}

## 💡 Top Insights
{{top_notes_by_reuse}}

## 🔄 CODE Cycle
- Collect: {{status}}
- Organize: {{status}}
- Distill: {{status}}
- Express: {{status}}

## 📅 다음 주 Focus
{{next_week_goals}}
```

#### Monthly 회고 (장기 트렌드)
```markdown
# {{year}}-{{month}} Monthly Review

## 🌲 Knowledge Forest
- Total Notes: {{count}} (+{{growth}})
- Evergreen: {{count}} (+{{growth}})
- Average Links: {{avg}}

## 📚 Domain Growth
{{domain_statistics_table}}

## 🏆 Most Valuable Notes
{{top_notes_by_reuse_count}}

## 🎯 Goals Achievement
{{goals_vs_actual}}

## 🔮 Next Month Focus
{{next_month_goals}}
```

---

### 7. 🔍 Search Agent (검색 Agent)

**슬로건**: "필요한 지식을 30초 내에 찾는다"

#### 책임
- Semantic search (의미 기반)
- 관련 노트 추천
- Quick jump (자주 찾는 노트)
- Graph navigation

#### 트리거
- `/search [query]` 명령어
- `/find [노트명]`
- `/related [노트]`

#### Multi-modal Search
```yaml
검색 방식:
  1. Semantic (AI embedding)
     - "Airflow에서 큰 데이터 전달하는 법"
     - → [[XCom-S3-패턴]], [[TaskFlow-API]]
  
  2. Tag-based
     - #airflow AND #data-passing
  
  3. Graph traversal
     - "Airflow" 노트에서 2 hops 이내
  
  4. Temporal
     - 최근 7일 내 작성/수정
  
  5. Frequency
     - 최근 자주 열어본 노트
```

#### Quick Jump 예시
```markdown
사용자: "/find airflow xcom"

Search Agent:
🎯 Top Results:
1. [[202511280901|Airflow XCom: S3 패턴]] ⭐️⭐️⭐️⭐️⭐️
   - 재사용: 3회
   - Links: 12개
   - Status: 🌲 Evergreen

2. [[Airflow-공식문서-XCom]] ⭐️⭐️⭐️
   - Type: Literature

3. [[DataHub-OIDC/notes.md]] ⭐️⭐️
   - Context: XCom 언급됨

🔗 Related:
- [[TaskFlow-API]]
- [[S3-데이터-전달]]
```

#### Graph Navigation
```markdown
사용자: "/related [[Airflow-XCom]]"

Search Agent:
🕸️ Network View:

[Airflow-DAG] ← [Airflow-Task] ← [Airflow-XCom] → [S3-패턴]
                                         ↓
                                   [Metadata-DB]

📍 2 hops away:
- [[Iceberg-Table]] (via S3)
- [[DBT-Artifacts]] (via Metadata-DB)

🎯 Suggested exploration:
"XCom과 DBT artifacts 비교" → 새로운 통찰?
```

---

### 8. ✍️ Express Agent (표현 Agent)

**슬로건**: "지식을 가치있는 산출물로 변환한다"

#### 책임
- 블로그 포스트 초안 생성
- 프로젝트 문서 작성
- 발표 자료 구성
- 노트 기반 컨텐츠 생성

#### 트리거
- `/express [주제] as [형식]` 명령어
- 프로젝트 완료 시
- Monthly 회고 후

#### 워크플로우
```
사용자: 주제 선택
    ↓
Express Agent: 관련 노트 수집
    ↓
스토리라인 구성
    ↓
초안 생성
    ↓
피드백 반영
    ↓
최종 산출물
    ↓
새로운 인사이트 → Permanent Note로 환원
```

#### 사용 예시
```markdown
사용자: "/express airflow-xcom-pattern as blog-post"

Express Agent:
✅ 관련 노트 수집:
   - [[202511280901|XCom S3 패턴]]
   - [[Airflow-공식문서-XCom]]
   - [[DataHub-프로젝트]] (실제 사례)

✅ 초안 구성:
   1. 서론: XCom 제한 문제
   2. 본론: S3 패턴 해결책
   3. 실전: DataHub 적용 사례
   4. 결론: 언제 사용할지

✅ 블로그 포스트 초안 생성:
   → 30-Flow/Drafts/airflow-xcom-blog.md

📝 개선 사항 발견:
   "XCom vs S3 성능 비교" 추가 필요
   → 새 Permanent Note 제안
```

#### 산출물 타입
```yaml
Blog Post:
  - 스토리텔링 구조
  - 코드 예시 포함
  - 실전 경험 강조

Project Documentation:
  - 구조화된 섹션
  - 기술 상세
  - 다이어그램 제안

Presentation:
  - 슬라이드 개요
  - 핵심 포인트
  - 시각 자료 제안

Weekly Report:
  - 성과 중심
  - 수치 집계
  - 다음 계획
```

---

## 🔄 Agent 간 협업

### Daily Cycle
```
Capture → Organizer → Linker → Curator
  ↓         ↓          ↓         ↓
Inbox   PARA/Zk   8+ Links  Status↑
  ↓
Reviewer (저녁 9시)
  ↓
Daily Dashboard
```

### Weekly Cycle
```
Curator → Synthesizer → Express
   ↓           ↓          ↓
Promote    MOC/Hub    Blog/Doc
   ↓
Reviewer (금요일)
   ↓
Weekly Dashboard
```

### Monthly Cycle
```
Synthesizer → Express → Reviewer
     ↓           ↓         ↓
 Patterns    Reports   Goals
     ↓
Strategic Planning
```

### Event-driven Communication
```yaml
Event Bus:
  - "note.created" → Organizer, Linker
  - "note.promoted" → Curator, Reviewer
  - "note.enriched" → Dashboard update
  - "orphan.detected" → Linker, User alert
  - "pattern.discovered" → Synthesizer
  - "goal.achieved" → Reviewer, Celebrate!
```

---

## 📊 성공 지표

### Agent별 KPI
```yaml
Capture Agent:
  - Capture rate: 3+ items/day
  - Inbox processing: 80% within 24h

Organizer Agent:
  - Classification accuracy: 90%+
  - PARA compliance: 95%+

Linker Agent:
  - Average links/note: 8+
  - Orphan rate: <5%
  - Link quality: >0.7

Curator Agent:
  - Promotion rate: 2+ notes/week
  - Evergreen ratio: 30%+

Synthesizer Agent:
  - MOC coverage: 80%+
  - Pattern discovery: 2+ /month

Reviewer Agent:
  - Review completion: 100%
  - Dashboard accuracy: 95%+

Search Agent:
  - Retrieval time: <30s
  - Result relevance: >0.8

Express Agent:
  - Output count: 2+ /month
  - Quality score: 4+/5
```

### 전체 시스템 건강도
```yaml
Knowledge Growth:
  - New notes/week: 5-10
  - Permanent notes: 100+ (year)
  - Network density: 8+ avg

Engagement:
  - Daily capture: 3+ items
  - Weekly review: 100%
  - Monthly reflection: 100%

Business Impact:
  - Problem solving: faster (노트 재사용)
  - Duplication: reduced
  - Insight quality: deeper
```

---

## 🚀 구현 로드맵

### Phase 1: Foundation (Week 1-2)
**목표**: 기본 습관 형성

- [ ] **Capture Agent** 구현
  - `/capture` 명령어
  - Fleeting note 템플릿
  - Daily note 통합

- [ ] **Organizer Agent** 확장
  - 기존 Content Organizer 개선
  - 일일 정리 워크플로우
  - 품질 검증 추가

- [ ] **Reviewer Agent** (Daily only)
  - Daily 회고 템플릿
  - 자동 통계 집계
  - 습관 추적

**성공 기준**:
- ✅ 3일 연속 Daily capture
- ✅ Inbox 정리 80%
- ✅ Daily 회고 100%

---

### Phase 2: Connection (Week 3-4)
**목표**: 지식 네트워크 구축

- [ ] **Linker Agent** 구현
  - Auto-link 알고리즘
  - Semantic search 통합
  - 8+ links 목표 달성

- [ ] **Search Agent** 구현
  - Multi-modal search
  - Quick jump
  - Graph navigation

**성공 기준**:
- ✅ 평균 links/note: 6+
- ✅ Orphan rate: <10%
- ✅ 검색 시간: <60s

---

### Phase 3: Intelligence (Week 5-6)
**목표**: 품질 및 통찰

- [ ] **Curator Agent** 구현
  - 자동 status 승격
  - Orphan 감지
  - Dashboard 생성

- [ ] **Synthesizer Agent** 구현
  - MOC 자동 생성
  - 패턴 발견
  - Hub 업데이트

- [ ] **Reviewer Agent** (Weekly)
  - Weekly 회고 자동화
  - 주간 통계
  - 목표 추적

**성공 기준**:
- ✅ Evergreen: 10개 이상
- ✅ MOC: 3개 생성
- ✅ Weekly review: 2회 연속

---

### Phase 4: Output (Week 7-8)
**목표**: 가치 실현

- [ ] **Express Agent** 구현
  - 블로그 포스트 초안
  - 프로젝트 문서
  - 발표 자료

- [ ] **Reviewer Agent** (Monthly)
  - Monthly 회고
  - 장기 트렌드 분석
  - 전략 계획

**성공 기준**:
- ✅ 블로그 포스트: 1편
- ✅ Monthly review 완료
- ✅ 전체 시스템 건강도: 80%+

---

## 📝 Next Steps

### 즉시 실행
1. **Agent 파일 생성**
   - `.claude/agents/` 폴더에 8개 agent 파일
   - 각각 상세 프롬프트 작성

2. **명령어 설정**
   - `.claude/commands/` 폴더에 슬래시 명령어
   - `/capture`, `/organize`, `/connect`, `/curate`, `/synthesize`, `/review`, `/search`, `/express`

3. **Hook 설정**
   - `.claude/hooks/` 폴더에 자동화 훅
   - `auto-capture.md`, `auto-organize.md`, `auto-link.md`

### 1주일 내
1. **Phase 1 시작**
   - Capture Agent 구현
   - Daily 습관 형성

2. **템플릿 작성**
   - Fleeting Note
   - Permanent Note
   - Daily Review

### 1개월 내
1. **전체 시스템 완성**
   - 8개 Agent 모두 구현
   - 자동화 워크플로우 완성

2. **측정 및 개선**
   - KPI 추적
   - 병목 지점 개선

---

## 📚 참고 문헌

1. **PARA Method**
   - Forte, Tiago. *Building a Second Brain* (2024)
   - [PARA Method](https://fortelabs.com/blog/para/)

2. **Zettelkasten**
   - Luhmann, Niklas. *Communication with Slip Boxes*
   - [Zettelkasten.de](https://zettelkasten.de/)

3. **CODE Cycle**
   - [Personal Knowledge Management Guide](https://www.glukhov.org/post/2025/07/personal-knowledge-management/)

4. **Network Analysis**
   - Sebastien, D. *Analyzing 8,000 Notes*
   - [PKM at Scale](https://www.dsebastien.net/personal-knowledge-management-at-scale-analyzing-8-000-notes-and-64-000-links/)

---

**Version**: 1.0  
**Last Updated**: 2025-11-29  
**Next Review**: 2025-12-29  
**Status**: 🌱 Seedling → 🌿 Budding (구현 후)

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

