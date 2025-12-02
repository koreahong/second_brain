# 템플릿 포매터 사용자 가이드

## 🎯 이것이 무엇인가요?

**템플릿 포매터**는 Notion의 RecordMaster 데이터베이스에 입력한 내용을 **자동으로** 각 Content Type의 템플릿에 맞게 변환하여 Obsidian에 저장하는 시스템입니다.

### 핵심 장점

```
Before (수동):
1. Notion에서 데이터 입력
2. 수동으로 템플릿 복사
3. 변수 치환 ({{title}} → 실제값)
4. Frontmatter 직접 작성
5. Obsidian에 복붙

After (자동화):
1. Notion에서 데이터 입력
2. Mig_Status = NEEDED로 설정
3. GitHub Actions 실행 (또는 수동 동기화)
4. ✨ 완료! Obsidian에 자동 생성됨
```

---

## 📋 현재 지원하는 Content Types

| Type | 설명 | 위치 |
|------|------|------|
| **Article** 📰 | 뉘앙스 있는 기사, 블로그 | 03-Resources/Articles/ |
| **Book** 📕 | 책 읽고 정리한 내용 | 03-Resources/Books/ |
| **Experience** 📝 | 주간 회고 / 업무 경험 | 02-Areas/Experience/Weekly/ |
| **Insight** 💡 | 깨달음 / 인생 관찰 | 30-Flow/Life-Insights/ |
| **Reference** 📚 | 기술 문서 / 개념 정리 | 03-Resources/Technology/ |
| **Project** 🎯 | 프로젝트 Hub | 02-Areas/Projects/ |

---

## 🚀 사용 방법

### Step 1: Notion에서 RecordMaster 열기

```
Notion → RecordMaster 데이터베이스
```

### Step 2: 새로운 레코드 생성

```
+ 새 항목 추가
```

### Step 3: 필수 정보 입력

| 필드 | 예시 | 설명 |
|------|------|------|
| **이름** | "빅블러 시대, 산업의 경계..." | 레코드의 제목 |
| **Content_Type** | Article | 어떤 타입의 콘텐츠인가 |
| **Category** | Technology, Career | 분류 (여러 개 선택 가능) |
| **Period** | 2025-12-02 | 관련 날짜 |
| **Company** | 크레프트테크놀로지스 | 회사 (선택) |

### Step 4: Mig_Status = NEEDED로 설정

```
Mig_Status: NEEDED  (필수!)
```

### Step 5: 자동화 실행

**방법 1: GitHub Actions 자동 실행**
- 매일 오전 9시 자동 실행
- 또는 GitHub Actions 탭에서 수동 실행

**방법 2: 로컬에서 수동 실행**
```bash
cd automation/
python notion_sync.py
```

### Step 6: 완료! Obsidian에서 확인

```
Obsidian에서 자동으로 생성된 파일 확인
↓
필요시 내용 추가 편집
```

---

## 📝 예제: Article 작성

### Notion에서 입력

```
이름: "빅블러 시대, 산업의 경계를 허무는 마케팅이 인기를 끄는 이유"
Content_Type: Article
Category: Technology, Reading
Period: 2025-12-02
Company: 아웃스탠딩
Mig_Status: NEEDED
```

### 자동 생성되는 Obsidian 파일

```markdown
---
tags:
  - article
  - reading
  - technology
created: 2025-12-02
updated: 2025-12-02
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

## 📝 주요 내용 요약

...

[나머지 템플릿]
```

---

## 🎨 Frontmatter 자동 생성 규칙

### 공통 필드 (모든 Content Type)

```yaml
tags:           # article, book, reference, insight, experience, project
created:        # Period 또는 Created 날짜 (YYYY-MM-DD)
updated:        # Updated 날짜 (YYYY-MM-DD)
title:          # 이름 필드
type:           # Content Type (소문자)
```

### Content Type별 추가 필드

**Experience만:**
```yaml
company: 크레프트테크놀로지스  # Company 필드
```

### 태그 자동 생성 규칙

```
tags = [
  Content_Type.lower(),           # article, book, ...
  ...Categories.lower(),          # technology, career, ...
  DEFAULT_TAGS_PER_TYPE           # reading, reflection, ...
]
```

**예시:**
```yaml
# Article + Category(Technology, Reading)
tags:
  - article
  - reading          # DEFAULT_TAGS
  - technology       # Category
```

---

## 🔄 템플릿 변수 치환

포매터가 자동으로 템플릿의 변수를 실제 값으로 바꿉니다.

### 현재 지원하는 변수

```markdown
# {{title}}           → 실제 제목으로 자동 변환
생성일: {{date}}     → YYYY-MM-DD로 자동 변환
회사: {{company}}    → 회사명으로 자동 변환 (Experience만)
```

### 사용 예

**원본 Template:**
```markdown
# {{title}}

생성일: {{date}}
회사: {{company}}
```

**자동 생성된 내용:**
```markdown
# 빅블러 시대, 산업의 경계를 허무는 마케팅

생성일: 2025-12-02
회사: N/A
```

---

## 🛠️ 동작 원리

### 포매팅 Flow

```
1. Notion에서 NEEDED 레코드 조회
   ↓
2. Content_Type 감지 (Article, Book, ...)
   ↓
3. 적절한 포매터 선택
   ArticleFormatter, BookFormatter, ...
   ↓
4. 필드 추출
   - 제목, 날짜, 카테고리, 회사명, ...
   ↓
5. Frontmatter 생성
   - 날짜 정규화 (YYYY-MM-DD)
   - 태그 생성 (Content_Type + Categories)
   ↓
6. 템플릿 로드
   99-Assets/Templates/{TYPE}.md
   ↓
7. 변수 치환
   {{title}}, {{date}}, {{company}} 등
   ↓
8. 최종 마크다운 생성
   --- (frontmatter) ---
   (본문)
   ↓
9. Obsidian에 저장
   /02-Areas/.../... (Content Type별)
   ↓
10. Mig_Status 업데이트
    NEEDED → MIGRATED
```

### 파일 구조

```
automation/
├── template_formatter.py          # 포매팅 엔진
│   ├── BaseFormatter              # 기본 포매터
│   ├── ArticleFormatter           # Article 특화
│   ├── BookFormatter              # Book 특화
│   ├── ExperienceFormatter        # Experience 특화
│   ├── InsightFormatter           # Insight 특화
│   ├── ReferenceFormatter         # Reference 특화
│   └── ProjectFormatter           # Project 특화
│
├── notion_sync.py                 # 메인 동기화 (통합)
├── test_formatter.py              # 테스트 스크립트
├── TEMPLATE_FORMATTER.md          # 상세 설계 문서
└── TEMPLATE_FORMATTER_GUIDE.md    # 이 파일
```

---

## 🧪 테스트

포매터가 제대로 작동하는지 확인하려면:

```bash
cd automation/
python test_formatter.py
```

**예상 출력:**
```
✅ Registry test passed
✅ Article formatter test passed
✅ Book formatter test passed
... (6개 포매터 모두)
✅ All tests passed!
```

---

## ⚠️ 주의사항

### DO ✅

- **Content_Type 필수:** 어떤 타입인지 반드시 설정
- **Mig_Status = NEEDED:** 동기화하려면 반드시 NEEDED로
- **이름(Title) 필수:** 제목이 없으면 "Untitled"로 생성됨
- **날짜 형식:** Period나 Created 중 하나는 있어야 함

### DON'T ❌

- **빈 Notion 레코드 동기화:** 최소한 제목은 입력
- **Content_Type 없이:** 동기화되지 않음
- **만든 후 템플릿 수정:** 다음 동기화 때 덮어씌워짐

---

## 🐛 문제 해결

### 문제: 파일이 생성되지 않음

**확인사항:**
1. Mig_Status = NEEDED 인가?
2. Content_Type이 설정되어 있는가?
3. 제목(이름)이 비어있지 않은가?

### 문제: Frontmatter가 깨짐

**확인사항:**
1. YAML 문법이 맞는가?
2. 중복된 태그가 있는가? (자동으로 제거됨)
3. 날짜 형식이 맞는가? (YYYY-MM-DD)

### 문제: 템플릿 변수가 치환되지 않음

**해결:**
- `{{title}}` (정확한 소문자)
- `{{company}}` (Experience만)
- `{{date}}`

---

## 📊 Content Type별 사용 시나리오

### Article 📰

**언제 사용:**
- 흥미로운 기사/블로그 발견
- 인사이트 있는 뉘앙스 있는 콘텐츠

**입력 예:**
```
이름: "팀장의 역할이 변하고 있다"
Content_Type: Article
Category: Career
Period: 2025-11-28
```

### Book 📕

**언제 사용:**
- 책을 읽고 정리
- 핵심 메시지 기록

**입력 예:**
```
이름: "The Lean Startup"
Content_Type: Book
Category: Technology, Career
Period: 2025-12-01
```

### Experience 📝

**언제 사용:**
- 주간 회고 작성
- 프로젝트 완료 후 정리

**입력 예:**
```
이름: "2025년 12월 1주차 회고"
Content_Type: Experience
Category: Reflection, Career
Period: 2025-12-02
Company: 크레프트테크놀로지스
```

### Insight 💡

**언제 사용:**
- 깨달음/명확화가 일어날 때
- 깊이 있는 생각 정리

**입력 예:**
```
이름: "데이터 거버넌스는 문화다"
Content_Type: Insight
Category: Life, Data-Governance
Period: 2025-12-01
```

### Reference 📚

**언제 사용:**
- 기술 개념 정리
- 프레임워크/도구 사용법

**입력 예:**
```
이름: "Apache Airflow DAG 작성"
Content_Type: Reference
Category: Technology, Data-Pipeline
Period: 2025-12-02
```

### Project 🎯

**언제 사용:**
- 프로젝트 Hub 생성
- 기술 스택 정리

**입력 예:**
```
이름: "DataHub 통합 구축"
Content_Type: Project
Category: Data-Governance, Technology
Period: 2025-11-15
```

---

## 📚 관련 문서

- **[TEMPLATE_FORMATTER.md](TEMPLATE_FORMATTER.md)** - 기술 설계 문서
- **[SCHEMA.md](SCHEMA.md)** - RecordMaster DB 스키마
- **[README.md](README.md)** - Automation 시스템 개요
- **[99-Assets/Templates/](../99-Assets/Templates/)** - 실제 템플릿 파일들

---

## 🎓 자주 묻는 질문

**Q: 템플릿을 커스터마이징할 수 있나요?**
A: 네! 99-Assets/Templates/ 디렉토리의 .md 파일을 수정하면 됩니다.

**Q: 특정 레코드만 동기화할 수 있나요?**
A: Mig_Status를 NEEDED로 설정한 것만 동기화됩니다.

**Q: 동기화 후 파일을 수정했는데, 다시 동기화되면 덮어씌워질까요?**
A: 네, 기본적으로 덮어씌워집니다. Mig_Status를 MIGRATED로 변경하면 안 됩니다.

**Q: 새로운 Content Type을 추가할 수 있나요?**
A: 현재는 6가지만 지원합니다. 추가하려면 template_formatter.py를 수정해야 합니다.

---

## 📞 지원

- **버그 보고:** GitHub Issues
- **기능 요청:** Notion RecordMaster에 코멘트
- **질문:** [CLAUDE.md](../.claude/CLAUDE.md) 참고

---

**Last Updated**: 2025-12-02
**Version**: 1.0
**Status**: Production Ready ✅
