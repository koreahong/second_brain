#!/usr/bin/env python3
"""
Create upgraded Notion templates based on actual user writing patterns
Combines user's proven structures with research-based frameworks
"""

import requests
import json
from pathlib import Path


def load_config():
    config_file = Path(__file__).parent / "config.json"
    with open(config_file) as f:
        return json.load(f)


def get_headers(api_token):
    return {
        'Authorization': f'Bearer {api_token}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }


def get_templates():
    """Define upgraded templates based on user's actual patterns"""
    return [
        {
            "name": "📋 [템플릿] Project",
            "content_type": "Project",
            "status": "Active",
            "priority": "Medium",
            "company": "Qraft",
            "category": ["Technology"],
            "tags": [],
            "blocks": [
                {"type": "heading_2", "text": "📋 프로젝트 개요"},
                {"type": "paragraph", "text": "이 프로젝트가 무엇이고, 왜 필요한지 간단히 설명하세요."},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🎯 목표 (SMART)"},
                {"type": "bulleted_list_item", "text": "Specific: 구체적으로 무엇을 달성할 것인가?"},
                {"type": "bulleted_list_item", "text": "Measurable: 어떻게 측정할 것인가?"},
                {"type": "bulleted_list_item", "text": "Achievable: 현실적으로 달성 가능한가?"},
                {"type": "bulleted_list_item", "text": "Relevant: 왜 중요한가? (비즈니스 임팩트)"},
                {"type": "bulleted_list_item", "text": "Time-bound: 언제까지? (마감일)"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🔍 현황 분석"},
                {"type": "heading_3", "text": "Situation (현재 상황)"},
                {"type": "paragraph", "text": "프로젝트를 시작하게 된 배경과 현재 문제점은?"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "Task (해결할 과제)"},
                {"type": "bulleted_list_item", "text": "기술적 과제: "},
                {"type": "bulleted_list_item", "text": "비즈니스 과제: "},
                {"type": "bulleted_list_item", "text": "팀/프로세스 과제: "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🛠️ 구현 계획"},
                {"type": "heading_3", "text": "기술 스택"},
                {"type": "bulleted_list_item", "text": "데이터베이스: "},
                {"type": "bulleted_list_item", "text": "파이프라인: "},
                {"type": "bulleted_list_item", "text": "모니터링: "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "주요 마일스톤"},
                {"type": "numbered_list_item", "text": "Phase 1: "},
                {"type": "numbered_list_item", "text": "Phase 2: "},
                {"type": "numbered_list_item", "text": "Phase 3: "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "📊 완료 사항"},
                {"type": "callout", "emoji": "✅", "text": "완료된 작업들을 업데이트하세요"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🎯 주요 성과"},
                {"type": "heading_3", "text": "기술적 성과"},
                {"type": "bulleted_list_item", "text": ""},

                {"type": "heading_3", "text": "비즈니스 성과"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "📊 메트릭"},
                {"type": "paragraph", "text": "| 항목 | 목표 | 달성 |"},
                {"type": "paragraph", "text": "|------|------|------|"},
                {"type": "paragraph", "text": "| SLA | 99% | - |"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "💡 인사이트 & 회고"},
                {"type": "heading_3", "text": "Keep (계속할 것)"},
                {"type": "bulleted_list_item", "text": ""},

                {"type": "heading_3", "text": "Problem (문제점)"},
                {"type": "bulleted_list_item", "text": ""},

                {"type": "heading_3", "text": "Try (시도할 것)"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🔗 관련 자료"},
                {"type": "bulleted_list_item", "text": "관련 프로젝트: "},
                {"type": "bulleted_list_item", "text": "참고 문서: "},
                {"type": "bulleted_list_item", "text": "관련 기술: "},
            ]
        },

        {
            "name": "📝 [템플릿] Experience (Weekly)",
            "content_type": "Experience",
            "status": "Active",
            "priority": "High",
            "company": "Qraft",
            "category": ["Reflection"],
            "tags": ["weekly"],
            "blocks": [
                {"type": "heading_2", "text": "📋 주간 요약"},
                {"type": "paragraph", "text": "이번 주를 한 문장으로 요약한다면? (예: 이번 주는 **DataHub 론칭**을 완료한 주입니다)"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🎯 주요 업무"},
                {"type": "callout", "emoji": "💡", "text": "이번 주 집중했던 프로젝트나 작업들을 구체적으로 작성하세요"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "[프로젝트명 1]"},
                {"type": "paragraph", "text": "**완료 사항**:"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},
                {"type": "paragraph", "text": "**기술적 성과**:"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "[프로젝트명 2]"},
                {"type": "paragraph", "text": "**완료 사항**:"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "💡 인사이트"},
                {"type": "callout", "emoji": "🔍", "text": "이번 주 배운 것, 깨달은 것을 기록하세요"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "[인사이트 제목 1]"},
                {"type": "paragraph", "text": "무엇을 배웠고, 왜 중요한가?"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "[인사이트 제목 2]"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🤔 ORID 회고"},
                {"type": "heading_3", "text": "Objective (객관적 사실)"},
                {"type": "paragraph", "text": "이번 주 무슨 일이 있었나?"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "Reflective (느낀 점)"},
                {"type": "paragraph", "text": "어떤 감정이 들었나? 무엇이 인상깊었나?"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "Interpretive (의미)"},
                {"type": "paragraph", "text": "왜 그런 일이 일어났을까? 무엇을 배웠나?"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "Decisional (다음 행동)"},
                {"type": "paragraph", "text": "다음 주에 무엇을 할 것인가?"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "📊 메트릭"},
                {"type": "paragraph", "text": "| 항목 | 수치 |"},
                {"type": "paragraph", "text": "|------|------|"},
                {"type": "paragraph", "text": "| 완료 태스크 | X개 |"},
                {"type": "paragraph", "text": "| 작성 코드 라인 | X줄 |"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🔗 관련 프로젝트"},
                {"type": "bulleted_list_item", "text": "메인 프로젝트: "},
                {"type": "bulleted_list_item", "text": "세부 프로젝트: "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "📚 관련 지식"},
                {"type": "bulleted_list_item", "text": "사용한 기술: "},
                {"type": "bulleted_list_item", "text": "학습한 개념: "},
            ]
        },

        {
            "name": "📚 [템플릿] Reference",
            "content_type": "Reference",
            "status": "Active",
            "priority": "Medium",
            "company": "",
            "category": ["Technology"],
            "tags": [],
            "blocks": [
                {"type": "heading_2", "text": "📋 개요"},
                {"type": "paragraph", "text": "이 기술/개념이 무엇인지 한 문장으로 설명하세요 (Feynman: 단순하게!)"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🎯 핵심 개념"},
                {"type": "callout", "emoji": "💡", "text": "가장 중요한 3가지만 뽑는다면?"},
                {"type": "numbered_list_item", "text": ""},
                {"type": "numbered_list_item", "text": ""},
                {"type": "numbered_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🔍 상세 설명"},
                {"type": "heading_3", "text": "First Principles (근본 원리)"},
                {"type": "paragraph", "text": "왜 이 기술이 만들어졌는가? 어떤 문제를 해결하는가?"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "작동 방식"},
                {"type": "paragraph", "text": "어떻게 동작하는가? (비유를 사용하여 설명)"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "주요 구성요소"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "💻 실전 활용"},
                {"type": "heading_3", "text": "언제 사용하는가?"},
                {"type": "bulleted_list_item", "text": "Use case 1: "},
                {"type": "bulleted_list_item", "text": "Use case 2: "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "Best Practices"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "코드 예제"},
                {"type": "code", "language": "python", "text": "# 간단한 사용 예제\n"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "⚠️ 주의사항 & 한계"},
                {"type": "bulleted_list_item", "text": "이런 경우엔 사용하지 마세요: "},
                {"type": "bulleted_list_item", "text": "알려진 문제점: "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🔗 관련 개념"},
                {"type": "bulleted_list_item", "text": "유사 기술: "},
                {"type": "bulleted_list_item", "text": "대안 기술: "},
                {"type": "bulleted_list_item", "text": "함께 사용하는 기술: "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "📖 참고 자료"},
                {"type": "bulleted_list_item", "text": "공식 문서: "},
                {"type": "bulleted_list_item", "text": "유용한 블로그: "},
                {"type": "bulleted_list_item", "text": "강의/튜토리얼: "},
            ]
        },

        {
            "name": "💡 [템플릿] Insight (본깨적)",
            "content_type": "Insight",
            "status": "Active",
            "priority": "Medium",
            "company": "",
            "category": ["Life"],
            "tags": [],
            "blocks": [
                {"type": "heading_2", "text": "💡 핵심 인사이트"},
                {"type": "paragraph", "text": "한 문장으로 이 깨달음을 표현한다면?"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "📖 경험 (Context)"},
                {"type": "paragraph", "text": "언제, 어디서, 무슨 일이 있었나?"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🤔 생각의 흐름"},
                {"type": "heading_3", "text": "처음 생각"},
                {"type": "paragraph", "text": "처음엔 어떻게 생각했는가?"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "전환점"},
                {"type": "paragraph", "text": "무엇이 생각을 바꾸게 했는가?"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "깨달음"},
                {"type": "paragraph", "text": "결국 무엇을 배웠는가?"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🎯 First Principles 분석"},
                {"type": "callout", "emoji": "🔍", "text": "근본적인 진실은 무엇인가? 가정을 벗겨내면 남는 것은?"},
                {"type": "bulleted_list_item", "text": "가정: "},
                {"type": "bulleted_list_item", "text": "근본 원리: "},
                {"type": "bulleted_list_item", "text": "새로운 접근: "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🧠 Mental Model"},
                {"type": "paragraph", "text": "이 인사이트를 다른 상황에도 적용할 수 있는 프레임워크는?"},
                {"type": "paragraph", "text": ""},
                {"type": "paragraph", "text": "**적용 가능한 다른 상황들:**"},
                {"type": "bulleted_list_item", "text": "업무: "},
                {"type": "bulleted_list_item", "text": "개인생활: "},
                {"type": "bulleted_list_item", "text": "관계: "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "✅ 실천 계획"},
                {"type": "paragraph", "text": "이 깨달음을 어떻게 실천할 것인가?"},
                {"type": "numbered_list_item", "text": "즉시 실천: "},
                {"type": "numbered_list_item", "text": "습관화: "},
                {"type": "numbered_list_item", "text": "장기 목표: "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🔗 관련 인사이트"},
                {"type": "bulleted_list_item", "text": "유사한 경험: "},
                {"type": "bulleted_list_item", "text": "반대되는 관점: "},
            ]
        },

        {
            "name": "📰 [템플릿] Article",
            "content_type": "Article",
            "status": "Active",
            "priority": "Medium",
            "company": "",
            "category": ["Reading"],
            "tags": [],
            "blocks": [
                {"type": "heading_2", "text": "📋 기본 정보"},
                {"type": "paragraph", "text": "**제목**: "},
                {"type": "paragraph", "text": "**출처**: "},
                {"type": "paragraph", "text": "**링크**: "},
                {"type": "paragraph", "text": "**작성일**: "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "📌 주요 이슈 요약"},
                {"type": "callout", "emoji": "💡", "text": "이 글의 핵심 메시지 3가지"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🌍 배경 및 맥락"},
                {"type": "paragraph", "text": "왜 이 글이 쓰여졌는가? 어떤 상황/트렌드와 연관되는가?"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "📝 주요 내용 요약"},
                {"type": "callout", "emoji": "📖", "text": "Progressive Summarization: 중요한 부분을 계층적으로 정리"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "[섹션 1 제목]"},
                {"type": "paragraph", "text": ""},
                {"type": "bulleted_list_item", "text": "핵심 포인트 1"},
                {"type": "bulleted_list_item", "text": "핵심 포인트 2"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "[섹션 2 제목]"},
                {"type": "paragraph", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "💡 시사점 및 인사이트"},
                {"type": "heading_3", "text": "내게 주는 교훈"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "업무 적용 가능성"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "의문점 & 추가 탐구"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🔗 관련 자료"},
                {"type": "bulleted_list_item", "text": "관련 아티클: "},
                {"type": "bulleted_list_item", "text": "관련 프로젝트: "},
                {"type": "bulleted_list_item", "text": "관련 기술/개념: "},
            ]
        },

        {
            "name": "📕 [템플릿] Book",
            "content_type": "Book",
            "status": None,
            "priority": "Low",
            "company": None,
            "category": ["Life"],
            "tags": [],
            "blocks": [
                {"type": "callout", "emoji": "📝", "text": "복제 후: 제목(책 제목), Category 조정, Tags 추가"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "📌 핵심 메시지"},
                {"type": "callout", "emoji": "💡", "text": "이 책이 전하는 핵심 메시지 Top 3"},
                {"type": "numbered_list_item", "text": ""},
                {"type": "numbered_list_item", "text": ""},
                {"type": "numbered_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "📖 챕터별 요약"},
                {"type": "callout", "emoji": "📚", "text": "Progressive Summarization: 중요 챕터만 선택적으로"},
                {"type": "paragraph", "text": ""},

                {"type": "heading_3", "text": "Chapter X: [제목]"},
                {"type": "paragraph", "text": "**핵심 개념**:"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},
                {"type": "paragraph", "text": "**인상깊은 문구**:"},
                {"type": "quote", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "💡 Action Items"},
                {"type": "paragraph", "text": "이 책을 읽고 실천할 것들:"},
                {"type": "numbered_list_item", "text": "즉시 적용: "},
                {"type": "numbered_list_item", "text": "단기 (1개월): "},
                {"type": "numbered_list_item", "text": "장기 (3-6개월): "},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🎯 업무/삶에 적용"},
                {"type": "heading_3", "text": "업무"},
                {"type": "bulleted_list_item", "text": ""},

                {"type": "heading_3", "text": "개인 성장"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🤔 생각할 거리"},
                {"type": "paragraph", "text": "이 책이 제기하는 질문들:"},
                {"type": "bulleted_list_item", "text": ""},
                {"type": "paragraph", "text": ""},

                {"type": "heading_2", "text": "🔗 관련 자료"},
                {"type": "bulleted_list_item", "text": "비슷한 주제의 책: "},
                {"type": "bulleted_list_item", "text": "관련 아티클: "},
                {"type": "bulleted_list_item", "text": "실천 프로젝트: "},
            ]
        }
    ]


def convert_block_to_notion(block):
    """Convert simple block definition to Notion block format"""
    block_type = block["type"]

    if block_type == "heading_1":
        return {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": block["text"]}}]
            }
        }
    elif block_type == "heading_2":
        return {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": block["text"]}}]
            }
        }
    elif block_type == "heading_3":
        return {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": block["text"]}}]
            }
        }
    elif block_type == "paragraph":
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": block["text"]}}] if block["text"] else []
            }
        }
    elif block_type == "bulleted_list_item":
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": block["text"]}}]
            }
        }
    elif block_type == "numbered_list_item":
        return {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": block["text"]}}]
            }
        }
    elif block_type == "code":
        return {
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"type": "text", "text": {"content": block["text"]}}],
                "language": block.get("language", "plain text")
            }
        }
    elif block_type == "callout":
        return {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": block["text"]}}],
                "icon": {"type": "emoji", "emoji": block.get("emoji", "💡")}
            }
        }
    elif block_type == "quote":
        return {
            "object": "block",
            "type": "quote",
            "quote": {
                "rich_text": [{"type": "text", "text": {"content": block["text"]}}]
            }
        }

    return None


def create_page_payload(db_id, template):
    """Create Notion API payload for page creation - minimal properties for templates"""
    # Build minimal properties for templates
    properties = {
        "이름": {
            "title": [
                {
                    "text": {
                        "content": template["name"]
                    }
                }
            ]
        },
        "Content_Type": {
            "select": {
                "name": template["content_type"]
            }
        },
        "Mig_Status": {
            "select": {
                "name": "SKIP"  # Templates should not be migrated
            }
        }
    }

    # Only add category and company if they have values
    if template.get("category"):
        properties["Category"] = {
            "multi_select": [{"name": cat} for cat in template["category"]]
        }

    if template.get("company"):
        properties["Company"] = {"select": {"name": template["company"]}}

    # Convert blocks
    children = []
    for block in template["blocks"]:
        notion_block = convert_block_to_notion(block)
        if notion_block:
            children.append(notion_block)

    # Notion limits to 100 blocks per request
    if len(children) > 100:
        children = children[:100]

    payload = {
        "parent": {"database_id": db_id},
        "properties": properties,
        "children": children
    }

    return payload


def create_template_page(api_token, db_id, template):
    """Create a template page in Notion database"""
    url = 'https://api.notion.com/v1/pages'
    headers = get_headers(api_token)

    payload = create_page_payload(db_id, template)

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.text


def main():
    config = load_config()
    api_token = config["notion"]["api_token"]
    db_id = config["notion"]["record_master_db_id"]

    print("📋 Creating UPGRADED Notion templates based on your actual patterns...")
    print("="*80)
    print()

    templates = get_templates()

    for template in templates:
        print(f"Creating: {template['name']}... ", end="", flush=True)

        success, result = create_template_page(api_token, db_id, template)

        if success:
            print("✅ Success")
        else:
            print(f"❌ Failed")
            print(f"   Error: {result}")

    print()
    print("="*80)
    print("✅ All upgraded templates created!")
    print()
    print("📝 What's different:")
    print("   - Project: SMART goals + STAR framework + KPT retrospective")
    print("   - Experience: Your actual Obsidian structure (주간 요약, 메트릭, etc.) + ORID")
    print("   - Reference: Feynman + First Principles + practical examples")
    print("   - Insight: First Principles + Mental Models + action items")
    print("   - Article: Your '컨텐츠 리스트' structure + Progressive Summarization")
    print("   - Book: Action-oriented + Progressive Summarization")
    print()


if __name__ == '__main__':
    main()
