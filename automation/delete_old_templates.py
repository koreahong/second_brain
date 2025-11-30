#!/usr/bin/env python3
"""
Delete old template pages from RecordMaster
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


def extract_text(rich_text_array):
    """Extract plain text from rich text"""
    if not rich_text_array:
        return ''
    return ''.join([rt.get('plain_text', '') for rt in rich_text_array])


def get_template_pages(api_token, db_id):
    """Get all template pages (Mig_Status = SKIP and name contains [템플릿])"""
    url = f'https://api.notion.com/v1/databases/{db_id}/query'
    headers = get_headers(api_token)

    payload = {
        "filter": {
            "property": "Mig_Status",
            "select": {
                "equals": "SKIP"
            }
        },
        "page_size": 100
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"Error fetching pages: {response.status_code}")
        print(response.text)
        return []

    return response.json().get('results', [])


def archive_page(api_token, page_id):
    """Archive (delete) a page"""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    headers = get_headers(api_token)

    payload = {
        "archived": True
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        return True
    else:
        print(f"Error archiving page: {response.status_code}")
        print(response.text)
        return False


def main():
    config = load_config()
    api_token = config["notion"]["api_token"]
    db_id = config["notion"]["record_master_db_id"]

    print("🗑️  Deleting old template pages...")
    print("="*80)
    print()

    pages = get_template_pages(api_token, db_id)

    if not pages:
        print("No template pages found (Mig_Status=SKIP)\n")
        return

    deleted_count = 0

    for page in pages:
        # Get page title
        properties = page.get('properties', {})
        title = ""

        for prop_name, prop_value in properties.items():
            if prop_value.get('type') == 'title':
                title = extract_text(prop_value.get('title', []))
                break

        # Only delete pages with [템플릿] in title
        if "[템플릿]" in title:
            print(f"Deleting: {title}... ", end="", flush=True)

            if archive_page(api_token, page['id']):
                print("✅")
                deleted_count += 1
            else:
                print("❌")
        else:
            print(f"Skipping (not a template): {title}")

    print()
    print("="*80)
    print(f"✅ Deleted {deleted_count} template pages\n")


if __name__ == '__main__':
    main()
