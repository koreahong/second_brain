---
title: Nginx 학습
created: 2024-02-23
tags: ["reference", "migrated", "resource"]
PARA: Resource
구분: []
---

# Nginx 학습

## 📝 내용

### 구성

- nginx 작동하는 방식은 크게 2가지가 있다

### simple directives

- 한줄로 되어 있는 것

- 예시: root /data/www;

### block directives

- 중괄호로 묶여 있는 것

- core : 환경 설정 파일의 최상단에 위치하며 한번만 사용할 수 있습니다. nginx의 기본적인 동작 방식을 정의합니다.

- http: 웹서버에 대한 동작을 설정하는 영역으로, server 블록과 location 블록의 루트 블록입니다.

- server: 가상 호스팅(Virtual Host)의 개념으로 하나의 서버를 커버합니다.

- location: server 블록 내에서 특정 URL을 처리하는 방법을 정의합니다.

- events: 네트워크 동작에 관련된 내용을 설정할 수 있습니다

```plain text
// 기본 - core

events{

}

http {
    server {
    	location / {

    	}

    	location /images/ {

    	}
	}
}

```

- 적용은 core-> http -> server -> location순으로 적용되며 동일한 simple directives가 block 별로 정의될 경우 depth가 가장 깊은 block의 설정을 따라갑니다.

## 🏷️ 분류

- **PARA**: Resource
- **구분**: 없음

## 🔗 연결

**Hub**: [[_Learning]]

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
