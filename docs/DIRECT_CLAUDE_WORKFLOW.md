# Direct Claude Workflow

## Goal

One request from JSup should produce a usable content pack:

1. best current AI/tech topic candidates,
2. the chosen angle,
3. evidence-backed draft copy,
4. recommended cover/source screenshot ideas,
5. explicit risk/fact-check flags.

This workflow is for **interactive creation first**, not blind auto-posting.

This workflow assumes the writer is **Claude in the current session**.
It does not assume a separate external LLM API runner.

## Core operating model

```
JSup request
  → intent normalization
  → trend/source retrieval
  → historical winner retrieval
  → fact pack assembly
  → verifier A
  → verifier B
  → reconciliation
  → structural-interest review
  → draft generation
  → self-critique / fact gate
  → final content pack
  → human review
  → optional publish
```

If publishing is later connected, OAuth belongs only to the Threads auth/posting layer.
The editorial reasoning and writing stay in-session.

## What the user can type

### Simple request

```text
Anthropic 최신 이슈 글 써줘
```

### Better request

```text
Anthropic 최신 이슈 중에서 조회수 ceiling 높은 주제로
7슬라이드 쓰레드 초안 뽑아줘.
커버는 1차 출처 스크린샷 위주로.
팩트체크 이슈 있으면 같이 표시.
```

### Existing-topic revision request

```text
이 주제로 다시 가자.
후킹은 더 세게, 결론은 덜 빨리 드러나게.
```

## Required internal stages

### 1. Intent normalization

Claude should first resolve:

- entity: Anthropic / OpenAI / benchmark / layoffs / funding / regulation / coding tools
- timeframe: latest / this week / evergreen / historical comparison
- output mode: single post / 7-slide thread
- risk level: casual / normal / high-stakes fact checking

### 2. Trend retrieval

Use fresh, automation-friendly sources first:

- Hacker News
- Reddit r/LocalLLaMA
- TechCrunch
- official vendor blogs: Anthropic, OpenAI, Google, Meta, xAI
- benchmarks / leaderboards
- policy and regulator sources when relevant

The system should not rely on one source alone unless it is the official primary source.

### 3. Historical winner retrieval

Pull from JSup's own winners and style references:

- 109k_view.docx
- 200k views.docx
- 201k views.docx
- 215k views.docx
- 306k_views.docx
- lower-performing references as contrast cases

The purpose is not copying. The purpose is retrieving:

- hook pattern,
- pacing,
- reversal placement,
- close style,
- channel fatigue risk.

### 4. Fact pack assembly

Before drafting, Claude should assemble a compact fact pack:

- claim
- source
- publication time
- quote or precise numeric evidence
- counterpoint or uncertainty

If a claim cannot be supported, it should be removed or flagged.

### 5. Verifier A / Verifier B

Two separate reviewers should inspect the topic independently.

They should both check:

- source hierarchy,
- factual support,
- stale or mixed-quarter numbers,
- benchmark freshness,
- claims that sound true but are overstated.

### 6. Reconciliation

The system should merge both verification passes into one final fact status:

- agreed facts,
- disputed facts,
- removed claims,
- safe interpretations.

If a core fact stays disputed, it should not survive into the draft unmarked.

### 7. Structural-interest review

Before drafting, the system should check whether the topic is structurally likely to travel.

It should inspect:

- hook tension,
- protagonist / antagonist,
- reversal potential,
- broad audience ceiling,
- same-company fatigue.

### 8. Draft generation

Default format for this account:

- 7-slide thread,
- Korean,
- 반말,
- clipped lines,
- high information density,
- no corporate phrasing,
- unresolved or tension-preserving close.

### 9. Critique gate

Claude should explicitly inspect:

- did the hook reveal the resolution too early?
- is there a protagonist / antagonist or clear conflict?
- is the subject too repetitive versus recent same-company posts?
- are any quarters, dates, rankings, or financial figures stale or mixed?
- is the topic structurally low-ceiling even if well written?

### 10. Final content pack

The final answer should contain all of these sections every time:

1. topic recommendation,
2. why this topic now,
3. verifier A summary,
4. verifier B summary,
5. reconciliation result,
6. structural-interest review,
7. thread draft,
8. evidence set,
9. image recommendation,
10. risk / fact-check notes.

## Decision rules for this account

### Prefer

- cognitive dissonance hooks,
- villain / winner / loser framing when factually justified,
- universal emotional stakes over narrow technical cleverness,
- primary-source screenshot covers,
- clean unresolved ending over tidy summary.

### Avoid

- rich-company-gets-richer funding angles with no human tension,
- consecutive same-company threads unless the angle is clearly new,
- generic AI optimism / pessimism,
- both-sides hedging in the copy,
- made-up simultaneity or drama.

## Recommended output modes

### Mode A — Topic Scout

Use when JSup asks what to write.

Return:

- top 3 topic candidates,
- viral ceiling score,
- freshness score,
- repetition risk,
- recommendation.

### Mode B — Full Draft Pack

Use when JSup already wants a thread.

Return:

- final angle,
- 7-slide draft,
- source list,
- screenshot recommendations,
- fact-check flags.

### Mode C — Revision

Use when JSup wants stronger hook / different framing without changing the topic.

Return:

- what changed,
- revised draft only,
- any new fact-check risks.

## Recommended v1 human/manual step

The manual step should remain:

- **final editorial approval before publishing**.

Everything else can be prepared automatically.
