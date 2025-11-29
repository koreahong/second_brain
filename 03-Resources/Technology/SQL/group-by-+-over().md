---
title: "group by + over()"
source: notion
notion_id: 1f2c6d43-3b4d-8030-b038-f5e78388be66
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["Query"]
링크: ["https://leetcode.com/problems/popularity-percentage/"]
최종편집시각: "2025-05-19T02:09:00.000Z"
제목: ""
상위 항목: []
PARA: "Resource"
tags: ["Query", "레퍼런스", "notion-import"]
---

```sql
WITH FriendshipsExpanded AS (
  -- Expanding friendships to account for both user1 and user2 as primary users
  SELECT 
    user1, 
    user2 
  FROM 
    Friends 
  UNION
  SELECT 
    user2, 
    user1 
  FROM 
    Friends
) 
SELECT 
  user1, 
  ROUND(
    -- Calculating the percentage popularity
    100 * COUNT(DISTINCT user2)::numeric / COUNT(user1) OVER (), 
    2
  ) AS percentage_popularity 
FROM 
  FriendshipsExpanded 
GROUP BY 
  user1 -- Grouping results by primary user
ORDER BY 
  user1;
```

관계를 뒤집어서 저장

### Group by + over()

위에 방식으로 진행하면 집계한 기준의 컬럼은 unique한 상태에서 over()에 적용된 집계함수 값이 생성된다.

위에 코드를 예로 들면

user1에 distinct가 적용된 상태에 count()를 하는데 over()로 인해서

user1 모든 데이터에 적용이 되는 것

user1에 1 ~ 9까지 값이 있을 때

여기에서 partition by user1을 하면 user1에 unique한개 나오니까 1로만 찍힘

