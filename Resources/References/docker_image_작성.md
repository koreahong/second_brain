---
title: docker image 작성
created: 2025-11-28
tags: ["reference", "migrated", "docker"]
PARA: 
구분: ["Docker"]
---

# docker image 작성

## 📝 내용

## 개념

- docker image는 모양 틀을 만드는 것, 빌드하면 해당 image대로 실행하는 실행 파일을 생성함.

## 목적

- 코드로 환경을 관리하기 위함.

## 서칭내용

### CAFE24 API 추출하는 image 생성

### 명령어정리

```sql
# 베이스 이미지 지정
FROM ubuntu:20.04

# 빌드 시 필요한 패키지 설치
RUN apt-get update && apt-get install -y python3 python3-pip

# 환경 변수 설정
ENV APP_ENV=production
ENV APP_SECRET=mysecretkey

# 작업 디렉토리 설정
WORKDIR /app

# 호스트의 파일을 컨테이너로 복사
COPY app.py /app

# 빌드 인자 설정
ARG BUILD_VERSION=1.0.0
RUN echo "Build version: $BUILD_VERSION"

# 볼륨 설정
VOLUME /data

# 포트 노출 설정
EXPOSE 8080

# 특정 사용자로 실행
RUN useradd -ms /bin/bash myuser
USER myuser

# 헬스체크 설정
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8080/ || exit 1

# 엔트리포인트와 기본 명령 설정
ENTRYPOINT ["python3"]
CMD ["app.py"]
```

- requirements 간략하게

- 필요한 파일만 copy

## 🏷️ 분류

- **PARA**: 
- **구분**: Docker

## 🔗 연결

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
