---
type: area
responsibility: 지속적
tags: [area]
---

# {{title}}

## 📖 정의

**이 영역은 무엇인가?**


**왜 중요한가?**


## 🎯 책임과 목표

**이 영역에서 내가 해야 하는 것:**
-
-
-

**성공 지표:**
-

## 🛠️ 주요 기술/도구

- [[기술1]]
- [[기술2]]
- [[기술3]]

## 📊 현재 프로젝트

```dataview
TABLE status, start
FROM "1-Projects"
WHERE contains(area, this.file.name)
SORT start DESC
```

## 📚 관련 학습

```dataview
LIST
FROM "Learning"
WHERE contains(concept, this.file.name)
SORT file.mtime DESC
LIMIT 10
```

## 🔥 주요 문제 해결

```dataview
TABLE status, severity
FROM "Learning/Problems"
WHERE contains(tags, "{{title}}")
SORT created DESC
```

## 🔗 관련 영역

**상위 영역:**
- [[]]

**하위 영역:**
- [[]]

**연관 영역:**
- [[]]

## 📈 성장 추적

### 2025-11
**시작 시점:**
-

**현재:**
-

**다음 단계:**
-

## 📝 핵심 개념

### [[개념1]]
-

### [[개념2]]
-

## 🎓 학습 로드맵

**기초:**
- [ ]

**중급:**
- [ ]

**고급:**
- [ ]

## 📚 참고 자료

**공식 문서:**
- [제목](URL)

**추천 아티클:**
- [[아티클1]]

**강의/코스:**
- [[코스1]]

---

**마지막 업데이트**: {{date:YYYY-MM-DD}}
**프로젝트 수**: `= length(filter(this.file.outlinks, (l) => contains(l.path, "1-Projects")))`
**학습 수**: `= length(filter(this.file.outlinks, (l) => contains(l.path, "Learning")))`
