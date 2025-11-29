---
title: "lateral 사용 == unpivotr"
source: notion
notion_id: 1f2c6d43-3b4d-80e3-a2da-ca7592025b10
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["Query"]
링크: []
최종편집시각: "2025-05-20T07:43:00.000Z"
제목: ""
상위 항목: []
PARA: "Resource"
tags: ["Query", "레퍼런스", "notion-import"]
---

```sql
SELECT 
  p.product_id,
  v.store,
  v.price
FROM Products p,
LATERAL (
  VALUES
    ('store1', p.store1),
    ('store2', p.store2),
    ('store3', p.store3)
) AS v(store, price)
WHERE v.price IS NOT NULL;
```

lateral은 unpivot과 같다.

lateral + value로 기존 테이블에서 어떤 컬럼을 unpivot할지 정하고

나중에 select문에 나머지 컬럼에 대해서 작성하면 됨.

```sql
SELECT product_id, 'store1' AS store, store1 AS price
FROM Products
WHERE store1 IS NOT NULL

UNION ALL

SELECT product_id, 'store2' AS store, store2 AS price
FROM Products
WHERE store2 IS NOT NULL

UNION ALL

SELECT product_id, 'store3' AS store, store3 AS price
FROM Products
WHERE store3 IS NOT NULL;
```

