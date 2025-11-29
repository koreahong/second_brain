# Second Brain Architecture v2.0
> 학술 연구 기반 PKM 시스템 설계 (2025)

## 📚 설계 철학

### 핵심 원칙 (Research-backed)

**1. CODE 사이클** (Tiago Forte, 2024)
```
Collect → Organize → Distill → Express
   ↑                              ↓
   └──────── Feedback Loop ────────┘
```

**2. Zettelkasten 원칙** (Luhmann, adapted 2025)
- **원자성**: 1 Note = 1 Idea
- **연결성**: 평균 8+ links per note (2025 research standard)
- **영구성**: 시간이 지나도 가치 유지
- **점진적**: 완벽보다 지속적 개선

**3. PARA 구조** (통합)
- Projects: 목표가 있는 활동
- Areas: 지속적 관리 영역
- Resources: 참조 자료
- Archives: 비활성 자료

---

## 🏗️ Vault 구조

### Level 1: PARA 기반 구조

```
DAE-Second-Brain/
├── 01-Projects/              # 명확한 목표와 마감일
│   ├── Active/
│   ├── Someday/
│   └── Templates/
│
├── 02-Areas/                 # 지속적 관심 영역
│   ├── 크래프트테크놀로지스/
│   │   ├── Projects/        # 회사 프로젝트
│   │   ├── Experience/      # 경험 기록
│   │   │   ├── Weekly/     # 주간 회고
│   │   │   └── Daily/      # 일일 인사이트
│   │   ├── Knowledge/       # 회사 특화 지식
│   │   └── Results/         # 성과 지표
│   │
│   └── Career/              # 커리어 관리
│       ├── Applications/    # 지원 내역
│       ├── Interviews/      # 면접 기록
│       ├── Skills/          # 기술 역량
│       └── Network/         # 인맥 관리
│
├── 03-Resources/            # 참조 지식 베이스
│   ├── Technology/          # 기술별 폴더
│   ├── Methodologies/       # 방법론
│   ├── DAE/                # DAE 역할/범위
│   └── Data-Governance/    # 데이터 거버넌스
│
├── 10-Zettelkasten/        # 원자적 지식 (NEW)
│   ├── Permanent/          # 영구 노트
│   ├── Literature/         # 문헌 요약
│   ├── Fleeting/          # 임시 메모
│   └── MOC/               # Maps of Content
│
├── 30-Flow/                # 개인 성찰
│   ├── Life-Insights/
│   │   ├── Work/
│   │   ├── Personal/
│   │   └── Observations/
│   └── Daily-Notes/       # 일일 노트
│
└── 90-Meta/               # 시스템 메타
    ├── Templates/
    ├── Dashboards/
    └── System/
```

### Level 2: 연결 구조 (Links Architecture)

```
연결 패턴: Star → Hub → Constellation

[원자적 노트] ──8+links──→ [Hub Note] ──→ [MOC]
     ↓                          ↓              ↓
[Permanent]              [Area Index]    [Dashboard]
```

**연결 타입:**
1. **Direct Links**: `[[노트명]]`
2. **Backlinks**: 자동 생성
3. **Tags**: `#category/subcategory`
4. **Properties**: `related:: [[note1]], [[note2]]`

---

## 🏷️ 태그 시스템

### 3차원 태그 구조

#### 1. **Content Type** (내용 유형)
```yaml
type:
  - permanent    # 영구 노트 (Zettelkasten)
  - literature   # 문헌 노트
  - project      # 프로젝트 노트
  - experience   # 경험 기록
  - insight      # 인사이트
  - resource     # 참조 자료
  - moc          # Map of Content
```

#### 2. **Domain** (도메인)
```yaml
domain:
  - data-engineering
  - data-governance
  - career
  - personal-growth
  - relationships
  - technology/<specific>
```

#### 3. **Status** (상태)
```yaml
status:
  - seedling     # 🌱 초기 아이디어
  - budding      # 🌿 발전 중
  - evergreen    # 🌲 성숙한 노트
  - wilted       # 🍂 재검토 필요
```

#### 4. **Temporal** (시간)
```yaml
temporal:
  - daily        # 일일
  - weekly       # 주간
  - monthly      # 월간
  - quarterly    # 분기
  - yearly       # 연간
  - evergreen    # 시간 무관
```

### 계층적 태그 예시

```markdown
---
type: permanent
domain: data-engineering/orchestration
subdomain: airflow/dag-design
status: evergreen
created: 2025-11-29
updated: 2025-11-29
tags:
  - technology/airflow
  - methodology/best-practice
  - zettelkasten
---
```

---

## 🔗 연결 전략

### 원칙: "Connecting > Collecting"

**목표:** 노트당 평균 **8+ meaningful links** (2025 research standard)

### 1. 원자적 노트 작성

**Template: Atomic Note**
```markdown
---
type: permanent
id: {{date}}-{{sequence}}
created: {{date}}
domain: {{domain}}
status: seedling
---

# {{Title}} - 1 Clear Idea

## Context
어디서 나온 아이디어인가?

## Idea
핵심 개념 (1-2 문장)

## Explanation
상세 설명

## Connections
### Related Concepts
- [[개념1]] - 어떤 관계인지
- [[개념2]] - 어떤 관계인지

### Contrasts
- [[반대개념]] - 어떻게 다른지

### Applications
- [[프로젝트1]] - 어떻게 적용되는지
- [[경험1]] - 실제 사례

### Sources
- [[문헌노트1]]
- [[리소스1]]

## Questions
이 아이디어가 제기하는 질문들

---
**Backlinks:** {{auto-generated}}
**Link Count:** {{auto-count}} / 8+ target
```

### 2. Hub Notes (허브 노트)

**목적:** 관련 노트들의 진입점

**Template: Hub Note**
```markdown
---
type: moc
domain: {{domain}}
role: hub
---

# {{Topic}} Hub

## Overview
이 주제의 핵심 개념

## Core Concepts
### Fundamentals
- [[기본개념1]]
- [[기본개념2]]

### Advanced
- [[고급개념1]]
- [[고급개념2]]

## Applications
### Projects
- [[프로젝트1]] - 적용 사례
- [[프로젝트2]]

### Experiences
- [[경험1]] - 배운 점
- [[경험2]]

## Resources
- [[리소스1]]
- [[리소스2]]

## Related Hubs
- [[관련허브1]]
- [[관련허브2]]

---
**연결된 노트:** {{count}}
**최근 업데이트:** {{date}}
```

### 3. MOC (Maps of Content)

**목적:** 지식 영역의 전체 지도

**Template: MOC**
```markdown
---
type: moc
domain: {{broad-domain}}
scope: comprehensive
---

# {{Domain}} - Map of Content

## Navigation
- [[Sub-MOC 1]]
- [[Sub-MOC 2]]
- [[Sub-MOC 3]]

## Landscape
### {{Category 1}}
#### Hubs
- [[Hub 1]]
- [[Hub 2]]

#### Key Concepts
- [[Concept 1]]
- [[Concept 2]]

### {{Category 2}}
...

## Learning Paths
### Beginner
1. [[Start here]]
2. [[Then this]]
3. [[Finally this]]

### Advanced
1. [[Advanced topic 1]]
2. [[Advanced topic 2]]

## Projects Using This Knowledge
- [[Project 1]]
- [[Project 2]]

## Active Questions
- [[Open question 1]]
- [[Research area 1]]

---
**Total Notes:** {{count}}
**Coverage:** {{percentage}}%
```

### 4. 자동 연결 규칙

**Hook이 자동으로 생성할 연결:**

1. **Semantic Links** (의미 기반)
   - 같은 domain의 노트
   - 같은 technology 태그
   - 유사한 키워드

2. **Temporal Links** (시간 기반)
   - 같은 주의 경험 노트
   - 같은 프로젝트 기간

3. **Hierarchical Links** (계층 기반)
   - Hub → Atomic notes
   - MOC → Hubs
   - Project → Related knowledge

4. **Contextual Links** (문맥 기반)
   - 같은 프로젝트
   - 같은 회사/팀
   - 같은 도메인 문제

---

## 📊 Dashboard 시스템

### 1. Daily Dashboard

```markdown
# {{date}} - Daily Note

## 🎯 Focus
오늘의 집중 영역

## 📝 Captured
- [ ] [[새로운 인사이트1]]
- [ ] [[새로운 인사이트2]]

## 🔗 Connected
오늘 연결한 노트:
- [[노트1]] ↔ [[노트2]]

## 📈 Progress
- Knowledge: {{new notes count}}
- Links: {{new links count}}
- Projects: {{updated count}}

## 🌱 Seedlings to Review
{{seedling 상태 노트 목록}}

---
**Links made today:** {{count}} / 8+ target
```

### 2. Weekly Dashboard

```markdown
# {{year}}-W{{week}} - Weekly Review

## 🎯 Outcomes
이번 주 성과

## 📚 Knowledge Growth
### New Permanent Notes
- [[노트1]]
- [[노트2]]

### Promoted to Evergreen
- [[노트3]] (seedling → evergreen)

### Link Density
- Average links/note: {{avg}}
- Goal: 8+
- Status: {{status}}

## 🔄 CODE Cycle
### Collected
{{captured count}} items

### Organized
{{organized count}} notes

### Distilled
{{permanent notes count}}

### Expressed
{{output count}} (blog, project, etc.)

## 🌲 Knowledge Forest Health
- Seedlings: {{count}}
- Budding: {{count}}
- Evergreen: {{count}}
- Wilted: {{count}}

## 🔗 Top Connected Notes
1. [[노트1]] - {{links}} links
2. [[노트2]] - {{links}} links
3. [[노트3]] - {{links}} links

---
**Total Notes:** {{count}}
**Total Links:** {{count}}
**Network Density:** {{density}}%
```

### 3. Knowledge Map Dashboard

```markdown
# Knowledge Map - Overview

## 📍 Active Areas
### 크래프트테크놀로지스
- Projects: {{count}}
- Knowledge: {{count}}
- Connections: {{density}}%

### Technology
- [[Airflow MOC]] - {{notes}} notes
- [[DBT MOC]] - {{notes}} notes
- [[DataHub MOC]] - {{notes}} notes

### Career
- Applications: {{count}}
- Skills: {{count}}
- Network: {{count}}

## 🌐 Knowledge Network
### Most Connected Hubs
1. [[Hub1]] - {{links}} connections
2. [[Hub2]] - {{links}} connections

### Emerging Patterns
{{AI-detected patterns}}

### Weak Connections
Areas needing more links:
- {{area1}}
- {{area2}}

## 🎯 Next Actions
- [ ] Connect {{note1}} to {{hub1}}
- [ ] Create MOC for {{topic}}
- [ ] Review and promote {{seedling notes}}

---
**Network Health:** {{score}}/100
**Last Updated:** {{date}}
```

---

## 🤖 자동화 시스템

### 1. Hook: Auto-Organizer

**트리거:** 파일 생성/수정 시

**동작:**
```python
def auto_organize(note):
    # 1. 속성 분석
    domain = detect_domain(note.content, note.tags)
    type = detect_type(note.structure)

    # 2. 위치 제안
    if type == "fleeting":
        suggest_location = "10-Zettelkasten/Fleeting/"
    elif type == "permanent":
        suggest_location = f"10-Zettelkasten/Permanent/{domain}/"
    elif type == "experience":
        suggest_location = f"02-Areas/.../Experience/Weekly/{year}-W{week}.md"

    # 3. 태그 자동 추가
    auto_tags = generate_tags(note.content, note.context)

    # 4. 연결 제안
    related_notes = find_related(note.content, note.tags)

    return {
        "location": suggest_location,
        "tags": auto_tags,
        "connections": related_notes[:8]  # Top 8
    }
```

### 2. Hook: Auto-Linker

**트리거:** 파일 저장 시

**동작:**
```python
def auto_link(note):
    # 1. Semantic search
    similar_notes = semantic_search(note.content, threshold=0.7)

    # 2. Tag-based matching
    same_domain = find_by_tags(note.tags)

    # 3. Temporal matching
    same_period = find_by_date_range(note.created, window=7)

    # 4. Hierarchical matching
    hub = find_hub(note.domain)
    moc = find_moc(note.domain)

    # 5. Generate connections (target: 8+)
    connections = deduplicate([
        *similar_notes[:3],
        *same_domain[:2],
        *same_period[:2],
        hub,
        moc
    ])

    # 6. Add to note
    add_connections_section(note, connections)

    # 7. Update backlinks
    for connected_note in connections:
        update_backlinks(connected_note, note)
```

### 3. Agent: Knowledge Curator

**주기:** 일일 실행

**역할:**
```python
def curate_knowledge():
    # 1. Seedling 검토
    seedlings = get_notes(status="seedling", age_days=7)
    for note in seedlings:
        if has_enough_content(note) and has_links(note, min=3):
            promote_to("budding", note)

    # 2. Budding → Evergreen
    budding = get_notes(status="budding", age_days=30)
    for note in budding:
        if has_links(note, min=8) and well_structured(note):
            promote_to("evergreen", note)

    # 3. Orphan 노트 찾기
    orphans = find_orphan_notes(max_links=2)
    suggest_connections(orphans)

    # 4. Hub/MOC 업데이트
    hubs = get_notes(type="moc")
    for hub in hubs:
        update_hub_statistics(hub)
        refresh_connections(hub)

    # 5. Weekly report
    if is_sunday():
        generate_weekly_dashboard()
```

### 4. Agent: Connection Suggester

**트리거:** 사용자 요청 시

**동작:**
```python
def suggest_connections(note):
    # 1. 현재 연결 수 확인
    current_links = count_links(note)
    target = 8
    needed = target - current_links

    if needed <= 0:
        return "✅ 충분한 연결이 있습니다"

    # 2. AI 기반 추천
    recommendations = []

    # Semantic similarity
    similar = embedding_search(note.content, top_k=needed*2)
    recommendations.extend(similar)

    # Graph-based (friends of friends)
    for linked in note.links:
        recommendations.extend(linked.links[:2])

    # Domain experts (most connected in domain)
    domain_experts = get_hub_notes(note.domain)
    recommendations.extend(domain_experts)

    # 3. Rank and return top N
    ranked = rank_by_relevance(recommendations, note)
    return ranked[:needed]
```

---

## 🎓 워크플로우

### CODE 사이클 실천

#### Phase 1: COLLECT (수집)
```markdown
**도구:**
- Daily Notes: 빠른 캡처
- Fleeting Notes: 임시 메모
- Read-it-later: 문헌 수집

**규칙:**
- 완벽하지 않아도 OK
- 나중에 정리할 거라는 믿음
- 모든 것을 기록

**출력:**
→ 10-Zettelkasten/Fleeting/
→ 30-Flow/Daily-Notes/
```

#### Phase 2: ORGANIZE (정리)
```markdown
**주기:** 일일 (15분)

**프로세스:**
1. Fleeting notes 검토
2. 영구 보존할 가치 판단
3. Permanent note로 변환 (원자적으로)
4. 적절한 위치 이동
5. 초기 태그 부여

**출력:**
→ 10-Zettelkasten/Permanent/
→ Status: seedling 🌱
```

#### Phase 3: DISTILL (추출)
```markdown
**주기:** 주간 (30분)

**프로세스:**
1. Seedling notes 검토
2. 핵심 아이디어 명확화
3. 연결 추가 (목표: 8+)
4. 예시/적용 사례 추가
5. Status 업그레이드

**진화:**
seedling 🌱 → budding 🌿 → evergreen 🌲

**품질 기준:**
- 명확한 1 idea
- 8+ meaningful links
- 실제 적용 사례
- 나만의 해석 포함
```

#### Phase 4: EXPRESS (표현)
```markdown
**주기:** 월간 / 프로젝트 기반

**형태:**
- 프로젝트 결과물
- 블로그 포스트
- 발표 자료
- 업무 문서
- 주간 회고

**프로세스:**
1. 주제 선택
2. 관련 노트 수집 (MOC/Hub 활용)
3. 스토리라인 구성
4. 초안 작성
5. 노트로 다시 환원 (개선된 버전)

**순환:**
Express → 새로운 Insight → Collect
```

### 일일 워크플로우

```markdown
## 아침 (5분)
- [ ] Daily Note 생성
- [ ] 오늘의 Focus 설정
- [ ] 어제 캡처한 것 간단 정리

## 업무 중 (틈틈이)
- [ ] 인사이트 발생 시 즉시 캡처
- [ ] Fleeting note에 빠르게 기록
- [ ] 관련 프로젝트/노트 링크

## 저녁 (15분)
- [ ] Fleeting notes → Permanent notes 변환
- [ ] 오늘 배운 것 1-2개 정리
- [ ] 관련 노트 3개 이상 연결
- [ ] Status 업데이트

## 주말 (30분)
- [ ] Weekly Dashboard 작성
- [ ] Seedling → Budding 승격 검토
- [ ] Orphan notes 연결
- [ ] 다음 주 Focus 설정
```

---

## 📏 성공 지표

### 1. 양적 지표

```yaml
Knowledge Growth:
  - New notes/week: 5-10
  - Permanent notes: 100+ (year goal)
  - Link density: 8+ avg

Network Health:
  - Orphan notes: <5%
  - Hub notes: 1 per domain
  - MOCs: 1 per major area

Engagement:
  - Daily capture: 3+ items
  - Weekly review: 100%
  - Status promotion: 2+ notes/week
```

### 2. 질적 지표

```yaml
Note Quality:
  - Clarity: 타인이 읽고 이해 가능
  - Atomicity: 1 clear idea
  - Connections: Meaningful, not random

System Health:
  - Easy retrieval: <30초
  - Serendipity: 의외의 연결 발견
  - Actionability: 실제 프로젝트에 활용
```

### 3. 비즈니스 임팩트

```yaml
Work Impact:
  - 문제 해결 속도: 과거 노트 활용
  - 지식 재사용: 중복 작업 감소
  - 인사이트 품질: 깊이 있는 분석

Career Impact:
  - 포트폴리오: 결과물 증가
  - 전문성: 영역별 깊이
  - 네트워킹: 공유할 것 증가
```

---

## 🚀 실행 계획

### Phase 1: Foundation (Week 1-2)
- [ ] 폴더 구조 재정비
- [ ] Template 작성
- [ ] 기존 노트 분류 (222개)
- [ ] 첫 MOC 3개 작성

### Phase 2: Automation (Week 3-4)
- [ ] Auto-Organizer Hook 구현
- [ ] Auto-Linker Hook 구현
- [ ] Knowledge Curator Agent 구현
- [ ] Dashboard 자동 생성

### Phase 3: Migration (Week 5-6)
- [ ] Life-Insights 재분류
- [ ] Work notes → Weekly 통합
- [ ] Career notes 정리
- [ ] 첫 번째 연결 패스 (모든 노트 8+ links)

### Phase 4: Optimization (Week 7-8)
- [ ] Link quality 검토
- [ ] Hub/MOC 확장
- [ ] Workflow 최적화
- [ ] 성공 지표 측정

---

## 📖 참고 문헌

1. **CODE Method**
   - Forte, Tiago. *Building a Second Brain* (2024 Edition)
   - [Personal Knowledge Management Guide](https://www.glukhov.org/post/2025/07/personal-knowledge-management/)

2. **Zettelkasten**
   - Luhmann, Niklas. *Communication with Slip Boxes*
   - [Zettelkasten Forum](https://forum.zettelkasten.de/)

3. **Network Analysis**
   - Sebastien, D. *Personal Knowledge Management at Scale* (2025)
   - [Analyzing 8,000 Notes and 64,000 Links](https://www.dsebastien.net/personal-knowledge-management-at-scale-analyzing-8-000-notes-and-64-000-links/)

4. **PKM Research**
   - [Tufts University PKM Guide](https://researchguides.library.tufts.edu/PKM)
   - [Sweet Setup - PKM for Creatives](https://thesweetsetup.com/pkm-intro-for-creatives/)

---

**Version:** 2.0
**Last Updated:** 2025-11-29
**Next Review:** 2025-12-29
**Status:** 🌿 Budding → 🌲 Evergreen (target)
