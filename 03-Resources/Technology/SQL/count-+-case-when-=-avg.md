---
title: "count + case when = avg"
source: notion
notion_id: 1f2c6d43-3b4d-8038-b206-da612648f1a6
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

