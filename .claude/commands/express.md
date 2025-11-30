Activate the Express Agent from `.claude/agents/express-agent.md`.

Request: {{user_message_after_command}}

Expected format: `[topic] as [type]`
Types: blog, doc, presentation, report

Workflow:
1. Collect related notes
2. Propose outline
3. Generate draft
4. Review & improve
5. Capture new insights

Create output in `30-Flow/Drafts/`.
