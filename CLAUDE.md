# CLAUDE.md — Loader for Claude/OpenCode sessions

This project uses a **layered instruction system**.

Do not rely on this file alone.

## Required read order

1. `AGENTS.md`
2. `SOUL.md`
3. `config/pipeline.yaml`
4. `config/sources.yaml`
5. `config/xactions.yaml`
6. `config/autosave.yaml`
7. relevant files in `checklists/`
8. `prompts/THREADS_PIPELINE_PROMPTS.md`
9. recent files in `content/published/` and `memory/cold/`

## Rule precedence

- Workflow/process conflicts → `AGENTS.md` and `config/*.yaml` win
- Voice/style conflicts → `SOUL.md` wins
- Quality gate conflicts → `checklists/*.md` win for delivery decisions

`CLAUDE.md` is a loader, not the operating source of truth.
If this file conflicts with `AGENTS.md`, follow `AGENTS.md`.

## Important behavior

- Never type raw `xactions ...` from memory when a script exists
- Use `scripts/x-search.sh` for X search
- Use `scripts/x-profile.sh` for X profile lookup
- Use `scripts/x-login-refresh.sh` to refresh the cookie workflow
- Use `scripts/validate-thread.sh` before treating a saved thread file as finished
- Never pass X auth tokens as CLI arguments
- Never paste X auth tokens into repo files, notes, or saved artifacts

## Mandatory pipeline

For all real thread requests (unless JSup explicitly asks for a lightweight casual post):
- dedup check against `content/covered_topics.json`
- X-first topic discovery
- fact pack
- verifier A
- verifier B
- reconcile
- draft
- critic gate
- approval
- autosave

No shortcuts.

## Output modes

- Mode A: topic scout
- Mode B: full draft pack
- Mode C: revision on the same topic
