#!/usr/bin/env python3
"""
Migrate single Notion database to Obsidian
Usage: python migrate_single_db.py <db_key>
Example: python migrate_single_db.py career
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from migrate_to_para import (
    load_config, query_all_pages, save_to_para, should_skip
)

def main():
    if len(sys.argv) < 2:
        print("Usage: python migrate_single_db.py <db_key>")
        print("\nAvailable databases:")
        config = load_config()
        for key, info in config['notion']['databases'].items():
            print(f"  - {key}: {info['name']}")
        sys.exit(1)

    db_key = sys.argv[1]

    print(f"🔄 Migrating single database: {db_key}")

    config = load_config()
    vault_root = Path(__file__).parent.parent

    if db_key not in config['notion']['databases']:
        print(f"❌ Database key '{db_key}' not found in config")
        sys.exit(1)

    db_info = config['notion']['databases'][db_key]
    db_name = db_info['name']
    db_id = db_info['id']

    print(f"\n📂 Processing: {db_name}")
    print(f"   ID: {db_id}")

    pages = query_all_pages(db_id, config)
    print(f"   Found {len(pages)} pages\n")

    migrated = 0
    skipped = 0

    for i, page in enumerate(pages, 1):
        result = save_to_para(page, vault_root, config, db_name)
        if result:
            migrated += 1
            print(f"   [{i}/{len(pages)}] ✅")
        else:
            skipped += 1
            print(f"   [{i}/{len(pages)}] ⏭️")

    print(f"\n🎉 Migration complete!")
    print(f"   ✅ Migrated: {migrated}")
    print(f"   ⏭️ Skipped: {skipped}")
    print(f"   📁 Location: {vault_root / db_name}")

if __name__ == '__main__':
    main()
