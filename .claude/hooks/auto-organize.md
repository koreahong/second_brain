# Auto-Organize Hook

## Trigger
When Claude Code writes or edits a markdown file in the vault

## Behavior

### 1. Detect Misplaced Files
If a file is in one of these temporary locations:
- `업무리스트/`
- `회고록/`
- `레퍼런스/`
- `본깨적/`
- `00-Inbox/`

**Action:**
- Alert user: "📍 This file appears to be in a temporary location. Would you like me to organize it?"
- If yes → invoke content-organizer agent

### 2. Auto-Tag Based on Content
When creating/editing any file, scan content and auto-add tags:

**Technology tags:**
- Mentions `airflow` → add `#airflow`
- Mentions `dbt` → add `#dbt`
- Mentions `datahub` → add `#datahub`
- Mentions `snowflake` → add `#snowflake`
- etc.

**Context tags:**
- In `Projects/Active/` → add `#active-project`
- In `Projects/Completed/` → add `#completed`
- In `Experience/Weekly/` → add `#weekly-reflection`
- In `Life-Insights/Work/` → add `#work-insight`

**Apply tags using:** `mcp__obsidian__manage_tags`

### 3. Auto-Link Creation
When editing a project file in `Projects/`, scan for:

**Technology mentions:**
- Extract tech keywords (airflow, dbt, snowflake, etc.)
- Search for related files: `mcp__obsidian__search_notes(query="{tech}", searchContent=true)`
- Add "## Related Knowledge" section with links

**Weekly mentions:**
- Extract `주차` (week number) from frontmatter
- Find corresponding weekly reflection
- Add to "## Weekly Reflections" section

**Implementation:**
```markdown
## Related Knowledge
- [[03-Resources/Technology/Airflow/DAG-Patterns]]
- [[03-Resources/Data-Governance/Metadata-Management]]

## Weekly Reflections
- [[Experience/Weekly/2025년-11월-24일]]
```

### 4. Backlink Creation
When a link is created, ensure backlink exists in target:

Example:
- If `Projects/Active/datahub-구축.md` links to `Technology/DataHub/Installation.md`
- Then add to `Installation.md`:
  ```markdown
  ## Used In
  - [[Projects/Active/datahub-구축]]
  ```

## Configuration

Enable/disable behaviors in frontmatter:
```yaml
auto_organize: true     # Auto-suggest organization
auto_tag: true          # Auto-add tags
auto_link: true         # Auto-create links
auto_backlink: true     # Auto-create backlinks
```

## Important Notes
- ALWAYS ask before moving files
- Only suggest, never force organization
- Preserve all existing frontmatter
- Use Obsidian MCP tools only
- Run silently - don't spam user with notifications
- Only alert for significant suggestions
