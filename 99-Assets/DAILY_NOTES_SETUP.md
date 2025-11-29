---
created: 2025-11-28
type: documentation
tags:
- anger
- achievement
- learning
- data
- project
- goal
- planning
- python
updated: '2025-11-30'
title: DAILY_NOTES_SETUP
aliases: []
---

# Daily Notes 설정 가이드

## 📅 구조

```
Flow/
├── Daily/           # 매일 회고
│   └── YYYY-MM-DD.md
├── Weekly/          # 주간 회고
│   └── YYYY-Wnn.md
└── Monthly/         # 월간 회고
    └── YYYY-MM.md
```

---

## 🎯 Daily Notes 사용법

### 1. 자동 생성 (Obsidian Settings)
1. Settings → Core Plugins → Daily notes 활성화
2. Date format: `YYYY-MM-DD`
3. New file location: `Flow/Daily`
4. Template: `Templates/daily-note.md`

### 2. 단축키
- `Ctrl/Cmd + P` → "Open today's daily note"
- 또는 좌측 캘린더 아이콘 클릭

### 3. Calendar 플러그인
Calendar 플러그인 설치하면 캘린더 뷰에서 날짜 클릭으로 생성 가능

---

## 📝 템플릿 구조

### Daily Note (매일 회고)
```yaml
---
created: YYYY-MM-DD
type: daily
tags: [daily, retrospective]
---

# YYYY-MM-DD (요일)

## 🎯 오늘의 목표
- [ ]
- [ ]

## 🚀 진행 중인 프로젝트
- [[프로젝트명]]:

## 💡 배운 점
### 새로운 개념
- [[개념]] -

### 문제 해결
- **문제**:
- **해결**:
- 관련 노트: [[]]

## 🔥 시행착오
### 이슈
**시도 1**:
**시도 2**:
**해결**:

## 🌟 하이라이트
**가장 중요한 것 3가지:**
1.
2.
3.

## 📅 내일 할 일
- [ ]
- [ ]

---
**에너지**: ⭐⭐⭐⭐⭐
**생산성**: ⭐⭐⭐⭐⭐
**학습량**: ⭐⭐⭐⭐⭐
```

---

## 🔄 Notion → Obsidian 마이그레이션

### 1. Notion Export
1. Notion 데이터베이스 열기
2. `...` → `Export`
3. Format: `Markdown & CSV` 선택
4. `Include subpages` 체크
5. Export

### 2. Import 스크립트
```python
# 스크립트로 자동 변환
python import_daily_notes.py <export-folder>
```

### 3. 수동 변환 (필요시)
- Notion 날짜 형식 → YYYY-MM-DD.md로 rename
- 메타데이터 추가
- 링크 구조 수정

---

## 📊 Daily Notes 활용

### Dataview로 통계 보기
```dataview
TABLE
  choice(contains(file.outlinks, ""), "✅", "❌") as "배움",
  choice(contains(file.outlinks, ""), "✅", "❌") as "프로젝트"
FROM "Flow/Daily"
WHERE file.day
SORT file.name DESC
LIMIT 30
```

### 최근 7일 회고
```dataview
LIST
FROM "Flow/Daily"
WHERE file.day >= date(today) - dur(7 days)
SORT file.name DESC
```

### 월별 통계
```dataview
TABLE
  length(file.outlinks) as "연결된 노트",
  length(rows) as "작성일"
FROM "Flow/Daily"
WHERE file.day
GROUP BY dateformat(file.day, "yyyy-MM") as Month
SORT Month DESC
```

---

## 🎯 회고 작성 원칙

### 매일 (5-10분)
- [ ] 오늘 한 일 3가지
- [ ] 배운 점 1가지
- [ ] 내일 할 일 3가지

### 주간 (20-30분)
- [ ] 이번 주 성과
- [ ] 배운 점 정리
- [ ] 다음 주 계획

### 월간 (1시간)
- [ ] 이번 달 하이라이트
- [ ] 목표 달성도
- [ ] 다음 달 OKR

---

## 🔗 연결 구조

```
Daily Note → Projects (진행 중인 프로젝트)
          → Knowledge/Concepts (배운 개념)
          → Knowledge/Experiences (겪은 경험)
          → Weekly Review (주간 회고)
```

---

## 💡 팁

### 1. 꾸준함이 핵심
- 매일 5분이라도 작성
- 비어있어도 OK (날짜 기록이 중요)
- 완벽하게 쓰려고 하지 말기

### 2. 링크 활용
- 배운 개념은 Concept 노트 생성
- 문제 해결은 Experience 노트 생성
- 프로젝트와 연결

### 3. 템플릿 커스터마이징
- 본인에게 맞는 구조로 수정
- 필요없는 섹션 제거
- 필요한 섹션 추가

---

## 📅 캘린더 뷰

Calendar 플러그인 설치 후:
- 좌측 사이드바에 캘린더 표시
- 날짜 클릭으로 Daily Note 생성/열기
- Dot으로 작성 여부 표시

---

*Last Updated: 2025-11-28*
*Status: Setup Complete*

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

