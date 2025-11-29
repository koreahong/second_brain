---
title: airflow ecs에 적용
type: resource
tags:
- airflow
- technology
- aws
- docker
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

## 개념

- 개념에 대해서 한 줄로 작성하되, 반드시 내가 스스로 정리한 말로 작성할 것
## 목적

- 개념이 필요하게 된 배경을 작성할 것
## 서칭내용

- ECS로 변경한 이유
  - airflow가 죽는 이슈 발생
    ⇒ 자동으로 다시 서비스가 시작될 수 있도록 컨테이너 서비스로 이전할 필요가 있다는 결론

- ECS 구축 순서
  1. Dockerfile 작성
  1. ECR docker image upload
  1. ALB, SecurityGroup, TargetGroup 생성
  1. ECS - Cluster, Task Definition, Service 생성
![ECS로 구현한 airflow 아키텍쳐](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/ac58c8f0-c2b5-4726-b783-f01776668ac3/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664OJTEPHF%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015635Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQDhBiWJwwKKYQhhwleu2NUOAvq%2BZLpXVMaMAEtW27WVFgIgDKSGoABiIDG%2F0wQQV2VKWWSG1hrbg%2FBfs5cCCt6cNXIqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDKYMaNUZczSPFb47TCrcA0rvmVBXblEBWd272k3L0BbBvl%2BF%2BFoaewaZI%2BABALUkIZCaiN2NjA0TSLyb305WJFlc5Y2OOv0R6vNTVuPL4FZgz7iwp%2B8xD%2BIgSpD0oU46cS1cBsI%2FLsXUPOnhloaa980ZXx348ckhFTtkl%2F1ZxaxmlxkRbWbff9rpHZEa01Ta30jaxJMCiH2v%2BIs%2B0z1CNROcYn91GcXEI4T%2BrzNvmzdXeMWBoz6FtZOA69gc7VYUuLlBuESdpzvkXyulF7lDX4LoHu%2BtpWVamZGDcVtmIbLs%2BVwC6v6u%2F%2B8KdsrIOO1YJwnY9dFKDoVGI4RwaaPSNep%2BBVSfpm4YpcrxV3sNJCyvzM8HMcJrP4Irp0sj9OjlTegV2tqIQYrr3TISHlbtyLT1ewJEPNZLk5E%2BOvWOp9gXagd8b3qcd8XyoAEtYPdvpSMZuX0vJKhrYFC9C7jNqbQC09E%2Fm1RG7qN%2F4Dlb%2BstdszEKTLLu8rGrGI8DDSLAKbIEGd7g5XoSX4h4i80ZSPVqWdk3qbKPxIJBW7kA0hU9AEfeI%2FkzeZyIzcdNm7KE%2F6C7wuG69fTZ78m3%2Fg0jHQKCCVhEo%2Fr2%2Bq7obwq42ozKskVVaqW9znQZWepopzDcaOvHwiyJtxZgBU3AMIWCqckGOqUBVhefRDS2alUr7FmzEGKpruHSkNwF3LIxagi20cihIAdjTdPoaqyJQg39Np9UNE8pcyP0xA41XOmHeYDrShk4mtpHDm%2Bo1KlUcithS8gBpXl5BuaaebvINuViHstosEdr%2FUu8eIHvFzYmeDD5e%2BqdTEGxGvCm%2FrJKxFpo9Vu%2FINNz9RKSwYfgcUTWtzzV6qigd1lL1haOtV83atcK03fCZohaZ8UZ&X-Amz-Signature=54a1e6f081db115bfc3d91ae378d1ef37e7afa32601e4aa36794287afc749b9c&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/072b53aa-16aa-473d-99b0-aa5c700e8d61/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664OJTEPHF%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015635Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQDhBiWJwwKKYQhhwleu2NUOAvq%2BZLpXVMaMAEtW27WVFgIgDKSGoABiIDG%2F0wQQV2VKWWSG1hrbg%2FBfs5cCCt6cNXIqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDKYMaNUZczSPFb47TCrcA0rvmVBXblEBWd272k3L0BbBvl%2BF%2BFoaewaZI%2BABALUkIZCaiN2NjA0TSLyb305WJFlc5Y2OOv0R6vNTVuPL4FZgz7iwp%2B8xD%2BIgSpD0oU46cS1cBsI%2FLsXUPOnhloaa980ZXx348ckhFTtkl%2F1ZxaxmlxkRbWbff9rpHZEa01Ta30jaxJMCiH2v%2BIs%2B0z1CNROcYn91GcXEI4T%2BrzNvmzdXeMWBoz6FtZOA69gc7VYUuLlBuESdpzvkXyulF7lDX4LoHu%2BtpWVamZGDcVtmIbLs%2BVwC6v6u%2F%2B8KdsrIOO1YJwnY9dFKDoVGI4RwaaPSNep%2BBVSfpm4YpcrxV3sNJCyvzM8HMcJrP4Irp0sj9OjlTegV2tqIQYrr3TISHlbtyLT1ewJEPNZLk5E%2BOvWOp9gXagd8b3qcd8XyoAEtYPdvpSMZuX0vJKhrYFC9C7jNqbQC09E%2Fm1RG7qN%2F4Dlb%2BstdszEKTLLu8rGrGI8DDSLAKbIEGd7g5XoSX4h4i80ZSPVqWdk3qbKPxIJBW7kA0hU9AEfeI%2FkzeZyIzcdNm7KE%2F6C7wuG69fTZ78m3%2Fg0jHQKCCVhEo%2Fr2%2Bq7obwq42ozKskVVaqW9znQZWepopzDcaOvHwiyJtxZgBU3AMIWCqckGOqUBVhefRDS2alUr7FmzEGKpruHSkNwF3LIxagi20cihIAdjTdPoaqyJQg39Np9UNE8pcyP0xA41XOmHeYDrShk4mtpHDm%2Bo1KlUcithS8gBpXl5BuaaebvINuViHstosEdr%2FUu8eIHvFzYmeDD5e%2BqdTEGxGvCm%2FrJKxFpo9Vu%2FINNz9RKSwYfgcUTWtzzV6qigd1lL1haOtV83atcK03fCZohaZ8UZ&X-Amz-Signature=9e1eb2df750e84576b202ffe35a04468a249648b525eed426d6e6b810ef060a0&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

