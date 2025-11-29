---
title: "in, exists 비교"
source: notion
notion_id: 1f2c6d43-3b4d-8070-bd14-e0ea06b4d283
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

## ✅ 먼저, IN의 NULL 문제

다음 예시를 봅시다:

```sql
sql
복사편집
select *
from users
where user_id in (1, 2, null);


```

- 이 쿼리는 의도상 user_id = 1 or 2 or null을 뜻하지만
- IN (1, 2, NULL) 은 NULL이 포함되어 있으면 전체 조건의 결과가 UNKNOWN이 될 수 있음
- 그래서 일치하는 값이 있어도 결과가 나오지 않거나, 예상치 못한 동작을 합니다.
➡️ 즉, IN은 NULL이 들어가면 결과가 깨질 수 있는 "NULL-unsafe" 연산자입니다.

---

## ✅ 반면 EXISTS는?

```sql
sql
복사편집
select *
from users u
where exists (
    select 1
    from logins l
    where l.user_id = u.user_id  -- l.user_id가 NULL이어도 됨
);


```

- EXISTS는 서브쿼리 결과가 한 행이라도 있으면 True
- 그 서브쿼리 결과에 NULL이 있든 없든 전혀 상관 없음
- NULL 값도 비교할 수 있고, 조건을 만족하는지 여부만 보기 때문에 결과가 안정적
➡️ 그래서 EXISTS는 NULL-safe 하다고 말합니다.

---

## 📌 예시로 비교해보기

### 1. IN 예시: NULL이 문제를 일으킴

```sql
sql
복사편집
select 1
where 1 in (null, 2);  -- 결과 없음!


```

- null이 포함되어 있으면 → 1 = null → UNKNOWN
- 따라서 전체 IN 조건이 불확실해져서 결과가 안 나옵니다
### 2. EXISTS 예시: NULL 있어도 결과 나옴

```sql
sql
복사편집
select 1
where exists (
    select 1
    where null is null  -- 이 조건은 True
);


```

- 조건이 만족되면 EXISTS는 그냥 True → 결과 나옴
- NULL을 비교하고 써도 괜찮음
---

## ✅ 결론 요약

> 그래서 서브쿼리 결과에 NULL 이 포함될 가능성이 있다면,

### 나의 말:

그럼 전반적으로 in과 exists 를 평가해줘 성능, null safe, 작동방식 등

그리고 not in과 not exists에 대해서도 같이

### ChatGPT의 말:

훌륭한 요청입니다.

IN, EXISTS, NOT IN, NOT EXISTS는 SQL에서 매우 자주 쓰이는 조건절이지만,

성능·NULL 처리·작동 방식에서 분명한 차이가 있습니다.

---

# ✅ IN vs EXISTS 전반적 비교

---

## ✅ 예제

### IN

```sql
sql
복사편집
select name
from users
where dept_id in (select id from departments where region = 'KR');


```

→ dept_id가 'KR' 지역에 있는 부서 중 하나에 속한 사람

- 서브쿼리 결과가 작으면 효율적
- BUT departments.id에 NULL이 포함되어 있으면 위험
---

### EXISTS

```sql
sql
복사편집
select name
from users u
where exists (
    select 1
    from departments d
    where d.region = 'KR' and d.id = u.dept_id
);


```

→ users에 대해 일치하는 부서가 하나라도 있으면 true

- departments.id에 NULL 있어도 OK
- 부서 쪽이 많고, users가 클수록 효율적
---

# ✅ NOT IN vs NOT EXISTS

이제 부정 연산을 보겠습니다.

---

### 🔥 NOT IN 문제 예시

```sql
sql
복사편집
select name
from users
where dept_id not in (select id from departments);  -- id에 NULL 있으면 전체 결과 없음!


```

- departments.id에 NULL이 있으면 → 전체 dept_id not in (...) 조건이 UNKNOWN → 모두 실패
- 굉장히 위험한 방식
---

### ✅ NOT EXISTS 예시 (권장)

```sql
sql
복사편집
select name
from users u
where not exists (
    select 1
    from departments d
    where d.id = u.dept_id
);


```

- 존재하지 않는 dept_id 를 가진 user를 찾는다
- departments.id에 NULL 있어도 OK
---

# ✅ 결론 요약

---

## ✅ 실무 요약 팁

- 🌟 항상 NOT EXISTS > NOT IN
- IN은 간단하고 서브쿼리 작을 때는 좋지만, NULL이 있으면 의도와 다른 결과가 나올 수 있음
- 서브쿼리 결과가 많거나, 로그 테이블 등에서 다룬다면 EXISTS가 더 적합
