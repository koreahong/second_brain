---
cssclass: dashboard
---

# 🧠 DAE Second Brain Dashboard

> 마지막 업데이트: `= date(now)`

## 🚀 진행 중인 프로젝트

```dataview
TABLE status as "상태", start as "시작일", area as "영역"
FROM "1-Projects"
WHERE status = "진행중"
SORT start DESC
```

## 📅 오늘 (Daily Note)

![[{{date:YYYY-MM-DD}}]]

## 💡 최근 학습 (7일)

```dataview
TABLE type as "타입", concept as "개념", importance as "중요도"
FROM "Learning"
WHERE created >= date(now) - dur(7 days)
SORT created DESC
LIMIT 10
```

## 🔥 최근 해결한 문제

```dataview
TABLE severity as "심각도", status as "상태", project as "프로젝트"
FROM "Learning/Problems"
WHERE status = "해결됨"
SORT created DESC
LIMIT 5
```

## 📊 영역별 현황

### Data Governance
```dataview
LIST
FROM "2-Areas/Data-Governance"
```

### Technology
```dataview
LIST
FROM "2-Areas/Technology"
```

## 📈 이번 주 통계

**작성한 노트**: `= length(filter(file.folder, (f) => contains(f, "Daily"))) `
**진행 중인 프로젝트**: `= length(filter("1-Projects", (p) => p.status = "진행중"))`
**새로운 학습**: `= length(filter("Learning", (l) => l.created >= date(now) - dur(7 days)))`

## 🎯 이번 주 목표

- [ ]
- [ ]
- [ ]

## 🔖 Quick Links

### 자주 쓰는 영역
- [[Metadata-Management]]
- [[Storage]]
- [[Lineage]]

### 템플릿
- [[Templates/daily-note]]
- [[Templates/project]]
- [[Templates/learning]]
- [[Templates/problem-solving]]

### Inbox
```dataview
LIST
FROM "0-Inbox"
SORT file.mtime DESC
```

## 📚 최근 아카이브

```dataview
TABLE status, start, end
FROM "4-Archives"
SORT end DESC
LIMIT 5
```

## 🌐 Graph View

![[graph.png]]

## 🔍 빠른 검색

**태그 클라우드:**
#DataHub #Keycloak #Snowflake #Airflow #DBT #권한관리 #성능최적화

---

**Shortcuts:**
- `Cmd + O`: Quick Switcher
- `Cmd + Shift + F`: Global Search
- `Cmd + G`: Graph View
- `Cmd + T`: New Daily Note
