# Template Formatter 자동화 시스템

## 📋 개요

Notion RecordMaster의 데이터를 각 Content Type의 템플릿에 맞게 자동으로 포매팅하는 시스템입니다.

### 핵심 기능

```
Notion Record Master
    ↓
    [Content_Type 감지]
    ├─ Project    → Project 템플릿
    ├─ Experience → Experience 템플릿
    ├─ Reference  → Reference 템플릿
    ├─ Insight    → Insight 템플릿
    ├─ Article    → Article 템플릿
    └─ Book       → Book 템플릿
    ↓
    [데이터 추출 및 정규화]
    ├─ 제목 (Title)
    ├─ 카테고리 (Categories)
    ├─ 태그 (Tags)
    ├─ 날짜 (Period/Created)
    ├─ 회사 (Company)
    └─ 커스텀 콘텐츠 필드
    ↓
    [템플릿 변수 치환]
    ├─ {{title}} → 실제 제목
    ├─ {{date}} → 생성 날짜
    ├─ {{category}} → 분류
    └─ [Template-specific variables]
    ↓
    [Frontmatter 자동 생성]
    ├─ tags: 배열 (카테고리 + 태그)
    ├─ created: YYYY-MM-DD (생성일)
    ├─ updated: YYYY-MM-DD (수정일)
    ├─ type: content_type
    ├─ title: {{title}}
    └─ [Template-specific metadata]
    ↓
    [Obsidian 마크다운 생성]
    └─ [frontmatter] + [template content]
```

---

## 🎯 Content Type별 포매팅 규칙

### 1. Article 📰

**Notion 필드:**
- Title → 기사 제목
- Content_Type = "Article"
- Category → 태그
- Period → 발행/수집 날짜
- [추가 필드 가능] URL, Source, Summary

**템플릿 변수:**
```markdown
# {{title}}

## 📌 주요 이슈 요약
- (3가지 포인트)

## 🌍 배경 및 맥락
...

[나머지 섹션]
```

**Frontmatter:**
```yaml
tags:
  - article
  - {{category}}  # Technology, Career, etc.
created: {{period_date}}
updated: {{updated_date}}
title: {{title}}
type: article
```

---

### 2. Book 📕

**Notion 필드:**
- Title → 책 제목
- Content_Type = "Book"
- Category → 주제
- Period → 읽은 날짜
- [추가 필드 가능] Author, Publisher

**템플릿 변수:**
```markdown
# {{title}}

## 📌 핵심 메시지
1. ...
2. ...
3. ...

[나머지 섹션]
```

**Frontmatter:**
```yaml
tags:
  - book
  - {{category}}
created: {{period_date}}
updated: {{updated_date}}
title: {{title}}
type: book
```

---

### 3. Experience 📝

**Notion 필드:**
- Title → 주간 요약
- Content_Type = "Experience"
- Category → Reflection, Career, etc.
- Period → 주차 날짜
- [추가 필드 가능] Summary, Lessons, Metrics

**템플릿 변수:**
```markdown
# {{title}}

## 📋 주간 요약
{{summary}}

## 🎯 주요 업무
[자동으로 템플릿 섹션 생성]

[나머지 ORID 섹션]
```

**Frontmatter:**
```yaml
tags:
  - experience
  - {{category}}
created: {{period_date}}
updated: {{updated_date}}
title: {{title}}
type: experience
company: {{company}}
week: {{period_week_number}}
```

---

### 4. Insight 💡

**Notion 필드:**
- Title → 깨달음 제목
- Content_Type = "Insight"
- Category → Work, Personal, etc.
- Period → 인사이트 발생 날짜
- [추가 필드 가능] Context, Lesson

**템플릿 변수:**
```markdown
# {{title}}

## 💡 핵심 인사이트
{{insight_summary}}

## 📖 경험 (Context)
[자동 섹션]

[나머지 섹션]
```

**Frontmatter:**
```yaml
tags:
  - insight
  - {{category}}
created: {{period_date}}
updated: {{updated_date}}
title: {{title}}
type: insight
```

---

### 5. Reference 📚

**Notion 필드:**
- Title → 기술/개념명
- Content_Type = "Reference"
- Category → Technology, Data-Governance, etc.
- Period → 학습/정리 날짜
- [추가 필드 가능] Description, Tags

**템플릿 변수:**
```markdown
# {{title}}

## 📋 개요
{{description}}

## 🎯 핵심 개념
[자동 섹션]

[나머지 섹션]
```

**Frontmatter:**
```yaml
tags:
  - reference
  - {{category}}
created: {{period_date}}
updated: {{updated_date}}
title: {{title}}
type: reference
```

---

### 6. Project 🎯

**Notion 필드:**
- Title → 프로젝트명
- Content_Type = "Project"
- Category → 프로젝트 카테고리
- Period → 프로젝트 기간
- [추가 필드 가능] Status, Objectives, Results

**템플릿 변수:**
```markdown
# {{title}}

## 🎯 목표
{{objectives}}

## 📅 기간
{{period}}

[나머지 섹션]
```

**Frontmatter:**
```yaml
tags:
  - project
  - {{category}}
created: {{period_date}}
updated: {{updated_date}}
title: {{title}}
type: project
status: {{status}}
```

---

## 🔧 구현 구조

### 파일 구조
```
automation/
├── template_formatter.py      # 메인 포매터 엔진
├── formatters/
│   ├── __init__.py
│   ├── base_formatter.py      # 기본 포매터 클래스
│   ├── article_formatter.py   # Article 특화
│   ├── book_formatter.py      # Book 특화
│   ├── experience_formatter.py # Experience 특화
│   ├── insight_formatter.py   # Insight 특화
│   ├── reference_formatter.py # Reference 특화
│   └── project_formatter.py   # Project 특화
├── templates/
│   ├── article.md
│   ├── book.md
│   ├── experience.md
│   ├── insight.md
│   ├── reference.md
│   └── project.md
└── tests/
    └── test_formatters.py
```

### 클래스 다이어그램

```python
# base_formatter.py
class BaseFormatter:
    """모든 포매터의 기본 클래스"""

    def __init__(self, record: dict, template: str):
        self.record = record
        self.template = template
        self.content_type = record['Content_Type']

    def extract_fields(self) -> dict:
        """Notion 레코드에서 필드 추출"""
        pass

    def generate_frontmatter(self) -> dict:
        """Frontmatter 자동 생성"""
        pass

    def substitute_variables(self) -> str:
        """템플릿 변수 치환"""
        pass

    def format(self) -> str:
        """최종 포매팅 수행"""
        return f"---\n{self._render_frontmatter()}\n---\n\n{self._render_body()}"

# article_formatter.py
class ArticleFormatter(BaseFormatter):
    """Article 특화 포매터"""
    pass

# [다른 포매터들...]
```

### 메인 Flow

```python
def format_record(notion_record: dict) -> str:
    """Notion 레코드를 Obsidian 마크다운으로 변환"""

    # 1. Content Type에 따라 적절한 포매터 선택
    content_type = notion_record['Content_Type']['select']['name']
    formatter_class = FORMATTER_REGISTRY[content_type]

    # 2. 템플릿 로드
    template = load_template(content_type)

    # 3. 포매터 생성 및 실행
    formatter = formatter_class(notion_record, template)
    formatted = formatter.format()

    return formatted
```

---

## 📝 예제

### Input: Notion Record (Article)

```json
{
  "properties": {
    "이름": {
      "title": [{"text": {"content": "빅블러 시대, 산업의 경계를 허무는 마케팅이 인기를 끄는 이유"}}]
    },
    "Content_Type": {
      "select": {"name": "Article"}
    },
    "Category": {
      "multi_select": [{"name": "Reading"}]
    },
    "Period": {
      "date": {"start": "2022-05-29"}
    },
    "Created": {
      "created_time": "2025-11-30T11:55:00.000Z"
    }
  }
}
```

### Output: Obsidian Markdown

```markdown
---
tags:
  - article
  - reading
created: 2022-05-29
updated: 2025-11-30
title: 빅블러 시대, 산업의 경계를 허무는 마케팅이 인기를 끄는 이유
type: article
---

# 빅블러 시대, 산업의 경계를 허무는 마케팅이 인기를 끄는 이유

## 📌 주요 이슈 요약

💡 이 글의 핵심 메시지 3가지

-
-
-

## 🌍 배경 및 맥락

왜 이 글이 쓰여졌는가? 어떤 상황/트렌드와 연관되는가?

[... 나머지 템플릿 섹션]
```

---

## 🔌 Integration Points

### 1. notion_sync.py와의 연계

```python
# notion_sync.py에서
from template_formatter import format_record

class RecordMasterSync:
    def sync_record(self, notion_record):
        # 기존 코드...

        # 포매터로 변환
        formatted_content = format_record(notion_record)

        # Obsidian에 저장
        self.save_to_obsidian(formatted_content, file_path)
```

### 2. 자동화 설정

```json
// config.json 추가
{
  "formatter": {
    "enabled": true,
    "auto_substitute_variables": true,
    "auto_generate_frontmatter": true,
    "tag_strategy": "combine"  // category + tags 합치기
  }
}
```

---

## ✅ Validation Rules

### 필수 필드 검증

```python
REQUIRED_FIELDS = {
    'Article': ['title', 'content_type'],
    'Book': ['title', 'content_type'],
    'Experience': ['title', 'content_type', 'period'],
    'Insight': ['title', 'content_type'],
    'Reference': ['title', 'content_type'],
    'Project': ['title', 'content_type', 'period']
}
```

### 날짜 형식 정규화

```python
# 입력: 다양한 날짜 형식
# 출력: YYYY-MM-DD

formats_to_try = [
    '%Y-%m-%d',
    '%Y-%m-%d %H:%M:%S',
    '%d/%m/%Y',
    '%Y/%m/%d'
]
```

---

## 🧪 Testing

### Unit Tests

```bash
pytest automation/tests/test_formatters.py -v
```

### Integration Tests

```bash
# 실제 Notion 레코드로 테스트
python automation/tests/test_integration.py
```

---

## 🎯 마이그레이션 전략

### Phase 1: 포매터 개발
- [ ] BaseFormatter 구현
- [ ] 6가지 포매터 구현
- [ ] 템플릿 변수 정의

### Phase 2: 통합 테스트
- [ ] notion_sync.py와 연계
- [ ] Frontmatter 생성 검증
- [ ] 파일 생성 테스트

### Phase 3: 운영
- [ ] GitHub Actions 적용
- [ ] 자동화 모니터링
- [ ] 오류 처리 및 로깅

---

## 📚 참고

- **템플릿 위치**: [99-Assets/Templates/](../99-Assets/Templates/)
- **마스터 DB**: RecordMaster (2bbc6d43-3b4d-803e-8f1c-dc23bda7b7c7)
- **관련 문서**: [SCHEMA.md](SCHEMA.md), [SETUP.md](SETUP.md)

---

**Last Updated**: 2025-12-02
**Status**: Design Phase
