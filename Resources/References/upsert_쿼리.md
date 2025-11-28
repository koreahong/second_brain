---
title: upsert 쿼리
created: 2024-02-23
tags: ["reference", "migrated", "resource"]
PARA: Resource
구분: []
---

# upsert 쿼리

## 📝 내용

```plain text
INSERT INTO crtbatch.monthly_snapshot_segmentation_mix_final (year_month, cus_cd, ord_label, ord_group_label, prd_label, prd_group_label, promo_label, promo_group_label, ord_lv1, prd_lv1, promo_lv1, ord_lv2, prd_lv2, promo_lv2, mix_lv1, mix_lv2)

SELECT

t1.*

FROM

(

select '202311' as year_month, cus_cd, ord_label, ord_group_label, prd_label, prd_group_label, promo_label, promo_group_label, ord_lv1, prd_lv1, promo_lv1, ord_lv2, prd_lv2, promo_lv2, mix_lv1, mix_lv2

from crtbatch.monthly_snapshot_segmentation_mix_final

where year_month = '202402'

) t1

inner JOIN

(

select *

from crtbatch.monthly_snapshot_segmentation_mix_final

where year_month = '202311'

AND mix_lv1 IS null

) t2

ON t1.cus_cd = t2.cus_cd

and t1.year_month = t2.year_month

ON CONFLICT (year_month, cus_cd) DO UPDATE

SET

ord_label = EXCLUDED.ord_label,

ord_group_label = EXCLUDED.ord_group_label,

prd_label = EXCLUDED.prd_label,

prd_group_label = EXCLUDED.prd_group_label,

promo_label = EXCLUDED.promo_label,

promo_group_label = EXCLUDED.promo_group_label,

ord_lv1 = EXCLUDED.ord_lv1,

prd_lv1 = EXCLUDED.prd_lv1,

promo_lv1 = EXCLUDED.promo_lv1,

ord_lv2 = EXCLUDED.ord_lv2,

prd_lv2 = EXCLUDED.prd_lv2,

promo_lv2 = EXCLUDED.promo_lv2,

mix_lv1 = EXCLUDED.mix_lv1,

mix_lv2 = EXCLUDED.mix_lv2

```

## 🏷️ 분류

- **PARA**: Resource
- **구분**: 없음

## 🔗 연결

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
