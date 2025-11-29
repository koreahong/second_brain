---
title: Hadoop
type: resource
tags:
- technology
- hadoop
- storage
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

### 하둡의 등장

- 1990년대 데이터 처리 문제와 DFS의 등장
  - 1990년대 데이터 폭증과 문제점
    - 1990년대에는 데이터 양이 기하급수적으로 증가하며 이를 저장하고 처리하는 데 어려움이 존재.
    - 저장 및 처리에 필요한 자원이 부족했고, 확장성 문제로 인해 비용이 매우 높았음.
    - 이러한 문제는 비즈니스 의사결정에 필요한 데이터를 효과적으로 활용하지 못하게 함.
  - DFS(Distributed File System)의 개발
    - 1995년, 컴퓨터 과학자 Doug Cutting이 DFS라는 분산 파일 시스템을 제안.
    - DFS는 데이터를 여러 노드에 분산 저장하여 확장성을 개선.
    - 저비용의 일반 하드웨어(commodity hardware)를 활용하여 저장소를 확장 가능.
  - DFS의 한계
    - 데이터는 분산 저장되었지만, 처리 시 모든 데이터를 다시 게이트웨이 노드로 가져와야 했음.
    - 이로 인해 원래의 문제(자원 부족, 처리 비용 증가)가 해결되지 않음.
    - DFS는 저장 문제를 일부 해결했지만, 데이터 처리 문제에서는 실패.
### MapReduce 도입

- Google의 GFS와 MapReduce의 도입
  - GFS(Google File System)의 개념
    - Google은 DFS와 유사한 GFS를 개발하여 데이터를 분산 저장.
    - DFS와 마찬가지로 데이터를 여러 노드에 분산하여 저장하고 확장성을 확보.
  - MapReduce의 도입
    - MapReduce의 개요 
      - MapReduce는 대규모 데이터를 처리하기 위한 분산 컴퓨팅 모델입니다.
    - MapReduce의 구조와 작동 방식
      - 코드작동: 데이터를 게이트웨이 노드로 가져오는 대신, 코드를 데이터가 있는 노드로 전송.
      - Map 단계: 데이터가 분산된 각 노드에서 코드가 실행되어 중간 결과를 생성.
      - Reduce 단계: 각 노드에서 코드가 실행되어 중간 결과(intermediate results)를 생성.
      - 중간 결과를 결합하여 최종 결과를 생성하는 두 단계(Map 단계와 Reduce 단계)를 도입.
      - 이러한 접근 방식은 데이터 처리의 효율성을 크게 향상시킴.
    - Map → shuffling → reduce 과정
      ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/8d99a8bb-72db-4390-a24a-c4955db3d9cb/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466QBHHYWEP%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T020309Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQDCkAGqlae8BYiC66XpHBo2L%2FW6aaXG81rtUbQ%2Fjk0rTgIhAOaXtPjKa%2BS0lkpePiLVKP4pmm2YN1Dwnp1o%2FtD2LgwKKogECML%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igx0YygDPKD29FuN87Iq3APBZvZ69eDdqT92%2FaLP%2B9OOey5K8P%2FRrx712BfkqiFFOqbj1akuPS66UqGeV35LCE9EzPGbAKzHt4e7Crhr28xdBPq8CkBRT%2F8MfzCOUkceKv%2BL8KSWaAsh8QeSPFH%2BVuaVUH8htNXJIH4BgseZhMuKkiCUy4jvmuRLqZlMOcOnRxRvS%2BwGRiKMyj3ZzBTjIpzVGOyssko2P4BbB9u7Dexwm%2FayFS255VjmSVe9gBklxi9if6c8MyJ2q70tkTFmvLw6pLRe7EYyhYXnVlYJPAcKKYr8%2FH9qKuhJbTTxjzrt63JGq3fJYBmWqscEPdeRXtdI9l7Nd1fS%2Fb9BihIQIf8OPJPifhqvaRhhqmcg%2BrvNRBcv%2B%2FpMx5xZG5k1KKyETR%2BgtVcRPRhdX2efnoZUg9VsEH2QUkJ0PGTAxhIqWYFgqh%2B6j6%2FKBjD5HCy5OiACbOLd7qwOPw21Jb2fRtxeZJyr40ZRjOm1t8qcMhXGRtlzkpsQ9lptYyrVjegbrk%2B7J8mzzHWxVyr1GnO3fgbbmrwzvxQUApwPNlxWwDL2MFzAvVCsGcWiyrWAvyFgizdVCjDkUlJP%2FGHy6Djd2GTfMhXsotlu4GzUufg6qOcVt%2FoTnD5YQrg%2BQMB%2BqcjdmzDkhanJBjqkAZOOYjKD69yxg93ENH91wzeFeL02zjPNgyh2DPbJUqzbeQg43MsqHoR%2F7gk7icbzDrDXZUTa76yBgJ8bBva5BrLV4lEaqxPAI%2BpeWUjrUlMWn10dHNxiWqqsMM6AQ0uh6HD4NkcSIEGaPFpe5JKa%2B7HezuPXT%2FiuGijWomHSw5J%2F6ULCxhxgju4ytiRnHaDOqzNPKQ%2BUQpfDPB%2FN5w57ZV3X2xiJ&X-Amz-Signature=620cb9a0a202ef135b9cdb26ba14dcae6e7ffda2e8ca99ffc425598c8b80f878&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

      ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/4b90ffec-277b-4f31-ac53-ca672c070f11/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466QBHHYWEP%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T020309Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQDCkAGqlae8BYiC66XpHBo2L%2FW6aaXG81rtUbQ%2Fjk0rTgIhAOaXtPjKa%2BS0lkpePiLVKP4pmm2YN1Dwnp1o%2FtD2LgwKKogECML%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igx0YygDPKD29FuN87Iq3APBZvZ69eDdqT92%2FaLP%2B9OOey5K8P%2FRrx712BfkqiFFOqbj1akuPS66UqGeV35LCE9EzPGbAKzHt4e7Crhr28xdBPq8CkBRT%2F8MfzCOUkceKv%2BL8KSWaAsh8QeSPFH%2BVuaVUH8htNXJIH4BgseZhMuKkiCUy4jvmuRLqZlMOcOnRxRvS%2BwGRiKMyj3ZzBTjIpzVGOyssko2P4BbB9u7Dexwm%2FayFS255VjmSVe9gBklxi9if6c8MyJ2q70tkTFmvLw6pLRe7EYyhYXnVlYJPAcKKYr8%2FH9qKuhJbTTxjzrt63JGq3fJYBmWqscEPdeRXtdI9l7Nd1fS%2Fb9BihIQIf8OPJPifhqvaRhhqmcg%2BrvNRBcv%2B%2FpMx5xZG5k1KKyETR%2BgtVcRPRhdX2efnoZUg9VsEH2QUkJ0PGTAxhIqWYFgqh%2B6j6%2FKBjD5HCy5OiACbOLd7qwOPw21Jb2fRtxeZJyr40ZRjOm1t8qcMhXGRtlzkpsQ9lptYyrVjegbrk%2B7J8mzzHWxVyr1GnO3fgbbmrwzvxQUApwPNlxWwDL2MFzAvVCsGcWiyrWAvyFgizdVCjDkUlJP%2FGHy6Djd2GTfMhXsotlu4GzUufg6qOcVt%2FoTnD5YQrg%2BQMB%2BqcjdmzDkhanJBjqkAZOOYjKD69yxg93ENH91wzeFeL02zjPNgyh2DPbJUqzbeQg43MsqHoR%2F7gk7icbzDrDXZUTa76yBgJ8bBva5BrLV4lEaqxPAI%2BpeWUjrUlMWn10dHNxiWqqsMM6AQ0uh6HD4NkcSIEGaPFpe5JKa%2B7HezuPXT%2FiuGijWomHSw5J%2F6ULCxhxgju4ytiRnHaDOqzNPKQ%2BUQpfDPB%2FN5w57ZV3X2xiJ&X-Amz-Signature=3864b635b76edb4b4febd51c97eb87cd76b89cdc144ed63315e0030a39283124&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

      ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/1738d27b-0269-4a59-802f-bb49ae3dc413/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466QBHHYWEP%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T020309Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQDCkAGqlae8BYiC66XpHBo2L%2FW6aaXG81rtUbQ%2Fjk0rTgIhAOaXtPjKa%2BS0lkpePiLVKP4pmm2YN1Dwnp1o%2FtD2LgwKKogECML%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igx0YygDPKD29FuN87Iq3APBZvZ69eDdqT92%2FaLP%2B9OOey5K8P%2FRrx712BfkqiFFOqbj1akuPS66UqGeV35LCE9EzPGbAKzHt4e7Crhr28xdBPq8CkBRT%2F8MfzCOUkceKv%2BL8KSWaAsh8QeSPFH%2BVuaVUH8htNXJIH4BgseZhMuKkiCUy4jvmuRLqZlMOcOnRxRvS%2BwGRiKMyj3ZzBTjIpzVGOyssko2P4BbB9u7Dexwm%2FayFS255VjmSVe9gBklxi9if6c8MyJ2q70tkTFmvLw6pLRe7EYyhYXnVlYJPAcKKYr8%2FH9qKuhJbTTxjzrt63JGq3fJYBmWqscEPdeRXtdI9l7Nd1fS%2Fb9BihIQIf8OPJPifhqvaRhhqmcg%2BrvNRBcv%2B%2FpMx5xZG5k1KKyETR%2BgtVcRPRhdX2efnoZUg9VsEH2QUkJ0PGTAxhIqWYFgqh%2B6j6%2FKBjD5HCy5OiACbOLd7qwOPw21Jb2fRtxeZJyr40ZRjOm1t8qcMhXGRtlzkpsQ9lptYyrVjegbrk%2B7J8mzzHWxVyr1GnO3fgbbmrwzvxQUApwPNlxWwDL2MFzAvVCsGcWiyrWAvyFgizdVCjDkUlJP%2FGHy6Djd2GTfMhXsotlu4GzUufg6qOcVt%2FoTnD5YQrg%2BQMB%2BqcjdmzDkhanJBjqkAZOOYjKD69yxg93ENH91wzeFeL02zjPNgyh2DPbJUqzbeQg43MsqHoR%2F7gk7icbzDrDXZUTa76yBgJ8bBva5BrLV4lEaqxPAI%2BpeWUjrUlMWn10dHNxiWqqsMM6AQ0uh6HD4NkcSIEGaPFpe5JKa%2B7HezuPXT%2FiuGijWomHSw5J%2F6ULCxhxgju4ytiRnHaDOqzNPKQ%2BUQpfDPB%2FN5w57ZV3X2xiJ&X-Amz-Signature=876e256d71167447f2775e65c246428f647ac8f9cf2ae72585cf592ed98092df&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

      - MapReduce의 확장 및 대안 
        - MapReduce와 Java
          - MapReduce는 Java로 작성된 프로그램을 기반으로 작동합니다.
          - Java를 학습해야 MapReduce를 효과적으로 사용할 수 있습니다.
        - 대안 기술 소개
          - MapReduce 외에도 Hive, Spark와 같은 대안 기술이 등장했습니다.
          - 이러한 기술은 Java 학습 없이도 대규모 데이터 처리가 가능합니다.
        - 향후 학습 방향
          - 이후 강의에서 Hive와 Spark를 포함한 다양한 빅데이터 도구를 학습할 예정입니다.
          - 이러한 도구를 통해 MapReduce의 한계를 보완하고, 더 효율적인 데이터 처리를 배울 수 있습니다.
### 아키택쳐

- 하둡 1.0 아키텍처의 기본 구조 
  ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/3f4851a7-8d8f-4245-9e73-0e1ea9768da1/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466Y7XQP2OV%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T020310Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIAW6dDlLbY0%2FqtYA1DzAAF5I2kZKgEux1JG4r2UYkmdIAiEAh2SA5Ox1GxO5aSyakfZsp33lqHy0Ead1RKcFHuK7EccqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDG8PonUs5TGT6bM1qircAwmQt1baM6uUcK0fmdyayoxuRUxZAGhmb6Jje7AFoYUYIDnHzdDPyT67Ar%2Bkmr3do1MO32QVcAOPs0eB4bN3POjFPrQLxRLFdzfSiHCxjxZeUyrZaFjzaoRenrRVn76BPUTXK%2FKyPx4uI%2BCnetqvcu%2BcL1ez0ZX%2FXJ5YNxTdmSYxgYDIQcz5n%2BnG8t6u%2FylLGEq3ssDSCscEULRcCCH4VkIuS0ji8GF9LKzzTIJXj62P%2Bx621Ayd9xWviX1wOzQ1rFczy%2B77RRDedt9iACriTbKsqyhsdKKXCPHJ2U%2BNasn4rHkCGk7MzvgKLU5zPTqGiofKFphPh6LkzJQ3Z6PxaXmRFFkZ7ySFL1mh3BqOnrT0Smr7G5ywTAR6NHu%2BhewvE%2FMGsUZyiS%2BVm9riTBOTT5gNdJ2tzarc6tpK4W4w8gQuNHgPWVXYHvZ0jVBHeBAAu5bJnYmJS7MCCzgLWKRxwPdEbg2NeyqWTmtjB33V58m0BL0T%2F7E04%2FgoeHBiFlFNxYYgvgbboTfI%2B8fmposYfSQ5%2BZlulN6S2RKTnXDJXZ0bGG8dG8tACGQwBRBFdR57BQyzuuhFfG7wQmkCt%2FS%2B8MWV782DyYrB82h4iIIKmLggGJdKCsA3qe36QUeNMO6EqckGOqUB7kNuT6UYF%2BQfd1RdJTCqv5E5QffL%2BlNrS8Fnc%2F1l5ROcjRkWU6q%2B8U8yzR3Q4T%2FHs99aJPtjZ83s6hV%2Fcltxddr4OINKh8DjTuVYRqfylyjjQPhixu%2BLknLub8RGzoNQJjcG%2FqIWTw1iV760S2UVbjFYCNaY%2B5Qp8wZjA27Dvxr877PD4lNuHbF2lMCse%2B276tfdImGZ6gc%2FPopHO9QIsMT3gCKV&X-Amz-Signature=496099c41b2d883bdae9d65dd0994a4325db51f5867f48d108a32280fb794f9f&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

  - 마스터-슬레이브 아키텍처 
    - 하둡 1.0은 마스터-슬레이브 아키텍처를 따릅니다.
    - 하나의 네임노드(Name Node)와 여러 개의 데이터 노드(Data Nodes)로 구성됩니다.
    - 네임노드는 높은 사양을 가진 컴퓨터이며, 데이터 노드는 일반적인 하드웨어로 구성됩니다.
  - 네임노드와 데이터 노드의 역할
    - 네임노드는 메타데이터를 유지 관리하며, 데이터 노드는 실제 데이터를 저장합니다.
    - 클라이언트의 쿼리는 네임노드로 전달되고, 네임노드는 적절한 데이터 노드로 리다이렉션합니다.
    - 데이터 노드는 네임노드의 지시에 따라 작업을 수행하고 결과를 반환합니다.
  - 메타데이터 저장 및 업데이트
    - 메타데이터 저장 구조
      - 네임노드는 메타데이터 정보를 FS 이미지라는 파일에 저장합니다.
      - FS 이미지는 RAM에 저장되며, 편집 로그(Edit Log)도 RAM에 존재합니다.
      - RAM은 휘발성이므로, 편집 로그는 하드 디스크에도 저장되어 시스템 재시작 시 데이터 손실을 방지합니다.
    - 세컨더리 네임노드의 역할
      - 세컨더리 네임노드는 주 네임노드가 다운될 경우를 대비한 대체 노드입니다.
      - 세컨더리 네임노드는 주 네임노드의 메타데이터를 주기적으로 가져와 FS 이미지에 병합합니다.
      - 이 병합 과정을 체크포인트(Checkpoint)라고 하며, 주기적으로 수행됩니다.
  - 데이터 노드의 상태 모니터링 
    - 하트비트(Heartbeat) 신호
      - 데이터 노드는 정기적으로 하트비트 신호를 네임노드에 보냅니다.
      - 하트비트는 데이터 노드의 건강 상태를 나타내는 신호입니다.
      - 네임노드는 하트비트를 받지 못하면 해당 데이터 노드를 "죽은" 것으로 간주하고 작업을 다른 데이터 노드로 재배치합니다.
    - 데이터 복제와 복제 계수
      - 데이터는 여러 데이터 노드에 복제되어 저장됩니다. 이를 통해 데이터 손실을 방지합니다.
      - 복제 계수는 데이터의 복사본 수를 나타내며, 예를 들어 복제 계수가 3이면 데이터는 3개의 노드에 저장됩니다.
      - 데이터 노드가 다운되면 복제 계수가 줄어들고, 네임노드는 다른 데이터 노드에 데이터를 재배치하여 복제 계수를 회복합니다.
  - 네임노드의 가용성 문제 
    - 안전 모드(Safe Mode)
      - 네임노드는 체크포인트를 업데이트하기 위해 안전 모드로 전환됩니다.
      - 안전 모드에서는 HDFS와의 상호작용이 중단되며, 메타데이터 업데이트가 이루어집니다.
      - 이 과정에서 네임노드는 가용성이 떨어지며, 클라이언트의 쿼리를 처리할 수 없습니다.
    - 네임노드 다운 시 데이터 손실
      - 네임노드가 다운되면 최신 메타데이터가 세컨더리 네임노드에 저장되지 않아 데이터 손실이 발생할 수 있습니다.
      - 세컨더리 네임노드는 마지막 체크포인트의 메타데이터만 가지고 있으며, 최신 트랜잭션 정보는 손실됩니다.
  - 내부 구성 요소
    - 작업 추적기(Job Tracker)와 태스크 추적기(Task Tracker)
      - 네임노드 내부에는 작업 추적기라는 서비스가 존재합니다.
      - 작업 추적기는 클라이언트 요청을 처리하고 태스크 추적기에 작업을 할당합니다.
      - 태스크 추적기는 데이터 노드에서 실제 작업을 수행하고, 결과를 작업 추적기에 보고합니다.
    - 주요 단점
      - 네임노드의 다운으로 인한 메타데이터 손실이 주요 단점입니다.
      - 네임노드의 크기가 증가함에 따라 메모리 부족 문제가 발생할 수 있습니다.
      - 블록 크기가 64MB로 제한되어 있어 작은 파일을 저장할 때 비효율적입니다.
        ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/ac370360-258c-41eb-9d4b-d400f9fb29c0/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466WCG5LACR%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T020320Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQCIvyvw1%2BtMQewKDuyLiu%2BHBFNPXtvCThHGLmjLBKqQcgIgMf5inp%2Bt1tG0H1CvPjsKHHE7%2B8xt0I4aixSNpLAsVaAqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDCJEER0u4xsfvORFoSrcAzfZaeqm0y9QCGuDRNPuLYcVN9TyAgjHSxBen6RuKaOS7W1VHw%2F1Ev3JpbQhFdTbBqknn2wBhdPNCSFHd8l5NGRkz%2FWhmBZSGBl8bLJpOAj358pIQ%2B%2F7UZ0%2FK6hYWaPYU3nk5r%2BluDM9bXYuD5u2SkbiZjD8pzed4NoBQAvndgtkkAKSrmddVAqxxxw9WIiAH0ocQVZ2GmGUC0Mml7nmOYGi4Kw%2BIWhSB%2F%2Bvu3b8SNRdBtXRyPkaWCmZT4mdVjW6WgghBLs5GTFmYONnBEf2fATdK9PHdom9toOF0WTp1oJBP7s3vmpaE548FgjlQxvko9VfQafxanxm2a96%2B1u37iMNlDaxUHbDwkKmU6Y4IEZApZsb8j%2FT3lKUntrOKRdu00jWYzEdqyU4ot1cNx0CKJr1y2pfJTUGsOXhH9stxm1zr2TW1T8Pcm6Ls%2FbDdi9a1zl63NGuzW%2BngsQ1%2F3gluDDrVN5TZCjN8%2BMNRn1FAdHSE%2F83BTDvd5nyNs33011YEDlJ%2BA2ae7lUDGTbX8EAJX5f8kVOTBdvIo36VuI%2FQ%2By2XLFWrAN9WVCcIkWjuhrIOAIzCjgnAMHGfxNyYPsW2VvKCxTjlZFdBkZ3P373AA%2BsW5nRzMNTedye%2F127MPGSqckGOqUBwZQoGUDP8oIjFhEBv5Jbg1suNvL1oZctUCX1gklpF7f2m57ldZXMAky439RuyLMh%2BLimSFuqLUpZT%2F9g8hk%2BiB6d064XHumcO6%2BeErFEyhHpst36TXTWuj89P1w2jBSVFnK8DWdFZNwNIRpHkKiJ8bbGQuo809RzBss%2BmP4bI54rGKj%2FVJ6GtsQA11huFATRB3sskhz8GWot4uZx4UOTsfCIZdt6&X-Amz-Signature=1338f574c2fbd661b70bb86558d45f39ad38c7d3f2cd11793b061f5851f0410c&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

        ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/24c37d32-756e-47ab-bf20-94f9bf803ec2/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466WCG5LACR%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T020320Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQCIvyvw1%2BtMQewKDuyLiu%2BHBFNPXtvCThHGLmjLBKqQcgIgMf5inp%2Bt1tG0H1CvPjsKHHE7%2B8xt0I4aixSNpLAsVaAqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDCJEER0u4xsfvORFoSrcAzfZaeqm0y9QCGuDRNPuLYcVN9TyAgjHSxBen6RuKaOS7W1VHw%2F1Ev3JpbQhFdTbBqknn2wBhdPNCSFHd8l5NGRkz%2FWhmBZSGBl8bLJpOAj358pIQ%2B%2F7UZ0%2FK6hYWaPYU3nk5r%2BluDM9bXYuD5u2SkbiZjD8pzed4NoBQAvndgtkkAKSrmddVAqxxxw9WIiAH0ocQVZ2GmGUC0Mml7nmOYGi4Kw%2BIWhSB%2F%2Bvu3b8SNRdBtXRyPkaWCmZT4mdVjW6WgghBLs5GTFmYONnBEf2fATdK9PHdom9toOF0WTp1oJBP7s3vmpaE548FgjlQxvko9VfQafxanxm2a96%2B1u37iMNlDaxUHbDwkKmU6Y4IEZApZsb8j%2FT3lKUntrOKRdu00jWYzEdqyU4ot1cNx0CKJr1y2pfJTUGsOXhH9stxm1zr2TW1T8Pcm6Ls%2FbDdi9a1zl63NGuzW%2BngsQ1%2F3gluDDrVN5TZCjN8%2BMNRn1FAdHSE%2F83BTDvd5nyNs33011YEDlJ%2BA2ae7lUDGTbX8EAJX5f8kVOTBdvIo36VuI%2FQ%2By2XLFWrAN9WVCcIkWjuhrIOAIzCjgnAMHGfxNyYPsW2VvKCxTjlZFdBkZ3P373AA%2BsW5nRzMNTedye%2F127MPGSqckGOqUBwZQoGUDP8oIjFhEBv5Jbg1suNvL1oZctUCX1gklpF7f2m57ldZXMAky439RuyLMh%2BLimSFuqLUpZT%2F9g8hk%2BiB6d064XHumcO6%2BeErFEyhHpst36TXTWuj89P1w2jBSVFnK8DWdFZNwNIRpHkKiJ8bbGQuo809RzBss%2BmP4bI54rGKj%2FVJ6GtsQA11huFATRB3sskhz8GWot4uZx4UOTsfCIZdt6&X-Amz-Signature=25c7760b8e28d8fb0a40c2793e7505aca8c7b6b7c5adf7413908c33b6291674b&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

- Hadoop 1.0의 한계와 개선 필요성
  - Hadoop 1.0의 주요 문제점
    - 네임노드 장애: 네임노드가 실패하면 FS 이미지와 최근 트랜잭션 데이터가 손실됨.
    - 네임노드 메모리 부족: 네임노드의 메모리가 가득 차면 시스템 문제가 발생.
    - 블록 크기 제한: 블록 크기가 64MB로 제한되어 데이터 처리 효율성이 낮음.
  - Hadoop 2.0에서의 개선 사항 (00:00:46)
    - 네임노드 고가용성: Zookeeper와 Journal Node를 도입하여 네임노드 장애 문제 해결.
    - 네임노드 확장성: Federation을 통해 네임노드의 메모리 부족 문제 해결.
    - 블록 크기 증가: 블록 크기를 64MB에서 128MB로 증가.
  - 네임노드 고가용성 (High Availability) 
    - Active-Standby 구조
      ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/d117b0d0-7b51-440f-b151-0023856d3ec0/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466RK5M4QTA%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T020322Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCA0haszY4Q1lnMmuIrBprfaXTDRRS6eClaJGM%2BO%2FYvqwIhAMkDhjeuUDb12lWC7GoKRniQqQG66ktx2rB8fC8hbEDPKogECML%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igz026%2FQZwOi0nLgQBYq3AMbvJaVJzQO7%2BgYMBEaEj3pOmutnd7Ueh05w1oPZ4ii6dEelXdtphJm2JohVaAs8rCec9wm1GJ7FJrRo5mH6SuZQNQquZU6oE6h5J8BgiBbEYc3jwiXm6KavND%2B9zZEpVC7vKoiukT%2BUoeDPDPLz9dXE0mqjZSsSrjzTIiYB2tlx1ErH6MHsXEEkgYKZ5V2gG%2FCvDk%2B%2F01WXdbUOCrD%2B0Q2ZecHlcmGbfpliCl4mTQZpR5Q8UxRR2JRvjMAy8DA02oVdQkBKKYLIiLzJxAyKk30Pevp5AuS%2BylbOaGkHcpvdpdyTDAxO9eKVBuD4Hbw6l7t1V6KT55xIuJHASAq7%2FOO8C68rCv6dQO4ET0wZDp4BGOVxVvKjzjnTQTvZ6HVER07IfSh8ra58fOJTwSJ4%2F%2FjLQgLPxV4Iq6IX3vHeu3G99RUslzRIwnptHBty0vILDpSrvhFO1iruHg9pSL5%2B2wnbMmpGPjRoDoHZ0tGSHqDYdTdOVLjcENfcmkXci2v5Ej8RxSWpeblwycsSZWvROifnOB2IJlUf7wKqlPGHmz0E2M0a8zgJfe9qOYQ3upX3r8Le%2FZe0xlaICDXUtNYOEYfPH5OHj4WhaxFA381o1CeDy2ZKg5bRwYjKKCmZDDFg6nJBjqkAfbxEmtr0y%2FdkyWNv9S%2BTyzRqO0DB67Am7SUDKhJ4v7okQW3Z5IcmBvZUxbjXcBqgiJ%2FHt4VzeHUw0SVfoOxz7Z0xAZxePr0eMPjulKcSANg9JZ76R%2BJCZSdA6Ue%2Fx6bhFoBiO%2BBl8Q%2Fs4fYqg7pmrXU%2FbtEga7yLA8ReF6xu4b8Sxqf5fGRItqo00BG92ALEwkIS1rdcFzPnbC13vae7Qu2YJBU&X-Amz-Signature=3205d33f5e6b7ba2a6605dbaddc758ee8f8f9bd4d69cf78c454e087c57ba124e&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

      - Zookeeper는 Active NameNode를 감시하고, Failover Controller와 통신해 상태를 관리합니다.
      - Active NameNode는 변경된 메타데이터 정보를 JournalNode에 기록합니다.
      - Standby NameNode는 JournalNode로부터 변경사항을 읽어들여 상태를 동기화합니다.
      - 만약 Active NameNode가 다운되면:
        - Zookeeper가 감지하고,
        - Standby NameNode를 Active로 승격시킵니다.
        - 클러스터는 중단 없이 계속 작동할 수 있어요.
  - Zookeeper의 역할
    - Zookeeper 정의: 분산 애플리케이션을 위한 조정 서비스로, 클러스터 동기화를 지원.
    - Hadoop에서의 역할: 네임노드의 하트비트를 모니터링하고 다른 노드와 조율.
  - Journal Node와 데이터 복제 
    - 데이터 저장 방식: 네임노드가 FS 이미지와 Journal Node에 데이터를 동시 기록.
    - 스탠바이 네임노드: 스탠바이 네임노드가 Journal Node에서 데이터를 읽어 메타데이터를 동기화.
  - 장애 시 처리 및 Split Brain 방지
    - 장애 처리: Zookeeper가 네임노드의 하트비트를 감지하지 못하면 스탠바이 네임노드를 활성화.
    - Split Brain 방지: Zookeeper가 Java 프로그램(Fencing)을 통해 중복 활성화를 방지.
  - YARN의 도입과 역할
    ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/c6827ddf-e567-4a70-b8f1-52055b7df3d1/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663EZSLKL2%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T020324Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIFbXmomChv4URftQwfW2bu18S0X0LdZ6XG56l%2BHv0nyXAiEA%2FZMJRJo7apS9nBIvU3%2FB6r%2BvAVvjQqQI%2B7k5uzWdNzkqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDDRh394rnIQNOZ4KZCrcA4CyDXNJ%2BX0Q7ikvHKHGIh%2FA64otW%2FHQwNlxja2cPWBaIEfTS%2FbOP5fWlkWWImMNPF2QUoadQ0c93VKyCrh8YcwWs3KpYynRnfdpZwcOLxZNrsbJKu7kXhmSce3eQXUJ162zpcCxxjlk24E%2FkOAaakh%2FKj5LVf1NEo0HY6dOZGcwaYJlfZqmy6NcY7gNMN9UQWxY3RWHdICv2AfzKqIjQzZKPbxdA5EtqpOaoP3H%2B8uTl77jhclMec7D%2FCue3dJVgyObUb1MFNAglJQ4h8HNLgqmZUu7pjJ6hAzhfnnBH3lYVjPPFSs9eDuTaK87neWDFKZ1B4AA1BMRJwivOUmCJr%2FVF6yhn6TmeGCX7sA%2BTNbNVd9MRPgbK1YzFz9rfeymP%2Fpme%2BOImajZg5yAiuON3FQ8Dex5ZL77tbqboFqPgd4YR1XMoplHG%2FAsNQjdceMVFTiq0LmuHDrzRIMkhwoCxYrOq05o3eqeE4PMxN7Z6nVugqHThppOj7n01UVB6g0WFK61BcT25U3vEHJvG5r86IHc7v60GOc4rbBNgSk04omVHN0g4W7oqmjP1KmtSDBRgJTsWvpWycd4k2388uivDNWElCOEPbzx85dbxWmTVwzpcMQNq1iRamWfGdhjMOGHqckGOqUBIoq7f8ZsykBiKkbcTEcuPx0z52imPvq7mwoymnPNeLi5io8K%2FgcWvhYuWCl7kAbnvQ3z%2F3VNMxVHXVxU1VsUWvJZf4oMB5AiXtBD4m6Ok72QozgoOBUrk4e%2B%2BHvT0ggBHnN%2FzF%2FCX4V0B%2BCLENhzpiEKwUIq7Ud0LFvqjUlkrDe56K228y2uYG%2FVyyGSvB7EIoZYjg38lGDciinrBdaYyesVXKvd&X-Amz-Signature=a6758a1d70c1ca9562ee0069a1ce1d791e86b134991e97bb1548d23b7d26a007&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

    - YARN의 정의와 중요성
      - YARN 정의: Yet Another Resource Negotiator로, 자원 관리 및 작업 스케줄링 기술.
      - 중요성: MapReduce 외에도 Hive, Spark 등 다양한 도구를 지원하여 유연성 증가.
    - YARN의 주요 구성 요소 
      ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/9493e635-b173-4607-b0f5-cb367ca4d62f/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666QMHGYG4%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T020325Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQDxDHVSHrhMv7KP5QCmTgZ5FDumhN1FwSZkIbSVCUG8pgIgMM9b%2Fyh71ly%2FIC%2Bq2vRKFgzZikryZhhLt4A6IzYm2ycqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDEAiSpubYJTn1Hg2hircAy1rEewz6ovsovfU1lEgoVx8xs0EDVDL0nelWIGAIrMO4BQdhUjG7ooI5FzcPutgrkuaP%2BJHKNGiE4sHkQn5FV2RCgF%2FY0dsdttIJ2IhW4rI9OpQZpFpIE6ObHldT2DMcdBxmfR%2FVOgk0n1jzh5S7DYta0azki5liHfWmnLXGfPrTmq7PtQ9kvDxdiLFt%2B96fNSZ4GogtgbMnPQd4YUoAqbZrrjzJPfPptdCKiHEBF%2FbR4besQtwtga0bODzv4wzAPaJOuLCFwqeeUT7KvmI2dTIcMqZ1ky09e8EOKWvH6xcYbLMN2XEg2oA2iVtQMO14lHULZi3kKDRyN56giAlep6aoFbygSTU3qXkvKq%2Bf7Hu9809OyuSVLRSU%2FDEa4zkEMhUMpbQWSaj5LuGTXRltrqM7e0mummkJ3WTJYqgo6QiJbbqvr%2BFhpeMtupz6i303AgqHxBdA5ZEdyDUwuujw5bNkNSIN8GGKsIXtBHGsrvpnR3msv2BmUC9uAKmd7fhEMPVE6Fo4cfwaWCeAePoY%2FzIk1KGnzdabZIEOHYI8gfxJAF1ztdQ%2FRODkAimfh4LKpTWpSfrrD4Ax0vLKP64Bfc6PpJbbBEDDVyjADVx9I5JloYCWUvDcc4%2F58L0MLGEqckGOqUBxphpOop8kEIk9YlkPSt1iQSpdgH6vU85gmSrBHAIkBXpBX31mlJW%2BKn%2F%2FHuPzIaJZqng6JL%2BC72cM5NJs%2BU30RAOQRhXiar3sps3seQdNNEk8EGofofq4%2BAMDhy9%2BhSRCVbhX1ZvhQxb1NmJwPtFXmgbOXvUN3UKxhjMW3WUyn82SxB2AELYO%2Fdf4UC3lG5P6Q2QaW4QrisLc8DIZf8XVyHPfXXe&X-Amz-Signature=5562c317a24010086d3c4aae53504d40b1d5f7a6765d7e2caf65b3f4982bf0c6&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

      - 리소스 매니저
        - 클러스터 전체의 리소스를 관리하고, 어느 노드에서 어떤 작업을 실행할지 결정해요.
        - YARN의 두뇌, 이전의 Job Tracker에서 이름 변경, 네임노드에서 실행.
        - 주요 역할:
          - Node 상태 모니터링
          - 자원 할당
          - ApplicationMaster 실행 요청
      - 노드 매니저
        - 각 노드마다 존재하는 YARN 에이전트
        - 이전의 Task Tracker에서 이름 변경, 데이터 노드에서 실행.
        - Resource Manager에게 현재 자원 상태(메모리, CPU 등)를 보고하고, 명령을 받아 컨테이너를 실행시켜요.
      - Container
        - YARN이 작업을 실행하기 위해 자원을 할당한 단위입니다.
        - 메모리, CPU 등의 리소스를 갖고 있고, 이 안에서 실제 작업(Task)이 수행돼요.
        - 예: Mapper나 Reducer 같은 것들이 실행됨.
      - Application Master (App Mstr)
        - 각 애플리케이션(Job)마다 하나씩 존재합니다.
        - App Mstr 자체도 컨테이너, Yarn의 컨테이너 단위 실행 원칙을 지키기 위함
        - ResourceManager로부터 컨테이너를 할당받고, 그 안에서 실행됩니다.
        - 데이터를 찾을 때 메타데이터를 통해서 확인하고, 해당 데이터노드에 컨테이너를 배치해달라고 ResourceManager에게 요청함
        - 주요 역할:
          - 어떤 작업을 어떤 노드에 분배할지 결정
          - 작업(Task)의 상태 모니터링
          - 문제가 생기면 다시 실행 요청 등
    - 작업 처리 흐름
      - 작업 제출: 클라이언트가 리소스 매니저에 작업을 제출.
      - 애플리케이션 매니저 생성: 리소스 매니저가 애플리케이션 매니저를 생성하고 클라이언트에 정보 전달.
      - 컨테이너에서 작업 실행: 애플리케이션 매니저가 작업을 컨테이너에 전달하여 실행.
      - 작업 완료 후 메모리 해제: 작업이 완료되면 컨테이너 메모리가 해제되고 애플리케이션 매니저가 삭제.
  - Hadoop 2.0의 내부 작동 방식 
    - 작업 ID와 로그 추적 (00:14:49)
      - 작업 ID 생성: 각 작업에 고유한 애플리케이션 ID가 생성되어 로그 추적 가능.
      - 문제 해결: 애플리케이션 ID를 사용해 로그를 확인하고 문제를 분석.
    - Hadoop 2.0의 주요 변화 요약
      - 네임노드 고가용성: Zookeeper와 Journal Node를 통한 데이터 손실 방지.
      - 네임노드 확장성: Federation으로 메모리와 저장 공간 문제 해결.
      - YARN 도입: 다양한 도구 지원으로 유연성과 효율성 향상.
- Hadoop 3.0 개요
  - Hadoop 3.0의 도입 배경
    - Hadoop 3.0은 이전 버전인 Hadoop 2.0과 비교하여 여러 중요한 변경 사항을 포함하고 있음.
    - 대부분의 프로젝트는 여전히 Hadoop 2.0을 사용하지만, 새로운 기능과 성능 최적화로 인해 3.0으로의 전환이 필요함.
    - Java 8이 필수적으로 요구되며, 이전 버전의 Java는 지원되지 않음.
  - 주요 변경 사항
    - 기본 포트 변경 및 성능 최적화가 이루어짐.
    - 두 개의 네임노드 지원: 하나는 활성 상태, 나머지 두 개는 대기 상태로 설정됨.
    - 데이터 복제 방식에서 새로운 개념인 소멸 코딩(erasure coding)이 도입됨.
  - 소멸 코딩(erasure coding)의 개념
    - 소멸 코딩의 정의와 목적
      - 소멸 코딩은 데이터 손실을 방지하기 위한 오류 수정 코드로, 데이터를 여러 블록으로 나누고 패리티 블록을 추가함.
      - 패리티 블록이란 원본 데이터 블록들을 계산해서 만든 복구용 블록
        ```plain text
        → 여기서 패리티 블록(P1) 만들기:
        
        P1 = 블록1 + 블록2 + 블록3 = 100 + 150 + 200 = 450
        
        이제 블록2가 날아가도,
        
        블록2 = P1 - 블록1 - 블록3 = 450 - 100 - 200 = 150
        ```

      - 패리티 블록을 사용하여 손실된 데이터를 복원할 수 있음.
      - 데이터 복제 없이 데이터 손실 문제를 해결하며 저장 공간을 절약함.
    - 데이터 복제와 소멸 코딩의 차이점
      - 데이터 복제 방식에서는 데이터가 여러 번 복제되어 저장 공간과 메모리 자원을 많이 소비함.
      - 소멸 코딩은 패리티 블록을 사용하여 데이터 복제를 대체하며, 저장 공간과 비용을 절감함.
      - 패리티 블록은 XOR 알고리즘을 사용하여 생성됨.
    - XOR 알고리즘의 원리
      - XOR은 배타적 OR을 의미하며, 입력 비트가 동일하면 0, 다르면 1을 출력하는 논리 연산임.
      - 데이터 블록의 비트를 XOR 연산하여 패리티 블록을 생성함.
      - 예를 들어, 데이터 블록 A와 B의 비트를 XOR 연산하면 패리티 블록이 생성됨.
  - 데이터 복구 과정
    - 데이터 복구의 원리 
      - 데이터 블록이 손실되었을 경우, 패리티 블록과 남아있는 데이터 블록을 사용하여 손실된 데이터를 복구할 수 있음.
      - XOR 연산을 통해 손실된 데이터 블록을 재구성함.
    - 소멸 코딩의 한계
      - 소멸 코딩은 한 개의 데이터 블록 손실만 복구 가능하며, 두 개 이상의 블록이 손실되면 복구가 불가능함.
      - 이를 극복하기 위해 Reed-Solomon 알고리즘이 사용될 수 있음.
    - Reed-Solomon 알고리즘 소개
      - Reed-Solomon 알고리즘은 더 높은 수준의 데이터 복구를 가능하게 함.
      - 이 알고리즘은 정체 행렬(identity matrix)을 사용하여 손실된 데이터를 복구함.
      - 추가적인 학습을 위해 Google에서 관련 자료를 검색할 것을 권장함.
  - 소멸 코딩의 실무적 중요성 
    - 이론적 이해의 필요성
      - 소멸 코딩과 관련된 이론은 일반적인 정보로서 유용하며, 엔지니어로서 기본적인 이해를 갖추는 것이 좋음.
      - 실무에서는 이론적 세부 사항을 깊이 이해하지 않아도 문제 없음.
    - 실무에서의 활용
      - 소멸 코딩은 데이터 손실 방지와 저장 공간 절약을 위해 중요한 기술로 활용됨.
      - 엔지니어와 소프트웨어 개발자는 이를 통해 효율적인 데이터 관리와 비용 절감을 실현할 수 있음.
    - 추가 학습 권장 
      - Reed-Solomon 알고리즘과 같은 고급 기술은 필요에 따라 학습 가능하며, 인터넷에서 관련 자료를 쉽게 찾을 수 있음.
      - 이론적 배경은 실무에서 직접적으로 필요하지 않더라도, 기술적 이해를 높이는 데 도움을 줄 수 있음.

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

