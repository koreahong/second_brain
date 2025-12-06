---
notion_id: 2c1c6d43-3b4d-80df-817c-c1e003918219
content_type: Article
created: "2025-12-06T17:45:00.000Z"
updated: "2025-12-06T17:49:00.000Z"
company: MEDIUM
period: 2025-12-07
category:
  - Reading
---

# Untitled

https://medium.com/@alirezarezvani/building-an-infinite-memory-engine-pixeltable-claude-code-for-context-aware-ai-development-cf683532475d

Disclosure: I used AI tools to help refine and structure this content. The insights and code examples are from my direct work experience or my own research and investigational work.

You’re debugging a production issue at 2 AM. You ask Claude Code for help. It suggests a fix that breaks authentication — because it doesn’t know you refactored that system last week.

You re-explain the architecture. Again. For the third time this month.

Sound familiar? According to Stack Overflow’s survey of over 90,000 developers, 66% say the most common frustration with AI assistants is that the code is “almost right, but not quite.” The brutal truth: conversations stop when context fills up, forcing you to start over and re-explain everything.

Introduction - Pixeltable DocumentationPixeltable is a declarative data infrastructure for building multimodal AI applications, enabling incremental storage…
docs.pixeltable.com

You’re not building with AI. You’re babysitting it.

But what if your AI coding assistant had perfect recall of every architectural decision, every failed experiment, every production incident — across sessions, across teammates, across months? What if it got smarter over time instead of dumber with every new chat?

That’s not a pipe dream. It’s what happens when you stop treating context as temporary input and start treating it as persistent infrastructure.

# The Context Chaos Problem

Let’s be honest about why current approaches fail.

Brittle RAG hacks are the first problem. You’ve probably tried this: spin up a vector database, write some scripts to chunk your codebase, generate embeddings, and hope for the best. It works… until it doesn’t. Code changes but your index doesn’t. You manually re-run scripts. You maintain three separate systems — vector DB, file storage, and orchestration scripts — just to answer “where did we implement rate limiting?”

A recent study found that 65% of developers report AI misses critical context during refactoring. That’s not because the AI is dumb. It’s because your context infrastructure is fragile.

Overstuffed context windows are even worse. Sure, Claude Opus 4.1 or Claude Sonnet 4.5 has a 200K token window. But developers consistently hit practical limits around 6,400–8,000 tokens despite advertised windows — because models perform hidden reasoning steps before generating responses. More context doesn’t mean better results. It means a distracted model that misses what actually matters.

Then there’s the lost decisions problem. Architecture decisions, past failures, and project context vanish across new chat sessions. Team knowledge gets siloed in individual conversations. There’s no audit trail of “why we chose this approach” six months later when everyone’s confused about the weird caching layer.

The fundamental problem? Current tools treat context as temporary input. We need context as persistent infrastructure.

# Rethinking Context: From Retrieval to Infrastructure

Here’s the mental model shift that changes everything.

Instead of asking “how do I feed my codebase to AI?”, ask “how do I build a queryable memory layer that grows smarter over time?”

This is where Pixeltable + Claude Code becomes interesting. Pixeltable acts as your persistent multimodal memory layer — storing code, docs, meeting recordings, design artifacts, and production logs. Claude Code sits on top as the agentic reasoning layer, querying that memory via the Model Context Protocol.

Together, they form a context engine with infinite recall.

Why does this matter? Because context isn’t retrieved on-demand anymore — it’s always available. Not just code, but multimodal: video demos, meeting transcripts, Figma mockups, incident logs. Pixeltable provides versioned, auditable storage with automatic lineage tracking — you know who decided what, when, and with which model.

Most importantly, it’s incremental. Changes to your data automatically trigger recomputation of embeddings and summaries. No manual re-indexing. No stale context. No maintaining three separate systems.

Stop Copy-Pasting Claude Code Instructions: I Tried Generating Perfect CLAUDE.mdOpen-source tool that generates customized CLAUDE.md files for Claude Code projects. Interactive setup, validation, and…
alirezarezvani.medium.com

# Architecture: Building the Memory Layer

Let’s get concrete. Here’s what this actually looks like.

The high-level architecture is straightforward: Pixeltable stores your knowledge as tables with computed columns. Claude Code queries those tables via MCP tools.

```plain text
import pixeltable as pxt
```

```plain text
# Create your knowledge base table
kb = pxt.create_table('knowledge_base', {
    'source_type': pxt.StringType(),    # code, doc, meeting, log, decision
    'path': pxt.StringType(),           # file path or URL
    'content': pxt.DocumentType(),      # multimodal content
    'created_at': pxt.TimestampType(),
    'metadata': pxt.JsonType()          # tags, owners, service, domain
})
```

This table is your memory. Everything goes here — code files, README docs, meeting transcripts, design screenshots, incident reports. The magic happens with computed columns.

```plain text
from pixeltable.functions import openai, huggingface
```

```plain text
# Auto-generate summaries on insert/update
kb.add_computed_column(
    summary=openai.chat_completions(
        model='gpt-4o-mini',
        messages=[{
            'role': 'user',
            'content': f'Summarize this concisely: {kb.content}'
        }]
    )
)# Auto-generate embeddings for semantic search
embed_model = huggingface.sentence_transformer.using(
    model_id='all-MiniLM-L6-v2'
)
kb.add_embedding_index('content', string_embed=embed_model)
```

Computed columns run automatically on new and updated data — define the transformation once, and it runs forever. Insert a new ADR document? Pixeltable generates the summary and embeddings automatically. Update code after a refactor? Embeddings refresh. No cron jobs. No manual pipeline orchestration.

# Connecting Your Codebase

Here’s how you ingest repositories with meaningful context:

```plain text
for service in ['auth-service', 'api-gateway', 'payment-processor']:
    repo_path = f'/repos/{service}'

    for file_path in get_code_files(repo_path):
        with open(file_path) as f:
            kb.insert([{
                'source_type': 'code',
                'path': file_path,
                'content': f.read(),
                'metadata': {
                    'service': service,
                    'language': detect_language(file_path),
                    'last_modified': get_mtime(file_path)
                }
            }])
```

Use .gitignore patterns to filter out build artifacts and dependencies—you want signal, not noise. Tag everything by service and domain so you can do filtered retrieval later.

You can track architectural decisions with computed columns:

```plain text
# Automatically identify and tag ADRs
kb.add_computed_column(
    is_adr=(kb.path.str_contains('ADR') |
            kb.path.str_contains('decision') |
            kb.content.str_contains('## Decision'))
)
```

The beauty of Pixeltable’s approach: transformations are embedded declaratively. Updates propagate automatically when your data changes.

From Assistant to Autonomous Engineer: The 9-Month Technical Evolution of Claude Code
alirezarezvani.medium.com

# Beyond Code: Multimodal Context

Code alone isn’t enough. Decisions happen in meetings. Requirements live in Figma. Bugs hide in production logs.

Meeting recordings are gold mines of context that usually evaporate:

```plain text
meetings = pxt.create_table('meetings', {
    'recording': pxt.VideoType(),
    'title': pxt.StringType(),
    'date': pxt.TimestampType(),
    'attendees': pxt.JsonType()
})
```

```plain text
# Auto-transcribe with Whisper
meetings.add_computed_column(
    transcript=openai.audio_transcriptions(
        model='whisper-1',
        audio=meetings.recording
    )
)# Extract action items automatically
meetings.add_computed_column(
    action_items=openai.chat_completions(
        model='gpt-4o-mini',
        messages=[{
            'role': 'user',
            'content': f'Extract action items from: {meetings.transcript}'
        }]
    )
)
```

Now when Claude Code helps refactor your authentication layer, it can reference the security team meeting from last month where you discussed session token requirements.

I Gave Claude Code 2.0 Our 3-Week Refactor at 11 PM. At 7 AM, It Was Done.What happened next will change how you think about AI development — and I’m challenging you to prove me wrong in 7…
alirezarezvani.medium.com

Design artifacts work the same way:

```plain text
designs = pxt.create_table('designs', {
    'image': pxt.ImageType(),
    'design_url': pxt.StringType(),
    'feature': pxt.StringType()
})
```

```plain text
# Extract visual context with GPT-4 Vision
designs.add_computed_column(
    description=openai.vision(
        prompt="Describe this UI design: layout, components, interactions",
        image=designs.image,
        model='gpt-4o-mini'
    )
)
```

Pixeltable natively handles images, videos, audio, and documents without separate storage systems. Everything is queryable in one unified interface.

# Connecting Claude Code via MCP

Here’s where it all comes together. Create an MCP server that exposes your Pixeltable memory to Claude Code:

```plain text
# pixeltable_mcp.py
from mcp import Server, Tool
import pixeltable as pxt

class PixeltableContext(Server):
    def __init__(self):
        self.kb = pxt.get_table('knowledge_base')

    @Tool(name="search_context")
    def search_knowledge_base(self, query: str, top_k: int = 5):
        """Semantic search across all context"""
        sim = self.kb.content.similarity(query)
        matches = (
            self.kb.order_by(sim, asc=False)
            .select(
                self.kb.source_type,
                self.kb.path,
                self.kb.summary,
                self.kb.metadata,
                score=sim
            )
            .limit(top_k)
        )
        return [dict(row) for row in matches]

    @Tool(name="search_by_service")
    def search_service_context(self, service: str, query: str):
        """Search within specific service context"""
        service_context = self.kb.where(
            self.kb.metadata['service'] == service
        )
        sim = service_context.content.similarity(query)
        return list(service_context.order_by(sim, asc=False).limit(5))
```

Configure Claude Code:

```plain text
claude mcp add pixeltable-context \
  --scope project \
  -- python pixeltable_mcp.py
```

Now watch what happens:

```plain text
You: I need to refactor the authentication service to support OAuth
```

```plain text
Claude Code calls:search_context("authentication OAuth refactor")Returns:
  - ADR-012: Why we chose session tokens over JWT (March 2024)
  - Incident: Auth bypass due to missing expiry check (Nov 2024)
  - Meeting transcript: Security team OAuth requirementsClaude Code: "Based on your ADR from March and the critical incident
in November, here's a safe OAuth approach that preserves the session
token validation layer..."
```

The context is grounded in your actual history. Not hallucinated. Retrieved and attributed.

# Governance and Auditability

If you’re building anything that matters — regulated industries, enterprise systems, compliance requirements — auditability isn’t optional.

Pixeltable’s lineage tracking shows exactly who changed what, when, and with which model. Every AI-generated change is traceable to the source context that influenced it.

```plain text
# Snapshot before major refactor
pxt.snapshot('knowledge_base',
             name='pre-auth-refactor',
             tags=['v2.0', 'stable'])

# Roll back if needed
pxt.restore('knowledge_base', snapshot='pre-auth-refactor')
```

For teams with sensitive data, implement access control through filtered views:

```plain text
# Engineers only see approved documentation
engineer_view = kb.where(
    (kb.metadata['approved'] == True) &
    (kb.metadata['classification'] != 'confidential')
)
```

This level of lineage tracking is crucial for healthcare, finance, and other regulated industries where traceability is mandatory.

# Getting Started

Here’s a minimal implementation you can run in 30 minutes:

```plain text
import pixeltable as pxt
import os

# 1. Create knowledge base
kb = pxt.create_table('knowledge_base', {
    'source_type': pxt.StringType(),
    'path': pxt.StringType(),
    'content': pxt.StringType(),
    'metadata': pxt.JsonType()
})
# 2. Add embeddings
from pixeltable.functions.huggingface import sentence_transformer
embed_model = sentence_transformer.using(model_id='all-MiniLM-L6-v2')
kb.add_embedding_index('content', string_embed=embed_model)
# 3. Ingest your first repo
extensions = {'.py', '.js', '.ts', '.md'}
for root, _, files in os.walk('/path/to/repo'):
    if 'node_modules' in root or '__pycache__' in root:
        continue

    for file in files:
        if any(file.endswith(ext) for ext in extensions):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                kb.insert([{
                    'source_type': 'code',
                    'path': file_path,
                    'content': f.read(),
                    'metadata': {'language': file.split('.')[-1]}
                }])
# 4. Query your context
query = "How do we handle authentication?"
sim = kb.content.similarity(query)
results = kb.order_by(sim, asc=False).limit(5)
for row in results:
    print(f"{row['path']}: {row['content'][:150]}...")
```

Phased rollout:

- Week 1: Ingest your most problematic service
- Week 2: Add meeting transcripts and ADRs
- Week 3: Connect Claude Code via MCP
- Week 4: Expand to full organizational memory
Teams report 70%+ reduction in processing costs through incremental updates. You only compute embeddings once per content change — not on every query.

# What Changes

Before: You’re explaining the same architecture for the third time this week. Claude Code suggests refactoring the caching layer without knowing you already tried that approach and it caused a production outage.

After: Claude Code queries your context engine. It finds the incident report from the failed caching refactor, the ADR explaining why you chose the current approach, and the meeting transcript where the team discussed tradeoffs. Its suggestion accounts for all of that history.

The AI doesn’t just answer faster. It gets smarter over time. Every incident documented, every decision recorded, every experiment logged makes the next interaction better.

Pixeltable + Claude Code isn’t just improved RAG. It’s infrastructure for infinite memory — multimodal, versioned, auditable, and team-wide. Context that compounds instead of evaporating.

GitHub - pixeltable/pixeltable: Pixeltable - Data Infrastructure providing a declarative…Pixeltable - Data Infrastructure providing a declarative, incremental approach for multimodal AI workloads. …
github.com

