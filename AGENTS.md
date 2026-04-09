# AGENTS.md — JSup Threads System

## Purpose

This repository is a production workflow for writing high-ceiling Korean AI/tech Threads posts for JSup.

This file is the **operating source of truth**.

If multiple files overlap:

1. `AGENTS.md` = workflow + boundaries + file ownership
2. `config/*.yaml` = machine-readable operating settings
3. `SOUL.md` = voice, rhythm, hook feel, channel identity
4. `checklists/*.md` = quality gates before delivery
5. `scripts/*.sh` = canonical command wrappers

## Read order at session start

1. `AGENTS.md`
2. `CLAUDE.md`
3. `SOUL.md`
4. `config/pipeline.yaml`
5. `config/sources.yaml`
6. `config/xactions.yaml`
7. `config/autosave.yaml`
8. relevant files in `checklists/`
9. `prompts/THREADS_PIPELINE_PROMPTS.md`
10. recent files in `content/published/` and `memory/cold/`

## File ownership

### `SOUL.md`
- Brand voice only
- Hook taste
- Vertical formatting feel
- JSup account identity

### `config/`
- Structured runtime rules
- Source priority
- X search settings
- Autosave rules

### `checklists/`
- Hook quality checks
- Fact-check checks
- Pacing checks
- Final release gate

### `scripts/`
- Canonical command entrypoints
- Prefer these over raw shell commands written from memory

### `memory/`
- `hot/` current session template/state
- `warm/` recent learnings and month-level notes
- `cold/` durable lessons and style DNA

### `reviews/`
- One directory per topic
- Fact pack, verifier outputs, reconciliation, critic notes

### `content/published/`
- Final approved thread archives

## Mandatory workflow

When JSup asks for a thread:

0. Check `content/covered_topics.json` first to avoid duplicate/fatigued topics
1. Run **X search first** using `scripts/x-search.sh`
2. Gather official / primary / article sources
3. Build fact pack
4. Run Verifier A (conservative source audit)
5. Run Verifier B (counter-evidence hunter)
6. Reconcile disagreements
   - **HARD RULE**: When Verifier B presents a direct quote (따옴표 안 문장) attributed to a specific source, the Reconciler MUST fetch or grep the original source to confirm the exact sentence exists verbatim. If not found, the quote is REJECTED and must not enter the draft. This applies even if Verifier B provides a URL.
7. Draft in Korean
8. Run critic gate
9. Revise if needed
10. Deliver to JSup
11. On approval, autosave final draft + review artifacts

## Output modes

### Mode A — Topic Scout
- top 3 candidates
- viral ceiling score
- repetition risk
- why now

### Mode B — Full Draft Pack
- recommendation
- verification summaries
- 7-slide draft
- evidence URLs
- cover recommendation
- risks

### Mode C — Revision
- same topic retained
- changed hook / pacing / close as requested
- revised risks if anything changed materially

## Hard rules

### Always
- Start topic discovery with X
- Prefer scripts over manual command reconstruction
- Store final approved threads in `content/published/`
- Store meaningful review artifacts in `reviews/`
- Update cold memory when a real lesson is learned
- Use full URLs only
- Refresh X auth only through `scripts/x-login-refresh.sh`

### Ask first
- Changing the account lane away from AI/tech news
- Deleting historical published drafts
- Changing autosave semantics
- Altering the 7-slide default output mode

### Never
- Skip X search because another source “looks enough”
- Skip verifier A/B for a serious thread
- Skip critic gate for a serious thread
- Put multiple major reveals into slide 1
- Treat one outlet’s “no comment” as universal silence without checking others
- Store secrets or cookies in repo files
- Pass auth tokens as CLI arguments
- Paste auth tokens into chat logs, notes, or saved review artifacts

## Operational notes

- X search is browser-cookie based, not API based
- `scripts/x-search.sh` is the canonical entrypoint
- `scripts/x-profile.sh` is the canonical profile lookup helper
- `scripts/x-login-refresh.sh` is the canonical cookie refresh helper
- `scripts/validate-thread.sh` is the canonical structural validator for saved thread files
- X auth tokens are sensitive session cookies. Handle transiently only.
- If X auth must be refreshed, use stdin or interactive login only. Never CLI args.

## Goal of this architecture

Move from:
- one long instruction file,
- memory-by-conversation,
- verification-by-intuition

To:
- layered instruction files,
- explicit scripts,
- archived review artifacts,
- reusable lessons,
- repeatable high-quality output.
