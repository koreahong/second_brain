#!/usr/bin/env python3
"""
Remove unnecessary properties from RecordMaster database schema
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


def remove_properties(api_token, db_id, properties_to_remove):
    """Remove properties from database schema by setting them to null"""
    url = f'https://api.notion.com/v1/databases/{db_id}'
    headers = get_headers(api_token)

    # Build properties object with null values to remove them
    properties = {}
    for prop_name in properties_to_remove:
        properties[prop_name] = None

    payload = {
        "properties": properties
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.text


def main():
    config = load_config()
    api_token = config["notion"]["api_token"]
    db_id = config["notion"]["record_master_db_id"]

    print("🗑️  Removing unnecessary properties from RecordMaster database...")
    print("="*80)
    print()

    # Properties to remove
    properties_to_remove = [
        "Status",          # 상태
    ]

    print("Removing properties:")
    for prop in properties_to_remove:
        print(f"  - {prop}")
    print()

    success, result = remove_properties(api_token, db_id, properties_to_remove)

    if success:
        print("✅ Successfully removed properties from database schema")
        print()
        print("📋 Remaining properties:")
        remaining_props = result.get("properties", {})
        for prop_name in remaining_props.keys():
            print(f"  - {prop_name}")
    else:
        print("❌ Failed to remove properties")
        print(f"Error: {result}")

    print()
    print("="*80)
    print()


if __name__ == '__main__':
    main()
