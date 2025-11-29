---
title: "Jenkins 시행착오"
source: notion
notion_id: 9af2b8fb-653f-4d4a-892e-8e1b287be4f8
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["Jenkins"]
링크: []
최종편집시각: "2025-09-13T03:51:00.000Z"
제목: ""
상위 항목: ["26dc6d43-3b4d-8080-bd88-e3d9c3a3a847"]
날짜: "2024-02-23"
PARA: "Resource"
tags: ["레퍼런스", "Jenkins", "notion-import"]
---

jenkins 빌드되는 디렉토리는 ~~ workspace로 떨어짐

- 위치는 바꿀 수 있음
workspace -> 폴더로 cp 나 scp해야함
- home 디렉토리로 하면 안되고 내가 정한 링크로 해야함
- /home~~ -> /var~~~
webhook을 등록하면 stage가 감지되면 자동 ci/cd가 되야하는데
네파서버는 ip문제로 stage에서 변동사항 감지되는게 안되고 있음

---

docker volumes 역할

```plain text
compose yaml에 volumns 역할은 docker 내부의 파일과 host서버의 파일을 연결시켜주는 역할이다
nepa_web을 예시로 들면

jenkins에서 배포하려고 하는데 젠킨스가 도커에서 돌아가기 때문에 기본 bash 경로가 도커 컨테이너 내부로 잡혀있다
빌드된 결과를 외부 호스트 파일로 연결할려고 하면, 도커 컨테이너 내부 파일과 호스트 파일을 연결시켜줘야 한다.

```

