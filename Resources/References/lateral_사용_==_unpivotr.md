---
title: lateral 사용 == unpivotr
created: 2025-11-28
tags: ["reference", "migrated", "resource", "query"]
PARA: Resource
구분: ["Query"]
---

# lateral 사용 == unpivotr

## 📝 내용

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

## 🏷️ 분류

- **PARA**: Resource
- **구분**: Query

## 🔗 연결

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
