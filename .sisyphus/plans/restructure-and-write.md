# Restructure Pipeline + Write New Viral Post

## Status: Ready to execute (backups created)

## Backups created
- `SOUL.md.bak`
- `checklists/hook-check.md.bak`
- `checklists/pre-delivery-gate.md.bak`

## Task 1: Rewrite SOUL.md (591 → ~120 lines)

Keep ONLY: account identity, voice, formatting rules, channel principles, visual policy, output contract, slide count flexibility, auto-save workflow.

REMOVE (moved to dedicated files):
- Hook rules (lines 224-284) → hook-check.md
- Slide pacing / information budget table (lines 255-284) → hook-check.md
- Fact-check policy summary (lines 429-437) → already in fact-check.md
- Source tier summary (lines 429-437) → already in fact-check.md
- Content pipeline diagram (lines 444-535) → already in AGENTS.md
- X search instructions (lines 539-591) → scripts/x-search.sh + AGENTS.md
- PUPPETEER instructions → scripts/ only

FIX self-contradiction: Line 34 "Mode A — 7-slide thread" conflicts with line 418 "Slide count is FLEXIBLE". Remove Mode A/B distinction entirely, keep only the flexible table.

New SOUL.md content is already drafted (see the write attempt above in this session - use that exact content).

## Task 2: Rewrite hook-check.md

Absorb from SOUL.md:
- "Hook rules" section (lines 224-253)
- "Hook intensity calibration" (lines 239-253)
- "Slide pacing rules" section (lines 255-284)
- "Information budget" table (lines 265-273)
- "Anti-pattern: front-loading" (lines 275-279)
- "Self-check before delivering" (lines 281-284)

Absorb from memory/cold/:
- hook-lessons.md (all 13 lines)
- style-dna.md hook shape section

ADD NEW checks:
- "한 메시지 원칙": "이 글의 핵심 메시지를 1문장으로 요약할 수 있는가? 못 하면 메시지 분산."
- "반전 포인트": "slide 3~5 사이에 독자의 초기 해석을 뒤집는 반전이 존재하는가?"
- "구체적 장면": "최소 1개 slide에 시간+장소+행위자+대화가 포함된 구체적 사건 장면이 있는가?"

Keep existing: Formula A~E, fail patterns, pre-draft checklist, S-tier pattern.

## Task 3: Rewrite pre-delivery-gate.md

ADD new gates (after Gate H):

### Gate I — Hook Withholding Test
- Slide 1 must NOT contain all three of: what + who + why
- Must withhold at least ONE for slide 2-3
- Test: "독자가 slide 1만 읽고 나머지를 90% 예측 가능한가? → FAIL"

### Gate J — Per-Slide Momentum Test
- Each slide must: create new question / escalate tension / reverse expectation
- Test: per-slide 1-sentence summary of "what new question this slide plants"
- Pure context dump without narrative framing = FAIL

### Gate K — Non-Redundancy Test
- Summarize each slide's core insight in 1 sentence
- If two summaries overlap >70% meaning = FAIL → merge or cut

### Gate L — Protagonist Activity Test
- Slide 1~3 must contain "X가 Y를 하고 있다" (active subject + active verb) minimum 1
- Passive-only narration ("~가 나왔다", "~가 발표됐다") = FAIL

### Gate M — Reversal Existence Test
- "slide 3~5 사이에 독자의 초기 해석을 뒤집는 반전이 존재하는가?"
- No reversal in any slide = FAIL

ADD to Gate H:
- "slide 1의 핵심 수치/문장이 마지막 slide에서 회수(echo)되는가?"

CHANGE Gate Report output rule:
- Internal execution: full report (as before)
- User-facing output: "PASS/FAIL + 1~2줄 핵심 요약" only
- Show full report ONLY when a gate fails

## Task 4: Update AGENTS.md pipeline

Remove SOUL.md pipeline diagram duplication (SOUL.md no longer has it).
Keep AGENTS.md pipeline as canonical.
Verifier A/B + Reconciler + Critic Gate = MANDATORY (oracle subagents).
Remove any "light mode" references. Always full pipeline.

## Task 5: Delete dead prompts

Delete from prompts/THREADS_PIPELINE_PROMPTS.md:
- Section 1 (Intent normalizer) - never used
- Section 7 (Style DNA builder) - style-dna.md exists
- Section 8 (Structural-interest reviewer) - never used in practice
- Section 11 (Visual planner) - Threads doesn't prioritize visuals

Keep: sections 2-6, 9, 10.

## Task 6: Merge memory/cold

Move hook-lessons.md content into hook-check.md (under "Lessons from JSup's posts" section).
Move style-dna.md hook shape into hook-check.md.
Replace original files with 1-line pointers: "→ See checklists/hook-check.md"

## Task 7: Write new viral post

After structure fixes are complete:
1. Dedup check against covered_topics.json
2. X search for fresh candidates (scripts/x-search.sh)
3. Web search for corroboration (Tier 1-3 sources)
4. Run Verifier A + B (oracle subagents, parallel)
5. Reconcile
6. Draft using improved hook-check.md rules
7. Run Critic Gate (oracle subagent)
8. Execute pre-delivery-gate.md (all gates A~M)
9. Deliver to JSup

## Key principles from analysis

From JSup's 100k+ posts:
- ALL have a reversal (slide 3-5)
- ALL echo slide 1's core phrase in the final slide
- ALL have at least 1 concrete scene (time+place+actor+dialogue)
- Density > rhythm in slide 1 (numbers, proper nouns, time markers)
- ONE core message per thread

From 쓰레드마케팅자료.pdf:
- 한 게시물 = 한 메시지 (3-4)
- 첫 줄 후킹이 전부 (3-2)
- 15-20자 per line (3-6, 3-8)
- 숫자와 구체성으로 신뢰 (3-3)
- 감정 연결 > 정보 전달 (1-4)

## Files to read at start of new session
1. This file (.sisyphus/plans/restructure-and-write.md)
2. SOUL.md.bak (to understand what to remove)
3. checklists/hook-check.md.bak (to understand what to add)
4. checklists/pre-delivery-gate.md.bak (to understand what to add)
5. AGENTS.md (pipeline section)
6. content/covered_topics.json (dedup)
