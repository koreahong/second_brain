---
title: "Elasticsearch"
source: notion
notion_id: 164c6d43-3b4d-80ca-a298-c9a71c59df34
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["DB"]
링크: []
최종편집시각: "2024-12-22T10:22:00.000Z"
제목: ""
상위 항목: []
날짜: "2024-12-22"
PARA: "Resource"
tags: ["레퍼런스", "DB", "notion-import"]
---

## 개념

- 비정형 데이터를 
- *객체 스토리지(Object Storage)**는 데이터를 파일 단위로 저장하는 방식으로, 파일을 객체(object)로 관리하는 데이터 저장소 기술입니다. 객체로 나눈다는 것은 데이터와 메타데이터를 같이 묶어서 저장하는 개념이다. 윈도우 퍼일은 블록단위로 나누어서 디스크에 저장한다. 객체스토리지는 통째로 저장하기 때문에 일부 수정할 수 없어서, 원본을 수정하고 통째로 다시 올려야 한다. 실제 디렉토리 구조가 아닌 디렉토리처럼 보이는 전체의 값이 키값이다.
- 비정형 데이터를 검색할 때, Elasticsearch를 사용한다.
- Elasticsearch는 json 데이터를 검색할 때 메타데이터를 이용해서 데이터를 빠르게 찾을 수 있게 하는 시스템이다. 메타데이터를 선별적으로 활용하여 역색인 등으로 저장한 다음, 이 색인을 활용하여 빠른 검색을 할 수 있게 함.
- S3가 저장될 때마다 트리거롤 lambda를 호출하여 json 파일마다 메타데이터를 추출하여 es에 저장하는 것을 구현하여 사용할 수 있다.
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/dcbef44b-5755-45ba-9154-c58bd62a7ebf/1000002255.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663J3BXIKH%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015707Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIGz%2BUGQWbMhCwNayc5EC8%2BmPZdilbZK%2B2rfmd6zN%2F45LAiEAllO7pX7UwiG6uDQ%2FnXoxdP3ll%2BP8LcApKkNh%2BYOoS%2F0qiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDKERKhnR13bBAy988yrcA%2Bw8SnISrhO0GqStc%2BpWTBqKkNWYwIFBQ8pyiMkBROf476ccZF%2BzgoICyRASg6btkP%2B5kA8SUf5OfJ3JAIE4maF30t1Qg7Bid70PlD62Weq0pl5BjhMG0kgPIwbB2eV1bxyucW0jQ5MDBhMkH9ODfG7JllboeKcD5oZuxb%2FYR0H5wSwWZFQOl9xmiP8OCMA6CSvE9Bvk7qyOH0%2FtKOFM8fjPEkMfZUgb8eiIDPGLlaVR1Rv3c%2Frc0psn2osX5iX3171nCmzAqbD01oseevcgBgzJvrycQnv1m8rwmE6bkG%2Fps3yLqbVrm03M%2FJGlemALQHCrzwMKkbFN9zTu3s3%2FMWmTLhXPbEvIgI6P9VhQ4Bi8Dmr3MYchZ3rdTAHeUNR5Hm62NBYjaaNVjZDEu3%2FcPsiKGApzMfdUHnFi3tyQe27NIgCfbBX8qw%2Fo1Knjch9BAzyoF5pFFddlKPK5wEK7oAEhBw8YJTOjKebV9cXneJ6%2FE4irgM7w8czUc2vlOZApA6bRZ%2B6mrZUFLJA6vc3rvD4NGh4esAaqCvZEefijfS5aUMUaSDZ6kKa1jtLvjD8RE1etMNtRs0gbXnDIppn7TAOTrhGrhDccH6RypXfoeK7F8E4vr6gLwZ5x0lUUMKiDqckGOqUBq561JXcdq%2BUHttX8wUgtlx%2FCik78ghCAcHFwV516HyEWiqwBiXFKGlLcLeQmyxI6n4wZX8dNzA2p7J%2BMaSG%2BBSXVoTehWNvn7OqjVa4g8797ULySvGNxPaNduofWbeO8AB2Suw%2FHmfTF%2FWVIdSkKWQ8P4AZX59dIGqQfuvRD%2BcNkTDdZrO2cFP0opzhTIRxhUZmwjNIf8i2iSd3rx%2BUBvIf5iycu&X-Amz-Signature=6daabe9ab24811b8c68d1c2ec052aa325f47058f9e8f81db16bc67e6bebf65da&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## 목적

- 객체 스토리지가 현재 트렌드에 맞는 이유에 대한 서칭
## 서칭내용

- 서칭하면서 알아낸 내용에 대해서 자세하게 작성할 것
