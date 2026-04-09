# Pipeline Architecture V1

> Status: historical architecture note. Superseded in practice by the current flat-file workflow built around `AGENTS.md`, `config/*.yaml`, `memory/`, and `reviews/`.

> Do not treat Postgres/pgvector/object-store references here as active infrastructure unless explicitly revived later.

## Bottom line

V1 should be a **single orchestrated workflow**, not a multi-agent swarm.

In direct-use mode, that orchestrated workflow runs inside the Claude session itself.
OAuth is only relevant for Threads auth/posting later.

Use:

- Postgres
- pgvector
- a simple source cache / object store

The system should do five things well:

1. discover fresh topics,
2. rank them with fatigue awareness,
3. run **two independent source-verification passes**,
4. reconcile disagreements and interest-structure risk,
5. generate a review-ready Korean content pack.

Publishing stays manual.

## Data stores

### 1. Creator memory

Stores JSup's own history:

- post text,
- view bucket,
- topic tags,
- company tags,
- hook type,
- reversal type,
- close type,
- embeddings,
- notes about why it won or underperformed.

### 2. Source cache

Stores fresh external materials:

- title,
- canonical URL,
- source domain,
- publish time,
- fetched text,
- extracted entities,
- extracted claims,
- screenshot-worthy sections.

### 3. Fatigue ledger

Stores recent publishing pressure:

- recent companies covered,
- recent themes,
- recent hook shapes,
- recent closes,
- penalties to apply for repetition.

### 4. Run artifacts

Stores each generation run:

- request,
- topic candidates,
- chosen angle,
- fact pack,
- draft,
- visual plan,
- review result.

## Workflow

```text
user request
  -> normalize brief
  -> discover topics
  -> rank with freshness + evidence + fatigue
  -> build fact pack
  -> verifier A review
  -> verifier B review
  -> reconciliation
  -> retrieve style references
  -> structural-interest review
  -> draft in Korean
  -> critic / fact gate
  -> visual planner
  -> human review
```

## Ranking logic

Suggested simple v1 score:

- freshness: 30
- evidence density: 25
- audience fit: 20
- style fit: 15
- fatigue penalty: up to -20

### Hard blocks

- no core claim without source support,
- no last-2-post same-company repeat unless materially new,
- no stale quarter or outdated leaderboard if a newer one exists.

## Generation rule

Korean copy should be generated **only after** the evidence pack exists.

That keeps the system from:

- inventing facts,
- drifting into generic commentary,
- over-translating weak sources into stronger claims.

## Required v1 modules

### A. Topic scout

Returns:

- top 3 candidates,
- why now,
- viral ceiling,
- repetition risk.

### B. Evidence packer

Returns:

- claim list,
- exact source snippets,
- source timestamps,
- uncertainty flags.

### C. Verifier A

Checks:

- source accuracy,
- date / quarter / benchmark freshness,
- whether each core claim has enough support,
- whether any claim should be downgraded to interpretation.

### D. Verifier B

Checks the same topic independently, but must not simply mirror A.

It should especially inspect:

- missing counter-evidence,
- bad source hierarchy,
- overstated causal claims,
- hidden ambiguities.

### E. Reconciler

Returns:

- agreed facts,
- disputed facts,
- unresolved questions,
- final publishability status.

### F. Style retriever

Returns:

- 2-4 closest winning references,
- 1 weak reference if ceiling feels low,
- pattern summary only.

### G. Structural-interest reviewer

Checks:

- hook strength,
- cognitive dissonance,
- protagonist / antagonist clarity,
- reversal potential,
- universal audience ceiling,
- same-company fatigue risk.

### H. Draft generator

Returns:

- chosen angle,
- 7-slide thread,
- source footer,
- follow CTA.

### I. Critic gate

Checks:

- hook reveal problem,
- weak conflict,
- missing reversal,
- unsupported claims,
- same-company fatigue.

### J. Visual planner

Returns:

- recommended source screenshot,
- fallback chart idea,
- capture target,
- why that visual supports the story.

## Dual verification rule

No serious draft should be surfaced unless:

- Verifier A and Verifier B both reviewed it,
- disputed facts are either resolved or explicitly flagged,
- the structural-interest reviewer says the topic is not obviously low-ceiling.

If the verifiers disagree on a core fact, the draft must not silently choose one side.

## What should remain manual

V1 manual step:

- final editorial approval before posting.

This is the right tradeoff because the account wins on:

- framing,
- factual trust,
- freshness,
- avoiding subtle topic fatigue.

## Failure points

### 1. Translation drift

English source says one thing, Korean summary says slightly more.

Fix:

- separate hard facts from interpretation,
- require quote-backed evidence for important claims.

### 2. Style overfitting

Retrieving only top winners can make output repetitive.

Fix:

- retrieve patterns, not lines,
- track recent hook and close repetition.

### 3. Visual hallucination

Recommending screenshots from pages that were not actually verified.

Fix:

- visual recommendations must attach to fetched URLs or verified pages.

## What to build first

1. creator memory
2. source discovery + cache
3. evidence packer
4. dual verification
5. reconciliation + structural-interest review
6. direct review-ready content output

## What to build later

1. auto screenshot capture
2. learned ranking from performance feedback
3. batch generation
4. broader async crawling
5. multi-channel support
