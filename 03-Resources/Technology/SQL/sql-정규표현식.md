---
title: sql 정규표현식
type: resource
tags:
- Query
---

## ✅ PostgreSQL 정규표현식 문법

---

---

> PostgreSQL은 \d, \w 등을 POSIX 호환으로 해석하지 않을 수 있음. 가능하면 [0-9], [A-Za-z_] 형태로 명시하는 것이 안정적입니다.

---

## ✅ 실전 예제 모음 (PostgreSQL 기준)

### 1. 이메일 형식이 유효한 경우만 필터

```sql

SELECT *
FROM Users
WHERE email ~ '^[a-zA-Z0-9_]+@[a-zA-Z]+\.(com|net|org)$'

```

### 2. 전화번호 형식 (010-1234-5678)

```sql

SELECT *
FROM Phones
WHERE number ~ '^010-\d{4}-\d{4}$';

```

### 3. 영문 이름만 필터링 (공백 없이)

```sql

SELECT *
FROM People
WHERE name ~ '^[A-Za-z]+$';

```

---

## 💡 PostgreSQL의 특수 기능

- SIMILAR TO : SQL 표준에 따른 간단한 정규식 (%, _ 등 와일드카드 포함)
- substring(text from pattern) : 정규표현식으로 문자열 일부 추출
- regexp_replace(text, pattern, replacement) : 정규식 기반 치환
- regexp_matches(text, pattern) : 여러 매칭 결과 리턴 (setof)
예:

```sql

SELECT regexp_matches('abc123def', '[a-z]+');
-- 결과: {"abc"} 첫 문자만 매칭

```

---

필요하시면 regexp_replace, regexp_matches, substring 등도 예시와 함께 설명드릴 수 있습니다.

어떤 부분 더 보고 싶으세요?

### 나의 말:

그럼 조건은 동일하나 _로 시작하면 안되는다는 조건이 추가되면?

### ChatGPT의 말:

좋습니다. 기존 조건에서 @ 앞부분이 _로 시작하면 안 된다는 조건이 추가되었으므로, 정규표현식을 다음과 같이 수정해야 합니다.

---

## ✅ 조건 정리 (최종)

1. @는 정확히 1개 포함
1. .com으로 끝남
1. @ 앞부분은 알파벳/숫자/언더스코어만 포함되며, 언더스코어로 시작하면 안 됨
1. @ 이후부터 .com 전까지는 알파벳만 포함
---

## ✅ PostgreSQL 정규표현식 쿼리

```sql
SELECT user_id, email
FROM Users
WHERE email ~ '^[a-zA-Z0-9][a-zA-Z0-9_]*@[a-zA-Z]+\.com$'
ORDER BY user_id;
```

---

## ✅ 정규표현식 설명

---

## ✅ 예시

PostgreSQL에서 cardinality(string_to_array(content, '@'))는 문자열에서 특정 구분자로 나눈 개수를 세는 방법 중 하나입니다.

이걸 분석해보면 다음과 같은 의미예요.

---

## ✅ 함수 구성

### 1. string_to_array(content, '@')

- "content"라는 문자열을 '@'를 기준으로 쪼갬
- 결과는 배열(array) 이 됨
예시:

```sql
SELECT string_to_array('Hello@John@Mike', '@');
-- 결과: {Hello, John, Mike}
```

---

### 2. cardinality(array)

- 배열의 원소 개수를 리턴
- 위 예시라면 cardinality(...) = 3
---

## ✅ 결합해서 해석하기

```sql
cardinality(string_to_array(content, '@'))
```

- '@' 기호로 나누고 → 그 조각이 몇 개인지 센다
- 즉, '@' 개수 = cardinality - 1
### 📌 주의점:

- '@'가 3번 나온다면 조각은 4개 → cardinality = 4
- 따라서 멘션 수는:
  ```sql
  
  cardinality(string_to_array(content, '@')) - 1
  
  
  ```

---

## ✅ 멘션이 3개 초과인지 체크하는 조건 예시

```sql

cardinality(string_to_array(content, '@')) - 1 > 3

```

---

## ✅ 전체 예시 쿼리 (위 문제에 적용)

```sql

SELECT tweet_id
FROM Tweets
WHERE
    LENGTH(content) > 140
    OR (cardinality(string_to_array(content, '@')) - 1) > 3
    OR (cardinality(string_to_array(content, '#')) - 1) > 3
ORDER BY tweet_id;

```

---

## 🔄 vs LENGTH - REPLACE 방식 차이

---

필요하면 regexp_split_to_array를 써서 @ 다음이 진짜 멘션인 경우만 추출하는 고급 방식도 알려줄게요!

### 나의 말:

postgresql에서 배열로 변환하면 이점이 있어?

### ChatGPT의 말:

아주 좋은 질문입니다. PostgreSQL에서 문자열을 배열로 변환(string_to_array)하면 몇 가지 중요한 장점이 생깁니다. 하지만 단점도 존재하기 때문에 언제 쓰면 좋은지 판단하는 것이 중요합니다.

---

## ✅ 배열로 변환할 때의 이점

### 1. 원소 단위로 조작이 가능해짐

배열로 바꾸면 각각의 조각에 대해 다음과 같은 연산을 할 수 있습니다:

- 특정 위치의 원소 추출: my_array[2]
- 반복 처리: unnest(my_array)
- 길이 측정: cardinality(my_array)
- 조건 필터링 (예: 특정 접두사로 시작하는 배열 원소만 필터링)
🔍 예:

```sql

SELECT unnest(string_to_array(content, ' '))
WHERE value LIKE '@%';

```

👉 트윗에서 멘션만 추출 가능

---

### 2. regexp_split_to_array()로 정규표현식 기준 분할도 가능

기본적인 구분자 외에도 정규표현식을 기준으로 split 가능

```sql

SELECT regexp_split_to_array('a@b@c@d', '@');
-- 결과: {a, b, c, d}

```

> 더 복잡한 패턴 기반 멘션/해시태그 분석 가능

---

### 3. array는 PostgreSQL의 1급 데이터 타입

- ANY, ALL, = ANY(array), @> 등과 같이 집합 연산이 가능
- WHERE '@John' = ANY(string_to_array(content, ' '))
  → content에 '@John'이 단어 단위로 포함되어 있는지 확인 가능

---

## ⚠️ 단점 및 주의사항

---

## ✅ 요약

---

## 🎯 실제 적용 예시 (멘션이 @로 시작하는 단어인 경우만 집계)

```sql

SELECT tweet_id
FROM Tweets
WHERE
    (
        SELECT COUNT(*)
        FROM unnest(string_to_array(content, ' ')) AS word
        WHERE word LIKE '@%'
    ) > 3;

```

이렇게 하면 공백 기준으로 split 후, 진짜 @멘션만 카운트할 수 있습니다.

더 고급 필터도 가능하죠.

## 📘 함수 정의

```sql
sql
복사편집
regexp_matches(source_text, pattern, [flags])

```

---

## ✅ 특징 요약

---

## 🔍 예제

```sql
sql
복사편집
SELECT regexp_matches('hello #SQL and #Postgres', '(#[A-z]+)', 'g');

```

📌 결과:

```plain text
bash
복사편집
{#SQL}
{#Postgres}

```

> 주의: regexp_matches()는 row-multiplied output이 아니라 array output이므로, unnest()와 함께 써야 행으로 펼쳐짐

---

## ✅ 활용 예: 해시태그 행 단위 분해

```sql
sql
복사편집
SELECT tweet_id, unnest(regexp_matches(tweet, '(#[A-z]+)', 'g')) AS hashtag
FROM Tweets;

```

→ 트윗별로 모든 해시태그를 한 행씩 펼쳐줌

---

## 💡 정리

---

필요하면 #해시태그_중복제거, 정규표현식 튜닝 등도 도와줄게요.

### 나의 말:

i랑 g랑 차이가 뭐야

### ChatGPT의 말:

좋습니다. regexp_matches()에서 사용하는 플래그 중 'i'와 'g'는 매우 중요한 역할을 합니다. 아래에 간단하고 명확하게 설명드릴게요:

---

## 📌 g (global)

- *"여러 개 매칭"**을 전부 반환
- 같은 문자열 내에서 패턴이 여러 번 등장해도 전부 찾아줌
### 예시

```sql
sql
복사편집
SELECT regexp_matches('hi #sql #data #AI', '(#[A-z]+)', 'g');

```

📌 결과:

```plain text
bash
복사편집
{#sql}
{#data}
{#AI}

```

---

## 📌 i (ignore case)

- 대소문자 구분 없이 매칭
- A = a, Hadoop = hadoop = HADOOP
### 예시

```sql
sql
복사편집
SELECT regexp_matches('I love #SQL and #sql', '(#sql)', 'gi');

```

📌 결과:

```plain text
bash
복사편집
{#SQL}
{#sql}

```

---

## 📋 정리 표

---

## 🧠 실전 팁

- 해시태그 추출할 땐 보통 'gi' 같이 써요.
  ```sql
  sql
  복사편집
  unnest(regexp_matches(tweet, '(#[A-z0-9_]+)', 'gi'))
  
  
  ```

- unnest() 없이 쓰면 배열 그대로 나오므로 보통 함께 사용합니다.