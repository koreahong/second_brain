# Search Agent (검색 Agent)

## Purpose
필요한 지식을 30초 내에 찾습니다.
"The best knowledge is the knowledge you can find when you need it"

## Role
- Semantic search (의미 기반)
- 관련 노트 추천
- Quick jump (자주 찾는 노트)
- Graph navigation (네트워크 탐색)
- Smart suggestions

## Usage
- `/search [query]` - 의미 기반 검색
- `/find [키워드]` - 빠른 검색
- `/related [노트]` - 관련 노트 찾기
- `/similar [노트]` - 유사 노트 찾기

## Multi-modal Search

### 1. Semantic Search (AI embedding)

```python
def semantic_search(query, top_k=10):
    """의미 기반 검색 - 가장 강력!"""

    # Query embedding
    query_vector = embed(query)

    # 모든 노트 검색
    results = []
    for note in all_notes:
        note_vector = embed(note.content)
        similarity = cosine_similarity(query_vector, note_vector)

        if similarity > 0.7:  # 관련성 임계값
            results.append({
                'note': note,
                'score': similarity,
                'reason': explain_similarity(query, note)
            })

    return sorted(results, key=lambda x: x['score'], reverse=True)[:top_k]
```

**Example:**
```
Query: "Airflow에서 큰 데이터 어떻게 전달하지?"

Results:
1. [[XCom-S3-패턴]] (0.95) 🌲
   → XCom 1MB 제한, S3 경로 전달 패턴

2. [[TaskFlow-API]] (0.89) 🌿
   → Task 간 데이터 전달, XCom 대안

3. [[Airflow-Metadata-DB]] (0.82) 🌱
   → XCom 저장소, 제한 이유
```

### 2. Tag-based Search

```
/find #airflow AND #data-passing

Results:
- [[XCom-패턴]]
- [[TaskFlow-API]]
- [[S3-Integration]]
```

### 3. Graph Traversal (네트워크 탐색)

```
/related [[Airflow-XCom]]

🕸️ Network View:

[Airflow-DAG] ← [Airflow-Task] ← [Airflow-XCom] → [S3-패턴]
                                         ↓
                                   [Metadata-DB]
                                         ↓
                                   [DataHub-프로젝트]

📍 Direct connections (1 hop):
- [[S3-패턴]]
- [[Metadata-DB]]
- [[TaskFlow-API]]

📍 2 hops away:
- [[Iceberg-Table]] (via S3)
- [[DBT-Artifacts]] (via Metadata-DB)
- [[DataHub-Auth]] (via DataHub-프로젝트)

🎯 Suggested exploration:
"XCom과 DBT artifacts는 비슷한 목적?"
→ 새로운 통찰 가능성!
```

### 4. Temporal Search

```
/search last week

Results (최근 7일):
- [[2025-11-28-airflow-discovery]]
- [[2025-11-29-xcom-pattern]]
- [[2025-11-30-keycloak-setup]]
```

### 5. Frequency-based (자주 열어본 노트)

```
/find frequently accessed

📊 Most Accessed (Last 30 days):
1. [[Python-Best-Practices]] - 15 times
2. [[Airflow-Hub]] - 12 times
3. [[Git-Commands]] - 10 times
```

## Smart Suggestions

```python
def smart_suggest(context):
    """컨텍스트 기반 스마트 제안"""

    suggestions = []

    # 1. 현재 프로젝트 기반
    if context.current_project:
        suggestions.extend(
            find_project_related_notes(context.current_project)
        )

    # 2. 최근 본 노트 기반
    if context.recent_notes:
        suggestions.extend(
            find_similar_to_recent(context.recent_notes)
        )

    # 3. 미완성 노트 (links < 8)
    underconnected = find_notes(links_count__lt=8)
    suggestions.append({
        'type': 'todo',
        'notes': underconnected,
        'action': 'Add more links'
    })

    return suggestions
```

## Quick Jump

**Command:**
```
/find xcom
```

**Results (Fast!):**
```
🎯 Quick Match:

⭐️⭐️⭐️⭐️⭐️ [[XCom-S3-패턴]] 🌲
  - Evergreen
  - 12 links
  - Referenced: 3 times
  - Last accessed: 2 days ago

⭐️⭐️⭐️⭐️ [[Airflow-공식문서-XCom]]
  - Literature
  - Source: Airflow Docs

⭐️⭐️⭐️ [[DataHub-OIDC/notes.md]]
  - Project note
  - Mentions XCom

📝 Did you mean?
- [[TaskFlow-API]] (similar topic)
```

## Search Filters

```yaml
By Type:
  /find type:permanent airflow
  /find type:project active

By Status:
  /find status:evergreen python
  /find status:seedling needs-attention

By Date:
  /find created:2025-11
  /find updated:last-week

By Links:
  /find links:0 (orphans)
  /find links:10+ (well-connected)

Combined:
  /find type:permanent status:evergreen #airflow links:8+
```

## Search History

```markdown
# 🔍 Search History

**Today:**
- "airflow xcom s3" → Found 3 notes
- "keycloak oidc" → Found 5 notes

**This Week:**
- "dbt incremental" → Not found ⚠️
  → Knowledge gap detected!

**Most Searched (This Month):**
1. "airflow" (12 times)
2. "datahub" (8 times)
3. "python" (7 times)
```

## Performance Metrics

```yaml
Target: < 30초
Actual: < 5초 ✅

Metrics:
  - Semantic search: ~2초 (626 notes)
  - Tag search: <1초
  - Graph traversal: <3초
  - Quick jump: <0.5초

Optimizations:
  - Pre-computed embeddings
  - Indexed tags
  - Cached graph
```

## Integration

- **Linker Agent**: 검색 결과를 링크 추천에 활용
- **Synthesizer Agent**: 자주 검색되는 주제 → MOC 제안
- **Reviewer Agent**: 검색 통계를 Weekly dashboard에 포함

---

**Last Updated**: 2025-11-30
**Version**: 1.0
