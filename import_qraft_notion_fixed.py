#!/usr/bin/env python3
"""
Import Qraft experience from Notion with proper child block handling
"""

import requests
import json
from pathlib import Path
from datetime import datetime
import sys

def load_config():
    """Load config.json"""
    config_path = Path(__file__).parent / 'config.json'
    with open(config_path, 'r') as f:
        return json.load(f)

def get_headers(config):
    """Get Notion API headers"""
    return {
        'Authorization': f'Bearer {config["notion"]["token"]}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

def query_database(database_id, config):
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
            sys.exit(1)

        data = response.json()
        all_results.extend(data.get('results', []))

        has_more = data.get('has_more', False)
        start_cursor = data.get('next_cursor')

    return all_results

def get_block_children(block_id, config):
    """Get children of a block recursively"""
    url = f'https://api.notion.com/v1/blocks/{block_id}/children'
    headers = get_headers(config)

    all_children = []
    has_more = True
    start_cursor = None

    while has_more:
        params = {}
        if start_cursor:
            params['start_cursor'] = start_cursor

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            return []

        data = response.json()
        children = data.get('results', [])

        # Recursively get children of children
        for child in children:
            if child.get('has_children'):
                child['children'] = get_block_children(child['id'], config)

        all_children.extend(children)

        has_more = data.get('has_more', False)
        start_cursor = data.get('next_cursor')

    return all_children

def get_page_content(page_id, config):
    """Get page content blocks with children"""
    return get_block_children(page_id, config)

def extract_rich_text(rich_text_array):
    """Extract plain text"""
    if not rich_text_array:
        return ''
    return ''.join([rt.get('plain_text', '') for rt in rich_text_array])

def block_to_markdown(block, indent=0):
    """Convert block to markdown with proper indentation"""
    block_type = block.get('type')
    indent_str = '  ' * indent

    result = ''

    if block_type == 'paragraph':
        text = extract_rich_text(block['paragraph'].get('rich_text', []))
        result = text + '\n\n' if text else ''

    elif block_type == 'heading_1':
        text = extract_rich_text(block['heading_1'].get('rich_text', []))
        result = f"# {text}\n\n"

    elif block_type == 'heading_2':
        text = extract_rich_text(block['heading_2'].get('rich_text', []))
        result = f"## {text}\n\n"

    elif block_type == 'heading_3':
        text = extract_rich_text(block['heading_3'].get('rich_text', []))
        result = f"### {text}\n\n"

    elif block_type == 'bulleted_list_item':
        text = extract_rich_text(block['bulleted_list_item'].get('rich_text', []))
        result = f"{indent_str}- {text}\n"

        # Process children
        if 'children' in block and block['children']:
            for child in block['children']:
                result += block_to_markdown(child, indent + 1)

    elif block_type == 'numbered_list_item':
        text = extract_rich_text(block['numbered_list_item'].get('rich_text', []))
        result = f"{indent_str}1. {text}\n"

        # Process children
        if 'children' in block and block['children']:
            for child in block['children']:
                result += block_to_markdown(child, indent + 1)

    elif block_type == 'to_do':
        text = extract_rich_text(block['to_do'].get('rich_text', []))
        checked = '[x]' if block['to_do'].get('checked', False) else '[ ]'
        result = f"{indent_str}- {checked} {text}\n"

        # Process children (indented content under checkbox)
        if 'children' in block and block['children']:
            for child in block['children']:
                result += block_to_markdown(child, indent + 1)

    elif block_type == 'code':
        text = extract_rich_text(block['code'].get('rich_text', []))
        lang = block['code'].get('language', '')
        result = f"```{lang}\n{text}\n```\n\n"

    elif block_type == 'quote':
        text = extract_rich_text(block['quote'].get('rich_text', []))
        result = f"> {text}\n\n"

    elif block_type == 'callout':
        text = extract_rich_text(block['callout'].get('rich_text', []))
        icon = block['callout'].get('icon', {})
        emoji = icon.get('emoji', '💡') if icon.get('type') == 'emoji' else '💡'
        result = f"{emoji} **{text}**\n\n"

        # Process children
        if 'children' in block and block['children']:
            for child in block['children']:
                result += block_to_markdown(child, indent)

    elif block_type == 'toggle':
        text = extract_rich_text(block['toggle'].get('rich_text', []))
        result = f"<details>\n<summary>{text}</summary>\n\n"

        # Process children
        if 'children' in block and block['children']:
            for child in block['children']:
                result += block_to_markdown(child, indent)

        result += "</details>\n\n"

    elif block_type == 'divider':
        result = "---\n\n"

    elif block_type == 'table_of_contents':
        result = "_Table of Contents_\n\n"

    else:
        # Unknown block type - try to extract any text
        pass

    return result

def extract_property(prop):
    """Extract property value"""
    prop_type = prop.get('type')

    if prop_type == 'title':
        return extract_rich_text(prop.get('title', []))
    elif prop_type == 'rich_text':
        return extract_rich_text(prop.get('rich_text', []))
    elif prop_type == 'select':
        select = prop.get('select')
        return select.get('name') if select else None
    elif prop_type == 'date':
        date = prop.get('date')
        return date.get('start') if date else None
    elif prop_type == 'checkbox':
        return prop.get('checkbox')
    elif prop_type == 'number':
        return prop.get('number')
    else:
        return None

def categorize(title):
    """Categorize based on title"""
    title_lower = title.lower()

    if any(kw in title_lower for kw in ['%', '달성', '개선', '향상', '절감', '증가', '성과']):
        return 'Achievements'
    elif any(kw in title_lower for kw in ['학습', '공부', 'learning']):
        return 'Learning'
    else:
        return 'Projects'

def save_page(page, output_dir, config):
    """Save page as markdown"""
    properties = page.get('properties', {})

    # Find title
    title = 'Untitled'
    for prop in properties.values():
        if prop.get('type') == 'title':
            title = extract_property(prop) or 'Untitled'
            break

    # Categorize
    category = categorize(title)
    category_dir = output_dir / category
    category_dir.mkdir(parents=True, exist_ok=True)

    # Get content with children
    page_id = page['id']
    blocks = get_page_content(page_id, config)
    content_md = ''.join([block_to_markdown(b) for b in blocks])

    # Frontmatter
    frontmatter = f"""---
type: qraft-experience
category: {category.lower()}
title: {title}
imported: {datetime.now().strftime('%Y-%m-%d')}
notion_id: {page_id}
---

"""

    # Save
    safe_name = title.replace('/', '-').replace('\\', '-')[:100]
    output_file = category_dir / f"{safe_name}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter + f"# {title}\n\n" + content_md)

    return output_file, category

def main():
    print("📥 Re-importing Qraft experience with full content...\n")

    # Load config
    config = load_config()
    db_config = config['notion']['databases']['work_list']
    database_id = db_config['id']

    # Output
    output_dir = Path(__file__).parent / 'Experiences' / 'Qraft-Full'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Query
    print(f"🔍 Querying: {db_config['name']}")
    pages = query_database(database_id, config)

    print(f"✅ Found {len(pages)} pages\n")

    # Process
    imported = {'Projects': [], 'Achievements': [], 'Learning': []}

    for i, page in enumerate(pages, 1):
        try:
            output_file, category = save_page(page, output_dir, config)
            imported[category].append(output_file.name)
            print(f"[{i}/{len(pages)}] ✅ {output_file.name[:60]}")
        except Exception as e:
            print(f"[{i}/{len(pages)}] ❌ {e}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 Import Summary")
    print("=" * 60)

    for category, files in imported.items():
        if files:
            print(f"\n{category}/ ({len(files)}개)")
            for f in files[:5]:
                print(f"  - {f}")
            if len(files) > 5:
                print(f"  ... and {len(files)-5} more")

    print(f"\n📁 Location: {output_dir}")
    print("\n✅ Complete! Now compare with old import to verify.")

if __name__ == '__main__':
    main()