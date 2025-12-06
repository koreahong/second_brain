---
name: File Change Hook
description: |
  Triggers when vault files are created or modified. Suggests organization and connections.

  **Triggers**: Any .md file create/edit in vault
  **Scope**: Detect temporary locations, suggest PARA migration, propose connections
  **Forbidden**: Auto-move files (requires user approval), auto-create connections

  This is a SUGGESTION ONLY hook. Always ask user before taking action.
enabled: false  # User must explicitly enable
model: claude-sonnet-4-5
---

# File Change Hook

**⚠️ This hook is DISABLED by default. Enable only if you want automatic suggestions.**

## Purpose

When you create or modify notes in the vault, this hook:
1. Detects if note is in temporary location (업무리스트/, 회고록/, etc.)
2. Suggests proper PARA location
3. Proposes temporal/thematic connections
4. Checks frontmatter completeness

## Trigger Conditions

```python
# When any .md file in vault is created/modified
if file_path.endswith('.md') and file_path.startswith(vault_root):
    trigger_hook()
```

## Hook Workflow

### 1. Detect Location Issues

```python
temporary_folders = [
    "업무리스트/",
    "회고록/",
    "레퍼런스/",
    "본깨적/"
]

if any(temp in file_path for temp in temporary_folders):
    → ⚠️ "Note is in temporary location"
    → "Suggest: Use Curator Agent to move to PARA structure"
```

### 2. Check Frontmatter

```python
frontmatter = read_frontmatter(file_path)

required_fields = ['created', 'updated', 'tags', 'company', 'status', 'type']

missing = [f for f in required_fields if f not in frontmatter]

if missing:
    → ⚠️ "Frontmatter incomplete: missing {missing}"
    → "Suggest: Add required fields"
```

### 3. Suggest Connections (if in final location)

```python
if not in_temporary_location(file_path):
    # Search temporal candidates
    created_date = frontmatter['created']
    week_start, week_end = get_week_range(created_date)

    temporal = search_notes(f"created:{week_start}..{week_end}")

    # Search thematic candidates
    tags = frontmatter['tags']
    thematic = search_notes(f"tags:{tags}")

    if temporal or thematic:
        → 💡 "Potential connections found:"
        → "Temporal: {temporal}"
        → "Thematic: {thematic}"
        → "Use Connection Curator to create links"
```

### 4. Suggest PARA Location (if in temp)

```python
note_type = frontmatter.get('type')
note_status = frontmatter.get('status')
tags = frontmatter.get('tags', [])

if note_type == 'project':
    if note_status == 'active':
        suggested = '02-Areas/크래프트테크놀로지스/Projects/Active/'
    elif note_status == 'completed':
        suggested = '02-Areas/크래프트테크놀로지스/Projects/Completed/'
elif note_type == 'reflection':
    year = created_date[:4]
    suggested = f'02-Areas/크래프트테크놀로지스/Experience/Weekly/{year}/'
# ... etc

→ 💡 "Suggested location: {suggested}"
→ "Use Curator Agent to move"
```

## Output Format

```markdown
📝 File Change Detected: {{file_name}}

**Current location**: {{current_path}}

### Issues
⚠️ In temporary location (업무리스트/)
⚠️ Missing frontmatter: ['company', 'status']

### Suggestions

**Move to**:
💡 02-Areas/크래프트테크놀로지스/Projects/Active/
   (Reason: type=project, status=active)

**Potential connections**:
💡 Temporal (same week):
   - [[2025년-12월-07일]] (3 days ago)
   - [[DataHub-구축-프로젝트]] (same week)

💡 Thematic (same tags):
   - [[Data-Governance-원칙]] (#data-governance)
   - [[Airflow-DAG-패턴]] (#airflow)

### Actions
Would you like me to:
1. [Y/n] Use Curator Agent to move to suggested location?
2. [Y/n] Use Connection Curator to create temporal connections?
3. [Y/n] Update frontmatter with missing fields?
```

## Important Notes

### ❌ NEVER Auto-Execute
- This hook **suggests only**
- Always ask user before:
  - Moving files
  - Creating connections
  - Modifying frontmatter

### ✅ User Approval Required
```
User: "Yes, move it"
→ Task tool → Curator Agent

User: "Yes, create connections"
→ Task tool → Connection Curator

User: "No thanks" or ignores
→ Skip, no action
```

### 🚫 Disabled by Default
- User must explicitly enable in settings
- Can be enabled per-session or globally
- Too aggressive if always on

## Enable/Disable

### Enable for current session
```
User: "Enable file change hook"
→ Set enabled = true for this session
```

### Enable globally
```
Edit this file:
---
enabled: true  # Change to true
---
```

### Disable
```
User: "Disable file change hook"
→ Set enabled = false
```

## Best Practices

- ✅ Use for migrated Notion content (many files need organizing)
- ✅ Use during "vault cleanup" sessions
- ✅ Disable during normal note-taking (too disruptive)
- ❌ Never auto-execute without user confirmation
- ❌ Never trigger on every single edit (too noisy)

## Advanced: Batch Mode

```
User: "Enable hook in batch mode for 업무리스트/"

→ Run hook on all files in 업무리스트/
→ Collect all suggestions
→ Present summary:
   - 46 files need moving
   - 127 potential connections
   - 23 frontmatter issues
→ Ask: "Run Orchestrator to fix all?"
```

## Reference
- [Curator Agent](../agents/knowledge__curator-agent.md)
- [Connection Curator](../agents/knowledge__connection-curator.md)
- [vault-structure.md](../conventions/knowledge/vault-structure.md)
