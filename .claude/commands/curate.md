Activate the Curator Agent from `.claude/agents/curator-agent.md`.

Run daily curation with CONTENT-FIRST approach:

1. **Check seedling → budding promotions**
   - READ each note to verify content quality
   - Check actual link meaningfulness (not just count)
   - Verify 3+ links have context explanations

2. **Check budding → evergreen promotions**
   - READ referenced notes to verify quality
   - Verify connections are bidirectional and meaningful
   - Check if note is self-contained and useful

3. **Detect orphan notes** 
   - Find notes with < 3 links
   - For each orphan: READ content to understand topic
   - Suggest connections based on:
     - Temporal context (same time period)
     - Company/project (Qraft vs aivelabs)
     - Actual content overlap (not just keywords!)

4. **Detect wilted notes**
   - Notes not updated in 6+ months
   - Minimal content or broken links
   - Suggest review, update, or archive

5. **Generate Knowledge Forest Health Report**
   - Connection quality metrics (not just quantity)
   - Temporal clustering analysis
   - Company period separation health

**IMPORTANT**: When suggesting connections for orphans, ALWAYS:
- Read the note content first
- Check the date and company period
- Find related notes from same time period
- Explain WHY they should connect
