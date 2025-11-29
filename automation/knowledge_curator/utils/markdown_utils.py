"""
Markdown 파일 처리 유틸리티
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml


class MarkdownNote:
    """Markdown 노트 객체"""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.frontmatter: Dict = {}
        self.content: str = ""
        self.raw_content: str = ""
        self._load()

    def _load(self):
        """파일 로드 및 파싱"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.raw_content = f.read()

        self.frontmatter, self.content = parse_frontmatter(self.raw_content)

    def save(self):
        """변경사항 저장"""
        new_content = serialize_frontmatter(self.frontmatter, self.content)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    def update_frontmatter(self, **kwargs):
        """Frontmatter 업데이트"""
        self.frontmatter.update(kwargs)

    def get_links(self) -> List[str]:
        """내부 링크 추출"""
        return extract_internal_links(self.content)

    def get_headings(self) -> List[Dict[str, any]]:
        """헤딩 추출"""
        return extract_headings(self.content)

    def get_code_blocks(self) -> List[str]:
        """코드 블록 추출"""
        return extract_code_blocks(self.content)

    def word_count(self) -> int:
        """단어 수 (공백 기준)"""
        return len(self.content.split())

    def char_count(self) -> int:
        """문자 수"""
        return len(self.content)


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """
    Frontmatter와 본문 분리

    Returns:
        (frontmatter_dict, content_without_frontmatter)
    """
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
            content_body = match.group(2)
            return frontmatter, content_body
        except yaml.YAMLError:
            # YAML 파싱 실패 시 빈 frontmatter
            return {}, content

    return {}, content


def serialize_frontmatter(frontmatter: Dict, content: str) -> str:
    """
    Frontmatter와 본문 결합
    """
    if not frontmatter:
        return content

    yaml_str = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
    return f"---\n{yaml_str}---\n{content}"


def extract_internal_links(content: str) -> List[str]:
    """
    내부 링크 추출 [[link]] 형식

    Returns:
        ['note1.md', 'note2.md', ...]
    """
    # [[link]] or [[link|alias]]
    pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    matches = re.findall(pattern, content)

    # 중복 제거
    return list(set(matches))


def extract_headings(content: str) -> List[Dict[str, any]]:
    """
    헤딩 추출

    Returns:
        [{'level': 1, 'text': 'Title'}, ...]
    """
    headings = []
    for line in content.split('\n'):
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append({'level': level, 'text': text})

    return headings


def extract_code_blocks(content: str) -> List[str]:
    """
    코드 블록 추출

    Returns:
        ['code1', 'code2', ...]
    """
    # ```language\ncode\n```
    pattern = r'```[a-z]*\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    return matches


def extract_tags(content: str, frontmatter: Dict) -> List[str]:
    """
    태그 추출 (frontmatter + inline)

    Returns:
        ['tag1', 'tag2', ...]
    """
    tags = set()

    # Frontmatter tags
    fm_tags = frontmatter.get('tags', [])
    if isinstance(fm_tags, list):
        tags.update(fm_tags)
    elif isinstance(fm_tags, str):
        tags.add(fm_tags)

    # Inline tags #tag
    inline_tags = re.findall(r'#([a-zA-Z0-9가-힣_-]+)', content)
    tags.update(inline_tags)

    return list(tags)


def extract_keywords(content: str, top_n: int = 10) -> List[str]:
    """
    키워드 추출 (간단한 빈도 기반)

    Returns:
        ['keyword1', 'keyword2', ...]
    """
    from collections import Counter

    # 불용어 (간단한 버전)
    stopwords = {
        '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로',
        '자', '에', '와', '한', '하다', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at'
    }

    # 단어 추출 (한글, 영문, 숫자만)
    words = re.findall(r'[가-힣a-zA-Z0-9]+', content.lower())

    # 2글자 이상, 불용어 제거
    words = [w for w in words if len(w) >= 2 and w not in stopwords]

    # 빈도 계산
    counter = Counter(words)
    return [word for word, count in counter.most_common(top_n)]


def has_todo_items(content: str) -> bool:
    """TODO 항목 존재 여부"""
    patterns = [
        r'- \[ \]',  # - [ ] todo
        r'- \[x\]',  # - [x] done
        r'TODO:',
        r'FIXME:',
    ]

    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True

    return False


def count_list_items(content: str) -> int:
    """리스트 항목 개수"""
    pattern = r'^\s*[-*+]\s+'
    return len(re.findall(pattern, content, re.MULTILINE))


def count_tables(content: str) -> int:
    """테이블 개수"""
    # Markdown 테이블 감지 (| --- | 형식)
    pattern = r'\|[\s\-:|]+\|'
    return len(re.findall(pattern, content))


def get_note_relative_path(vault_root: Path, note_path: Path) -> str:
    """
    Vault root 기준 상대 경로

    Returns:
        '01-Projects/Note.md'
    """
    try:
        return str(note_path.relative_to(vault_root))
    except ValueError:
        return str(note_path)
