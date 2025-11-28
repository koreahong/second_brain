#!/usr/bin/env python3
"""
Import Notion daily retrospective database to Obsidian Daily Notes

Usage:
    python import_daily_notes.py <notion-export-folder>
"""

import os
import sys
import re
import shutil
from pathlib import Path
from datetime import datetime
import csv

def extract_date_from_title(title):
    """Extract date from various Notion title formats"""
    # Try YYYY-MM-DD format
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', title)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

    # Try YYYY/MM/DD format
    match = re.search(r'(\d{4})/(\d{2})/(\d{2})', title)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

    # Try YYYY.MM.DD format
    match = re.search(r'(\d{4})\.(\d{2})\.(\d{2})', title)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

    return None

def convert_notion_to_daily_note(notion_file, output_dir):
    """Convert a single Notion export to Daily Note format"""
    with open(notion_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract date from filename or content
    filename = notion_file.stem
    date_str = extract_date_from_title(filename)

    if not date_str:
        # Try to find date in content
        lines = content.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            date_str = extract_date_from_title(line)
            if date_str:
                break

    if not date_str:
        print(f"⚠️  Could not extract date from: {filename}")
        return None

    # Parse date
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_name = date_obj.strftime('%A')  # Get day name
    except:
        print(f"⚠️  Invalid date format: {date_str}")
        return None

    # Remove Notion frontmatter if exists
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Create new frontmatter
    frontmatter = f"""---
created: {date_str}
type: daily
tags: [daily, retrospective, notion-import]
imported: {datetime.now().strftime('%Y-%m-%d')}
---

# {date_str} ({day_name})

"""

    # Clean up content
    # Remove title if it's just the date
    content = re.sub(r'^#\s+\d{4}[-/\.]\d{2}[-/\.]\d{2}.*?\n', '', content)

    # Combine
    final_content = frontmatter + content.strip()

    # Write to output
    output_file = output_dir / f"{date_str}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

    return date_str

def import_from_csv(csv_file, output_dir):
    """Import from Notion CSV export"""
    imported = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Notion database exports have different column names
            # Common patterns: "Name", "Title", "Date", etc.

            # Try to find date column
            date_str = None
            for key in row.keys():
                if 'date' in key.lower() or 'created' in key.lower():
                    date_str = row[key]
                    break

            if not date_str:
                # Try to extract from Name/Title
                for key in ['Name', 'Title', 'name', 'title']:
                    if key in row:
                        date_str = extract_date_from_title(row[key])
                        if date_str:
                            break

            if not date_str:
                print(f"⚠️  Skipping row (no date found): {row}")
                continue

            # Normalize date
            try:
                date_obj = datetime.strptime(date_str[:10], '%Y-%m-%d')
                normalized_date = date_obj.strftime('%Y-%m-%d')
                day_name = date_obj.strftime('%A')
            except:
                print(f"⚠️  Invalid date: {date_str}")
                continue

            # Build content from all columns
            content_parts = []
            for key, value in row.items():
                if value and key.lower() not in ['name', 'title', 'date', 'created']:
                    content_parts.append(f"## {key}\n\n{value}\n")

            content = '\n'.join(content_parts) if content_parts else "_내용 없음_\n"

            # Create daily note
            frontmatter = f"""---
created: {normalized_date}
type: daily
tags: [daily, retrospective, notion-import]
imported: {datetime.now().strftime('%Y-%m-%d')}
---

# {normalized_date} ({day_name})

"""

            final_content = frontmatter + content

            # Write
            output_file = output_dir / f"{normalized_date}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_content)

            imported.append(normalized_date)

    return imported

def main():
    if len(sys.argv) < 2:
        print("Usage: python import_daily_notes.py <notion-export-folder-or-csv>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"❌ Path not found: {input_path}")
        sys.exit(1)

    # Output directory
    vault_dir = Path(__file__).parent
    output_dir = vault_dir / 'Flow' / 'Daily'
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"📥 Importing from: {input_path}")
    print(f"📁 Output directory: {output_dir}")
    print()

    imported = []

    # Check if it's a CSV file
    if input_path.is_file() and input_path.suffix == '.csv':
        print("📊 Importing from CSV...")
        imported = import_from_csv(input_path, output_dir)

    # Check if it's a directory (Notion export folder)
    elif input_path.is_dir():
        print("📂 Importing from Notion export folder...")

        # Find all markdown files
        md_files = list(input_path.glob('**/*.md'))

        if not md_files:
            print("❌ No markdown files found in the export folder")
            sys.exit(1)

        for md_file in md_files:
            result = convert_notion_to_daily_note(md_file, output_dir)
            if result:
                imported.append(result)

        # Also check for CSV files in the export
        csv_files = list(input_path.glob('**/*.csv'))
        for csv_file in csv_files:
            try:
                csv_imported = import_from_csv(csv_file, output_dir)
                imported.extend(csv_imported)
            except Exception as e:
                print(f"⚠️  Error processing CSV {csv_file.name}: {e}")

    else:
        print(f"❌ Invalid input: {input_path}")
        print("Please provide a Notion export folder or CSV file")
        sys.exit(1)

    # Summary
    print()
    print("=" * 60)
    print(f"✅ Import Complete!")
    print(f"   Total notes imported: {len(set(imported))}")
    print(f"   Location: {output_dir}")
    print()

    if imported:
        # Show date range
        dates = sorted(set(imported))
        print(f"   Date range: {dates[0]} to {dates[-1]}")
        print()
        print(f"   First 10 dates:")
        for date in dates[:10]:
            print(f"     - {date}")
        if len(dates) > 10:
            print(f"     ... and {len(dates) - 10} more")

    print("=" * 60)
    print()
    print("💡 Next steps:")
    print("   1. Open Obsidian")
    print("   2. Go to Flow/Daily folder")
    print("   3. Review imported notes")
    print("   4. Enable Calendar plugin for better navigation")

if __name__ == '__main__':
    main()
