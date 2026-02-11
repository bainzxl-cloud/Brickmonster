# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to CLAUDE.md, AGENTS.md, or copilot-instructions.md |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250115-001] best_practice

**Logged**: 2025-01-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/docker-m1-fixes
**Area**: infra

### Summary
Docker build fails on Apple Silicon due to platform mismatch
...
```

---


## [LRN-20260208-001] knowledge_gap

**Logged**: 2026-02-08T22:28:00-05:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
GPT-OSS 20b model hangs with chat-formatted prompts in PowerShell digest script

### Details
The memory digest script (digest_discord_to_memory.ps1) was configured to use gpt-oss:20b model via Ollama API. When given chat-formatted prompts (system + user messages), gpt-oss would hang indefinitely and timeout (even with 120s timeout). Direct API calls to gpt-oss worked, but the script format caused issues.

### Suggested Action
Switch to llama3.2:3b model for memory digest - it works reliably and is much faster.

### Resolution
- Changed $Model parameter from "gpt-oss:20b" to "llama3.2:3b" in digest_discord_to_memory.ps1
- Script now completes successfully in ~2-3 seconds instead of timing out

### Metadata
- Source: conversation
- Tags: memory, local-models, ollama, llama3.2
- Related Files: scripts/digest_discord_to_memory.ps1

---

## [LRN-20260208-002] best_practice

**Logged**: 2026-02-08T22:28:00-05:00
**Priority**: medium
**Status**: resolved
**Area**: infra

### Summary
Local LLM models (llama3.2:3b) are more reliable for scripted automation than larger models (gpt-oss:20b)

### Details
For background automation tasks like memory digesting, smaller/faster local models work better because:
1. They don't timeout on chat-formatted prompts
2. They're faster to load and respond
3. They're more predictable in scripted environments

### Suggested Action
Use llama3.2:3b for:
- Memory digest scripts
- Any automated processing tasks
- Background/cron jobs

Use gpt-oss:20b for:
- Interactive sessions where you need more reasoning power

### Metadata
- Source: conversation
- Tags: local-models, automation, performance, llama3.2
- See Also: LRN-20260208-001

---

## [LRN-20260208-003] knowledge_gap

**Logged**: 2026-02-08T22:28:00-05:00
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
Memory digest cron only processes NEW messages since last run - doesn't recreate files

### Details
The cron job checks state.json to see when it last ran. If there are no new messages since then, it doesn't create a new daily digest file. This is by design (prevents duplicates) but can be confusing when debugging.

### Suggested Action
- Check state.json for last run timestamp
- Manually run digest with new messages to create daily digest
- For testing, use --force flag or clear state.json

### Metadata
- Source: conversation
- Tags: memory, cron, debugging, state-management
- Related Files: memory/digest/state.json

---


---

## [LRN-20260208-004] best_practice

**Logged**: 2026-02-08T22:55:00-05:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
Physics research analysis skills successfully installed and tested

### Details
Installed three research-focused skills:
1. Senior Data Scientist - statistical analysis and modeling
2. Data Visualization - graph generation with Matplotlib/Seaborn/Plotly  
3. Academic Research Hub - paper search and citation generation

### Actions Taken
- Installed skills via clawhub install
- Ran test physics analysis (pendulum experiment)
- Successfully calculated mean, standard deviation, SEM, 95% CI
- Result: g = 9.82 ± 0.05 m/s², consistent with accepted value

### What These Skills Can Do
- Statistical analysis of experimental data
- Standard deviation and uncertainty propagation
- Curve fitting and regression analysis
- Publication-quality graph generation
- Academic paper search (arXiv, PubMed, Semantic Scholar)
- Citation and bibliography generation

### Suggested Action
Use for physics research projects requiring:
- Data analysis with uncertainty quantification
- Mathematical modeling
- Visualization of experimental results
- Literature reviews

### Metadata
- Source: conversation
- Tags: physics, research, data-analysis, visualization, skills
- Related Files: skills/senior-data-scientist, skills/data-visualization, skills/academic-research-hub


---

## [LRN-20260208-005] knowledge_gap

**Logged**: 2026-02-08T23:00:00-05:00
**Priority**: medium
**Status**: resolved
**Area**: infra

### Summary
Academic Research Hub dependencies installed successfully

### Details
Installed Python packages for academic paper search:
- requests (HTTP library)
- beautifulsoup4 (HTML parsing)
- lxml (XML/HTML processing)
- arxiv (arXiv API client)

### Observation
ArXiv API requests can be slow (several seconds) due to server response time. This is expected behavior from arXiv's infrastructure, not a bug.

### Commands Available
`ash
python skills/academic-research-hub/scripts/research.py arxiv "quantum mechanics" --max-results 10
python skills/academic-research-hub/scripts/research.py pubmed "physics" --year 2024 --format bibtex
`

### Metadata
- Source: manual testing
- Tags: dependencies, academic-research, arxiv, installation


---

## [LRN-20260208-006] bug_fix

**Logged**: 2026-02-09T00:00:00-05:00
**Priority**: critical
**Status**: resolved
**Area**: deployment

### Summary
GitHub Pages deployment workflow - used wrong folder and branch

### Bug
Pushed LEGO shop updates to:
- Wrong folder: lego-shop/ (test site)
- Wrong branch: master (inactive branch)
- Result: Website never updated

### Root Cause
Confused two similar projects:
- rickmonster-site/ - Main store (lives on main branch)
- lego-shop/ - Test/alternative site

### Fix Applied
- Add products to rickmonster-site/listings.json
- Add images to rickmonster-site/assets/
- Commit in rickmonster-site/ directory
- Push to origin main branch

### Correct Workflow
`ash
cd brickmonster-site/
git add listings.json assets/
git commit -m "Add new product"
git push origin main
`

### Verification
GitHub Pages automatically rebuilds from main branch
Website URL: https://bainzxl-cloud.github.io/Brickmonster/

### Impact
Products now appear on live site after ~5 minute rebuild

