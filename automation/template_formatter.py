#!/usr/bin/env python3
"""
Template Formatter Engine for Notion Record Master
자동으로 Notion 레코드를 템플릿에 맞게 포매팅합니다.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import re


class BaseFormatter(ABC):
    """모든 포매터의 기본 클래스"""

    # 각 포매터가 오버라이드해야 할 속성
    CONTENT_TYPE = None
    TEMPLATE_NAME = None
    DEFAULT_TAGS = []

    def __init__(self, notion_record: Dict[str, Any], template_path: Path = None):
        """
        Args:
            notion_record: Notion API에서 받은 레코드 dict
            template_path: 사용자 정의 템플릿 경로 (선택)
        """
        self.notion_record = notion_record
        self.template_path = template_path
        self.template_content = self._load_template()
        self.extracted_fields = {}

    def _load_template(self) -> str:
        """템플릿 파일 로드"""
        if self.template_path and self.template_path.exists():
            return self.template_path.read_text()

        # 기본 템플릿 경로
        default_path = Path(__file__).parent / "99-Assets/Templates" / f"{self.TEMPLATE_NAME}.md"
        if default_path.exists():
            return default_path.read_text()

        # 템플릿을 찾을 수 없으면 빈 문자열 반환
        return ""

    def extract_title(self) -> str:
        """제목 추출"""
        try:
            title_prop = self.notion_record['properties'].get('이름')
            if title_prop and title_prop['type'] == 'title':
                title_array = title_prop.get('title', [])
                return ''.join([t.get('plain_text', '') for t in title_array])
        except (KeyError, TypeError):
            pass
        return "Untitled"

    def extract_date(self, field_name: str = 'Period') -> Optional[str]:
        """날짜 추출 (YYYY-MM-DD 형식)"""
        try:
            date_prop = self.notion_record['properties'].get(field_name)
            if date_prop and date_prop['type'] == 'date':
                date_obj = date_prop.get('date')
                if date_obj and date_obj.get('start'):
                    return date_obj['start']
        except (KeyError, TypeError):
            pass
        return None

    def extract_created_date(self) -> str:
        """생성 날짜 추출"""
        try:
            created_prop = self.notion_record['properties'].get('Created')
            if created_prop and created_prop['type'] == 'created_time':
                timestamp = created_prop.get('created_time')
                if timestamp:
                    # ISO 형식을 YYYY-MM-DD로 변환
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    return dt.strftime('%Y-%m-%d')
        except (KeyError, TypeError, ValueError):
            pass
        return datetime.now().strftime('%Y-%m-%d')

    def extract_updated_date(self) -> str:
        """수정 날짜 추출"""
        try:
            updated_prop = self.notion_record['properties'].get('Updated')
            if updated_prop and updated_prop['type'] == 'last_edited_time':
                timestamp = updated_prop.get('last_edited_time')
                if timestamp:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    return dt.strftime('%Y-%m-%d')
        except (KeyError, TypeError, ValueError):
            pass
        return datetime.now().strftime('%Y-%m-%d')

    def extract_categories(self) -> List[str]:
        """카테고리 추출"""
        try:
            category_prop = self.notion_record['properties'].get('Category')
            if category_prop and category_prop['type'] == 'multi_select':
                return [item['name'] for item in category_prop.get('multi_select', [])]
        except (KeyError, TypeError):
            pass
        return []

    def extract_company(self) -> Optional[str]:
        """회사 정보 추출"""
        try:
            company_prop = self.notion_record['properties'].get('Company')
            if company_prop and company_prop['type'] == 'select':
                select_obj = company_prop.get('select')
                if select_obj:
                    return select_obj.get('name')
        except (KeyError, TypeError):
            pass
        return None

    def generate_tags(self) -> List[str]:
        """최종 태그 생성 (Content Type + Categories)"""
        tags = [self.CONTENT_TYPE.lower()] if self.CONTENT_TYPE else []
        tags.extend([cat.lower() for cat in self.extract_categories()])
        tags.extend([tag.lower() for tag in self.DEFAULT_TAGS])
        return list(set(tags))  # 중복 제거

    def generate_frontmatter(self) -> Dict[str, Any]:
        """Frontmatter 딕셔너리 생성"""
        title = self.extract_title()
        return {
            'tags': self.generate_tags(),
            'created': self.extract_date('Period') or self.extract_created_date(),
            'updated': self.extract_updated_date(),
            'title': title,
            'type': self.CONTENT_TYPE.lower() if self.CONTENT_TYPE else 'note'
        }

    def substitute_variables(self, content: str) -> str:
        """템플릿의 {{variable}} 치환"""
        title = self.extract_title()
        date = self.extract_date('Period') or self.extract_created_date()

        substitutions = {
            'title': title,
            'date': date,
            'today': datetime.now().strftime('%Y-%m-%d'),
        }

        # 추가 치환은 서브클래스에서 오버라이드
        substitutions.update(self._get_additional_substitutions())

        # {{variable}} 패턴 치환
        for key, value in substitutions.items():
            pattern = r'\{\{' + key + r'\}\}'
            content = re.sub(pattern, str(value) if value else '', content, flags=re.IGNORECASE)

        return content

    def _get_additional_substitutions(self) -> Dict[str, Any]:
        """서브클래스에서 추가 치환 정의"""
        return {}

    def render_frontmatter(self) -> str:
        """Frontmatter를 YAML 형식으로 렌더링"""
        fm = self.generate_frontmatter()
        lines = ['---']

        for key, value in fm.items():
            if isinstance(value, list):
                lines.append(f'{key}:')
                for item in value:
                    lines.append(f'  - {item}')
            else:
                lines.append(f'{key}: {value}')

        lines.append('---')
        return '\n'.join(lines)

    def render_body(self) -> str:
        """본문을 렌더링 (변수 치환 포함)"""
        return self.substitute_variables(self.template_content)

    def format(self) -> str:
        """최종 포매팅: frontmatter + body"""
        frontmatter = self.render_frontmatter()
        body = self.render_body()
        return f"{frontmatter}\n\n{body}"


# ============================================================================
# Content Type별 포매터
# ============================================================================

class ArticleFormatter(BaseFormatter):
    """Article 포매터"""
    CONTENT_TYPE = 'Article'
    TEMPLATE_NAME = 'Article'
    DEFAULT_TAGS = ['article', 'reading']


class BookFormatter(BaseFormatter):
    """Book 포매터"""
    CONTENT_TYPE = 'Book'
    TEMPLATE_NAME = 'Book'
    DEFAULT_TAGS = ['book', 'reading']


class ExperienceFormatter(BaseFormatter):
    """Experience 포매터"""
    CONTENT_TYPE = 'Experience'
    TEMPLATE_NAME = 'Exprience'  # 주의: 원본 파일명이 오타로 되어있음
    DEFAULT_TAGS = ['experience', 'reflection']

    def generate_frontmatter(self) -> Dict[str, Any]:
        """Experience용 확장 frontmatter"""
        fm = super().generate_frontmatter()
        company = self.extract_company()
        if company:
            fm['company'] = company
        return fm

    def _get_additional_substitutions(self) -> Dict[str, Any]:
        """Experience 추가 변수"""
        company = self.extract_company()
        return {
            'company': company or 'N/A'
        }


class InsightFormatter(BaseFormatter):
    """Insight 포매터"""
    CONTENT_TYPE = 'Insight'
    TEMPLATE_NAME = 'Insigth'  # 주의: 원본 파일명이 오타로 되어있음
    DEFAULT_TAGS = ['insight', 'life-learning']


class ReferenceFormatter(BaseFormatter):
    """Reference 포매터"""
    CONTENT_TYPE = 'Reference'
    TEMPLATE_NAME = 'Reference'
    DEFAULT_TAGS = ['reference', 'knowledge']


class ProjectFormatter(BaseFormatter):
    """Project 포매터"""
    CONTENT_TYPE = 'Project'
    TEMPLATE_NAME = 'hub-note'
    DEFAULT_TAGS = ['project', 'work']


# ============================================================================
# 포매터 레지스트리
# ============================================================================

FORMATTER_REGISTRY = {
    'Article': ArticleFormatter,
    'Book': BookFormatter,
    'Experience': ExperienceFormatter,
    'Insight': InsightFormatter,
    'Reference': ReferenceFormatter,
    'Project': ProjectFormatter,
}


# ============================================================================
# 메인 함수
# ============================================================================

def get_formatter(content_type: str, notion_record: Dict[str, Any],
                  template_path: Optional[Path] = None) -> Optional[BaseFormatter]:
    """
    Content Type에 맞는 포매터 인스턴스 생성
    """
    formatter_class = FORMATTER_REGISTRY.get(content_type)
    if not formatter_class:
        print(f"❌ Unknown content type: {content_type}")
        return None

    return formatter_class(notion_record, template_path)


def format_record(notion_record: Dict[str, Any], template_path: Optional[Path] = None) -> Optional[str]:
    """
    Notion 레코드를 Obsidian 마크다운으로 변환
    """
    try:
        # Content Type 추출
        content_type_prop = notion_record['properties'].get('Content_Type')
        if not content_type_prop or content_type_prop['type'] != 'select':
            print("❌ No Content_Type found in record")
            return None

        content_type = content_type_prop['select']['name']

        # 적절한 포매터 생성
        formatter = get_formatter(content_type, notion_record, template_path)
        if not formatter:
            return None

        # 포매팅 실행
        return formatter.format()

    except (KeyError, TypeError) as e:
        print(f"❌ Error formatting record: {e}")
        return None


def format_records_batch(notion_records: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    여러 레코드를 한 번에 포매팅
    """
    results = {}
    for i, record in enumerate(notion_records):
        try:
            title = record['properties'].get('이름', {}).get('title', [{}])[0].get('plain_text', 'Untitled')
            formatted = format_record(record)
            if formatted:
                results[title] = formatted
            else:
                results[title] = None
        except (KeyError, IndexError, TypeError):
            results[f"Record_{i}"] = None

    return results


# ============================================================================
# 유틸리티
# ============================================================================

def validate_notion_record(notion_record: Dict[str, Any]) -> bool:
    """Notion 레코드 유효성 검사"""
    required_keys = ['properties', 'id']
    return all(key in notion_record for key in required_keys)


def print_formatter_info():
    """등록된 포매터 정보 출력"""
    print("📋 등록된 포매터:")
    for content_type, formatter_class in FORMATTER_REGISTRY.items():
        print(f"  - {content_type}: {formatter_class.__name__}")


if __name__ == '__main__':
    print_formatter_info()
