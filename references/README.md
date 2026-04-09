# References Operating Guide

## Purpose

This folder exists to turn JSup's historical winners into usable retrieval context.

The references should be used for:

- hook analysis,
- pacing analysis,
- angle selection,
- anti-pattern detection,
- style conditioning.

They should **not** be used for copying wording.

## Reference tiers

### Tier 1 — JSup's own winning posts

Primary style references:

- 150kviews.docx
- 109k_view.docx
- 200k views.docx
- 201k views.docx
- 215k views.docx
- 306k_views.docx

These should dominate style retrieval.

Note: `150kviews.docx` is especially useful for hooks built on extreme ratio contrast
(small starting capital / tiny team / massive output) even when slide 1 delays the proper nouns until slide 2.

### Tier 2 — JSup's weaker posts

Contrast references:

- 85k_views.docx
- 43k_view.docx
- 51.4k_views.docx
- 57.5k_views.docx

These are useful for diagnosing ceiling and weak hooks.

### Tier 3 — External guide material

- 쓰레드마케팅자료.pdf

Use this only for generic structural heuristics such as:

- first-line hook importance,
- readability,
- template families,
- reference-analysis habits.

Do not overfit to this PDF. JSup's account is AI/tech news-driven, not generic marketing content.

## Suggested metadata per reference

Each parsed reference should eventually have:

```json
{
  "file": "306k_views.docx",
  "views": 306000,
  "topic": "Anthropic / layoffs / benchmark / pricing / regulation",
  "hook_type": "contrarian | stat | warning | reversal",
  "narrative_shape": "conflict -> escalation -> reversal -> unresolved close",
  "angle_type": "market power | labor | product | benchmark | ethics",
  "close_type": "unresolved | pointed summary | follow CTA",
  "notes": "same-company fatigue risk low because angle is distinct"
}
```

## Minimum ingestion plan

### DOCX

On macOS use:

```bash
textutil -convert txt "109k_view.docx" -output "references/parsed/109k_view.txt"
```

### PDF

Keep the PDF as original source, but store manual notes or extracted text summaries in `references/parsed/`.

## Retrieval policy

When generating a new draft:

1. retrieve 2-4 closest winners by topic or hook pattern,
2. retrieve 1 weak reference if the topic feels low-ceiling,
3. extract only pattern-level guidance,
4. never reuse exact lines unless they are factual labels or source names.

## What to retrieve from references

- how the hook withholds resolution,
- where the reversal happens,
- how numbers are introduced,
- how the close preserves curiosity,
- what made a topic broad enough to travel.
