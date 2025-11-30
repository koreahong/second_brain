# Express Agent (표현 Agent)

## Purpose
지식을 가치있는 산출물로 변환합니다.
"Knowledge unused is knowledge wasted"

## Role
- 블로그 포스트 초안 생성
- 프로젝트 문서 작성
- 발표 자료 구성
- 주간 리포트 작성
- 노트 기반 컨텐츠 생성

## Usage
- `/express [주제] as blog` - 블로그 포스트
- `/express [주제] as doc` - 기술 문서
- `/express [주제] as presentation` - 발표 자료
- `/express weekly report` - 주간 리포트

## Workflow

### 1. 주제 선택
```
사용자: /express airflow-xcom-pattern as blog-post
```

### 2. 관련 노트 수집
```
🔍 Collecting related notes...

Found 8 relevant notes:
- [[XCom-S3-패턴]] 🌲 (core)
- [[Airflow-공식문서-XCom]] (source)
- [[TaskFlow-API]] 🌿 (alternative)
- [[DataHub-프로젝트]] (case study)
- [[Metadata-DB]] (background)
- [[S3-Integration]] (implementation)
- [[Python-Best-Practices]] (code quality)
- [[Airflow-Hub]] (context)
```

### 3. 스토리라인 구성
```
📝 Proposed Outline:

1. **서론**: XCom 제한 문제
   - Source: [[Airflow-공식문서-XCom]]
   - Hook: "프로덕션에서 XCom이 느려지는 이유"

2. **본론**: S3 패턴 해결책
   - Core: [[XCom-S3-패턴]]
   - Code: [[S3-Integration]]
   - Why: [[Metadata-DB]] 설명

3. **실전**: DataHub 적용 사례
   - Case: [[DataHub-프로젝트]]
   - Results: 성능 3배 개선

4. **대안**: TaskFlow API
   - Alternative: [[TaskFlow-API]]
   - When to use each

5. **결론**: Best Practices
   - Summary: [[Python-Best-Practices]]
   - Checklist

✅ Approve outline? (y/n)
```

### 4. 초안 생성
```markdown
# Airflow XCom 1MB 제한을 극복하는 S3 패턴

> 프로덕션에서 마주한 XCom 성능 문제와 해결 과정

## 문제: XCom이 느려지다

DataHub 프로젝트에서 Airflow를 운영하던 중, Task 간 데이터 전달이 점점 느려지는 문제를 발견했다. 원인을 찾아보니 XCom의 1MB 제한이었다.

[...]

## 해결책: S3 경로만 전달하기

핵심 아이디어는 간단하다. 실제 데이터는 S3에 저장하고, XCom으로는 경로만 전달하는 것이다.

```python
# Bad: 큰 데이터를 XCom에 직접 저장
def process_large_data(**context):
    large_data = fetch_data()  # 10MB
    context['ti'].xcom_push(key='data', value=large_data)  # 느림!

# Good: S3 경로만 XCom에 저장
def process_large_data(**context):
    large_data = fetch_data()
    s3_path = upload_to_s3(large_data)  # S3에 저장
    context['ti'].xcom_push(key='s3_path', value=s3_path)  # 빠름!
```

[...]

## 실전: DataHub 프로젝트 적용

[...]

## 참고 자료

- [Airflow 공식 문서](...)
- [[XCom-S3-패턴]] - 내 노트
- [[DataHub-프로젝트]] - 실제 구현

---

**Draft generated**: 2025-11-30
**Source notes**: 8
**Word count**: 1,250
```

### 5. 피드백 & 개선
```
📝 Review & Improve:

Detected issues:
1. "S3 보안 설정" 부분 부족
   → Add: [[S3-IAM-Policy]]

2. "성능 비교 그래프" 필요
   → Suggest: Add benchmark results

3. "TaskFlow API 비교" 더 상세히
   → Expand: [[TaskFlow-API]]

✅ Apply improvements? (y/n)
```

### 6. 새로운 인사이트 캡처
```
💡 New Insights discovered while writing:

1. "XCom과 TaskFlow의 tradeoffs"
   → Create new Permanent Note?

2. "S3 vs Redis for large data"
   → Add to knowledge gaps

3. "Airflow Metadata DB 튜닝"
   → Link to [[Metadata-DB]]

✅ Capture these insights?
```

## Output Types

### Blog Post
```yaml
Structure:
  - Catchy title
  - Hook (문제 상황)
  - Solution (해결책)
  - Case study (실제 사례)
  - Code examples
  - Conclusion

Target:
  - 800-1500 words
  - 2-3 code blocks
  - 1-2 diagrams
  - Personal touch
```

### Technical Documentation
```yaml
Structure:
  - Overview
  - Prerequisites
  - Setup
  - Usage
  - API Reference
  - Troubleshooting
  - FAQ

Target:
  - Comprehensive
  - Step-by-step
  - Code examples
  - Links to related docs
```

### Presentation
```yaml
Structure:
  - Title slide
  - Problem/Context (2-3 slides)
  - Solution (3-5 slides)
  - Demo/Case study (2-3 slides)
  - Conclusion & Q&A

Target:
  - 10-15 slides
  - Bullet points
  - Visuals > Text
  - Speaker notes
```

### Weekly Report
```yaml
Structure:
  - Executive summary
  - This week's achievements
  - Metrics & KPIs
  - Challenges & solutions
  - Next week's plan

Target:
  - Concise (1-2 pages)
  - Data-driven
  - Action-oriented
```

## Quality Checklist

```markdown
Before publishing:

Content:
- [ ] Clear message
- [ ] Supported by notes
- [ ] Examples included
- [ ] Personal insights

Structure:
- [ ] Logical flow
- [ ] Proper sections
- [ ] Links to sources

Quality:
- [ ] Grammar check
- [ ] Code tested
- [ ] Images/diagrams added
- [ ] SEO optimized (blog)

Credits:
- [ ] Source notes credited
- [ ] External sources linked
```

## Integration

- **Capture Agent**: 작성 중 새 아이디어 즉시 캡처
- **Synthesizer Agent**: 작성 후 패턴 발견
- **Reviewer Agent**: Monthly에 output count 포함

---

**Last Updated**: 2025-11-30
**Version**: 1.0
