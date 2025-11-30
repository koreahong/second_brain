---
title: 'exists 활용 '
type: resource
tags:
  - query
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

## 🔥 한 줄 정리

> 모든 조건을 만족해야 할 때 (ALL) → NOT EXISTS

---

## 📌 왜 그런지 예제로 설명

---

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
  → 즉, 모든 전공 과목에서 A 받아야 통과

---

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

---

## 💡 왜 그런 구조가 되는가?

SQL에서는 NOT EXISTS (...)는 부정을 통해 전체 만족을 표현함:

- “A를 안 받은 과목이 하나도 없다” → “모든 과목에서 A를 받았다”
  → 부정을 통해 전체 조건 만족을 표현

반면 EXISTS (...)는 “조건을 만족하는 게 하나라도 있다” → 부분 만족이면 충분

---

## ✅ 기억법 요약

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

