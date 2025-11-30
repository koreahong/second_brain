---
title: MiniIO
type: resource
tags:
  - minio
  - technology
  - storage
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---


---

## 📋 Qraft 적용 사례

MinIO는 S3 호환 오브젝트 스토리지로, HFT팀의 바이너리 데이터 저장을 위해 2025년 9월 아키텍처로 결정되었습니다.

### 주요 적용 배경
- **PCAP 데이터 저장**: HFT팀의 네트워크 패킷 데이터를 바이너리로 저장
- **DB 대안**: 리서처의 백테스팅 요구사항에 맞는 파일 기반 저장소
- **중앙 관리**: 기존 분산된 파일 저장을 중앙화하면서도 성능 유지

---

## 📎 Related

### 사용된 프로젝트 (Qraft)

**[[HFT팀-데이터-요청|HFT팀 PCAP 데이터 처리]]** (2025년 9월)
   - **시기**: [[2025년-9월-8일|2025년 9월 8일]]
   - **문제**: DB 기반 저장 방식으로는 HFT팀 백테스팅 요구 충족 불가
   - **해결**: **MinIO 기반 스토리지 아키텍처** 결정
   - **효과**:
     - 리서처는 기존 바이너리 데이터 활용 방식 유지
     - 중앙 관리 및 거버넌스 가능
     - UDP 손실 고려한 PCAP 데이터 효율적 저장

### Knowledge

- [[DataHub|DataHub]] - MinIO 메타데이터 관리 (계획)
- [[Airflow|Airflow]] - MinIO 데이터 적재 오케스트레이션

