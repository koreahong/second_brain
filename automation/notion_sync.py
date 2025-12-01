#!/usr/bin/env python3
"""
Notion Record Master to Obsidian Sync
Unified sync system using a single master database
"""

import requests
import json
from pathlib import Path
from datetime import datetime
import sys
import os


class RecordMasterSync:
    """레코드 마스터 데이터베이스 동기화"""

    def __init__(self, config_path="config.json"):
        """Initialize with config file"""
        config_file = Path(__file__).parent / config_path

        if not config_file.exists():
            raise FileNotFoundError(
                f"Config file not found: {config_path}\n"
                "Please create it from config.template.json"
            )

        with open(config_file) as f:
            self.config = json.load(f)

        # Read API token from environment variable, fallback to config
        self.api_token = os.getenv("NOTION_API_KEY") or self.config["notion"].get("api_token")
        self.db_id = self.config["notion"]["record_master_db_id"]
        self.vault_path = Path(self.config["obsidian"]["vault_path"])
        self.location_mapping = self.config["obsidian"]["location_mapping"]
        self.sync_settings = self.config["notion"]["sync_settings"]

    def get_headers(self):
        """Get Notion API headers"""
        return {
            'Authorization': f'Bearer {self.api_token}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }

    def fetch_records_to_migrate(self):
        """Mig_Status=NEEDED인 레코드 조회"""
        url = f'https://api.notion.com/v1/databases/{self.db_id}/query'
        headers = self.get_headers()

        filter_config = {
            "filter": {
                "property": "Mig_Status",
                "select": {
                    "equals": self.sync_settings["filter_status"]
                }
            },
            "sorts": [
                {
                    "property": "Updated",
                    "direction": "descending"  # 최근 수정된 것부터
                }
            ],
            "page_size": self.sync_settings["batch_size"]
        }

        all_results = []
        has_more = True
        start_cursor = None

        while has_more:
            if start_cursor:
                filter_config['start_cursor'] = start_cursor

            response = requests.post(url, headers=headers, json=filter_config)

            if response.status_code != 200:
                print(f"❌ API Error: {response.status_code}")
                print(response.text)
                return []

            data = response.json()
            all_results.extend(data.get('results', []))

            has_more = data.get('has_more', False)
            start_cursor = data.get('next_cursor')

        return all_results

    def extract_property(self, prop):
        """Extract property value from Notion property"""
        if not prop:
            return None

        prop_type = prop.get('type')

        if prop_type == 'title':
            title_array = prop.get('title', [])
            return ''.join([t.get('plain_text', '') for t in title_array])

        elif prop_type == 'rich_text':
            rt_array = prop.get('rich_text', [])
            return ''.join([rt.get('plain_text', '') for rt in rt_array])

        elif prop_type == 'select':
            select = prop.get('select')
            return select.get('name') if select else None

        elif prop_type == 'multi_select':
            return [item.get('name') for item in prop.get('multi_select', [])]

        elif prop_type == 'date':
            date = prop.get('date')
            if date:
                return date.get('start')
            return None

        elif prop_type == 'number':
            return prop.get('number')

        elif prop_type == 'checkbox':
            return prop.get('checkbox')

        elif prop_type == 'created_time':
            return prop.get('created_time')

        elif prop_type == 'last_edited_time':
            return prop.get('last_edited_time')

        else:
            return None

    def extract_page_properties(self, page):
        """Notion 페이지 속성 추출"""
        props = page["properties"]

        return {
            "id": page["id"],
            "title": self.extract_property(props.get("Name")) or "Untitled",
            "content_type": self.extract_property(props.get("Content_Type")),
            "category": self.extract_property(props.get("Category")) or [],
            "tags": self.extract_property(props.get("Tags")) or [],
            "company": self.extract_property(props.get("Company")),
            "period": self.extract_property(props.get("Period")),
            "status": self.extract_property(props.get("Status")),
            "created": props.get("Created", {}).get("created_time"),
            "updated": props.get("Updated", {}).get("last_edited_time"),
        }

    def get_block_children(self, block_id):
        """Get children of a block recursively"""
        url = f'https://api.notion.com/v1/blocks/{block_id}/children'
        headers = self.get_headers()

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
                    child['children'] = self.get_block_children(child['id'])

            all_children.extend(children)

            has_more = data.get('has_more', False)
            start_cursor = data.get('next_cursor')

        return all_children

    def get_page_content(self, page_id):
        """Notion 페이지 본문 가져오기"""
        blocks = self.get_block_children(page_id)
        return self.blocks_to_markdown(blocks)

    def extract_rich_text(self, rich_text_array):
        """Extract plain text from rich text"""
        if not rich_text_array:
            return ''
        return ''.join([rt.get('plain_text', '') for rt in rich_text_array])

    def block_to_markdown(self, block, indent=0):
        """Convert single block to markdown"""
        block_type = block.get('type')
        indent_str = '  ' * indent
        result = ''

        if block_type == 'paragraph':
            text = self.extract_rich_text(block['paragraph'].get('rich_text', []))
            if text:
                result = f"{indent_str}{text}\n\n" if indent > 0 else text + '\n\n'

        elif block_type in ['heading_1', 'heading_2', 'heading_3']:
            level = block_type[-1]
            text = self.extract_rich_text(block[block_type].get('rich_text', []))
            if indent > 0:
                result = f"{indent_str}**{text}**\n\n"
            else:
                result = f"{'#' * int(level)} {text}\n\n"

        elif block_type == 'bulleted_list_item':
            text = self.extract_rich_text(block['bulleted_list_item'].get('rich_text', []))
            result = f"{indent_str}- {text}\n"
            if 'children' in block and block['children']:
                for child in block['children']:
                    result += self.block_to_markdown(child, indent + 1)

        elif block_type == 'numbered_list_item':
            text = self.extract_rich_text(block['numbered_list_item'].get('rich_text', []))
            result = f"{indent_str}1. {text}\n"
            if 'children' in block and block['children']:
                for child in block['children']:
                    result += self.block_to_markdown(child, indent + 1)

        elif block_type == 'to_do':
            text = self.extract_rich_text(block['to_do'].get('rich_text', []))
            checked = '[x]' if block['to_do'].get('checked', False) else '[ ]'
            result = f"{indent_str}- {checked} {text}\n"
            if 'children' in block and block['children']:
                for child in block['children']:
                    result += self.block_to_markdown(child, indent + 1)

        elif block_type == 'code':
            text = self.extract_rich_text(block['code'].get('rich_text', []))
            lang = block['code'].get('language', '')
            if indent > 0:
                lines = text.split('\n')
                indented_code = '\n'.join([indent_str + line for line in lines])
                result = f"{indent_str}```{lang}\n{indented_code}\n{indent_str}```\n\n"
            else:
                result = f"```{lang}\n{text}\n```\n\n"

        elif block_type == 'quote':
            text = self.extract_rich_text(block['quote'].get('rich_text', []))
            result = f"{indent_str}> {text}\n\n"

        elif block_type == 'callout':
            text = self.extract_rich_text(block['callout'].get('rich_text', []))
            icon = block['callout'].get('icon')
            emoji = icon.get('emoji', '💡') if icon and icon.get('type') == 'emoji' else '💡'
            result = f"{emoji} **{text}**\n\n"
            if 'children' in block and block['children']:
                for child in block['children']:
                    result += self.block_to_markdown(child, indent)

        elif block_type == 'toggle':
            text = self.extract_rich_text(block['toggle'].get('rich_text', []))
            result = f"<details>\n<summary>{text}</summary>\n\n"
            if 'children' in block and block['children']:
                for child in block['children']:
                    result += self.block_to_markdown(child, indent)
            result += "</details>\n\n"

        elif block_type == 'divider':
            result = "---\n\n"

        elif block_type == 'image':
            image_data = block.get('image', {})
            caption = self.extract_rich_text(image_data.get('caption', []))
            url = ''
            if image_data.get('type') == 'file':
                url = image_data.get('file', {}).get('url', '')
            elif image_data.get('type') == 'external':
                url = image_data.get('external', {}).get('url', '')

            if url:
                alt = caption if caption else 'image'
                result = f"![{alt}]({url})\n\n"

        elif block_type == 'bookmark':
            bookmark = block.get('bookmark', {})
            url = bookmark.get('url', '')
            caption = self.extract_rich_text(bookmark.get('caption', []))
            if url:
                display = caption if caption else url
                result = f"🔖 [{display}]({url})\n\n"

        return result

    def blocks_to_markdown(self, blocks):
        """Convert blocks array to markdown"""
        return ''.join([self.block_to_markdown(b) for b in blocks])

    def determine_target_path(self, record):
        """Content_Type 기반 목표 경로 결정"""
        content_type = record["content_type"]
        base_path = self.location_mapping.get(content_type, "03-Resources")

        # 추가 분류 로직
        if content_type == "Reference":
            # Category로 세부 분류
            if record["category"]:
                category = record["category"][0]  # 첫 번째 카테고리
                base_path = f"{base_path}/{category}"

        elif content_type == "Insight":
            # Company로 Work/Personal 구분
            if record["company"] in ["aivelabs", "Qraft"]:
                base_path = f"{base_path}/Work"
            else:
                base_path = f"{base_path}/Personal"

        elif content_type == "Project":
            # Status로 Active/Completed/Archived 구분
            status = record["status"] or "Active"
            base_path = base_path.replace("/Active", f"/{status}")

        return base_path

    def create_frontmatter(self, record):
        """Obsidian frontmatter 생성"""
        frontmatter = {
            "notion_id": record["id"],
            "content_type": record["content_type"],
            "created": record["created"],
            "updated": record["updated"],
        }

        # Tags 추가
        if record["tags"]:
            frontmatter["tags"] = record["tags"]

        # 선택적 필드
        if record["company"]:
            frontmatter["company"] = record["company"]
        if record["period"]:
            frontmatter["period"] = record["period"]
        if record["status"]:
            frontmatter["status"] = record["status"]
        if record["category"]:
            frontmatter["category"] = record["category"]

        # YAML 형식으로 변환
        lines = ["---"]
        for key, value in frontmatter.items():
            if isinstance(value, list):
                if value:  # 빈 리스트가 아닐 때만
                    lines.append(f"{key}:")
                    for item in value:
                        lines.append(f"  - {item}")
            elif value is not None:
                # 문자열에 콜론이 포함된 경우 따옴표로 감싸기
                if isinstance(value, str) and ':' in value:
                    lines.append(f'{key}: "{value}"')
                else:
                    lines.append(f"{key}: {value}")
        lines.append("---")

        return "\n".join(lines)

    def sanitize_filename(self, filename):
        """파일명 정리"""
        # 특수문자 제거
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "-")

        # 길이 제한
        if len(filename) > 100:
            filename = filename[:100]

        return filename.strip()

    def create_obsidian_note(self, record, content):
        """Obsidian 노트 생성"""
        target_path = self.determine_target_path(record)
        full_path = self.vault_path / target_path

        # 디렉토리 생성
        full_path.mkdir(parents=True, exist_ok=True)

        # 파일명 생성 (특수문자 제거)
        filename = self.sanitize_filename(record["title"])
        file_path = full_path / f"{filename}.md"

        # 중복 방지
        counter = 1
        while file_path.exists():
            file_path = full_path / f"{filename}-{counter}.md"
            counter += 1

        # 파일 생성
        frontmatter = self.create_frontmatter(record)
        full_content = f"{frontmatter}\n\n# {record['title']}\n\n{content}"

        file_path.write_text(full_content, encoding="utf-8")

        # 상대 경로 반환
        return str(file_path.relative_to(self.vault_path))

    def update_migration_status(self, page_id, obsidian_path, success=True):
        """Notion 페이지의 마이그레이션 상태 업데이트"""
        url = f'https://api.notion.com/v1/pages/{page_id}'
        headers = self.get_headers()

        # Mig_Status만 업데이트 (다른 migration 관련 속성은 제거됨)
        properties = {
            "Mig_Status": {
                "select": {
                    "name": "DONE" if success else "ERROR"
                }
            }
        }

        payload = {"properties": properties}
        response = requests.patch(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"⚠️ Failed to update status: {response.status_code}")
            return False

        return True

    def sync(self):
        """메인 동기화 함수"""
        print("🔄 Starting Record Master Sync...\n")

        # 1. NEEDED 레코드 조회
        print(f"🔍 Fetching records with Mig_Status={self.sync_settings['filter_status']}...")
        records = self.fetch_records_to_migrate()

        print(f"📊 Found {len(records)} records\n")

        if len(records) == 0:
            print("✅ Nothing to migrate. All done!")
            return

        success_count = 0
        error_count = 0
        results = {
            "Project": [],
            "Experience": [],
            "Reference": [],
            "Insight": [],
            "Article": [],
            "Book": []
        }

        # 2. 레코드 처리
        for i, page in enumerate(records, 1):
            try:
                # 속성 추출
                record = self.extract_page_properties(page)
                print(f"[{i}/{len(records)}] 📝 {record['title'][:50]}...")

                # Content_Type 확인
                if not record['content_type']:
                    print(f"   ⚠️ Skipping: Content_Type not set")
                    continue

                # 본문 가져오기
                content = self.get_page_content(page["id"])

                # Obsidian 노트 생성
                obsidian_path = self.create_obsidian_note(record, content)
                print(f"   ✅ Created: {obsidian_path}")

                # 상태 업데이트
                if self.update_migration_status(page["id"], obsidian_path, success=True):
                    success_count += 1
                    results[record['content_type']].append(obsidian_path)
                else:
                    print(f"   ⚠️ File created but status update failed")

            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                self.update_migration_status(page["id"], "", success=False)
                error_count += 1

        # 3. 요약
        print("\n" + "=" * 60)
        print("📊 Sync Summary")
        print("=" * 60)

        for content_type, paths in results.items():
            if paths:
                print(f"\n{content_type} ({len(paths)}개)")
                for path in paths[:3]:
                    print(f"  - {path}")
                if len(paths) > 3:
                    print(f"  ... and {len(paths)-3} more")

        print(f"\n✅ Success: {success_count}")
        print(f"❌ Errors: {error_count}")
        print(f"📁 Vault: {self.vault_path}")
        print("\n✨ Migration complete!\n")


def main():
    """Main entry point"""
    try:
        syncer = RecordMasterSync()
        syncer.sync()
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"❌ Config error: Missing key {e}")
        print("Please check your config.json structure")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
