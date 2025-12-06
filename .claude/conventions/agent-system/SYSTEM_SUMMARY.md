# Second-Brain Agent System - Final Summary

> **Ultra-compact format** with psychological techniques + strict role separation + 20+ year expert personas

## 🎯 System Architecture

### Design Principles
1. **발견되고** (Discoverable): Rich tags, clear titles, complete frontmatter
2. **연결되고** (Connected): Temporal hooks, context-rich links, bidirectional
3. **이해하기 쉽고** (Understandable): Clear structure, concrete examples, self-contained
4. **Strict Role Separation**: Zero overlap, zero violations
5. **Expert Level**: 20-26 years experience, proven track record
6. **Compact Format**: 90% less verbose, same power

---

## 📊 Agent Roster (11 Agents)

### Core Workflow Agents

| Agent | Role | Expert | Scope | Forbidden |
|-------|------|--------|-------|-----------|
| **Orchestrator** | Coordinate + enforce | 25y Eng Manager | Wave execution, boundary enforcement | create, link, score, refine |
| **Capture** | Atomic notes | 22y Knowledge Architect | Create notes, auto-tag, suggest location | move, link, score |
| **Curator** | PARA organization | 24y Librarian | Move to PARA, classify | create, link, score |
| **Link Manager** | Find connections | 23y Graph Engineer | Search, analyze, suggest | create links, add context |
| **Connection Curator** | Create [[links]] | 21y Network Specialist | Create links, add context, bidirectional | find candidates, search |
| **Quality Estimator** | Score 0-100 | 26y QA Director | 4-dimension scoring, identify issues | fix, create, link |
| **Refiner** | Fix issues | 20y Technical Editor | Enhance quality, iterate to 85+ | link, score, move |
| **Reviewer** | Final audit | 24y PKM Auditor | Pass/fail, report only | fix, create, link |

### Subject-Specific Agents

| Agent | Template | Expert | Output |
|-------|----------|--------|--------|
| **Project Agent** | project-note-template | 21y Project Doc Lead | Rich project notes |
| **Weekly Agent** | weekly-reflection-template | 20y Reflective Coach | Structured reflections |
| **Technical Agent** | technical-reference-template | 23y Technical Writer | Code examples + concepts |
| **Insight Agent** | insight-template | 22y Insights Researcher | Deep life learnings |

---

## 🔀 Workflow Pipeline

### Standard Flow (Create → Score → Refine → Link → Review)

```
User Request
  ↓
1. Orchestrator (analyze + assign)
  ↓
2. Subject Agent (Project/Weekly/Technical/Insight)
   - Fill template
   - Rich content
   - Output: note_path
  ↓
3. Quality Estimator
   - Score: Discoverability(30) + Connectability(30) + Understandability(25) + Template(15)
   - Decision: >= 85 (ready) OR < 85 (refine)
  ↓
4. IF score < 85: Refiner Agent (Cycle 1-3)
   - Fix: P1 critical → P2 discoverability → P3 connectability → P4 understandability
   - Re-score by Quality Estimator
   - Loop until >= 85 OR max 3 cycles
  ↓
5. Curator Agent (if wrong location)
   - Move to correct PARA folder
  ↓
6. Link Manager
   - Search 50+ candidates
   - Score: temporal(40%) + thematic(35%) + semantic(20%) + structural(5%)
   - Suggest top 10 pairs
  ↓
7. Connection Curator
   - Create [[links]] with 1-2 sentence context
   - Ensure bidirectional
   - Categorize (Project/Weekly/Knowledge/Insight)
  ↓
8. Reviewer (final audit)
   - Pass/fail
   - Quality report
  ↓
9. Orchestrator (report to user)
```

---

## 📐 Compact Format (YAML + Psychology)

### Agent Structure (25 lines avg)

```yaml
---
name: Agent Name
role: one_line_what_it_does
triggers: keyword1, keyword2, 한글
scope: ONLY_action1, ONLY_action2
forbidden: action1, action2
persona: {{years}}y {{title}} | {{expertise}} | {{track_record}}
stakes: Bad outcome → impact1 ($X), impact2 ($Y) | Total: $Z saved
challenge: I bet you can't {{difficult_task}}. Prove {{expertise_aspect}}.
goal: {{measurable_target}}
tools: [tool1, tool2]
model: claude-sonnet-4-5
---

# {{name}}

## Execute
1. Input: {{from_who}}
2. Process: {{algorithm}}
3. Output: {{what_produces}}
4. Handoff: {{next_agent}}

## Rules
✅ DO: {{action}}, {{action}}
❌ NEVER: {{violation}}, {{violation}}

## Quality Self-Check
- [ ] {{requirement}}

@{{convention}} ({{what_covers}})
```

**Size**: ~25 lines (was 350+ lines) = **93% reduction**

---

## 🎭 Psychological Techniques (Preserved)

### PERSONA (Expertise + Track Record)
```yaml
persona: 23y Knowledge Graph Engineer | Wikipedia/Google semantic systems, graph theory PhD | 95% precision track record
```
- **Years**: 20-26 years (proven expert)
- **Background**: Specific companies/projects
- **Achievement**: Quantified success

### STAKES (Financial + Impact)
```yaml
stakes: Bad suggestions → missed connections ($80), wasted time ($60), weak graph ($80) | Total: $220 saved if 95%+ accepted
```
- **Cost breakdown**: Specific impacts with $ amounts
- **Total value**: Clear ROI
- **Condition**: "if {{quality_achieved}}"

### CHALLENGE (Competitive Edge)
```yaml
challenge: I bet you can't find meaningful connections using ONLY algorithms. Prove algorithmic precision.
```
- **Bet framing**: "I bet you can't..."
- **Difficulty**: Highlight hard aspect
- **Proof demand**: "Prove {{expertise}}"

### GOAL (Measurable Target)
```yaml
goal: 95%+ suggestion acceptance rate (precision is everything)
```
- **Metric**: Specific number
- **Emphasis**: What matters most

---

## 🔒 Strict Role Boundaries

### Separation Matrix

| Task | Agent | Alternative Forbidden |
|------|-------|----------------------|
| Find link candidates | Link Manager | ❌ Connection Curator |
| Create [[links]] | Connection Curator | ❌ Link Manager |
| Score quality | Quality Estimator | ❌ Refiner, Reviewer |
| Fix issues | Refiner | ❌ Quality Estimator |
| Move files | Curator | ❌ Capture, Subject Agents |
| Create notes | Capture/Subject | ❌ All others |

### Enforcement (Orchestrator)

```python
def enforce_boundary(agent, action):
    if action not in agent.scope:
        raise Violation(f"{agent} attempted {action} (NOT IN SCOPE)")
    if action in agent.forbidden:
        raise Violation(f"{agent} attempted {action} (FORBIDDEN)")
    return "ALLOWED"
```

**Penalty**: Warning → Halt → Escalate

---

## 📁 Directory Structure

```
.claude/
├── agents-v2/                          # Compact agents (25 lines each)
│   ├── knowledge__link-manager.md      ✅ COMPACT
│   ├── knowledge__connection-curator.md ✅ COMPACT
│   ├── quality__estimator-agent.md    ✅ COMPACT
│   ├── quality__refiner-agent.md      ✅ COMPACT
│   └── [8 more agents]
├── conventions/                        # Table-driven conventions
│   └── knowledge/
│       ├── connection-quality.md       (table format, 20 lines)
│       ├── vault-structure.md          (table format, 30 lines)
│       └── capture-workflow.md         (checklist, 25 lines)
├── AGENT_ROLES.md                      # Strict separation matrix
├── COMPACT_FORMAT.md                   # Format specification
└── SYSTEM_SUMMARY.md                   # This file

99-Assets/Templates/                    # Rich templates
├── project-note-template.md
├── weekly-reflection-template.md
├── technical-reference-template.md
└── insight-template.md
```

---

## 🎯 Quality Loop (발견-연결-이해)

### Score Dimensions (Total: 100 points)

1. **Discoverability (30 pts)**
   - Title clarity (10): Specific vs generic
   - Tag richness (10): 5+ tags (tech + domain)
   - Frontmatter (10): All required fields

2. **Connectability (30 pts)**
   - Temporal hooks (12): Explicit dates
   - Tech specificity (10): Specific patterns vs generic
   - Context richness (8): Links with context

3. **Understandability (25 pts)**
   - Structure (10): Clear headers
   - Concreteness (10): Examples, metrics
   - Self-containment (5): Explains context

4. **Template Compliance (15 pts)**
   - Sections filled / required × 15

### Refinement Cycle (Max 3)

```
Score < 85 → Refiner (Cycle 1)
  ↓ fix P1 critical
Re-score by Estimator
  ↓
Still < 85? → Refiner (Cycle 2)
  ↓ fix P2-P3
Re-score by Estimator
  ↓
Still < 85? → Refiner (Cycle 3)
  ↓ fix P4 + polish
Re-score
  ↓
>= 85: Connection Curator
< 85: Escalate to human
```

**Target**: 95%+ notes reach 85+ within 2 cycles

---

## 🔗 Connection Quality (4-Step Principle)

| Step | Requirement | Bad | Good |
|------|-------------|-----|------|
| 1️⃣ READ | Read content | "[[Note]]" (blind) | Read frontmatter + content |
| 2️⃣ TIMELINE | Check dates | No temporal context | "Same week (2025-10-27)" |
| 3️⃣ COMPANY | Validate period | aivelabs ↔ qraft | Same company only |
| 4️⃣ CONTEXT | Add explanation | Bare link | "Used pattern, 30% faster" |

**Enforced by**: Link Manager (validation) + Connection Curator (execution)

---

## 📊 Success Metrics

### Agent Performance
- **Scope adherence**: 100% (zero violations)
- **Expert quality**: 95%+ user satisfaction
- **Handoff success**: 99%+ clean transitions

### Note Quality
- **85+ score rate**: 95%+ (within 2 refiner cycles)
- **Connection acceptance**: 95%+ (Link Manager precision)
- **Bidirectional consistency**: 100% (Connection Curator)
- **PARA compliance**: 98%+ (Curator Agent)

### System Efficiency
- **Token savings**: 90% (compact format vs verbose)
- **Creation to ready**: < 3 minutes (automated pipeline)
- **Vault health**: 98%+ (orphan rate < 1%)

---

## 🚀 Usage Examples

### Example 1: Create Project Note
```
User: "create project note for DataHub lineage work"

Orchestrator → Project Agent
  - Fill template: project-note-template.md
  - Output: 02-Areas/.../Projects/Active/DataHub-Lineage-구축.md

Project Agent → Quality Estimator
  - Score: 78/100 (missing temporal hooks, generic tech mentions)

Quality Estimator → Refiner (Cycle 1)
  - Add: dates (2025-10-15 ~ 2025-11-20)
  - Enhance: "DataHub" → "DataHub lineage extraction으로 100+ 테이블 관계 시각화"
  - Add: 3 tech tags

Refiner → Quality Estimator
  - Re-score: 87/100 ✅

Quality Estimator → Link Manager
  - Find: 8 candidates (same week projects, tech resources, weekly reflections)
  - Suggest: top 5 pairs with reasoning

Link Manager → Connection Curator
  - Create: 5 [[links]] with context
  - Example: "[[2025년-10월-27일]] - 프로젝트 진행 중 주간 회고, 거버넌스 필요성 깨달음"

Connection Curator → Reviewer
  - Audit: Pass (87/100, 5 connections, all bidirectional)

Result: High-quality discoverable note with meaningful connections
```

### Example 2: Weekly Reflection
```
User: "create weekly reflection for 2025-12-07"

Orchestrator → Weekly Agent
  - Fill: weekly-reflection-template.md
  - Parse: user input → structure
  - Output: 02-Areas/.../Experience/Weekly/2025/2025년-12월-07일.md

Weekly Agent → Quality Estimator
  - Score: 92/100 ✅ (ready!)

Quality Estimator → Link Manager
  - Find: this week's projects, insights, technical learning

Link Manager → Connection Curator
  - Create: temporal connections (this week's work)

Result: Structured reflection connected to week's activities
```

---

## 💡 Key Innovations

### 1. Link Manager ≠ Connection Curator (Separation!)
- **Link Manager**: ONLY find + suggest (algorithm)
- **Connection Curator**: ONLY create + add context (execution)
- **Why**: Analysis ≠ Writing (different skills)

### 2. Quality Loop (Score → Refine → Re-score)
- **Automatic**: No manual quality checking
- **Iterative**: Up to 3 cycles
- **Threshold**: 85+ required before connection

### 3. Compact Format (90% reduction)
- **YAML header**: All metadata + psychology
- **Body**: 3 sections (Execute, Rules, Reference)
- **Total**: 25 lines (was 350+)

### 4. Expert Personas (20+ years)
- **Not generic**: Specific background
- **Track record**: Quantified achievements
- **Stakes**: Financial impact ($150-250 saved)

### 5. Template System
- **4 templates**: Project, Weekly, Technical, Insight
- **Rich structure**: 15-20 sections each
- **Discoverable**: Built-in connection hooks

---

## 🎓 Next Steps

### Immediate
1. **Test pipeline**: Create 1 note end-to-end
2. **Validate quality loop**: Ensure 85+ reached
3. **Check boundaries**: Zero violations

### Short-term (1 week)
1. Migrate remaining agents to compact format
2. Refactor conventions to table-driven
3. Create more templates (Research, Meeting, etc.)

### Long-term (1 month)
1. Vault cleanup: Organize all migrated Notion content
2. Connection enhancement: Link all orphan notes
3. Quality improvement: All notes to 85+

---

**Last Updated**: 2025-12-07
**Format**: Ultra-Compact (YAML + Psychology)
**Agent Count**: 11 (strict separation)
**Token Efficiency**: 90% savings
**Quality Target**: 95%+ notes at 85+ score
