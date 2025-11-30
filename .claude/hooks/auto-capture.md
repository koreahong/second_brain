# Auto-Capture Hook

Automatically enhance captured notes with context.

## Trigger
- `on_note_create` in `00-Inbox/`

## Actions

1. **Auto-detect tags**
   ```python
   tags = detect_tags_from_content(note.content)
   # airflow, dbt, python, etc.
   ```

2. **Capture context**
   ```yaml
   captured: {{timestamp}}
   context:
     current_project: {{active_project}}
     recent_notes: [{{recent_3_notes}}]
     related_tags: [{{auto_tags}}]
   review_by: {{tomorrow}}
   ```

3. **Link to Daily Note**
   - Find today's Daily Note
   - Add to ## Captured section
   - Create bidirectional link

4. **Set reminder**
   - 24-hour reminder to organize
   - If inbox >= 10: Alert user

5. **Suggest related notes**
   ```
   💡 Related notes you might want to link:
   - [[{{related_1}}]] (0.85 similarity)
   - [[{{related_2}}]] (0.78 similarity)
   ```

## Enhancement

**Before:**
```markdown
---
---

Airflow XCom S3 pattern idea
```

**After:**
```markdown
---
type: fleeting
captured: 2025-11-30T14:30:00
context:
  project: DataHub-OIDC
  tags: [airflow, xcom, s3, pattern]
review_by: 2025-12-01
status: inbox
---

# Airflow XCom S3 pattern idea

Airflow XCom S3 pattern idea

## Context
- Current project: [[DataHub-OIDC]]
- Related: [[Airflow-Hub]], [[S3-Integration]]

## Next
→ Review and convert to Permanent Note by tomorrow
```

## Skip Conditions
- Notes already organized (not in Inbox)
- System files
