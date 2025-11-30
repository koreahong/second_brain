# Auto-Curate Hook

Automatically check note quality and suggest promotions.

## Trigger
- `on_note_save`
- `daily_6am`

## Actions

1. **Check note age and quality**
   ```python
   if note.age >= 7_days and note.status == "seedling":
       if qualifies_for_budding(note):
           suggest_promotion("budding")

   if note.age >= 30_days and note.status == "budding":
       if qualifies_for_evergreen(note):
           suggest_promotion("evergreen")
   ```

2. **Detect issues**
   - Orphan (links < 3)
   - Wilted (not updated 180+ days)
   - Minimal content (< 100 chars)

3. **Notify user**
   ```
   🌱 [[{{note_title}}]] is ready for promotion!

   ✅ Age: {{age}} days (>= 7)
   ✅ Content: {{char_count}} chars (>= 300)
   ✅ Links: {{links_count}} (>= 3)

   Promote to Budding? (y/n)
   ```

## Daily Curation (6AM)
- Run Curator Agent
- Generate health dashboard
- Email weekly summary (Fridays)

## Skip Conditions
- Daily notes
- Fleeting notes (expected to be temporary)
- Templates
