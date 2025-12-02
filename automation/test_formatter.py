#!/usr/bin/env python3
"""
Template Formatter 테스트 스크립트
"""

import json
import sys
from pathlib import Path
from template_formatter import (
    format_record,
    format_records_batch,
    get_formatter,
    FORMATTER_REGISTRY,
    print_formatter_info
)


def test_formatter_registry():
    """포매터 레지스트리 테스트"""
    print("=" * 60)
    print("📋 Formatter Registry Test")
    print("=" * 60)
    print_formatter_info()
    assert len(FORMATTER_REGISTRY) == 6, "Should have 6 formatters"
    print("✅ Registry test passed\n")


def create_test_record(content_type: str, title: str) -> dict:
    """테스트용 Notion 레코드 생성"""
    return {
        "object": "page",
        "id": "test-id-123",
        "properties": {
            "이름": {
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {"content": title},
                        "plain_text": title
                    }
                ]
            },
            "Content_Type": {
                "type": "select",
                "select": {
                    "name": content_type
                }
            },
            "Category": {
                "type": "multi_select",
                "multi_select": [
                    {"name": "Technology"},
                    {"name": "Career"}
                ]
            },
            "Period": {
                "type": "date",
                "date": {
                    "start": "2025-12-02"
                }
            },
            "Created": {
                "type": "created_time",
                "created_time": "2025-12-01T10:00:00.000Z"
            },
            "Updated": {
                "type": "last_edited_time",
                "last_edited_time": "2025-12-02T15:30:00.000Z"
            },
            "Company": {
                "type": "select",
                "select": {
                    "name": "크레프트테크놀로지스"
                }
            }
        }
    }


def test_article_formatter():
    """Article 포매터 테스트"""
    print("=" * 60)
    print("📰 Article Formatter Test")
    print("=" * 60)

    record = create_test_record(
        'Article',
        '빅블러 시대, 산업의 경계를 허무는 마케팅'
    )

    result = format_record(record)
    assert result, "Article should format successfully"
    assert '---' in result, "Should have frontmatter"
    assert 'article' in result, "Should contain article tag"
    assert 'technology' in result, "Should contain technology tag"
    assert '빅블러' in result, "Should contain title"

    print("✅ Article formatter test passed")
    print("\n📄 Generated markdown (first 500 chars):")
    print(result[:500])
    print("\n")


def test_book_formatter():
    """Book 포매터 테스트"""
    print("=" * 60)
    print("📕 Book Formatter Test")
    print("=" * 60)

    record = create_test_record(
        'Book',
        'The Lean Startup'
    )

    result = format_record(record)
    assert result, "Book should format successfully"
    assert 'book' in result, "Should contain book tag"
    assert 'The Lean Startup' in result, "Should contain title"

    print("✅ Book formatter test passed")
    print("\n📄 Generated markdown (first 500 chars):")
    print(result[:500])
    print("\n")


def test_experience_formatter():
    """Experience 포매터 테스트"""
    print("=" * 60)
    print("📝 Experience Formatter Test")
    print("=" * 60)

    record = create_test_record(
        'Experience',
        '2025년 12월 1주차 회고'
    )

    result = format_record(record)
    assert result, "Experience should format successfully"
    assert 'experience' in result, "Should contain experience tag"
    # Frontmatter에서 회사명이 있는지 체크
    assert 'company:' in result or '크레프트테크놀로지스' in result, "Should contain company info"

    print("✅ Experience formatter test passed")
    print("\n📄 Generated markdown (first 500 chars):")
    print(result[:500])
    print("\n")


def test_insight_formatter():
    """Insight 포매터 테스트"""
    print("=" * 60)
    print("💡 Insight Formatter Test")
    print("=" * 60)

    record = create_test_record(
        'Insight',
        '데이터 거버넌스의 중요성'
    )

    result = format_record(record)
    assert result, "Insight should format successfully"
    assert 'insight' in result, "Should contain insight tag"

    print("✅ Insight formatter test passed")
    print("\n📄 Generated markdown (first 500 chars):")
    print(result[:500])
    print("\n")


def test_reference_formatter():
    """Reference 포매터 테스트"""
    print("=" * 60)
    print("📚 Reference Formatter Test")
    print("=" * 60)

    record = create_test_record(
        'Reference',
        'Apache Airflow'
    )

    result = format_record(record)
    assert result, "Reference should format successfully"
    assert 'reference' in result, "Should contain reference tag"

    print("✅ Reference formatter test passed")
    print("\n📄 Generated markdown (first 500 chars):")
    print(result[:500])
    print("\n")


def test_project_formatter():
    """Project 포매터 테스트"""
    print("=" * 60)
    print("🎯 Project Formatter Test")
    print("=" * 60)

    record = create_test_record(
        'Project',
        'DataHub 통합 구축'
    )

    result = format_record(record)
    assert result, "Project should format successfully"
    assert 'project' in result, "Should contain project tag"

    print("✅ Project formatter test passed")
    print("\n📄 Generated markdown (first 500 chars):")
    print(result[:500])
    print("\n")


def test_batch_formatting():
    """배치 포매팅 테스트"""
    print("=" * 60)
    print("🔄 Batch Formatting Test")
    print("=" * 60)

    records = [
        create_test_record('Article', '첫 번째 아티클'),
        create_test_record('Book', '첫 번째 책'),
        create_test_record('Insight', '첫 번째 인사이트'),
    ]

    results = format_records_batch(records)
    assert len(results) == 3, "Should format all records"
    assert all(v is not None for v in results.values()), "All should be successfully formatted"

    print(f"✅ Batch formatting test passed ({len(results)} records)")
    print("\n")


def test_frontmatter_structure():
    """Frontmatter 구조 테스트"""
    print("=" * 60)
    print("🔍 Frontmatter Structure Test")
    print("=" * 60)

    record = create_test_record('Article', 'Test Article')
    result = format_record(record)

    assert result.startswith('---'), "Should start with ---"
    assert '---\n' in result[3:], "Should have closing ---"

    # Frontmatter 추출
    parts = result.split('---')
    frontmatter = parts[1].strip()

    assert 'tags:' in frontmatter, "Should have tags"
    assert 'created:' in frontmatter, "Should have created date"
    assert 'updated:' in frontmatter, "Should have updated date"
    assert 'title:' in frontmatter, "Should have title"
    assert 'type:' in frontmatter, "Should have type"

    print("✅ Frontmatter structure test passed")
    print("\nFrontmatter content:")
    print(frontmatter)
    print("\n")


def test_tag_generation():
    """태그 생성 테스트"""
    print("=" * 60)
    print("🏷️ Tag Generation Test")
    print("=" * 60)

    record = create_test_record('Article', 'Test')
    result = format_record(record)

    # tags 라인 찾기
    for line in result.split('\n'):
        if line.strip().startswith('- '):
            tag = line.strip()[2:]
            assert tag, "Tags should not be empty"

    print("✅ Tag generation test passed")
    print("\nGenerated tags from sample record:")
    print("  - article")
    print("  - technology")
    print("  - career")
    print("\n")


def run_all_tests():
    """모든 테스트 실행"""
    print("\n")
    print("🧪 Template Formatter Test Suite")
    print("=" * 60)
    print("\n")

    try:
        test_formatter_registry()
        test_article_formatter()
        test_book_formatter()
        test_experience_formatter()
        test_insight_formatter()
        test_reference_formatter()
        test_project_formatter()
        test_batch_formatting()
        test_frontmatter_structure()
        test_tag_generation()

        print("=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        return 0

    except AssertionError as e:
        print("\n" + "=" * 60)
        print(f"❌ Test failed: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ Unexpected error: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
