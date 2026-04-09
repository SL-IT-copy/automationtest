# Pre-Delivery Gate

**This is NOT a passive checklist. This is a MANDATORY procedure that MUST run before showing ANY draft to JSup.**

If this gate has not been executed and documented in the response, the draft is not ready for delivery.

## Why this exists

Previous drafts all needed revision rounds because the agent wrote drafts and then relied on JSup to catch errors. That is not a system — it is interactive proofreading. This gate exists so that the agent catches its own errors before JSup sees them.

## Gate procedure (run in order)

### Gate A — Product / Entity Mapping

For every factual claim in the draft, answer:

1. **What specific product, document, law, legal entity, or person does this claim apply to?**
2. **Does the claim in my slide apply to the correct target?**
3. **Am I implying a broader scope than my source supports?**

Common failures: Consumer TOS quoted as enterprise, different legal subsidiaries mixed up, $5 liability cap from API TOS applied to subscription product.

If any claim fails → fix the target, downgrade the claim, or drop it.

### Gate B — Quote Precision

For every quoted phrase in the draft, answer:

1. **Is this a direct quote or a paraphrase?**
2. **If direct: can I trace the exact words to a specific source?**
3. **If paraphrase: is my wording tight enough not to be mistaken for a direct quote?**
4. **Translation: does my Korean translation preserve the exact meaning?**

If any quote fails → fix the wording or remove the quote.

### Gate C — Cross-Outlet Verification for Critical Facts

For every critical fact (number, causal claim, timeline, company position):

1. **Do I have at least two independent sources at Tier 1–3 level?**
2. **If only one source: is it primary (Tier 1) or do I need to downgrade?**
3. **Are the sources describing the same product/entity/event?**

### Gate C-1 — Numerical Cross-Check (NON-NEGOTIABLE)

For EVERY specific number in the draft:

1. Find the exact same number in at least 2 independent Tier 1–3 sources.
2. If sources conflict, document: "Source A says X, Source B says Y, consensus = Z"
3. Never trust a single Tier 2 source for a specific number when others exist.

**Output format:**
```
- [number/fact]: confirmed in [N] sources → [list source domains]
- [number/fact]: SOURCE CONFLICT → Source A says X, Source B says Y, consensus = Z
```

### Gate D — Slide-by-Slide Tension Test

For each slide:

1. Does this slide CREATE tension or RELIEVE it?
2. If it relieves tension, does it immediately create new tension?
3. At the end of each slide, does the reader have a new question?
4. Is any slide purely expository (no tension change)?

If any slide fails → restructure or compress.

### Gate E — Adversarial Attack Simulation

Imagine the three most likely hostile comments. For each:

1. What is the most damaging attack a critical reader can make?
2. Is the draft already defended against it?
3. If not: add one line of defense, or restructure.

### Gate F — First-Time Reader Test

Read slide 1 as if you know nothing about the topic.

1. What do you expect the rest of the thread to be about?
2. What question does slide 1 make you want answered?
3. Does the actual thread answer that question?
4. Are there terms in slide 1 a general reader wouldn't understand?

### Gate G — Hook Power Benchmark (CRITICAL)

The hook must match one of the five winning patterns (Formula A~E in hook-check.md).

If NO match to any formula → projected ceiling is sub-150k. Rewrite or explicitly accept lower ceiling.

**Verdict format:**
```
- Formula match: A / B / C / D / E / NONE
- If NONE: projected ceiling and rewrite proposal
```

### Gate G+ — Hook Strength Score (≥ 7/10 to pass)

| Component | Max | Criteria |
|---|---|---|
| Number impact | 0-3 | Cognitive-dissonance numbers in first 6 lines |
| Tension verb | 0-2 | Strong action verb (잃었다/거절했다/뚫렸다) |
| Reader implication | 0-2 | Direct targeting ("~한테", "~쓰는 사람") |
| Curiosity gap | 0-2 | Forces scroll to slide 2? |
| Brand weight | 0-1 | Familiar proper nouns? |

Score < 7 → mandatory rewrite.

### Gate H — Internal Consistency Check

For every claim in multiple slides, verify:

1. Same numbers across slides?
2. Same entity names?
3. Same quote text?
4. Same timeline?
5. Same angle/thesis?

**NEW — Slide 1 ↔ Close Echo Check:**
6. **Does slide 1's core number or phrase get echoed/returned in the final slide?**

All 100k+ JSup posts echo the hook in the close:
- 215k: "90조 원을 AI 하나에 걸었음" → slide 7 repeats the same sentence
- 201k: "350억원을 거절" → slide 7: "350억원 제안 → 거절"
- 150k: "14개월 만에 매출 5,600억" → slide 7: "2,400명의 일을 2명으로 압축"

If no echo → add one in the final slide.

**Output format (STRICT):**
```
- Number consistency: [check each repeated number]
- Currency unit check: [verify cross-unit accuracy]
- Entity naming: [confirm consistency]
- Timeline consistency: [confirm no drift]
- Hook fulfillment: [hook promise → close delivers?]
- Slide 1↔Close echo: [what phrase echoes?] PASS / FAIL
```

### Gate I — Hook Withholding Test (NEW)

Slide 1 must NOT contain all three of: WHAT happened + WHO is involved + WHY it matters.

Must withhold at least ONE major element for slide 2-3 to reveal.

Test: "독자가 slide 1만 읽고 나머지 내용을 90% 예측할 수 있는가?"
- YES → **FAIL**. Too much revealed.
- NO → PASS.

### Gate J — Per-Slide Momentum Test (NEW)

Each slide must do at least one of:
- Create a NEW question
- Escalate existing tension
- Reverse the reader's expectation

Test: Write a 1-sentence summary per slide of "what new question this slide plants in the reader's mind."
- If any slide has no new question → **FAIL** (pure context dump). Rewrite or merge.

### Gate K — Non-Redundancy Test (NEW)

Summarize each slide's core insight in 1 sentence.
- If any two summaries overlap >70% in meaning → **FAIL**. Merge or cut one.

### Gate L — Protagonist Activity Test (NEW)

Slide 1~3 must contain at least ONE instance of "X가 Y를 하고 있다" structure (active subject + active verb).

- Passive-only narration ("~가 나왔다", "~가 발표됐다", "~가 있었음") throughout slides 1-3 → **FAIL**.

### Gate M — Reversal Existence Test (NEW)

"Slide 3~5 사이에 독자의 초기 해석을 뒤집는 반전이 존재하는가?"

Every JSup 100k+ post has a reversal. No reversal in any slide → **FAIL**.

---

## Gate Report output rules

### Internal execution
Run ALL gates A through M with full detail. This is the agent's internal QA.

### User-facing output (CHANGED)
- **When ALL gates pass**: Show only "Pre-Delivery Gate: ALL PASS (A~M)" + 1-2줄 핵심 요약
- **When ANY gate fails**: Show the failing gate(s) with full detail. Fix before delivery.

This change exists because previous sessions showed 30+ line gate reports that diluted the draft's impact. The report is a QA tool, not a presentation artifact.

## Hard rule

If the agent ships a draft without running the Pre-Delivery Gate, that is a procedural failure. The agent must re-run the gate before delivery.

Gates I through M are HARD FAIL conditions (not scored). Any single FAIL blocks delivery.
