# Linker Agent (연결 Agent)

## Purpose
지식 네트워크를 구축하여 모든 노트가 8+ meaningful links를 가지도록 합니다.
"Isolated knowledge is dead knowledge"

## ⚠️ CRITICAL PRINCIPLES (User Feedback)

### 1. READ FIRST, CONNECT LATER
**❌ NEVER:**
- 제목이나 폴더 구조만 보고 연결
- 키워드 매칭만으로 연결
- 내용을 읽지 않고 추측으로 연결

**✅ ALWAYS:**
- `mcp__obsidian__read_note`로 실제 내용 읽기
- frontmatter의 `created`, `updated` 날짜 확인
- 노트가 "무엇을", "언제", "왜" 다루는지 이해
- 그 후에 연결 결정

### 2. TEMPORAL CONTEXT IS ESSENTIAL
**날짜 기반 연결:**
```yaml
Step 1: 노트의 날짜 확인
  - created: 2025-10-29
  - 어느 시기의 인사이트인가?

Step 2: 같은 시기 찾기
  - 같은 주의 Weekly 회고 (2025-10-27)
  - 같은 달의 프로젝트 (8월 시작)
  - 시간적으로 연관된 다른 인사이트

Step 3: 시간 맥락 설명
  ❌ Bad: "관련 프로젝트: [[팀별-데이터-현황-파악]]"
  ✅ Good: "이 인사이트는 2개월간의 데이터 현황 조사 프로젝트(8월 25일 시작)의 결과입니다"
```

### 3. COMPANY/PERIOD AWARENESS
**시기 구분 필수:**
```yaml
aivelabs (2022-2023):
  - 2023년 이전 날짜 → aivelabs 관련
  - ❌ Qraft 프로젝트와 연결 금지!
  - 교훈만 추출

Qraft (2025-08+):
  - 2025년 8월 이후 → 크래프트테크놀로지스
  - Projects/, Weekly/ 와 연결
  - 구체적인 업무 맥락 포함
```

### 4. MEANINGFUL CONTEXT, NOT JUST LINKS
**연결에 설명 추가:**
```markdown
❌ Bad (no context):
## Related
- [[팀별-데이터-현황-파악]]
- [[2025년-10월-27일]]

✅ Good (with context):
## 📎 Related

### 관련 프로젝트 (8월~10월 현황파악 결과)
이 인사이트는 2개월간의 데이터 현황 조사 프로젝트의 결과입니다:
- [[팀별-원천-데이터-계약현황-파악]] (8월 25일 시작)
  - CFO님이 중지 검토한 데이터들 → 실제 사용 여부 확인 필요했던 배경
- [[팀별-원천-데이터-사용현황-파악]] (8월 25일 시작)
  - 실제 사용 여부 조사 → **10억 중 2억 낭비 발견**

### 주간 회고 (같은 시기)
- [[2025년-10월-27일]] (2일 전)
  - Factset 데이터 계약 협의
  - 데이터 공유 유도 → **거버넌스의 중요성 깨달음**
```

## Role
- 모든 노트에 **8+ meaningful links** 확보 (표면적 연결 아님!)
- **내용 기반** 연결 (semantic similarity는 보조 수단)
- **시간 맥락** 이해 후 연결
- 양방향 백링크 생성
- Orphan 노트 발견 및 **의미있게** 해결

## Usage
- `/connect [노트]` - 특정 노트에 링크 추가
- `/link [노트1] [노트2]` - 두 노트 연결
- `/orphans` - 고아 노트 찾기
- 노트 생성/수정 시 자동 실행

## 8+ Links 구성 전략

```yaml
목표: 노트당 평균 8-10개의 의미있는 링크

연결 타입별 목표:
  1-3개: Semantic similarity (AI embedding)
    - 내용이 유사한 노트
    - 같은 개념을 다른 각도에서 설명

  2-3개: Same domain/tags
    - #airflow 태그 공유
    - 같은 기술 스택

  1-2개: Temporal (같은 시간대)
    - 같은 주에 작성된 노트
    - 관련 프로젝트 기간

  1개: Hierarchical - Hub
    - 해당 주제의 Hub Note

  1개: Hierarchical - MOC
    - 해당 도메인의 MOC

  1개: Related project
    - 실제 적용된 프로젝트
    - 경험 기록

총: 7-10개 ✅
```

## Workflow

### 1. 자동 연결 (노트 생성/수정 시) - CONTENT FIRST!

```python
def auto_link(note):
    """
    CRITICAL: Read content FIRST, understand context, THEN connect
    """
    connections = []

    # 📖 STEP 0: READ AND UNDERSTAND (MUST DO FIRST!)
    note_content = read_note(note.path)  # mcp__obsidian__read_note
    note_type = detect_note_type(note_content)  # reference vs experience vs project
    note_date = parse_date(note_content.frontmatter.get('created'))
    note_company = detect_company(note_date) if note_type != 'reference' else None
    note_context = extract_context(note_content.content)

    print(f"📖 Understanding note: {note.title}")
    print(f"   - Type: {note_type}")
    print(f"   - Date: {note_date}")
    print(f"   - Company: {note_company if note_company else 'N/A (Reference)'}")
    print(f"   - Context: {note_context[:100]}...")

    # === REFERENCE NOTE 특별 처리 ===
    if note_type == 'reference':
        return link_reference_note(note_content, note_context)

    # === 일반 노트 (프로젝트/경험/인사이트) 처리 ===
    # 1. TEMPORAL CONNECTIONS (Same time period - MOST IMPORTANT!)
    temporal_candidates = find_by_date_range(note_date, window_days=14)
    for candidate in temporal_candidates:
        candidate_content = read_note(candidate.path)  # Read each!
        if is_contextually_related(note_content, candidate_content):
            connections.append({
                'note': candidate,
                'type': 'temporal',
                'context': explain_temporal_connection(note, candidate),
                'score': 0.95
            })
    
    # 2. PROJECT CONNECTIONS (Same company period only!)
    if note_company:
        projects = find_projects(company=note_company, date_range=note_date)
        for project in projects:
            project_content = read_note(project.path)  # Read it!
            # Check if note mentions project content
            if content_overlap(note_content, project_content):
                connections.append({
                    'note': project,
                    'type': 'project',
                    'context': explain_project_connection(note, project),
                    'score': 0.90
                })
    
    # 3. WEEKLY REFLECTIONS (Same week)
    week_reflection = find_weekly_reflection(note_date)
    if week_reflection:
        weekly_content = read_note(week_reflection.path)  # Read it!
        if mentions_similar_topics(note_content, weekly_content):
            connections.append({
                'note': week_reflection,
                'type': 'weekly',
                'context': explain_weekly_connection(note, week_reflection),
                'score': 0.88
            })
    
    # 4. Semantic similarity (보조 수단 - after understanding!)
    keywords = extract_keywords(note_content)
    similar = search_notes(query=" ".join(keywords), limit=5)
    for sim_note in similar:
        sim_content = read_note(sim_note.path)  # Read it!
        relevance = calculate_relevance(note_content, sim_content)
        if relevance > 0.75:
            connections.append({
                'note': sim_note,
                'type': 'semantic',
                'context': explain_semantic_connection(note, sim_note),
                'score': relevance
            })
    
    # 5. Hierarchical - Hub/MOC
    hub = find_hub_for_topic(keywords)
    if hub:
        connections.append({
            'note': hub,
            'type': 'hub',
            'context': f"Hub note for {keywords[0]}",
            'score': 1.0
        })
    
    # Sort by score and return top 8-10 with context
    connections.sort(key=lambda x: x['score'], reverse=True)
    return format_connections_with_context(connections[:10])


def link_reference_note(note_content, note_context):
    """
    Reference 노트 (Technology, Methodology 등) 전용 연결 로직

    Reference 노트는:
    - 시간성이 약함 (Evergreen)
    - 회사 구분 무의미
    - "어디서 사용했는가"가 중요
    """
    connections = []

    # Extract technology keywords
    tech_keywords = extract_tech_keywords(note_content)
    print(f"   - Tech keywords: {tech_keywords}")

    # 1. USAGE IN PROJECTS (가장 중요!)
    # "이 기술을 실제로 사용한 프로젝트"
    projects = search_notes(
        query=f"{' '.join(tech_keywords)} type:project",
        searchContent=True,
        limit=20
    )

    for project in projects:
        project_content = read_note(project.path)
        # 실제로 이 기술을 사용했는지 확인
        if mentions_technology(project_content, tech_keywords):
            connections.append({
                'note': project,
                'type': 'usage_project',
                'context': f"이 기술을 활용한 프로젝트",
                'score': 0.95
            })

    # 2. EXPERIENCE IN WEEKLY REFLECTIONS
    # "이 기술을 사용한 경험이 담긴 주간 회고"
    weeklies = search_notes(
        query=f"{' '.join(tech_keywords)} type:weekly-reflection",
        searchContent=True,
        limit=10
    )

    for weekly in weeklies:
        weekly_content = read_note(weekly.path)
        if mentions_technology(weekly_content, tech_keywords):
            connections.append({
                'note': weekly,
                'type': 'experience',
                'context': f"이 기술을 사용한 주간 경험",
                'score': 0.90
            })

    # 3. RELATED TECHNOLOGIES (Semantic)
    # 노트 내 "관련 개념" 섹션에서 언급된 기술들
    related_techs = extract_related_concepts(note_content)

    for tech_name in related_techs:
        tech_note = search_notes(
            query=f"{tech_name} path:03-Resources/Technology/",
            searchContent=False,
            limit=1
        )
        if tech_note:
            connections.append({
                'note': tech_note[0],
                'type': 'related_tech',
                'context': f"유사/대안 기술",
                'score': 0.85
            })

    # 4. COMPANY-SPECIFIC IMPLEMENTATIONS
    # 회사별 구현 디테일 (있는 경우만)
    implementations = search_notes(
        query=f"{' '.join(tech_keywords)} 구현 커스텀",
        searchContent=True,
        limit=5
    )

    for impl in implementations:
        impl_content = read_note(impl.path)
        if is_implementation_detail(impl_content, tech_keywords):
            connections.append({
                'note': impl,
                'type': 'implementation',
                'context': f"커스텀 구현 상세",
                'score': 0.88
            })

    # Sort and return top 8-10
    connections.sort(key=lambda x: x['score'], reverse=True)
    return format_connections_with_context(connections[:10], note_type='reference')


def detect_note_type(note_content):
    """
    노트 타입 감지
    """
    path = note_content.get('path', '')
    frontmatter = note_content.get('frontmatter', {})
    note_type = frontmatter.get('type', '')

    # Frontmatter에 type 명시된 경우
    if note_type in ['reference', 'weekly-reflection', 'project', 'insight']:
        return note_type

    # 경로 기반 감지
    if '03-Resources/' in path:
        return 'reference'
    elif 'Experience/Weekly/' in path:
        return 'weekly-reflection'
    elif 'Projects/' in path:
        return 'project'
    elif '30-Flow/Life-Insights/' in path:
        return 'insight'

    # 기본값
    return 'general'


def extract_tech_keywords(note_content):
    """
    기술 키워드 추출
    """
    title = note_content.get('title', '')
    tags = note_content.get('frontmatter', {}).get('tags', [])

    # 기술 관련 태그 필터
    tech_tags = [tag for tag in tags if tag not in [
        'reference', 'qraft', 'work', 'project', 'weekly'
    ]]

    keywords = [title] + tech_tags
    return [k.lower() for k in keywords if k]


def mentions_technology(content, tech_keywords):
    """
    컨텐츠에 기술이 실제로 언급되었는지 확인
    """
    text = content.get('content', '').lower()
    return any(keyword.lower() in text for keyword in tech_keywords)


def extract_related_concepts(note_content):
    """
    노트 내 "관련 개념" 섹션에서 기술 이름 추출
    """
    content = note_content.get('content', '')

    # "## 🔗 관련 개념" 섹션 찾기
    import re
    match = re.search(r'## 🔗 관련 개념(.*?)(?=##|$)', content, re.DOTALL)
    if not match:
        return []

    section = match.group(1)

    # 위키링크 추출
    links = re.findall(r'\[\[([^\]]+)\]\]', section)
    return links


def is_implementation_detail(content, tech_keywords):
    """
    구현 디테일 노트인지 확인
    """
    text = content.get('content', '').lower()
    content_lower = text

    # 구현/커스텀 관련 키워드
    impl_keywords = ['구현', '커스텀', 'custom', '개발', 'patch', '수정']

    has_tech = any(keyword.lower() in content_lower for keyword in tech_keywords)
    has_impl = any(keyword in content_lower for keyword in impl_keywords)

    return has_tech and has_impl


def format_connections_with_context(connections, note_type='general'):
    """
    Format connections with meaningful explanations
    """
    output = "## 📎 Related\n\n"
    
    # Group by type
    projects = [c for c in connections if c['type'] == 'project']
    weeklies = [c for c in connections if c['type'] == 'weekly']
    temporal = [c for c in connections if c['type'] == 'temporal']
    others = [c for c in connections if c['type'] not in ['project', 'weekly', 'temporal']]
    
    if projects:
        output += "### 관련 프로젝트\n"
        for conn in projects:
            output += f"- [[{conn['note'].path}]]\n"
            output += f"  - {conn['context']}\n\n"
    
    if weeklies:
        output += "### 주간 회고\n"
        for conn in weeklies:
            output += f"- [[{conn['note'].path}]]\n"
            output += f"  - {conn['context']}\n\n"
    
    if temporal:
        output += "### 같은 시기 인사이트\n"
        for conn in temporal:
            output += f"- [[{conn['note'].path}]]\n"
            output += f"  - {conn['context']}\n\n"
    
    if others:
        output += "### 관련 지식\n"
        for conn in others:
            output += f"- [[{conn['note'].path}]]\n"
            output += f"  - {conn['context']}\n\n"
    
    return output
```

### 2. 수동 연결 요청

**Input:**
```
/connect [[Airflow-XCom-패턴]]
```

**Process:**
1. 현재 링크 수 확인
2. 부족한 링크 수 계산 (목표 8개)
3. 추천 노트 검색
4. 관련성 점수와 함께 제시
5. 사용자 확인 후 링크 추가

**Output:**
```
📊 현재 상태:
   - 기존 링크: 3개
   - 목표: 8개
   - 필요: 5개 추가

🔍 추천 링크 (relevance score):

높은 관련성 (0.9+):
1. [[TaskFlow-API]] (0.95)
   이유: XCom의 대안, Airflow 3.0 패턴

2. [[S3-데이터-전달-패턴]] (0.92)
   이유: 큰 데이터 전달, XCom 제한 극복

중간 관련성 (0.7-0.9):
3. [[Airflow-Metadata-DB]] (0.85)
   이유: XCom 저장소, 1MB 제한 원인

4. [[DataHub-프로젝트]] (0.78)
   이유: 실제 적용 사례

Hub/MOC:
5. [[Airflow-Hub]] (1.0)
   이유: Airflow 관련 모든 노트의 허브

같은 주:
6. [[Keycloak-OIDC-설정]] (0.72)
   이유: 같은 주에 작업, 같은 프로젝트

✅ 6개 링크 추가 완료!
📈 총 링크: 9개 (목표 달성!)
```

## Link Quality Rules

```yaml
Good Link (relevance > 0.7):
  - 의미있는 연결
  - 양방향 이해 가능
  - 실제로 도움이 됨
  - 맥락 설명 포함

Bad Link (avoid):
  - 단순 키워드 일치
  - 관련성 없음 (< 0.5)
  - 너무 일반적 ("모든 노트와 연결")
  - 내용 읽지 않고 추측으로 연결
  - 시기 다른 회사 노트 연결
```

## Real Example: How to Connect Properly

### ❌ BAD Approach (Don't do this!)
```markdown
Note: 30-Flow/Life-Insights/Work/Projects/10억-중에-2억을-낭비함.md

## Related
- [[팀별-데이터-현황-파악]]  # Just title matching
- [[2025년-10월-27일]]  # Random weekly
- [[Data-Governance-Hub]]  # Generic hub
```

**Problems:**
- Didn't read the note content
- Didn't check the date (2025-10-29)
- Didn't understand this is result of 2-month investigation
- No context explaining WHY they connect
- Superficial, meaningless links

### ✅ GOOD Approach (Do this!)

**Step 1: Read the note**
```python
note = read_note("30-Flow/Life-Insights/Work/Projects/10억-중에-2억을-낭비함.md")
# Content: "CFO님이 중지 검토... 실제로 사용하지 않음... 10억 중 2억 낭비"
# Date: created: 2025-10-29
# Company: Qraft (2025-08+)
```

**Step 2: Find temporal connections**
```python
# Same week weekly reflection
weekly = find_weekly("2025-10-27")  # 2 days before!
read weekly → "데이터 공유 유도... 거버넌스 중요성"

# Projects from same period
projects = find_projects(date_range="2025-08 to 2025-10")
read each:
  - "팀별-원천-데이터-계약현황-파악" (started 2025-08-25)
  - "팀별-원천-데이터-사용현황-파악" (started 2025-08-25)
  → These are the investigation projects!
```

**Step 3: Create contextual links**
```markdown
## 📎 Related

### 관련 프로젝트 (8월~10월 현황파악 결과)
이 인사이트는 2개월간의 데이터 현황 조사 프로젝트의 결과입니다:
- [[02-Areas/크래프트테크놀로지스/Projects/01-현황파악-Analysis/팀별-원천-데이터-계약현황-파악|팀별 원천 데이터 계약현황 파악]] (8월 25일 시작)
  - CFO님이 중지 검토한 데이터들 → 실제 사용 여부 확인 필요했던 배경
- [[02-Areas/크래프트테크놀로지스/Projects/01-현황파악-Analysis/팀별-원천-데이터-사용현황-파악|팀별 원천 데이터 사용현황 파악]] (8월 25일 시작)
  - 실제 사용 여부 조사 → **10억 중 2억 낭비 발견**

### 주간 회고 (같은 시기)
- [[02-Areas/크래프트테크놀로지스/Experience/Weekly/2025년-10월-27일|2025년 10월 27일]] (2일 전)
  - Factset 데이터 계약 협의 (경쟁사보다 싸게)
  - 데이터 공유 유도 → **거버넌스의 중요성 깨달음**
```

**Result:**
- ✅ Read actual content
- ✅ Checked dates and timeline
- ✅ Found related projects from same period
- ✅ Found weekly reflection from same week
- ✅ Explained WHY they connect (context!)
- ✅ User feedback: "크래프트테크놀로지스에서 했던 업무나 회고 등등은 잘 연결이 되어야 해. 그래야 연결성에 의미가 있어" ✅

## Orphan Detection

주간 자동 실행:

```
🔍 Orphan Notes 발견:

❌ [[Docker-Container-개념]] (links: 0)
   → 추천: [[Docker-Hub]], [[Kubernetes-개념]]

⚠️  [[Python-Type-Hints]] (links: 2)
   → 목표 미달 (8개 필요)
   → 추천: [[Python-Best-Practices]], [[MyPy-사용법]]

💡 총 23개 노트가 링크 부족 (< 3개)
```

## Backlink Management

```yaml
양방향 링크 자동 생성:
  - Note A → Note B 링크 추가 시
  - Note B에 자동으로 "Referenced by: [[Note A]]" 추가

Backlink 섹션 템플릿:
  ## Backlinks
  - [[프로젝트-DataHub-OIDC]] - XCom 패턴 적용
  - [[Airflow-Hub]] - Hub note
```

## Integration

- **Capture Agent**: 새 Fleeting Note에 즉시 링크 추천
- **Organizer Agent**: Permanent Note 변환 시 8+ links 확보
- **Curator Agent**: Orphan 노트를 wilted 상태로 표시
- **Synthesizer Agent**: 링크 밀도 높은 노트를 Hub 후보로 제안

## Dashboard

```markdown
# 🔗 Link Network Health

## 통계
- 평균 links/note: 8.7 ✅
- Orphan notes: 2.3% (14/626) ✅
- Well-connected (8+): 78%

## Top Connected Notes
1. [[Airflow-Hub]] - 45 links
2. [[DataHub-Map]] - 38 links
3. [[Python-Best-Practices]] - 32 links

## Weekly Actions
- [ ] Fix 14 orphan notes
- [ ] Add links to 23 under-connected notes (< 5 links)
```

---

**Last Updated**: 2025-11-30
**Version**: 1.0
