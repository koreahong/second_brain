---
title: "임의 테이블 생성, union vs values"
source: notion
notion_id: 1f2c6d43-3b4d-8085-b56b-ebf6183fc0fc
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["Query"]
링크: []
최종편집시각: "2025-05-19T02:09:00.000Z"
제목: ""
상위 항목: []
PARA: "Resource"
tags: ["Query", "레퍼런스", "notion-import"]
---

### ⚖️ 비교 요약

### ✅ 1. VALUES 사용 예시 (2컬럼)

```sql

SELECT *
FROM (
    VALUES
        ('Low Salary', 0),
        ('Average Salary', 0),
        ('High Salary', 0)
) AS salary_levels(category, accounts_count);


```

특징

- 간결하고 직관적임
- 컬럼명 직접 지정 가능 (AS alias(col1, col2))
- 정적인 값들 나열할 때 유리 (예: 기준 목록, 레퍼런스 테이블)
---

### ✅ 2. UNION ALL 사용 예시 (2컬럼)

```sql
sql
복사편집
SELECT 'Low Salary' AS category, 0 AS accounts_count
UNION ALL
SELECT 'Average Salary', 0
UNION ALL
SELECT 'High Salary', 0;


```

특징

- SELECT 문법을 그대로 따름
- 동적 조건이 포함된 서브쿼리와 혼합하기 쉬움
- 하지만 값이 많아질수록 중복된 코드가 많아져서 지저분함
---

