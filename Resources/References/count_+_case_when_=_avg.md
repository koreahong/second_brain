---
title: count + case when = avg
created: 2025-11-28
tags: ["reference", "migrated", "resource", "query"]
PARA: Resource
구분: ["Query"]
---

# count + case when = avg

## 📝 내용

```sql
select
    s.user_id,
    coalesce(
        else round(
            sum(case c.action when 'confirmed' then 1 else 0 end)    
            / count(c.action)::numeric,
            2
        ), 0.00
        ) as confirmation_rate
from 
    Signups s
left join Confirmations c
    on c.user_id = s.user_id
group by
    s.user_id;
```

여기에서 sum / count(*) 하는 부분은 avg로 대체가능

```sql
select
    s.user_id,
    coalesce(
        round(
            avg(case when c.action = 'confirmed' then 1 else 0 end),
            2
        ),
        0.00
    ) as confirmation_rate
from 
    Signups s
left join Confirmations c
    on c.user_id = s.user_id
group by
    s.user_id;
```

## 🏷️ 분류

- **PARA**: Resource
- **구분**: Query

## 🔗 연결

**Hub**: [[_Database]]

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
