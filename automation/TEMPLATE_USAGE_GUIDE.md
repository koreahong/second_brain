# 📋 RecordMaster Template Usage Guide

## 🎯 Overview

These templates are designed based on **your actual writing patterns** combined with research-based frameworks to help you create richer, more meaningful content in Notion that flows seamlessly to Obsidian for knowledge network building.

## 📊 Your Writing Pattern Analysis

From analyzing your Notion databases, I found:

**크래프트 회고 (Weekly Reflections)**:
- Notion: Brief bullet points
- Obsidian: Rich structure with 주간 요약, 주요 업무, 인사이트, 관련 프로젝트, 메트릭

**컨텐츠 리스트 (Articles)**:
- Structured analysis: 주요 이슈 요약 → 배경 및 맥락 → 주요 내용 요약 → 시사점 및 인사이트

**Templates now guide you to create the rich Obsidian-style content directly in Notion!**

---

## 📋 Template 1: Project

**When to use**: Starting a new work project, initiative, or technical task

**Frameworks combined**:
- SMART Goals (목표 설정)
- STAR (Situation-Task-Action-Result)
- KPT (Keep-Problem-Try 회고)

### How to fill it out:

#### 1️⃣ 📋 프로젝트 개요
- **One sentence** describing what and why
- Example: "DataHub를 도입하여 메타데이터를 통합 관리하고 데이터 거버넌스를 확립"

#### 2️⃣ 🎯 목표 (SMART)
Fill each bullet to ensure your goal is well-defined:
- **Specific**: "38개 데이터 asset의 lineage 추적"
- **Measurable**: "메타데이터 수집 자동화율 100%"
- **Achievable**: "기존 Airflow/DBT 활용"
- **Relevant**: "데이터 품질 이슈 80% 감소 목표"
- **Time-bound**: "2025-11-30까지"

#### 3️⃣ 🔍 현황 분석 (STAR)
- **Situation**: 현재 무엇이 문제인가?
- **Task**: 구체적으로 무엇을 해결해야 하나?

#### 4️⃣ 🛠️ 구현 계획
- 기술 스택과 마일스톤을 구체적으로
- Phase별로 나누면 진행 상황 추적 용이

#### 5️⃣ 💡 인사이트 & 회고 (KPT)
프로젝트 진행하면서 지속적으로 업데이트:
- **Keep**: 잘했던 것 (예: "Custom Source 개발로 Airflow 3.x 호환")
- **Problem**: 문제점 (예: "URN 인코딩 불일치")
- **Try**: 다음에 시도할 것

### 💡 Pro Tips:
- 프로젝트 시작할 때: 목표와 현황 분석 먼저
- 진행 중: 완료 사항, 성과, 메트릭 업데이트
- 완료 후: KPT 회고로 마무리

---

## 📝 Template 2: Experience (Weekly)

**When to use**: 매주 금요일 또는 주말에 한 주를 회고할 때

**Frameworks combined**:
- Your actual Obsidian structure (주간 요약, 주요 업무, 인사이트, 메트릭)
- ORID (Objective-Reflective-Interpretive-Decisional)

### How to fill it out:

#### 1️⃣ 📋 주간 요약
- **한 문장**으로 이번 주를 정의
- Example: "이번 주는 **DataHub 론칭**을 완료한 주입니다"

#### 2️⃣ 🎯 주요 업무
각 프로젝트별로:
- **완료 사항**: 구체적으로 무엇을 했는가
- **기술적 성과**: 어떤 기술적 도전을 해결했는가

Your actual pattern from Obsidian:
```markdown
### DataHub 론칭

**완료 사항**:
- Airflow 3.x와 DataHub 연동 (Custom Source 개발)
- DBT 메타데이터 자동 수집

**기술적 성과**:
- Local, Dev, Prod 환경 분리
- 권한 관리 (Keycloak 그룹 기반)
```

#### 3️⃣ 💡 인사이트
이번 주 배운 것을 섹션별로:
- 각 인사이트에 제목 붙이기
- 무엇을 배웠고 왜 중요한지 설명

#### 4️⃣ 🤔 ORID 회고
더 깊은 성찰을 위해:
- **Objective**: 무슨 일이 있었나? (사실)
- **Reflective**: 어떤 감정? 무엇이 인상깊었나?
- **Interpretive**: 왜 그런 일이? 무엇을 배웠나?
- **Decisional**: 다음 주 무엇을 할 것인가?

#### 5️⃣ 📊 메트릭
Your actual pattern:
```markdown
| 항목 | 수치 |
|------|------|
| 수집 Assets | 38개 |
| Task Dependencies | 79개 |
```

### 💡 Pro Tips:
- 금요일 오후에 작성하면 신선한 기억
- 🔗 관련 프로젝트, 📚 관련 지식에 백링크 추가
- Obsidian 동기화 후 자동으로 네트워크 형성됨

---

## 📚 Template 3: Reference

**When to use**: 새로운 기술, 개념, 도구를 배울 때

**Frameworks combined**:
- Feynman Technique (단순하게 설명)
- First Principles (근본 원리)
- Zettelkasten (연결 가능한 원자적 노트)

### How to fill it out:

#### 1️⃣ 📋 개요
- **한 문장**으로 설명 (Feynman: 12살 아이에게 설명하듯)
- Example: "Airflow는 데이터 파이프라인을 스케줄링하고 모니터링하는 워크플로우 관리 도구"

#### 2️⃣ 🎯 핵심 개념
- **3가지만** 뽑기
- 가장 중요한 것부터 순서대로

#### 3️⃣ 🔍 상세 설명
- **First Principles**: 왜 만들어졌는가? 어떤 문제 해결?
- **작동 방식**: 비유를 사용해서 설명
  - Example: "Airflow는 오케스트라 지휘자처럼..."

#### 4️⃣ 💻 실전 활용
- **언제 사용**: Concrete use cases
- **Best Practices**: 실제 사용 경험
- **코드 예제**: 간단하고 실행 가능한 예제

#### 5️⃣ 🔗 관련 개념
Zettelkasten 원칙:
- 유사 기술과 비교
- 대안 기술 언급
- 함께 사용하는 기술 연결

### 💡 Pro Tips:
- 공식 문서 읽으면서 작성
- "왜?"를 3번 묻기 (First Principles)
- 다른 Reference와 적극 연결

---

## 💡 Template 4: Insight (본깨적)

**When to use**: 삶이나 업무에서 "아하!" 순간이 왔을 때

**Frameworks combined**:
- First Principles (근본 원리 파악)
- Mental Models (재사용 가능한 사고 프레임워크)
- Action-oriented (실천 계획)

### How to fill it out:

#### 1️⃣ 💡 핵심 인사이트
- **한 문장**으로 깨달음 표현
- Example: "데이터 거버넌스는 기술이 아니라 문화다"

#### 2️⃣ 📖 경험 (Context)
- 언제, 어디서, 무슨 일이 있었나
- 구체적인 상황 묘사

#### 3️⃣ 🤔 생각의 흐름
- **처음 생각**: "처음엔 DataHub만 도입하면 해결될 줄 알았다"
- **전환점**: "하지만 팀원들이 사용하지 않았다"
- **깨달음**: "도구보다 팀의 문화와 프로세스가 중요하다"

#### 4️⃣ 🎯 First Principles 분석
- 가정 벗겨내기
- 근본 원리 찾기
- 새로운 접근 방법

#### 5️⃣ 🧠 Mental Model
이 인사이트를 **다른 상황에도 적용**:
- 업무:
- 개인생활:
- 관계:

#### 6️⃣ ✅ 실천 계획
Insight는 행동으로:
- **즉시 실천**: 내일 당장 할 수 있는 것
- **습관화**: 꾸준히 할 것
- **장기 목표**: 6개월~1년 목표

### 💡 Pro Tips:
- 감정이 동할 때 바로 작성
- Mental Model로 만들면 재사용 가능
- 관련 인사이트와 연결

---

## 📰 Template 5: Article

**When to use**: 유용한 아티클이나 블로그 읽었을 때

**Frameworks combined**:
- Your '컨텐츠 리스트' structure (주요 이슈, 배경, 내용, 시사점)
- Progressive Summarization (중요한 것만 계층적으로)

### How to fill it out:

#### 1️⃣ 📌 주요 이슈 요약
Your actual pattern:
```markdown
- 핵심 메시지 1
- 핵심 메시지 2
- 핵심 메시지 3
```

#### 2️⃣ 🌍 배경 및 맥락
- 왜 이 글이 쓰여졌나?
- 어떤 트렌드/상황과 연관?

#### 3️⃣ 📝 주요 내용 요약
Progressive Summarization 원칙:
1. 첫 읽기: 전체 훑기
2. 두 번째: 중요한 부분 하이라이트
3. 세 번째: 핵심만 요약

섹션별로 정리:
```markdown
### [섹션 1 제목]
- 핵심 포인트 1
- 핵심 포인트 2
```

#### 4️⃣ 💡 시사점 및 인사이트
Your actual pattern:
- **내게 주는 교훈**:
- **업무 적용 가능성**:
- **의문점 & 추가 탐구**:

### 💡 Pro Tips:
- 나중에 다시 읽을 필요 없게 작성
- 핵심만 추출 (Progressive Summarization)
- Action item 찾기

---

## 📕 Template 6: Book

**When to use**: 책을 다 읽고 정리할 때

**Frameworks combined**:
- Progressive Summarization
- Action-oriented approach

### How to fill it out:

#### 1️⃣ 📌 핵심 메시지
- **Top 3만** 뽑기
- 나머지는 과감히 버리기

#### 2️⃣ 📖 챕터별 요약
**모든 챕터 요약하지 마세요!**
- 중요한 챕터만 선택
- 핵심 개념 + 인상깊은 문구

#### 3️⃣ 💡 Action Items
책은 읽는 것이 아니라 실천하는 것:
- **즉시 적용**: 내일부터
- **단기 (1개월)**:
- **장기 (3-6개월)**:

#### 4️⃣ 🎯 업무/삶에 적용
구체적으로:
- 업무에 어떻게 적용?
- 개인 성장에 어떻게 적용?

### 💡 Pro Tips:
- 읽으면서 메모 → 완독 후 정리
- 80/20 원칙: 20% 내용이 80% 가치
- 한 달 후 Action Items 실천 여부 체크

---

## 🔄 Workflow: Notion → Obsidian

### 1. Notion에서 작성
- 적절한 템플릿 선택 (Duplicate)
- Content_Type, Company, Category, Tags 설정
- 템플릿 가이드 따라 내용 작성
- Mig_Status를 "NEEDED"로 변경

### 2. 자동 동기화
- GitHub Actions가 매일 자동 실행
- 또는 수동: `python3 automation/notion_sync.py`

### 3. Obsidian에서 재분류
- `/organize` 명령어로 자동 분류
- 또는 수동으로 적절한 폴더로 이동
- 관련 노트와 백링크 생성

### 4. 지식 네트워크 구축
- Auto-Link Hook이 자동으로 관련 노트 연결
- 수동으로 더 깊은 연결 추가
- 태그와 백링크로 네트워크 강화

---

## 🎯 Best Practices

### ✅ DO

1. **템플릿의 질문에 답하기**
   - 빈 칸 채우기가 아니라, 질문에 대한 답변 작성

2. **구체적으로 작성**
   - "DataHub 설정" ❌
   - "Airflow 3.x와 DataHub 연동 (Custom Source 개발)" ✅

3. **백링크 활용**
   - Notion에서도 [[페이지명]] 형식으로 링크
   - Obsidian 동기화 후 자동 연결

4. **Properties 정확히 설정**
   - Company, Category, Tags는 Frontmatter로 변환됨
   - 일관된 태그 사용

5. **지속적 업데이트**
   - 프로젝트는 진행하면서 업데이트
   - Weekly는 매주 작성
   - 완료 후 회고 추가

### ❌ DON'T

1. **템플릿을 그대로 두지 마세요**
   - 가이드는 지우고 내용으로 채우기

2. **너무 완벽하게 쓰려 하지 마세요**
   - 일단 쓰고 나중에 다듬기
   - 80% 완성도면 충분

3. **모든 필드를 채우려 하지 마세요**
   - 관련 없는 섹션은 삭제
   - 필요한 것만 작성

4. **Notion에만 두지 마세요**
   - 정기적으로 Obsidian 동기화
   - 지식 네트워크 구축이 목표

---

## 🔧 Troubleshooting

### Q: 템플릿이 너무 길어요
A: 관련 없는 섹션은 삭제하세요. 템플릿은 가이드일 뿐입니다.

### Q: Obsidian 동기화가 안 돼요
A: Mig_Status가 "NEEDED"인지 확인하세요. "SKIP"은 동기화 안 됩니다.

### Q: 백링크가 작동하지 않아요
A: Notion에서 [[페이지명]] 형식으로 작성하고, Obsidian에서 정확한 파일명으로 수정하세요.

### Q: 어떤 템플릿을 써야 할지 모르겠어요
A:
- 업무 프로젝트 → Project
- 주간 회고 → Experience
- 기술 학습 → Reference
- 삶의 깨달음 → Insight
- 아티클 요약 → Article
- 책 정리 → Book

---

## 📚 Related Documents

- [automation/README.md](automation/README.md) - Automation overview
- [automation/AUTOMATION_SETUP.md](automation/AUTOMATION_SETUP.md) - Setup guide
- [.claude/CLAUDE.md](.claude/CLAUDE.md) - Project instructions

---

**Last Updated**: 2025-11-30
**Version**: 2.0 (Upgraded based on actual writing patterns)
