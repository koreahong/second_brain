#!/usr/bin/env python3
"""
Batch connect remaining Qraft project files
"""

import os
from pathlib import Path

# Project groupings
GROUPS = {
    "인프라/파이프라인": [
        "gitlab ci cd 세팅.md",
        "MinIO 적재 - 호출 테스트.md",
        "sftp 적재 테스트.md",
        "HFT lseg sftp 파일 배치 dag 개발.md",
        "git setting.md",
    ],
    "데이터 개발": [
        "Invesco 크롤링 데이터 개발.md",
        "slickcharts 마이그레이션.md",
        "flex master table 개발.md",
        "qraft_origin으로 옮기기.md",
    ],
    "벤더 소통": [
        "factset 영업 담당자님 소통.md",
        "지혜님 FRED 기안 혹은 갱신건 요청.md",
        "refinitiv DSS quota 종목 줄이기.md",
    ],
    "팀 협업": [
        "HFT팀 NYSE ARCA 데이터 찾기.md",
        "MFT팀 배치 작업.md",
        "MFT팀 데이터벤토, DataScope 적재위치 물어보기.md",
    ],
    "프로세스 정립": [
        "데이터 구매 - 적재 요청 프로세스 정립.md",
        "적재 - 구매 프로세스 그리기.md",
        "팀별 데이터 거버넌스 깊이 설정.md",
        "데이터벤토 관리 방안.md",
    ],
    "온보딩/문서화": [
        "업무 범위 파악, 문서 디렉토리 정리.md",
        "데이터 온보딩.md",
        "Jira 업무방식 결정.md",
        "ERD 작성.md",
        "벤더사 테이블 명세서 요청.md",
    ],
    "기타 작업": [
        "전사공지.md",
        "팀별 질문 사항.md",
        "상구님 질문.md",
        "Data Guide 계정 찾기.md",
        "confluence draw.io app download 김보성님 요청.md",
        "요청하는 피카츄 워크플로 변경.md",
        "iceberg + datahub.md",
    ],
}

def add_related_section(file_path: Path, related_content: str):
    """Add Related section to a file if it doesn't have one"""
    content = file_path.read_text(encoding='utf-8')

    # Skip if already has Related section
    if "## 🔗 Related" in content:
        print(f"  ⏭️  Skipped (already has Related): {file_path.name}")
        return False

    # Add Related section at the end
    new_content = content.rstrip() + "\n\n" + related_content
    file_path.write_text(new_content, encoding='utf-8')
    print(f"  ✅ Added Related section: {file_path.name}")
    return True

def main():
    base_path = Path("/Users/qraft_hongjinyoung/DAE-Second-Brain/Experiences/Qraft/Projects")

    # Infrastructure/Pipeline group
    print("\n🔧 Infrastructure/Pipeline Group:")
    infra_files = GROUPS["인프라/파이프라인"]
    for filename in infra_files:
        file_path = base_path / filename
        if not file_path.exists():
            print(f"  ⚠️  Not found: {filename}")
            continue

        related = """---

## 🔗 Related

### 인프라/파이프라인 프로젝트
- [[airflow 3.0, dbt local test]] - Airflow 환경 구축
- [[gitlab ci cd 세팅]] - CI/CD 파이프라인
- [[MinIO 적재 - 호출 테스트]] - MinIO 스토리지 테스트
- [[sftp 적재 테스트]] - SFTP 데이터 전송
- [[git setting]] - Git 설정

### 관련 Hub
- [[Experiences/Qraft/README]] - Qraft 경험 모음
"""
        add_related_section(file_path, related)

    # Data Development group
    print("\n📊 Data Development Group:")
    data_dev_files = GROUPS["데이터 개발"]
    for filename in data_dev_files:
        file_path = base_path / filename
        if not file_path.exists():
            print(f"  ⚠️  Not found: {filename}")
            continue

        related = """---

## 🔗 Related

### 데이터 개발 프로젝트
- [[Invesco 크롤링 데이터 개발]] - Invesco 데이터 수집
- [[slickcharts 마이그레이션]] - Slickcharts 데이터 이전
- [[flex master table 개발]] - Master 테이블 개발
- [[qraft_origin으로 옮기기]] - DB 마이그레이션

### 적재 파이프라인
- [[원천 데이터 적재 파이프라인 개발]] - 적재 파이프라인 구축

### 관련 Hub
- [[Experiences/Qraft/README]] - Qraft 경험 모음
"""
        add_related_section(file_path, related)

    # Vendor Communication group
    print("\n🤝 Vendor Communication Group:")
    vendor_files = GROUPS["벤더 소통"]
    for filename in vendor_files:
        file_path = base_path / filename
        if not file_path.exists():
            print(f"  ⚠️  Not found: {filename}")
            continue

        related = """---

## 🔗 Related

### 벤더 소통 프로젝트
- [[factset 영업 담당자님 소통]] - FactSet 벤더 협력
- [[지혜님 FRED 기안 혹은 갱신건 요청]] - FRED 데이터 계약
- [[refinitiv DSS quota 종목 줄이기]] - Refinitiv 할당량 조정

### 데이터 계약
- [[팀별 원천 데이터 계약현황 파악]] - 데이터 계약 현황

### 관련 Hub
- [[Experiences/Qraft/README]] - Qraft 경험 모음
"""
        add_related_section(file_path, related)

    # Team Collaboration group
    print("\n👥 Team Collaboration Group:")
    team_files = GROUPS["팀 협업"]
    for filename in team_files:
        file_path = base_path / filename
        if not file_path.exists():
            print(f"  ⚠️  Not found: {filename}")
            continue

        # Custom related for each team file
        if "HFT" in filename:
            related = """---

## 🔗 Related

### HFT 팀 프로젝트
- [[HFT팀 데이터 요청 ]] - HFT 데이터 요청
- [[HFT lseg sftp 파일 배치 dag 개발]] - SFTP 배치 개발

### 관련 Hub
- [[Experiences/Qraft/README]] - Qraft 경험 모음
"""
        elif "MFT" in filename:
            related = """---

## 🔗 Related

### MFT 팀 프로젝트
- [[MFT팀 데이터 요청]] - MFT 데이터 요청
- [[MFT팀 데이터 사용현황 파악]] - MFT 사용 현황
- [[MFT팀 배치 작업]] - MFT 배치 작업
- [[MFT팀 데이터벤토, DataScope 적재위치 물어보기]] - 데이터 위치 조사

### 관련 Hub
- [[Experiences/Qraft/README]] - Qraft 경험 모음
"""
        add_related_section(file_path, related)

    # Process Establishment group
    print("\n📋 Process Establishment Group:")
    process_files = GROUPS["프로세스 정립"]
    for filename in process_files:
        file_path = base_path / filename
        if not file_path.exists():
            print(f"  ⚠️  Not found: {filename}")
            continue

        related = """---

## 🔗 Related

### 프로세스 정립 프로젝트
- [[데이터 구매 - 적재 요청 프로세스 정립]] - 구매/적재 프로세스
- [[적재 - 구매 프로세스 그리기]] - 프로세스 문서화
- [[팀별 데이터 거버넌스 깊이 설정]] - 거버넌스 수준 설정
- [[데이터벤토 관리 방안]] - 데이터벤토 관리

### 원천 데이터 관리
- [[팀별 원천 데이터 계약현황 파악]] - 데이터 계약 현황

### 관련 Hub
- [[Experiences/Qraft/README]] - Qraft 경험 모음
"""
        add_related_section(file_path, related)

    # Onboarding/Documentation group
    print("\n📚 Onboarding/Documentation Group:")
    onboard_files = GROUPS["온보딩/문서화"]
    for filename in onboard_files:
        file_path = base_path / filename
        if not file_path.exists():
            print(f"  ⚠️  Not found: {filename}")
            continue

        related = """---

## 🔗 Related

### 온보딩/문서화 프로젝트
- [[업무 범위 파악, 문서 디렉토리 정리]] - 업무 범위 정의
- [[데이터 온보딩]] - 데이터 온보딩 가이드
- [[Jira 업무방식 결정]] - 협업 프로세스
- [[ERD 작성]] - 데이터 모델링
- [[벤더사 테이블 명세서 요청]] - 데이터 스펙 문서화

### 관련 Hub
- [[Experiences/Qraft/README]] - Qraft 경험 모음
"""
        add_related_section(file_path, related)

    # Others group
    print("\n🔧 Other Projects:")
    other_files = GROUPS["기타 작업"]
    for filename in other_files:
        file_path = base_path / filename
        if not file_path.exists():
            print(f"  ⚠️  Not found: {filename}")
            continue

        related = """---

## 🔗 Related

### 관련 Hub
- [[Experiences/Qraft/README]] - Qraft 경험 모음
"""
        add_related_section(file_path, related)

    print("\n✅ Qraft project connections complete!")

if __name__ == "__main__":
    main()
