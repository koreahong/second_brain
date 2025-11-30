---
title: count + case when = avg
type: resource
tags:
  - query
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

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

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

