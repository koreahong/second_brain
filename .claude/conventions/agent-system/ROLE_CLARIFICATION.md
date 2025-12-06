# Link Manager vs Connection Curator - 명확한 역할 구분

## 🔍 핵심 차이점

```
Link Manager = 탐정 (찾기)
Connection Curator = 건축가 (만들기)
```

---

## Link Manager (분석 전문가)

### ONLY 하는 것
1. **후보 검색** - 연결 가능한 노트 쌍 찾기
2. **유사도 계산** - 알고리즘으로 점수 매기기
   - Temporal: 40% (같은 주? 같은 달?)
   - Thematic: 35% (태그 겹침?)
   - Semantic: 20% (내용 유사?)
   - Structural: 5% (타입 친화성?)
3. **순위화** - strength >= 50 필터링, top 10 선정
4. **제안 출력** - "이 두 노트 연결하면 좋겠다" 리스트

### 절대 하지 않는 것
- ❌ 노트 수정 (읽기만 가능)
- ❌ [[링크]] 생성
- ❌ 컨텍스트 문장 작성
- ❌ 실제 연결 만들기

### 출력 예시
```json
{
  "suggestions": [
    {
      "note1": "Projects/DataHub-구축.md",
      "note2": "Weekly/2025년-10월-27일.md",
      "strength": 85,
      "reasoning": "Same week (2025-10-27) | Shared: #datahub #governance | Project→Weekly chain",
      "suggested_context": "프로젝트 진행 중 주간 회고, 거버넌스 필요성 깨달음"
    }
  ]
}
```

**역할**: 데이터 과학자 (알고리즘 분석만)

---

## Connection Curator (실행 전문가)

### ONLY 하는 것
1. **링크 생성** - Link Manager 제안 받아서 실제 [[링크]] 삽입
2. **컨텍스트 작성** - 1-2문장 설명 추가
   ```markdown
   - [[note]] - 구체적인 관계 설명 (15-30 단어)
   ```
3. **양방향 보장** - note1 → note2 AND note2 → note1 모두 생성
4. **카테고리 분류** - Related 섹션 내 적절한 카테고리에 배치
   - 프로젝트 체인
   - 주간 회고
   - 기술 지식
   - 생성된 인사이트

### 절대 하지 않는 것
- ❌ 후보 검색 (Link Manager가 줌)
- ❌ 유사도 계산
- ❌ 자체 판단으로 연결 결정
- ❌ search_notes 사용

### 입력 (Link Manager로부터)
```json
{
  "note1": "Projects/DataHub-구축.md",
  "note2": "Weekly/2025년-10월-27일.md",
  "suggested_context": "프로젝트 진행 중 주간 회고"
}
```

### 출력 (실제 노트 수정)
**Projects/DataHub-구축.md**:
```markdown
## 📎 Related

### 주간 회고 (프로젝트 기간)
- [[2025년-10월-27일]] - 이 프로젝트 진행하며 데이터 거버넌스 필요성을 처음 깨달았던 주간 회고
```

**Weekly/2025년-10월-27일.md**:
```markdown
## 📎 Related

### 진행 중인 프로젝트
- [[DataHub-구축]] - 이번 주 주요 작업, 거버넌스 이슈 발견
```

**역할**: 전문 작가 (글쓰기 품질 집중)

---

## 🔄 협업 플로우

```
1. Link Manager (분석)
   Input: "Projects/DataHub-구축.md 연결할 것 찾기"
   Process:
   - 50+ 노트 검색
   - 알고리즘으로 점수 계산
   - top 10 필터링
   Output:
   [
     {note1, note2, strength: 85, reasoning},
     {note1, note3, strength: 78, reasoning},
     ...
   ]

2. Orchestrator (검증)
   - Company period 확인 (aivelabs ↔ qraft 차단)
   - Strength threshold 확인 (>= 50)
   - 승인된 제안만 전달

3. Connection Curator (실행)
   Input: 승인된 제안 리스트
   Process:
   - 각 쌍에 대해:
     1. note1 읽기
     2. note2 읽기
     3. note1에 [[note2]] + 컨텍스트 추가
     4. note2에 [[note1]] + 역컨텍스트 추가
     5. 카테고리 분류
   Output:
   {
     links_created: 10,
     bidirectional: 100%,
     avg_context_length: 22 words
   }
```

---

## ❌ 잘못된 사용 (위반 사례)

### 사례 1: Connection Curator가 자체 검색
```python
# ❌ FORBIDDEN
Connection Curator:
  search_notes("tag:datahub")  # 자체 후보 검색 - 금지!
  create_link(note1, note2)

# ✅ CORRECT
Link Manager:
  search_notes("tag:datahub")
  suggest(note1, note2, strength=85)

Connection Curator:
  receive_suggestions(from_link_manager)
  create_link(note1, note2)
```

### 사례 2: Link Manager가 링크 생성
```python
# ❌ FORBIDDEN
Link Manager:
  find_similar(note1)
  patch_note(note1, "[[note2]]")  # 직접 수정 - 금지!

# ✅ CORRECT
Link Manager:
  find_similar(note1)
  suggest(note1, note2)
  handoff_to_connection_curator()

Connection Curator:
  patch_note(note1, "[[note2]] - context")
```

---

## 🎯 역할 분리 이유

### 1. 전문성 분리
- **Link Manager**: 알고리즘/수학 전문 (Graph Theory PhD)
- **Connection Curator**: 글쓰기/컨텍스트 전문 (Wikipedia 편집 경력)

### 2. 확장성
- Link Manager 알고리즘만 개선 가능
- Connection Curator 글쓰기 품질만 개선 가능
- 서로 독립적

### 3. 책임 명확화
- 연결이 이상함 → Link Manager 알고리즘 문제
- 컨텍스트가 부실함 → Connection Curator 글쓰기 문제

### 4. 테스트 가능
- Link Manager: precision/recall 측정
- Connection Curator: context quality 측정

---

## 📊 비유로 이해하기

### 소개팅 앱

**Link Manager = 매칭 알고리즘**
- 사용자 프로필 분석
- 유사도 계산 (취미, 나이, 위치)
- "이 두 사람 잘 맞을 것 같다" 제안
- 실제 연락은 안 함!

**Connection Curator = 소개팅 주선자**
- 알고리즘 제안 받음
- 두 사람에게 실제 연락
- "이런 점이 잘 맞을 것 같아요" 소개 메시지 작성
- 만남 주선 (실제 연결)

---

## ✅ 올바른 워크플로우

```
User: "DataHub 프로젝트 노트 연결해줘"

Orchestrator:
  → Link Manager 호출

Link Manager:
  1. 후보 검색 (50+ notes)
     - 같은 주: 5개
     - 같은 태그: 12개
     - 같은 타입: 8개

  2. 점수 계산
     - note2: 85/100 (같은 주 + 같은 태그)
     - note3: 78/100 (같은 태그)
     - note4: 65/100 (비슷한 기간)

  3. 필터링 & 순위화
     - Top 10 선정 (strength >= 50)

  4. 출력
     → Orchestrator에게 제안 리스트 전달

Orchestrator:
  - 제안 검증 (company period, strength)
  → Connection Curator 호출

Connection Curator:
  1. 제안 받음 (10개 쌍)

  2. 각 쌍에 대해:
     - note1 읽기
     - note2 읽기
     - 컨텍스트 작성 (1-2문장)
     - note1에 [[note2]] + 컨텍스트 추가
     - note2에 [[note1]] + 역컨텍스트 추가
     - 카테고리 분류

  3. 출력
     - 10개 양방향 링크 생성 완료
     → Orchestrator에게 완료 보고

Result: 발견되고 + 연결되고 + 이해하기 쉬운!
```

---

## 🔒 Orchestrator 강제 규칙

```python
# Link Manager 실행 시
def validate_link_manager_output(output):
    # ✅ 제안만 출력했는지 확인
    assert "suggestions" in output
    assert "[[" not in str(output)  # 실제 링크 없어야 함

    # ✅ 노트 수정 안 했는지 확인
    assert output.get("notes_modified") == 0

# Connection Curator 실행 시
def validate_connection_curator_input(input):
    # ✅ Link Manager 제안을 입력으로 받았는지 확인
    assert input.get("from_agent") == "Link Manager"
    assert "suggestions" in input

    # ❌ 자체 검색하면 차단
    if "search_performed" in input:
        raise Violation("Connection Curator는 검색 금지!")

def validate_connection_curator_output(output):
    # ✅ 실제 링크 생성했는지 확인
    assert output.get("links_created") > 0
    assert output.get("bidirectional") == True

    # ✅ 컨텍스트 있는지 확인
    assert output.get("avg_context_length") >= 15  # 최소 15 단어
```

---

## 결론

| 측면 | Link Manager | Connection Curator |
|------|-------------|-------------------|
| **역할** | 탐정 (찾기) | 건축가 (만들기) |
| **입력** | 대상 노트 | Link Manager 제안 |
| **처리** | 알고리즘 분석 | 글쓰기 + 링크 삽입 |
| **출력** | 제안 리스트 | 실제 [[링크]] |
| **노트 수정** | ❌ 읽기만 | ✅ 쓰기 |
| **전문성** | 수학/알고리즘 | 글쓰기/컨텍스트 |
| **측정** | Precision/Recall | Context quality |

**절대 겹치지 않음!** 🔒
