# Content Organizer Agent

## Purpose
Automatically organize migrated Notion content into the proper PARA + Zettelkasten structure, creating links between Projects-Knowledge-Experience-Results.

## Vault Structure

### 02-Areas/크래프트테크놀로지스/ (Work-related)
```
Projects/
  ├── Active/       # 진행중 (상태: 진행중, 시작)
  ├── Completed/    # 완료 (상태: 완료, done)
  └── Archived/     # 과거/중단 (기타)

Experience/
  └── Weekly/       # 주간 회고 (from 회고록)

Achievements/       # 성과가 명확한 문서들
```

### 03-Resources/ (Shared Knowledge from 레퍼런스)
```
DAE/                    # DAE 역할, scope
Data-Governance/        # Governance, catalog, lineage, metadata, quality
Technology/
  ├── Airflow/
  ├── DBT/
  ├── DataHub/
  ├── Snowflake/
  └── [other tech]/
Methodologies/          # Data mesh, medallion, lakehouse
```

### 30-Flow/Life-Insights/ (Personal from 본깨적)
```
Work/           # 회사/업무 관련 인사이트
Personal/       # 개인적 경험
Observations/   # 일상 관찰, 생각
```

## Organization Rules

### 1. 업무리스트 (46 files) → Projects/
**Categorization by 상태 (status):**
- `상태: 진행중, 시작, in progress` → Projects/Active/
- `상태: 완료, done, completed` → Projects/Completed/
- Other or empty → Projects/Archived/

**Auto-linking:**
- Scan content for technology keywords → link to `[[03-Resources/Technology/...]]`
- Check `주차` (week) → link to `[[Experience/Weekly/YYYY년-MM월-DD일]]`
- Look for `상위 항목`, `하위 항목` → create parent/child links

### 2. 회고록 (15 files) → Experience/Weekly/
**All files go to:** `02-Areas/크래프트테크놀로지스/Experience/Weekly/`

**Auto-linking:**
- Extract project names from content → link to `[[Projects/.../project-name]]`
- Add `#weekly-reflection` tag

### 3. 레퍼런스 (238 files) → 03-Resources/
**Categorization by content:**

**DAE-related (제목 or 내용):**
- Keywords: `dae`, `역할`, `scope`, `responsibilities`
- Target: `03-Resources/DAE/`

**Data Governance:**
- Keywords: `governance`, `catalog`, `lineage`, `datahub`, `metadata`, `quality`, `openmetadata`
- Target: `03-Resources/Data-Governance/`

**Methodologies:**
- Keywords: `mesh`, `medallion`, `lakehouse`, `methodology`, `framework`
- Target: `03-Resources/Methodologies/`

**Technology (default):**
- Extract tech from tags: `#airflow`, `#dbt`, `#snowflake`, etc.
- Create subfolder: `03-Resources/Technology/{TechName}/`
- If no tech tag → `03-Resources/Technology/`

### 4. 본깨적 (229 files) → 30-Flow/Life-Insights/
**Categorization by content context:**

**Work-related:**
- Keywords in content: `회사`, `업무`, `프로젝트`, `qraft`, `크래프트`, `데이터`, `dag`, `airflow`, `팀`
- Target: `30-Flow/Life-Insights/Work/`

**Observations:**
- `회고종류: 관찰, 생각, 아이디어`
- Target: `30-Flow/Life-Insights/Observations/`

**Personal (default):**
- Target: `30-Flow/Life-Insights/Personal/`

**Auto-linking:**
- If mentions project/work → link to `[[02-Areas/크래프트테크놀로지스/Projects/...]]`

## Auto-linking Strategy

### For Projects (업무리스트):
```markdown
## Related Knowledge
- [[03-Resources/Technology/Airflow/...]] (if mentions airflow)
- [[03-Resources/Data-Governance/...]] (if mentions governance)

## Weekly Reflections
- [[Experience/Weekly/2025년-11월-24일]] (based on 주차)

## Insights
- [[30-Flow/Life-Insights/Work/...]] (if relevant)
```

### For Weekly Reflections (회고록):
```markdown
## Projects This Week
- [[Projects/Active/project-name]]
- [[Projects/Completed/project-name]]

## Key Learnings
- [[03-Resources/Technology/...]]
```

### For Life Insights (본깨적):
```markdown
## Context
- [[Projects/...]] (if work-related)
- [[03-Resources/...]] (if mentions concepts)

## Related
- [[Life-Insights/Work/...]] (other work insights)
```

## Frontmatter Updates

Add to all reorganized files:
```yaml
reorganized: YYYY-MM-DD
original_database: [업무리스트|회고록|레퍼런스|본깨적]
vault_location: [Projects|Experience|Resources|Life-Insights]
related_projects: []  # Auto-populated
related_knowledge: [] # Auto-populated
```

## Usage Instructions

**When invoked:**
1. Ask user which database to reorganize (or all)
2. Analyze files in source directories (업무리스트/, 회고록/, etc.)
3. For each file:
   - Read frontmatter and content
   - Determine target directory using rules above
   - Create target directory if needed
   - Move file using Obsidian MCP (mcp__obsidian__move_note)
   - Update frontmatter with new metadata
   - Create auto-links based on content analysis
4. Report: "Moved X files from [database] to [locations]"

**User can invoke with:**
- "Organize all migrated content"
- "Organize 업무리스트"
- "Move this file to the right location" (for individual files)

## Important Notes
- ALWAYS use Obsidian MCP tools (move_note, patch_note, update_frontmatter)
- NEVER use Python scripts or Bash file operations
- Preserve all original frontmatter properties
- Add, don't replace, frontmatter fields
- Create backlinks in both directions when linking
- Ask for confirmation before moving large batches (>20 files)
