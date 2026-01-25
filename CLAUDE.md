# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Claude Code Skills repository** - a collection of modular, self-contained packages that extend Claude's capabilities for content production, product management, and knowledge extraction. Skills are invoked using the `/skill-name` syntax and execute specialized workflows autonomously.

**Key Architecture Principles:**
- All skills are stored in this directory and symlinked to `~/.claude/skills/` for global access
- Skills follow a "silent execution protocol" - they complete tasks without interrupting for confirmation
- Skills use a three-tier loading system: metadata (always loaded) → SKILL.md body (on trigger) → bundled resources (on demand)

## Repository Structure

```
/Users/dj/Desktop/小静的skills/
├── [skill-name]/              # Individual skill directories
│   ├── SKILL.md              # Main skill file (required)
│   ├── knowledge/            # Knowledge base files (optional)
│   ├── scripts/              # Executable scripts (optional)
│   └── .tmp/                 # Temporary files (auto-managed)
├── skill-standards/          # Skill development standards and rules
│   ├── SKILL.md
│   └── knowledge/
│       ├── optimization-rules.md
│       ├── self-check-list.md
│       ├── skill-template.md
│       └── learned-patterns.json
├── .agent/rules/             # Agent workflow rules
│   ├── buile-skills.md       # Skill architect workflow
│   └── instruction-architect.md
└── knowledge/                # Shared knowledge base
    └── skill-creation-guide.md
```

## Common Development Commands

### Creating a New Skill

```bash
# Step 1: Create skill directory
mkdir -p /Users/dj/Desktop/小静的skills/[skill-name]

# Step 2: Create SKILL.md file
# (Use Write tool to create the file)

# Step 3: Create global symlink
ln -s /Users/dj/Desktop/小静的skills/[skill-name] \
      /Users/dj/.claude/skills/[skill-name]

# Step 4: Verify deployment
ls -la /Users/dj/.claude/skills/[skill-name]
# Expected: lrwxr-xr-x ... -> /Users/dj/Desktop/小静的skills/[skill-name]
```

### Testing a Skill

```bash
# Invoke skill directly
/skill-name [arguments]

# Check if skill is properly linked
ls -la /Users/dj/.claude/skills/
```

### Modifying a Skill

```bash
# Edit files directly in this directory - changes take effect globally
# No need to update symlinks
```

## Critical Development Rules

### 1. Skill Storage Rule (MUST FOLLOW)

**✅ CORRECT:**
```
Create in: /Users/dj/Desktop/小静的skills/[skill-name]/
Symlink to: /Users/dj/.claude/skills/[skill-name]
```

**❌ WRONG:**
```
Create directly in: /Users/dj/.claude/skills/[skill-name]/
```

### 2. Silent Execution Protocol

All skills MUST follow the silent execution protocol:
- ❌ **NEVER** ask for confirmation to proceed
- ❌ **NEVER** ask "Do you need more information?"
- ❌ **NEVER** pause mid-execution for user feedback
- ✅ **ALWAYS** generate complete output in one go
- ✅ **ALWAYS** use default values when data is missing
- ✅ **ALWAYS** handle errors silently and continue

### 3. Composite Skill Synchronization

When modifying composite skills (e.g., `content-production-pipeline`), changes MUST be synchronized to branch skills:

```
content-production-pipeline (composite)
├── topic-discovery (branch) → Must sync
├── xiaohongshu-content-generator (branch) → Must sync
├── wechat-content-generator (branch) → Must sync
└── video-script-generator (branch) → Must sync
```

**Sync checklist:**
- API usage rules (e.g., DALL-E restrictions)
- Error handling/retry logic
- Output format/cleaning rules
- Quality validation steps

### 4. Automatic Triggers (AI Must Execute)

**Trigger 1: After Creating New Skill**
- Auto-execute self-check for required sections
- Check for: silent execution protocol, output templates, error handling
- Reference: `skill-standards/knowledge/skill-template.md`

**Trigger 2: When Optimizing Skill**
- Auto-read: `skill-standards/knowledge/optimization-rules.md`
- Apply relevant rules during optimization
- Focus on: R01 (silent protocol), R07 (knowledge consistency), R11 (composite sync)

**Trigger 3: After Optimization Complete**
- Analyze if optimization is generalizable
- Record to: `skill-standards/knowledge/learned-patterns.json`
- Promote to formal rule if used ≥2 times

**Trigger 4: Before Publishing Skill**
- Auto-read: `skill-standards/knowledge/self-check-list.md`
- Check all items: 🔴 critical, 🟡 recommended, 🟢 optional
- Output check report

## Skill Categories

### Content Production (5 skills)
- `xiaohongshu-content-generator` (v5.4) - Xiaohongshu posts with images
- `wechat-content-generator` (v3.7) - WeChat articles
- `video-script-generator` (v2.0) - Video scripts with scenes
- `content-production-pipeline` (v1.4) - Full content workflow
- `topic-discovery` (v3.0) - Trending topic research

### Product Management (4 skills)
- `product-catalog` (v1.0) - Product database access
- `product-optimizer` (v1.0) - SKU optimization
- `product-selector` (v2.0) - Product selection analysis
- `product-pipeline` (v2.0) - Product optimization workflow

### Knowledge Management (3 skills)
- `knowledge-extractor` - Extract methodologies from documents
- `docs-scraper` - Scrape documentation websites
- `pdf-processing` - PDF conversion and quality assessment

### Tools/Development (3 skills)
- `account-stage-manager` - Multi-platform account tracking
- `skill-standards` - Skill development standards
- `skill-suitability-evaluator` - Evaluate if task suits skill creation

## Key File Locations

**Skill Standards:**
- Template: `skill-standards/knowledge/skill-template.md`
- Optimization rules: `skill-standards/knowledge/optimization-rules.md`
- Self-check list: `skill-standards/knowledge/self-check-list.md`
- Learned patterns: `skill-standards/knowledge/learned-patterns.json`

**Agent Rules:**
- Skill architect: `.agent/rules/buile-skills.md`
- Instruction design: `.agent/rules/instruction-architect.md`

**Documentation:**
- Creation guide: `knowledge/skill-creation-guide.md`

## SKILL.md Structure

Every skill must have a SKILL.md file with:

```yaml
---
name: skill-name
description: "What it does and when to use it"
---
```

**Required sections:**
1. Silent Execution Protocol (🔴 critical)
2. Overview
3. Execution workflow
4. Output templates (🔴 critical)
5. Good cases / Anti-patterns
6. Error handling (🔴 critical)

**Keep SKILL.md under 500 lines** - split detailed content into knowledge/ files.

## Important Notes

- **Context is shared:** Skills share the context window with everything else - keep them concise
- **Claude is smart:** Only add context Claude doesn't already have
- **Progressive disclosure:** Use the three-tier loading system effectively
- **No README files:** Skills should only contain what AI agents need to work
- **Symlinks are key:** Always verify symlinks are correct after creation
