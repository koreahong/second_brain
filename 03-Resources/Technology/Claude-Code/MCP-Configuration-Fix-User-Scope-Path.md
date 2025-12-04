---
tags:
  - claude-code
  - mcp
  - configuration
  - infrastructure
created: 2025-12-01
updated: 2025-12-01
status: Active
---

# Claude Code MCP Configuration Fix - User Scope Path

## Issue Discovered

When setting up common MCP servers to work across all projects, the configuration was placed at:
- **Wrong path**: `~/.claude-code/mcp.json` ❌

But Claude Code doesn't load from this location. The configuration was not being detected in other projects.

## Root Cause

Claude Code uses a **three-tier configuration hierarchy**:

```
Tier 1: Enterprise Policies (managed, highest priority)
Tier 2: Project Scope (./.mcp.json in project root)
Tier 3: User Scope (~/.claude/ directory, lowest priority)
```

The issue: `~/.claude-code/` is **not** part of Claude Code's official configuration discovery paths.

## The Correct Solution

Move the common MCP configuration to the **correct user scope path**:

```bash
# From (wrong location):
~/.claude-code/mcp.json

# To (correct location):
~/.claude/mcp.json
```

### Step-by-step Fix

```bash
# 1. Create the correct directory if it doesn't exist
mkdir -p ~/.claude

# 2. Move the file
mv ~/.claude-code/mcp.json ~/.claude/mcp.json

# 3. Verify
ls -la ~/.claude/mcp.json
```

## Configuration Hierarchy Explained

### User Scope: `~/.claude/mcp.json`
- Applies to **all projects** automatically
- Contains common/shared MCP servers
- Example: obsidian, notion, context7

### Project Scope: `./.mcp.json`
- Applies to **single project** only
- Contains project-specific MCP servers
- Example: datahub (Second-Brain only)

### Loading Behavior
- Project `.mcp.json` **extends** user scope (not replaces)
- Allows shared MCP servers + project-specific overrides
- No duplication needed across projects

## Current Setup (Before Fix)

```
~/.claude-code/mcp.json                  (NOT loaded ❌)
├── obsidian
├── notion
└── context7

Second-Brain/.mcp.json                   (Loaded ✅)
└── datahub
```

Other projects: Can't see common MCPs because they're in wrong directory

## Intended Setup (After Fix)

```
~/.claude/mcp.json                       (Loaded automatically ✅)
├── obsidian
├── notion
└── context7

Second-Brain/.mcp.json                   (Loads + extends ✅)
└── datahub

qraft_data_platform/.mcp.json            (Any other project)
└── [project-specific MCPs]
```

## Official Documentation

- Claude Code MCP Documentation: https://code.claude.com/docs/en/mcp.md
- Claude Code Settings & Configuration: https://code.claude.com/docs/en/settings.md

## Verification

After moving the file, verify Claude Code sees all MCPs:

```bash
claude /doctor
```

Or open Claude Code in a different project and confirm that obsidian, notion, context7 MCPs are available.

---

**Status**: Ready to implement
**Updated**: 2025-12-01
