---
tags:
  - datahub
  - mcp
  - model-context-protocol
  - ai-agent
  - metadata
  - lineage
  - qraft
  - reference
created: 2025-11-30
updated: 2025-11-30
company: 크래프트테크놀로지스
status: evergreen
type: reference
---

# DataHub MCP Server

## 📋 개요

**DataHub MCP Server**는 Model Context Protocol (MCP)을 구현한 서버로, AI 에이전트가 DataHub의 메타데이터를 자연어로 쿼리하고 활용할 수 있게 해주는 인터페이스입니다.

**핵심 가치**: "AI 에이전트가 신뢰할 수 있는 데이터를 찾고, 리니지를 추적하며, 비즈니스 맥락을 이해하여 정확한 SQL을 생성할 수 있도록 지원"

## 🎯 핵심 개념

> 💡 가장 중요한 3가지

1. **Metadata Context for AI**: LLM이 조직의 데이터 자산 구조를 이해하고 활용
2. **Lineage-Aware Queries**: 데이터 흐름과 의존성을 파악하여 영향도 분석
3. **Natural Language Interface**: 자연어 질문으로 데이터 검색 및 SQL 생성

## 🔍 상세 설명

### First Principles (근본 원리)

**왜 DataHub MCP가 만들어졌는가?**

전통적인 데이터 카탈로그는 **사람이 UI를 통해 검색**하도록 설계되었습니다. 하지만 AI 시대에는:
- AI 에이전트가 **자율적으로** 데이터를 탐색해야 함
- **맥락(context)**을 이해하고 적절한 데이터를 선택해야 함
- **리니지**를 추적하여 영향도를 분석해야 함

DataHub MCP는 이러한 문제를 해결하기 위해, AI 에이전트가 DataHub 메타데이터에 접근할 수 있는 **표준화된 인터페이스**를 제공합니다.

### 작동 방식

**비유**: DataHub MCP는 "데이터 카탈로그의 사서(Librarian)"와 같습니다.

## 💻 실전 활용

### Qraft에서의 활용 방안

현재 Qraft에서 운영 중인 DataHub 환경에 MCP를 추가하면:
- **데이터 발견**: Claude Code가 자동으로 적절한 데이터 찾기
- **영향도 분석**: 스키마 변경 시 영향받는 팀 자동 알림
- **SQL 생성**: 자연어로 쿼리 요청 → 정확한 SQL 자동 생성
- **품질 모니터링**: Critical 데이터셋 일일 자동 체크

## 🔗 관련 개념

### Qraft 프로젝트 문서
- [[DataHub-도입]] - Qraft에서의 DataHub 도입 과정
- [[DataHub-커스텀-구현-상세]] - Custom Source 및 Runtime Patch
- [[데이터-거버넌스-전략-수립]] - 거버넌스 체계

### 관련 Weekly
- [[2025년-11월-24일]] - DataHub 론칭 및 MCP 활용 계획

---

**작성일**: 2025-11-30
**작성자**: Data Analytics Engineer
**참고**: DataHub v0.13.0 및 MCP Server 기준
