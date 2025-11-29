---
description: Organize migrated Notion content into PARA structure
---

Invoke the content-organizer agent to reorganize migrated content.

Analyze files in these directories:
- 업무리스트/ (46 files)
- 회고록/ (15 files)
- 레퍼런스/ (238 files)
- 본깨적/ (229 files)

Organize them into:
- 02-Areas/크래프트테크놀로지스/ (work projects + weekly reflections)
- 03-Resources/ (shared knowledge)
- 30-Flow/Life-Insights/ (personal life insights)

Follow the rules in `.claude/agents/content-organizer.md`.

Ask which database to organize first, or suggest organizing all if user agrees.

Use Obsidian MCP tools only - no Python scripts or Bash file operations.
