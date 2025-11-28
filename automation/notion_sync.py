#!/usr/bin/env python3
"""
Notion to Obsidian Sync with Migration Status Tracking
Automatically syncs Notion pages with mig_status='NEEDED' to Obsidian vault
"""

import requests
import json
from pathlib import Path
from datetime import datetime
import sys
import os

def load_config():
    """Load config.json with environment variable fallback"""
    config_path = Path(__file__).parent.parent / 'config.json'

    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Fallback to environment variables (for GitHub Actions)
        raise FileNotFoundError("config.json not found. Please create it from config.template.json")

def get_headers(config):
    """Get Notion API headers"""
    return {
        'Authorization': f'Bearer {config["notion"]["token"]}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

def query_database_with_filter(database_id, config, force_sync=False):
    """Query database with mig_status filter"""
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    headers = get_headers(config)

    # Build filter for mig_status = "NEEDED" unless force sync
    payload = {}
    if not force_sync:
        payload['filter'] = {
            'property': 'mig_status',
            'select': {
                'equals': 'NEEDED'
            }
        }

    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
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

def update_migration_status(page_id, config, status='Done'):
    """Update page's mig_status to Done"""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    headers = get_headers(config)

    payload = {
        'properties': {
            'mig_status': {
                'select': {
                    'name': status
                }
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"⚠️ Failed to update status: {response.status_code}")
        return False

    return True

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
        if text:
            result = f"{indent_str}{text}\n\n" if indent > 0 else text + '\n\n'

    elif block_type in ['heading_1', 'heading_2', 'heading_3']:
        level = block_type[-1]
        text = extract_rich_text(block[block_type].get('rich_text', []))
        if indent > 0:
            result = f"{indent_str}**{text}**\n\n"
        else:
            result = f"{'#' * int(level)} {text}\n\n"

    elif block_type == 'bulleted_list_item':
        text = extract_rich_text(block['bulleted_list_item'].get('rich_text', []))
        result = f"{indent_str}- {text}\n"
        if 'children' in block and block['children']:
            for child in block['children']:
                result += block_to_markdown(child, indent + 1)

    elif block_type == 'numbered_list_item':
        text = extract_rich_text(block['numbered_list_item'].get('rich_text', []))
        result = f"{indent_str}1. {text}\n"
        if 'children' in block and block['children']:
            for child in block['children']:
                result += block_to_markdown(child, indent + 1)

    elif block_type == 'to_do':
        text = extract_rich_text(block['to_do'].get('rich_text', []))
        checked = '[x]' if block['to_do'].get('checked', False) else '[ ]'
        result = f"{indent_str}- {checked} {text}\n"
        if 'children' in block and block['children']:
            for child in block['children']:
                result += block_to_markdown(child, indent + 1)

    elif block_type == 'code':
        text = extract_rich_text(block['code'].get('rich_text', []))
        lang = block['code'].get('language', '')
        if indent > 0:
            lines = text.split('\n')
            indented_code = '\n'.join([indent_str + line for line in lines])
            result = f"{indent_str}```{lang}\n{indented_code}\n{indent_str}```\n\n"
        else:
            result = f"```{lang}\n{text}\n```\n\n"

    elif block_type == 'quote':
        text = extract_rich_text(block['quote'].get('rich_text', []))
        result = f"{indent_str}> {text}\n\n"

    elif block_type == 'callout':
        text = extract_rich_text(block['callout'].get('rich_text', []))
        icon = block['callout'].get('icon', {})
        emoji = icon.get('emoji', '💡') if icon.get('type') == 'emoji' else '💡'
        result = f"{emoji} **{text}**\n\n"
        if 'children' in block and block['children']:
            for child in block['children']:
                result += block_to_markdown(child, indent)

    elif block_type == 'toggle':
        text = extract_rich_text(block['toggle'].get('rich_text', []))
        result = f"<details>\n<summary>{text}</summary>\n\n"
        if 'children' in block and block['children']:
            for child in block['children']:
                result += block_to_markdown(child, indent)
        result += "</details>\n\n"

    elif block_type == 'divider':
        result = "---\n\n"

    elif block_type == 'image':
        image_data = block.get('image', {})
        caption = extract_rich_text(image_data.get('caption', []))
        url = ''
        if image_data.get('type') == 'file':
            url = image_data.get('file', {}).get('url', '')
        elif image_data.get('type') == 'external':
            url = image_data.get('external', {}).get('url', '')

        if url:
            alt = caption if caption else 'image'
            result = f"{indent_str}![{alt}]({url})\n\n" if indent > 0 else f"![{alt}]({url})\n\n"

    elif block_type == 'bookmark':
        bookmark = block.get('bookmark', {})
        url = bookmark.get('url', '')
        caption = extract_rich_text(bookmark.get('caption', []))
        if url:
            display = caption if caption else url
            result = f"{indent_str}🔖 [{display}]({url})\n\n" if indent > 0 else f"🔖 [{display}]({url})\n\n"

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
    elif prop_type == 'multi_select':
        return [item.get('name') for item in prop.get('multi_select', [])]
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

    # Extract title
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

    # Extract additional metadata
    tags = []
    for prop_name, prop in properties.items():
        if prop.get('type') == 'multi_select':
            tags.extend(extract_property(prop) or [])

    # Frontmatter
    frontmatter_lines = [
        '---',
        'type: qraft-experience',
        f'category: {category.lower()}',
        f'title: {title}',
        f'imported: {datetime.now().strftime("%Y-%m-%d")}',
        f'notion_id: {page_id}',
        f'mig_status: synced'
    ]

    if tags:
        frontmatter_lines.append(f'tags: {json.dumps(tags)}')

    frontmatter_lines.append('---\n')
    frontmatter = '\n'.join(frontmatter_lines)

    # Save
    safe_name = title.replace('/', '-').replace('\\', '-')[:100]
    output_file = category_dir / f"{safe_name}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter + f"\n# {title}\n\n" + content_md)

    return output_file, category

def main():
    """Main sync function"""
    print("🔄 Starting Notion to Obsidian sync...\n")

    # Load config
    config = load_config()

    # Get environment variables for GitHub Actions
    force_sync = os.getenv('FORCE_SYNC', 'false').lower() == 'true'
    target_db = os.getenv('TARGET_DB', 'work_list')

    db_config = config['notion']['databases'][target_db]
    database_id = db_config['id']

    # Output directory
    output_dir = Path(__file__).parent.parent / 'Experiences' / 'Qraft'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Query with filter
    filter_msg = "all items" if force_sync else "mig_status='NEEDED'"
    print(f"🔍 Querying: {db_config['name']} ({filter_msg})")

    pages = query_database_with_filter(database_id, config, force_sync)

    print(f"✅ Found {len(pages)} pages to sync\n")

    if len(pages) == 0:
        print("ℹ️ Nothing to sync. All done!")
        return

    # Process pages
    imported = {'Projects': [], 'Achievements': [], 'Learning': []}
    synced_count = 0

    for i, page in enumerate(pages, 1):
        try:
            output_file, category = save_page(page, output_dir, config)
            imported[category].append(output_file.name)

            # Update migration status in Notion
            page_id = page['id']
            if update_migration_status(page_id, config, 'Done'):
                synced_count += 1
                print(f"[{i}/{len(pages)}] ✅ {output_file.name[:60]}")
            else:
                print(f"[{i}/{len(pages)}] ⚠️ Saved but status update failed: {output_file.name[:60]}")

        except Exception as e:
            print(f"[{i}/{len(pages)}] ❌ Error: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 Sync Summary")
    print("=" * 60)

    for category, files in imported.items():
        if files:
            print(f"\n{category}/ ({len(files)}개)")
            for f in files[:5]:
                print(f"  - {f}")
            if len(files) > 5:
                print(f"  ... and {len(files)-5} more")

    print(f"\n✅ Successfully synced {synced_count}/{len(pages)} pages")
    print(f"📁 Location: {output_dir}")

if __name__ == '__main__':
    main()