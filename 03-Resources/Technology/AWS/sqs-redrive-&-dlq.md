---
title: sqs redrive & dlq
type: resource
tags:
- sqs
- aws
- lambda
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

## 개념

- sqs + lambda 진행시 소화하지 못한 메세지는 dead lock queue로 빠지게 하거나 redrive를 해야함.
## 목적

- 람다로 요청한 메세지들에 대한 관리
## 서칭내용

### 일반 큐와 dlq 연결

- 일반 메세지 큐 세팅
  - DLQ를 선택하고 최대 수신(Maximum receives)을 구성합니다. 최대 수신은 메시지가 DLQ로 전송되기 전에 다시 처리되는 횟수입니다.
    ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/36573c12-15d4-4ce9-ae86-091ebc497b57/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466QG2O5QMB%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015642Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQDs9HSpKYYLrlcSZjYk5Vh%2BsU%2B1DOzpnEhi%2FNKDEMBwNgIhAMv8%2B8G%2FrfAdLRCjgsP1oLOcE5yK6TtG3PHy1MKcgR2fKogECML%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igyr9ApWVag6tZgsmNAq3AO0tRFamRWPxBHHOF97qRD%2FskSDzMhk2aaxEteMix7eh7CliB1BZGFkz62d3Nj%2FsFITkW6oPzjAvd%2FYMByV0k8uJWv4J%2B88wCGE29ySA2AlqwDA9ddwOOXQG7UfApuHwe%2BJyl58nVXKFTevDc8nVw3Yw31M3fXb19WBB3vdxar34vtQUTgXBRS1fkKP8Zj3uFKThZCtZx0NelkLHTk7yitVmU44HgER%2F32eZzHxWbY3KAtV7WG7iuJaMnQH%2BR2sgL3qIlMymO2e15kXyj2m8HdANYzJKoRRixvHq1IDVVz0W6QQowMpCHSERg5gqTFgBO67qGTVMEFIr6w%2BiPHxYTBtZjhZ9W6qhFg4c6MCKpmzlicLFoP6DElWb3P%2FL8S7hlblUWgUOsJrYk2DxL5ejq4SLdGNPtbfBv%2BUSXJwJr7sNdvoI8hK2DpO%2Bt%2FMtLs4Yt37iPaUp%2FbDBzWAjrIMCOe2NUi5vlRa1bh3P8ilmnHXaEy%2BzB9JLXXlSgcM96wpZAISnrwZg6T%2Fj8BZsR0MUxD%2FzyXhZ2rrGMLiXTkLcuV5I%2B2xdSqY9Ymm1asPFuMf%2BC9i1Udv0qwrQsKcmRn0krCGZBAK83Xz8L%2FWCUJHc7eUUaIVBrcx1vrd22JJzDCdgqnJBjqkAaNRng4znjyeI70EcXL95QRCaL8bJFNjJ0SZyjbjJziwKZKkVM%2BbUmhUvEEMb%2BlTPzYRpj4d%2FYqHpiLVvBsJEWXMQDGt5BUGLVU9W7Sz6KHxigGaYVuc5LF58NFh8RUjIeSE%2FXGWY2DPrnx8N%2FzN7b%2Bj5naLiQ%2Fj%2Fq%2Bx5o%2FZ23D%2BAvL8GtjMYklL1%2F0GZSdlHT%2Bvw993daF0bvS6EIRFCOqoJP9G&X-Amz-Signature=1623400618e91efe12d8ef72c90ff30d79c12793f56cd9b4eee6ed2084956421&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

- 배달 못한 편지 대기열 세팅
  - 리드라이브
특정 대기열만 이 DLQ를 사용할 수 있도록 설정
    ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/dba7f6f0-1dc4-464b-8f85-aa364b878590/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZK7JAOG5%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015642Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIHfQO1IzONUfEEj2t60DoDh8gf3RAuPo1z%2FKGOMMfhf%2FAiEAjb6w0J3xCoxbEp5%2BYF5HQGQ9MlGgMJcdYViKQhZ%2BiHQqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFBiJ0MQQhheh1MOOCrcA5haNu%2FoAMh56l%2B4xEJkZtAvH7XpfCUbq%2BNAM4nlGxF%2FpYoyRITHAtiyEa0JGfpE48Qaju8Klr6%2B90vLaRx3JEHvvD4E1JopaUM9OXB91fcjkQD8bHNCKHuQdtsM2vKEzJ74qU7uNKjD0X%2BAQHofk%2FXxyRrk7jvRtLFPZEFsyKU5ZaZHYtQaXc%2F9kWXTqUozf1I7qN%2FB7R5NKsr4ZzvYzQxRkGXRH4PEnQCQgO8OSi48y%2F6zYJazIEq2YCX8GC1bhtfXPBniJlzW6B2mD5cC5LYZBWS4z2Elwx0AhErrpGMd6wEYZbrxybkMizr4nY6bO4B%2BrgQP1mADix2OoEytZ076D%2BVXLEIUaAyw6TFr8B669p66dGHc1KI2sx2SXWlONil8SDiQXEEU4%2Bw8gW57rP6k5V48pBkkn38oTPpbsKPYy5%2BYB5Oh8SeeGm3eULyTaAoEkce382t9QgOmvVLQmtXhCR8ZCM1%2BEnHM4FXyl%2FOmO6GIJYcIBcWvFqIrG9%2BA1ES2UukoBrLO6vHh9fJWehmO5weL0ZXrSv3doN2jT2YCRh4bp1RPb44CmF3J1UJYzwY9a3xZeIlRVqemywZXVJA1pNt29yMoZiNkl6JiJzPt90ggU1H3hAR4%2Fex6MLKBqckGOqUBqLYZGm6kOm2Iyok%2BUwjapood6cjEexTorZbEKVa7POjnhICDdIIBE9f%2B%2BVii12hDpSjHc2pKUeG%2BGPN%2FQe16HRcK1doUb7CkFKHAztPaSSNTt%2FPaQ6gOSc6JYUETgho8TAu6KN706tyUzSRJitA35OmLQ%2BGuOGUCzZuumLcrY%2Bs9XQORtOKL53PGdqGD5DcTyMh94MEtArRB5%2FWZPc0aW7yF1xHR&X-Amz-Signature=09ce9569cb27df32d2eb6a004db368aeb7cc285ed57ec3b0516f6c8f0670214e&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

docker build -t lambda_container -f dockerfile_lambda .

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

