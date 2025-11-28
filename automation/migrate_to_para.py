#!/usr/bin/env python3
"""
Migrate Notion content to PARA structure
Excludes: Outstanding, Medium (bookmarks)
"""

import requests
import json
from pathlib import Path
from datetime import datetime
import sys
import os
import re

# Load existing notion_sync functions
sys.path.insert(0, str(Path(__file__).parent))
from notion_sync import (
    load_config, get_headers, get_page_content,
    block_to_markdown, extract_property
)

def should_skip(title):
    """Check if page should be skipped"""
    skip_keywords = ['outstanding', 'medium', '아웃스탠딩', '미디엄']
    return any(kw in title.lower() for kw in skip_keywords)

def categorize_for_para(title, properties):
    """Categorize content for PARA structure"""
    title_lower = title.lower()

    # Check if it's a retrospective/memoir
    if any(kw in title_lower for kw in ['회고', 'retrospective', 'memoir', 'weekly']):
        return 'weekly', None

    # Check for achievements
    if any(kw in title_lower for kw in ['%', '달성', '개선', '향상', '절감', '증가', '성과', 'achievement']):
        return 'achievements', None

    # Check for learning resources
    if any(kw in title_lower for kw in ['학습', '공부', 'learning', 'study', 'tutorial']):
        return 'resources', None

    # Default to projects
    return 'projects', None

def query_all_pages(database_id, config):
    """Query all pages from database"""
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    headers = get_headers(config)

    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        payload = {}
        if start_cursor:
            payload['start_cursor'] = start_cursor

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            return []

        data = response.json()
        all_results.extend(data.get('results', []))

        has_more = data.get('has_more', False)
        start_cursor = data.get('next_cursor')

    return all_results

def sanitize_filename(title):
    """Create safe filename from title"""
    # Remove special characters
    safe = re.sub(r'[<>:"/\\|?*]', '', title)
    safe = safe.strip().replace(' ', '-')
    return safe[:100]  # Limit length

def save_to_para(page, vault_root, config, db_name):
    """Save page to appropriate PARA location"""
    properties = page.get('properties', {})

    # Extract title
    title = 'Untitled'
    for prop in properties.values():
        if prop.get('type') == 'title':
            title = extract_property(prop) or 'Untitled'
            break

    # Skip if contains excluded keywords
    if should_skip(title):
        print(f"⏭️  Skipping: {title}")
        return None

    # Categorize
    category, subcategory = categorize_for_para(title, properties)

    # Determine target directory
    if category == 'weekly':
        target_dir = vault_root / '02-Areas' / '크래프트테크놀로지스' / 'Weekly'
    elif category == 'achievements':
        target_dir = vault_root / '02-Areas' / '크래프트테크놀로지스' / 'Achievements'
    elif category == 'resources':
        target_dir = vault_root / '03-Resources' / 'Qraft'
    else:  # projects
        target_dir = vault_root / '01-Projects' / 'Qraft'

    target_dir.mkdir(parents=True, exist_ok=True)

    # Get content
    page_id = page['id']
    blocks = get_page_content(page_id, config)
    content_md = ''.join([block_to_markdown(b) for b in blocks])

    # Extract tags
    tags = ['qraft', '크래프트']
    for prop_name, prop in properties.items():
        if prop.get('type') == 'multi_select':
            tags.extend(extract_property(prop) or [])

    # Create frontmatter
    frontmatter_lines = [
        '---',
        f'type: {category}',
        f'title: {title}',
        f'source: notion',
        f'notion_id: {page_id}',
        f'imported: {datetime.now().strftime("%Y-%m-%d")}',
        f'database: {db_name}',
        f'tags: [{", ".join(tags)}]',
        '---',
        ''
    ]

    # Combine
    full_content = '\n'.join(frontmatter_lines) + '\n' + content_md

    # Save
    filename = sanitize_filename(title) + '.md'
    filepath = target_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"✅ Saved: {category}/{filename}")
    return filepath

def main():
    print("🔄 Migrating Notion to PARA structure...")
    print("⏭️  Excluding: Outstanding, Medium")

    config = load_config()
    vault_root = Path(__file__).parent.parent

    databases = config['notion']['databases']

    total_migrated = 0
    total_skipped = 0

    for db_key, db_info in databases.items():
        db_name = db_info['name']
        db_id = db_info['id']

        print(f"\n📂 Processing: {db_name}")

        pages = query_all_pages(db_id, config)
        print(f"   Found {len(pages)} pages")

        for page in pages:
            result = save_to_para(page, vault_root, config, db_name)
            if result:
                total_migrated += 1
            else:
                total_skipped += 1

    print(f"\n🎉 Migration complete!")
    print(f"   ✅ Migrated: {total_migrated}")
    print(f"   ⏭️  Skipped: {total_skipped}")

if __name__ == '__main__':
    main()
