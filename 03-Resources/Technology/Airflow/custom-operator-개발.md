---
title: "custom operator 개발"
source: notion
notion_id: 944cf14a-ec60-4122-b3d7-df562ac29277
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["Airflow"]
링크: []
최종편집시각: "2024-10-20T07:15:00.000Z"
제목: ""
상위 항목: []
날짜: "2024-06-11"
PARA: "Resource"
tags: ["레퍼런스", "Airflow", "notion-import"]
---

🔖 [https://mightytedkim.tistory.com/150](https://mightytedkim.tistory.com/150)

너무 좋은데 러닝 커브가 있다는게 단점이에요.

그리고 custom operator 만들어달라는 요구가 들어오는 것도 무서워요.

'우리팀만' 사용하면 airflow 2.0의 taskflow api로 멋있게 만들겠지만

구축 후 운영을 고려한다면 python operator 보다는 custom operator만 오픈하는 것을 추천합니다.

---

🔖 [https://www.astronomer.io/docs/learn/airflow-importing-custom-hooks-operators](https://www.astronomer.io/docs/learn/airflow-importing-custom-hooks-operators)

custom opreator 만들고 .output으로 값 호출

add >> multiply >> use_cat_fact_hook(multiply.output)

