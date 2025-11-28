---
title: exists 활용 
created: 2025-11-28
tags: ["reference", "migrated", "resource", "query"]
PARA: Resource
구분: ["Query"]
---

# exists 활용 

## 📝 내용

## 🔥 한 줄 정리

> 모든 조건을 만족해야 할 때 (ALL) → NOT EXISTS

## 📌 왜 그런지 예제로 설명

### ✅ NOT EXISTS → ALL 조건에 적합

```sql
-- 이 학생이 모든 전공 과목에서 A를 받았는가?
SELECT s.student_id
FROM students s
WHERE NOT EXISTS (
    SELECT 1
    FROM courses c
    WHERE c.major = s.major
    AND NOT EXISTS (
        SELECT 1
        FROM enrollments e
        WHERE e.student_id = s.student_id
          AND e.course_id = c.course_id
          AND e.grade = 'A'
    )
)
```

- 안쪽 NOT EXISTS → A 받은 적 없음

- 바깥 NOT EXISTS → 그런 과목이 하나도 없어야 함

### ✅ EXISTS → ANY 조건에 적합

```sql
-- 이 학생이 전공 과목 중 하나라도 A 받은 게 있는가?
SELECT s.student_id
FROM students s
WHERE EXISTS (
    SELECT 1
    FROM courses c
    JOIN enrollments e ON e.course_id = c.course_id
    WHERE c.major = s.major
      AND e.student_id = s.student_id
      AND e.grade = 'A'
)
```

→ 하나라도 A 받은 전공 과목이 있으면 EXISTS → TRUE → 통과

## 💡 왜 그런 구조가 되는가?

SQL에서는 NOT EXISTS (...)는 부정을 통해 전체 만족을 표현함:

- “A를 안 받은 과목이 하나도 없다” → “모든 과목에서 A를 받았다”

반면 EXISTS (...)는 “조건을 만족하는 게 하나라도 있다” → 부분 만족이면 충분

## ✅ 기억법 요약

## 🏷️ 분류

- **PARA**: Resource
- **구분**: Query

## 🔗 연결

**Hub**: [[_HUB_Database]], [[_HUB_Learning]]

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
