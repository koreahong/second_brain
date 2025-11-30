#!/usr/bin/env python3
"""Check RecordMaster database schema"""

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


def get_database_schema(api_token, db_id):
    url = f'https://api.notion.com/v1/databases/{db_id}'
    headers = get_headers(api_token)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

    return response.json()


def main():
    config = load_config()
    api_token = config["notion"]["api_token"]
    db_id = config["notion"]["record_master_db_id"]

    print("🔍 Fetching RecordMaster schema...\n")

    db_info = get_database_schema(api_token, db_id)

    if db_info:
        print("📊 Database Properties:\n")
        properties = db_info.get("properties", {})

        for prop_name, prop_info in properties.items():
            prop_type = prop_info.get("type")
            print(f"  - {prop_name}: {prop_type}")

            # Show options for select/multi_select
            if prop_type in ["select", "multi_select"]:
                options = prop_info.get(prop_type, {}).get("options", [])
                if options:
                    option_names = [opt["name"] for opt in options]
                    print(f"    Options: {', '.join(option_names)}")

        print("\n" + "="*60)
        print("Full schema (JSON):")
        print("="*60)
        print(json.dumps(properties, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
