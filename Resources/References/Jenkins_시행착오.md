---
title: Jenkins 시행착오
created: 2024-02-23
tags: ["reference", "migrated", "resource", "jenkins"]
PARA: Resource
구분: ["Jenkins"]
---

# Jenkins 시행착오

## 📝 내용

jenkins 빌드되는 디렉토리는 ~~ workspace로 떨어짐

- 위치는 바꿀 수 있음
workspace -> 폴더로 cp 나 scp해야함

- home 디렉토리로 하면 안되고 내가 정한 링크로 해야함

- /home~~ -> /var~~~

webhook을 등록하면 stage가 감지되면 자동 ci/cd가 되야하는데
네파서버는 ip문제로 stage에서 변동사항 감지되는게 안되고 있음

docker volumes 역할

```plain text
compose yaml에 volumns 역할은 docker 내부의 파일과 host서버의 파일을 연결시켜주는 역할이다
nepa_web을 예시로 들면

jenkins에서 배포하려고 하는데 젠킨스가 도커에서 돌아가기 때문에 기본 bash 경로가 도커 컨테이너 내부로 잡혀있다
빌드된 결과를 외부 호스트 파일로 연결할려고 하면, 도커 컨테이너 내부 파일과 호스트 파일을 연결시켜줘야 한다.

```

## 🏷️ 분류

- **PARA**: Resource
- **구분**: Jenkins

## 🔗 연결

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
