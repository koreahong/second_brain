---
title: Nginx 학습
type: resource
tags:
- technology
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

[https://nginx.org/en/docs/http/ngx_http_core_module.html#location](https://nginx.org/en/docs/http/ngx_http_core_module.html#location)

---

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

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

