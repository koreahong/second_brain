---
title: postgresql 파티셔닝
type: resource
tags:
- DB
---

## 개념

- postgresql 파티셔닝하는 방법
## 목적

- 파티셔닝을 통해서 테이블관리 효율화
- 특히 파티션 키 단위로 테이블을 관리하기 좋음
## 서칭내용

- 파티션할 테이블 생성
  - 최초 테이블을 생성할때 partition by를 사용해서 특정 컬럼을 파티션 키로 지정하여 생성함
    ```sql
    CREATE TABLE logs (
        id SERIAL PRIMARY KEY,
        event_date DATE NOT NULL,
        user_id INT,
        action TEXT
    ) PARTITION BY RANGE (event_date);
    ```

- 파티션 테이블 생성
  - 파티션 키 타입 결정
    - 파티션 키로는 range, list가 있음
      - range
        - 주로 날짜, 숫자 등 순서가 있는 값을 다룰 때, 시간의 흐름에 따라 데이터가 누적
      - list
        - 주로 제한된 값의 집합을 기준으로 분할할 때 유용합니다.
      - hash
        - 데이터가 균등하게 분할. 이 방식은 주로 특정 범위나 카테고리가 아닌, 고르게 분산된 데이터를 필요로 할 때 유용합니다.
    ```sql
    DROP TABLE IF EXISTS partition_{data_interval_end};
    CREATE TABLE IF NOT EXISTS partition_{data_interval_end}
    PARTITION OF aivelabs.ga_view_mart
    FOR VALUES IN ('{data_interval_end}');
    ```