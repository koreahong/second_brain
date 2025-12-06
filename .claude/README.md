# Second-Brain Agent System

> Knowledge management agents based on qraft_data_platform architecture

## 📋 Overview

This agent system automates knowledge capture, curation, connection, and review workflows following PARA + Zettelkasten methodology.

**Inspired by**: `qraft_data_platform/.claude/` architecture
- Specialized agents with clear responsibilities
- Convention-Agent separation (agents read conventions, not duplicate)
- Orchestrator coordinates multi-step workflows
- Dynamic agent discovery (no hardcoding)

## 🤖 Agent Architecture

### Orchestrator Pattern

```
User Request
    ↓
Orchestrator (analyzes request)
    ↓
┌─────────────┬─────────────┬─────────────┐
│  Wave 1     │  Wave 2     │  Wave 3     │
│  (Parallel) │  (Depends)  │  (Validate) │
└─────────────┴─────────────┴─────────────┘
    ↓
Integrated Report
```

**Key Principles**:
1. **Pure Orchestration**: Never executes directly, only coordinates
2. **Wave Execution**: Parallel when possible, sequential when dependencies exist
3. **Dynamic Discovery**: Glob + Read agents at runtime (no hardcoding)
4. **Minimal Context**: Each agent receives only necessary information

## 📁 Directory Structure

```
.claude/
├── agents/                              # Specialist agents
│   ├── orchestrator.md                 # Multi-agent coordinator
│   ├── knowledge__capture-agent.md     # Note capture & tagging
│   ├── knowledge__connection-curator.md # Meaningful connections
│   ├── knowledge__curator-agent.md     # PARA organization
│   └── knowledge__reviewer-agent.md    # Quality validation
├── conventions/                         # Shared knowledge
│   └── knowledge/
│       ├── vault-structure.md          # PARA + Zettelkasten
│       ├── connection-quality.md       # 4-step principle
│       └── capture-workflow.md         # Frontmatter, atomicity
├── hooks/                              # Automation triggers
│   └── file-change-hook.md            # Suggest on file change
└── CLAUDE.md                           # Main configuration
```

## 🎯 Specialist Agents

### 1. Capture Agent
**Purpose**: Atomic note creation with proper metadata

**Triggers**: "capture note", "save thought", "캡처"

**Workflow**:
```
User Input
  ↓
Analyze content (type, keywords, tech)
  ↓
Generate frontmatter (tags, company, status)
  ↓
Create atomic note (200-500 words)
  ↓
Suggest location (not moved yet)
  ↓
Suggest connections (not created yet)
```

**Key Features**:
- Auto-detect technology tags (#airflow, #dbt)
- Auto-detect company period (aivelabs/qraft)
- Generate complete frontmatter
- Atomic note principle (one concept = one note)
- **NEVER** creates connections or moves files

**Convention**: `conventions/knowledge/capture-workflow.md`

### 2. Connection Curator
**Purpose**: Create meaningful temporal and thematic connections

**Triggers**: "connect notes", "create links", "백링크"

**Workflow (4-Step Principle)**:
```
1️⃣ READ FIRST
   - Read actual content (not just titles!)
   - Extract dates, company, context

2️⃣ CHECK TIMELINE
   - Find same week/month notes
   - Search temporal candidates

3️⃣ COMPANY PERIOD
   - aivelabs ↔ qraft separation (strict!)
   - No cross-period links

4️⃣ ADD CONTEXT
   - 1-2 sentence explanation
   - Categorized sections (Project/Weekly/Knowledge/Insight)
   - Bidirectional links
```

**Key Features**:
- Temporal priority (same week > same month > same quarter)
- Company period validation (aivelabs vs qraft)
- Context-rich connections (no bare links!)
- Bidirectional consistency
- **NEVER** captures notes or reorganizes vault

**Convention**: `conventions/knowledge/connection-quality.md`

### 3. Curator Agent
**Purpose**: Organize vault into PARA structure

**Triggers**: "organize vault", "curate", "PARA", "정리"

**Workflow**:
```
Analyze current location
  ↓
Read frontmatter (type, status, tags)
  ↓
Classify target location
  - project → Projects/ (by status)
  - reflection → Experience/Weekly/ (by year)
  - reference → Resources/ (by tech)
  - insight → Life-Insights/ (by context)
  ↓
Move note to PARA location
  ↓
Update frontmatter (updated date)
  ↓
Detect orphans (no connections)
```

**Key Features**:
- Bulk migration (업무리스트 → Projects/)
- Type-based classification
- Tag-based sub-folder (Airflow/, DBT/)
- Orphan detection
- **NEVER** creates notes or connections

**Convention**: `conventions/knowledge/vault-structure.md`

### 4. Reviewer Agent
**Purpose**: Validate note quality and vault health

**Triggers**: "review note", "validate quality", "검증"

**Workflow**:
```
Read note content
  ↓
Calculate quality score (0-100):
  - Frontmatter completeness (20 pts)
  - Connection quality (30 pts)
  - Content atomicity (20 pts)
  - PARA compliance (15 pts)
  - Tag relevance (15 pts)
  ↓
Validate each connection:
  - Content read? (not just keyword match)
  - Temporal relationship?
  - Company period consistent?
  - Context explanation?
  - Bidirectional?
  ↓
Detect orphans
  ↓
Generate report
```

**Key Features**:
- Multi-dimensional scoring
- Connection validation (4-step principle check)
- Orphan detection with suggestions
- Vault health metrics
- **NEVER** auto-fixes (report only)

**Convention**: `conventions/knowledge/connection-quality.md`

### 5. Orchestrator
**Purpose**: Coordinate multi-agent workflows

**Triggers**: "capture and organize", "migrate all", "full review"

**Workflow**:
```
1. Dynamic Agent Discovery
   Glob: .claude/agents/*.md
   Read: frontmatter of each agent
   Build: agents_map dynamically

2. Task Decomposition
   Analyze user request
   Match keywords to agents
   Identify dependencies

3. Wave Planning
   Wave 1: Independent tasks (parallel)
   Wave 2: Dependent tasks (sequential)
   Wave 3: Final validation

4. Execute Waves
   Task tool → each agent
   Collect results

5. Integrate Results
   Synthesize reports
   Provide unified output
```

**Key Features**:
- Zero hardcoding (dynamic discovery!)
- Parallel execution when possible
- Minimal context handoff
- Token efficiency (~60% savings vs manual)

**Convention**: All conventions (reads as needed)

## 📚 Conventions (Single Source of Truth)

### vault-structure.md
**Purpose**: PARA + Zettelkasten folder rules

**Key Sections**:
- PARA structure definition
- Folder placement rules (type → location)
- Frontmatter requirements
- Connection structure templates
- Migration patterns (Notion → Obsidian)

**Used by**: All agents

### connection-quality.md
**Purpose**: 4-step connection principle

**Key Sections**:
- READ FIRST (content, not titles!)
- CHECK TIMELINE (temporal priority)
- COMPANY PERIOD (aivelabs ↔ qraft separation)
- ADD CONTEXT (explanations, categories)
- Quality scoring criteria
- Validation checklist

**Used by**: Connection Curator, Reviewer

### capture-workflow.md
**Purpose**: Atomic note creation

**Key Sections**:
- Atomic note principle (200-500 words)
- Frontmatter template (required fields)
- Auto-tag strategy (tech, domain, company)
- Location suggestion logic
- Note structure templates (by type)

**Used by**: Capture Agent

## 🔄 Common Workflows

### Quick Capture
```bash
User: "capture this DataHub insight"

→ Capture Agent
  - Create note with frontmatter
  - Auto-tag: #datahub, #data-governance, #qraft
  - Suggest: 03-Resources/Technology/DataHub/
  - Suggest connections (not created)

Output: Draft note + suggestions
```

### Full Organization
```bash
User: "organize all migrated content"

→ Orchestrator
  Wave 1: Curator (bulk)
    - 업무리스트 → Projects/ (46 files)
    - 회고록 → Experience/Weekly/ (15 files)
    - 레퍼런스 → Resources/ (238 files)
    - 본깨적 → Life-Insights/ (229 files)

  Wave 2: Connection Curator
    - Temporal links (same week)
    - Project chains (Project → Knowledge → Insight)
    - Company validation (aivelabs ↔ qraft)

  Wave 3: Reviewer
    - Quality scores
    - Orphan detection
    - PARA compliance

Output: Organized vault + quality report
```

### Connection Enhancement
```bash
User: "find and connect orphan notes"

→ Orchestrator
  Wave 1: Reviewer (orphan detection)
    - Find notes without connections
    - Search temporal candidates
    - Search thematic candidates

  Wave 2: Connection Curator
    - Read actual content
    - Validate relationships
    - Create contextualized links

  Wave 3: Reviewer (validation)
    - Check connection quality
    - Calculate improvement score

Output: Enhanced connections + metrics
```

### Weekly Review
```bash
User: "weekly knowledge review"

→ Orchestrator
  Wave 1 (parallel):
    - Reviewer: Vault health
    - Connection Curator: This week's notes

  Wave 2: Connection Curator
    - Link weekly notes to projects
    - Link insights to reflections

  Wave 3: Reviewer
    - Quality report
    - Action items

Output: Weekly health report
```

## 🎨 Vault Structure (PARA + Zettelkasten)

```
Second-Brain/
├── 02-Areas/                        # Long-term interests
│   └── 크래프트테크놀로지스/
│       ├── Projects/
│       │   ├── Active/             # In progress
│       │   ├── Completed/          # Done
│       │   └── Archived/           # Cancelled/old
│       ├── Experience/
│       │   └── Weekly/             # Weekly reflections
│       │       ├── 2024/
│       │       └── 2025/
│       └── Achievements/           # Results
├── 03-Resources/                    # Reference knowledge
│   ├── DAE/                        # DAE role/scope
│   ├── Data-Governance/
│   ├── Technology/
│   │   ├── Airflow/
│   │   ├── DBT/
│   │   ├── DataHub/
│   │   └── [tech]/
│   └── Methodologies/
├── 10-Zettelkasten/                # Atomic knowledge
│   ├── Permanent/                  # Concepts
│   └── Literature/                 # Reference summaries
└── 30-Flow/                        # Life insights
    └── Life-Insights/
        ├── Work/
        ├── Personal/
        └── Observations/
```

## 🔧 Agent Naming Convention

**Pattern**: `{category}__{agent-name}.md`

**Categories**:
- `knowledge__`: Knowledge management (capture, curate, connect, review)
- `airflow__`: Airflow-specific (future: DAG validation)
- `dbt__`: DBT-specific (future: model validation)
- `infra__`: Infrastructure tools (future: git, jira agents)

**Why?**
- Clear categorization
- Easy Glob filtering: `knowledge__*.md`
- Consistent with qraft_data_platform pattern

## 📊 Comparison: qraft_data_platform vs Second-Brain

| Aspect | qraft_data_platform | Second-Brain |
|--------|---------------------|--------------|
| **Purpose** | Code quality & data platform | Knowledge management |
| **Agents** | 17 agents (Airflow, DBT, Quality, Infra) | 5 agents (Capture, Curate, Connect, Review, Orchestrator) |
| **Conventions** | airflow/, dbt/, quality/, infrastructure/ | knowledge/ only |
| **Orchestrator** | Multi-domain coordination | Knowledge workflow coordination |
| **Pattern** | Convention-Agent separation | Same (borrowed!) |
| **Discovery** | Dynamic (Glob + Read) | Same (borrowed!) |
| **Wave Execution** | Parallel/Sequential | Same (borrowed!) |
| **Tools** | Bash, Read, Write, Grep, MCP (GitLab, Jira) | Obsidian MCP, Read, Glob |

**Shared Infrastructure** (`~/claude-shared/`):
- `conventions/quality/security.md` (both use)
- `conventions/infrastructure/git-workflow.md` (both use)

## 🚀 Usage Examples

### Example 1: Capture Daily Insight
```
User: "capture this insight: DataHub lineage helps identify data ownership"

→ Capture Agent executes

Output:
✅ Note captured

Title: DataHub-Lineage-데이터-소유권-식별
Location: 03-Resources/Technology/DataHub/ (suggested)
Tags: #datahub, #data-governance, #lineage, #qraft
Company: qraft

Suggested connections:
- [[팀별-원천-데이터-계약현황-파악]] (related project)
- [[2025년-12월-07일]] (this week's reflection)

Next steps:
1. Review location (Curator can move)
2. Create connections (Connection Curator)
3. Validate quality (Reviewer)
```

### Example 2: Organize Temporary Folder
```
User: "organize 업무리스트 folder"

→ Orchestrator coordinates

Wave 1: Curator Agent
- Analyzed 46 notes
- Moved by status:
  - Active: 12 → Projects/Active/
  - Completed: 28 → Projects/Completed/
  - Archived: 6 → Projects/Archived/

Wave 2: Connection Curator
- Created 87 temporal connections (same week)
- Created 54 thematic connections (same tech)
- Validated company periods (all qraft)

Wave 3: Reviewer
- Avg quality: 85/100
- Orphans: 3 notes (need review)
- PARA compliance: 100%

Output: 46 notes organized, 141 connections created
```

### Example 3: Weekly Review
```
User: "review this week's knowledge"

→ Orchestrator coordinates

Wave 1 (parallel):
- Reviewer: Vault health check
- Connection Curator: This week's notes (5 notes)

Wave 2: Connection Curator
- Linked 5 notes to projects
- Linked 2 insights to weekly reflection
- Created temporal chains

Wave 3: Reviewer
- Weekly quality: 92/100
- New connections: 12
- Orphans: 0

Output:
📊 Weekly Knowledge Report

Activity: 5 new notes
Quality: 92/100 (↑5 from last week)
Connections: 12 new
Projects: 2 active, 1 completed

Highlights:
- [[DataHub-구축-프로젝트]] completed
- [[데이터-거버넌스의-중요성]] insight created
- All notes connected (zero orphans!)
```

## 🛠️ Advanced: Custom Agent Creation

Want to add a new agent? Follow qraft_data_platform pattern:

### 1. Create Agent File
```markdown
---
name: My Custom Agent
description: |
  What it does. Auto-trigger when:

  **Triggers**: keyword1, keyword2, 키워드
  **Scope**: What it does
  **Forbidden**: What it doesn't (delegate to other agents)

  Persona: Senior X (Ny, expertise)
  Stakes: Bad outcome → impact ($Z saved)
  Goal: Measurable outcome
tools: [list, of, tools]
model: claude-sonnet-4-5
---

# My Custom Agent

## Convention
[Reference convention files]

## Workflow
[3-5 steps max]

## Best Practices
[Do's and don'ts]
```

### 2. Create Convention (if needed)
```markdown
# My Convention

> Update rule: What to add, keep concise

Convention content...
```

### 3. Update CLAUDE.md
Add to agent list:
```markdown
**My Custom Agent** (`.claude/agents/my-custom-agent.md`)
- **Triggers**: keyword1, keyword2
- **Scope**: What it does
- **Forbidden**: What it doesn't
```

### 4. Test Dynamic Discovery
```bash
# Orchestrator will auto-discover via:
Glob: .claude/agents/*.md
Read: .claude/agents/my-custom-agent.md

# No code changes needed!
```

## 🎯 Key Innovations (vs Manual Workflow)

### 1. Dynamic Agent Discovery
**Before** (Manual):
```python
# Hardcoded agent list
agents = ["capture", "curator", "reviewer"]  # Breaks when adding new agent
```

**After** (Dynamic):
```python
# Auto-discover at runtime
agents = Glob(".claude/agents/*.md")  # New agents auto-recognized!
```

### 2. Convention-Agent Separation
**Before** (Duplication):
```markdown
# capture-agent.md (500 lines)
- Frontmatter rules (200 lines)
- Tagging strategy (150 lines)
- ...

# curator-agent.md (500 lines)
- Frontmatter rules (200 lines)  ← DUPLICATED!
- ...
```

**After** (Single Source):
```markdown
# capture-agent.md (150 lines)
Convention: @capture-workflow.md

# curator-agent.md (150 lines)
Convention: @vault-structure.md

# conventions/capture-workflow.md (200 lines)
Frontmatter rules (shared by all agents)
```

### 3. Wave Execution
**Before** (Sequential):
```
Task 1 → Task 2 → Task 3 → Task 4
(Total: 4 x 30s = 120s)
```

**After** (Parallel Waves):
```
Wave 1: Task 1 ║ Task 2 ║ Task 3 (parallel)
Wave 2: Task 4 (depends on 1-3)
(Total: 30s + 30s = 60s, 50% faster!)
```

### 4. Token Efficiency
**Before** (Manual):
```
Read all conventions → Context: 10,000 tokens
Execute task → Output: 5,000 tokens
Total: 15,000 tokens
```

**After** (Lazy Load):
```
Read only needed convention → Context: 2,000 tokens
Agent executes → Output: 5,000 tokens
Total: 7,000 tokens (53% savings!)
```

## 📈 Success Metrics

### Vault Health
- **Connection Quality**: Target 95%+ (temporal + contextual)
- **Orphan Rate**: Target < 1% (notes without connections)
- **PARA Compliance**: Target 100% (notes in correct locations)
- **Frontmatter Completeness**: Target 100% (all required fields)

### Agent Performance
- **Capture**: 100% of thoughts captured (zero lost insights)
- **Connection**: 95%+ meaningful connections (not surface-level)
- **Organization**: 100% PARA compliance (correct locations)
- **Review**: Quality score > 90/100 (vault health)

### Efficiency
- **Token Savings**: 60% vs manual (convention lazy-loading)
- **Time Savings**: 50% via parallel waves
- **Maintenance**: Zero hardcoded agents (dynamic discovery)

## 🔍 Troubleshooting

### Agent Not Triggering?
```bash
# Check trigger keywords in YAML frontmatter
Read: .claude/agents/{agent}.md (first 20 lines)

# Verify Orchestrator can discover
Glob: .claude/agents/*.md
```

### Connection Quality Low?
```bash
# Run Reviewer to diagnose
User: "review note quality"

# Check 4-step principle compliance
→ Content read? (not just keywords)
→ Temporal context? (same week/month)
→ Company period? (aivelabs ↔ qraft)
→ Context explanation? (1-2 sentences)
```

### PARA Compliance Issues?
```bash
# Check frontmatter
→ type field set? (project|reflection|reference|insight|concept)
→ status field set? (draft|active|completed|archived)

# Run Curator to fix
User: "organize misplaced notes"
```

## 📚 References

### qraft_data_platform (Source Pattern)
- `/Users/qraft_hongjinyoung/qraft_data_platform/.claude/`
- Orchestrator pattern
- Convention-Agent separation
- Dynamic discovery via Glob + Read

### Shared Conventions (Global)
- `~/claude-shared/conventions/quality/security.md`
- `~/claude-shared/conventions/infrastructure/git-workflow.md`

### Documentation
- [CLAUDE.md](./../CLAUDE.md) - Main configuration
- [vault-structure.md](conventions/knowledge/vault-structure.md) - PARA guide
- [connection-quality.md](conventions/knowledge/connection-quality.md) - 4-step principle
- [capture-workflow.md](conventions/knowledge/capture-workflow.md) - Atomic notes

---

**Last Updated**: 2025-12-07
**Claude Code Version**: Claude Sonnet 4.5
**Architecture**: Based on qraft_data_platform agent system
