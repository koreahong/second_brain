# Auto-Link Hook

Automatically create links when notes are created or modified.

## Trigger
- `on_note_create`
- `on_note_save`

## Actions

1. **Check current link count**
   - If >= 8 links: Skip (already well-connected)
   - If < 8 links: Activate Linker Agent

2. **Activate Linker Agent**
   - Use `.claude/agents/linker-agent.md`
   - Find 8+ meaningful connections
   - Add links automatically

3. **Update backlinks**
   - Add "Referenced by" sections
   - Maintain bidirectional links

4. **Notify user**
   ```
   ✅ Auto-linked: [[{{note_title}}]]
   - Added: {{new_links_count}} links
   - Total: {{total_links}} (goal: 8+)
   ```

## Quality Rules
- Only add links with relevance > 0.7
- Avoid duplicate links
- Prefer Evergreen notes
- Include link descriptions

## Skip Conditions
- Fleeting notes (too early)
- Templates
- System files
- README files
