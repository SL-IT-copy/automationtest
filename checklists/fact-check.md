# Fact Check

## Source Tier Policy (BALANCED, NOT EXCLUSIONARY)

The goal is **source balance**, not source exclusion. Every important fact should have at least one Tier 1, 2, or 3 source. X / blogs / individual posts (Tier 4) are valuable for discovery, color, and viral signals — and can be cited in slides when used appropriately (see Tier 4 rules below).

The rule of thumb: **if a slide leans heavily on a single Tier 4 source for a critical factual claim, that claim is fragile.** Either find Tier 1-3 corroboration, downgrade the language ("주장됨", "보고됨"), or attribute it explicitly ("X에서 한 사용자가 ~라고 썼음").

### Tier 1 — Primary sources (preferred)
- Company official statements (blog posts, press releases, SEC filings, internal memos that have been published)
- Government documents (court filings, regulatory letters, hearing records)
- Direct verified company / executive quotes (e.g. CEO official statement, named spokesperson)
- Vendor security advisories (CVE entries, PSIRT bulletins)
- Academic papers and benchmark leaderboards from the maintainer

### Tier 2 — Major journalism (must be present for any non-trivial fact)
- **English**: Wired, Fortune, Bloomberg, Reuters, AP, NYT, WSJ, FT, Business Insider, The Verge, CNN Business
- **Tech-focused**: TechCrunch, VentureBeat, The Information, Ars Technica
- **Korean**: 조선일보, 한겨레, 한국경제, 매일경제, 디지털투데이, 토큰포스트, IT조선, 전자신문, 블로터, ZDNet Korea

### Tier 3 — Specialized media (acceptable for technical/niche facts)
- **Cybersecurity**: The Record, BleepingComputer, The Hacker News, SecurityWeek, GovInfoSecurity, DataBreachToday, The Register
- **AI/ML specialist**: Import AI, Stratechery, Platformer (substack with editorial standards)
- **Major analyst firms**: SIG, Gartner, Forrester research notes
- **Major company security blogs**: Wiz.io research, CrowdStrike, Mandiant, Microsoft Security

### Tier 4 — X / blogs / individual posts (DISCOVERY + SUPPORTING REFERENCE)
- X posts by accounts that are not the subject of the story
- Personal Substacks, Medium analyses by individuals
- Reddit, Hacker News comments
- LinkedIn posts by non-officials

**Tier 4 is valuable for:**
- Topic discovery (X is often 12-48 hours ahead of mainstream)
- Viral signal measurement (which framings are landing)
- Finding hidden angles mainstream missed (e.g. Korean reaction)
- Adding color, rhythm, or human texture to a slide
- Corroborating a Tier 1-3 fact with on-the-ground reaction

**Tier 4 limits:**
- Should NOT be the sole evidence for a critical numerical fact (e.g. "4만 명 영향")
- Should NOT be the sole evidence for a contested causal claim (e.g. "이렇게 뚫렸다")
- When used standalone, attribute explicitly: "X에서 한 사용자가 ~라고 썼음", "한 보안 연구자가 X에 올린 글에 따르면"
- The viral count (좋아요 수) can be cited as evidence of the reaction itself, not of the underlying claim

### Tier 5 — Self-source quotes (special case, allowed with attribution)
- A person's own X / social post = primary evidence of THAT person's experience or statement
- Always attribute explicitly: "X에서 한 한국 사용자가 이렇게 썼음" — NOT "한국 사용자들이 그렇다"
- The post is evidence of "this person said this," not "this is generally true"
- Verified accounts of executives / spokespeople posting company news = treated as Tier 1 primary

## Required for every draft

- Every core claim maps to a source at Tier 1, 2, or 3
- Every number has a date context AND a Tier 1-3 source (not Tier 4)
- Every company response claim was checked across multiple outlets
- If one outlet says "no comment," verify whether another outlet got a comment
- Hard facts and interpretation are separated
- Disputed core facts are removed or flagged
- The 🔗 source URL in slide 7 must be Tier 1-3

## Source presentation in slides (NOT bibliography)

Sources are for **verification**, not for **showing off**. The reader should not see a list of outlets unless one specific outlet IS the story.

### Wrong (bibliography style)
```
xda-developers (4월 3일).
TechCrunch (4월 5일).
PCMag, Tom's Hardware,
cybersecuritynews, gadgets360.

주요 매체가 4월 첫 주에 동시 보도.
```

This reads like a footnote dump. The reader doesn't care which 6 outlets covered it. They care about WHAT happened.

### Right (subtle integration)
```
이번 주에 외신이 동시에 짚으면서 바이럴이 됨.
```
or
```
지난주 미국 매체들이 일제히 보도.
```
or just state the fact and move on.

### Rules for slide-level source mentions

1. **Default: don't name outlets in slides at all**. Save the outlet name for the 🔗 link in slide 7.
2. **Exception A — when the outlet itself IS news**: "Wired가 단독 입수", "TechCrunch가 단독 보도" → name it because the outlet's reporting is the story.
3. **Exception B — when a single primary source is the verification anchor**: "공식 약관에 따르면", "회사가 직원에게 보낸 이메일에 따르면" → name the source type, not the outlet.
4. **Exception C — when an executive's own quote is being cited**: "Andreessen이 X에 올린 글", "Altman이 블로그에 쓴 글" → name the platform/person, not the outlet that reported it.
5. **Never list 3+ outlets in a slide.** That's a footnote, not a thread.
6. **Never timestamp every source ("4월 3일... 4월 5일...")**. One date for the event, not for each outlet.
7. **Korean media mentions**: same rules. "한국 매체도 보도함" is fine. "디지털투데이, 토큰포스트, IT조선이 보도" is NOT fine.

### What goes in slide 7 (the 🔗 link)
- Pick the **strongest single Tier 1-2 source** for the URL
- Primary source > major mainstream > specialist
- Example: Wired > Fortune > TechCrunch > The Register
- Korean source if the topic is Korea-specific

### What goes in the metadata file (content/published/...md)
- Full source list with URLs
- This is the bibliography. Slides are not.

## X / xactions usage rule (BALANCED)

**X is great for discovery and color. Mainstream is great for verification. Use both, balanced.**

Correct workflow:
1. Use `xactions` to find breaking topics, viral angles, sentiment spikes
2. Identify candidate facts from X chatter
3. **Cross-check every critical numerical or causal claim against Tier 1-3 sources**
4. Keep Tier 4 references in the draft when they ADD value:
   - viral signal ("X에서 좋아요 9,900개")
   - executive's own words from verified accounts (Andreessen, CEO posts)
   - hidden Korean / regional angles mainstream missed
   - one-line color that mainstream wouldn't print
5. If a critical fact has ONLY Tier 4 evidence after verification attempts → either drop, downgrade ("주장됨"), or attribute explicitly

Wrong workflow:
1. Find story on X
2. Pull every number, quote, and detail from X without cross-checking
3. Write slides as if X claims are mainstream facts
4. Cite Wired in slide 7 to look credible without actually using Wired's facts

Right balance:
- **80% of facts in slides should trace to Tier 1-3 sources**
- **Tier 4 fills the remaining 20% with attribution and color**
- A thread that feels alive uses both registers: the cold journalism number AND the human X reaction

## Counter-evidence prompts

- Did another outlet report a different company response?
- Did another source use a more precise date, number, or scope?
- Is this a lawsuit allegation, confirmed fact, or official admission?
- Is this benchmark or financial figure stale?
- Is the only source for this claim a Tier 4 X post?

## Auto-fail

- unsourced core claim
- mixed-quarter comparison
- outdated leaderboard used as current truth
- one-source certainty on contested issue
- **any fact in slides 1-7 that has only Tier 4 sourcing**
- **any executive quote that cannot be cross-referenced to a Tier 1-3 outlet OR the executive's own verified account**
- **any direct quote (따옴표 안 문장) from Verifier B that has not been grep/fetch verified against the original source text — URL 제시 여부와 무관하게 원문 대조 필수**
