# Workflow

## Default working style

This repo now supports two workflows.

### 1. Direct Claude workflow

Use this when JSup is actively in session and wants a result immediately.

This is the **canonical** workflow.

There is no separate LLM runner script in v1.
The writing pipeline runs inside the Claude session itself.

Typical request:

```text
Anthropic 최신 이슈 글 써줘
```

Expected result:

- best angle,
- evidence-backed draft,
- visual recommendation,
- fact-check risks,
- dual verification result.

This is the preferred workflow for high-quality editorial work.

### 2. OpenClaw / Telegram workflow

Use this when JSup wants remote prompting, scheduled scouting, or review on phone.

That flow is documented in `DEPLOY.md`.

It is optional.

## Authentication split

- **content generation**: happens here, inside Claude
- **Threads posting/auth**: can use OAuth / Meta token flow later when posting is needed

## Direct Claude commands

### Topic scout only

```text
오늘 쓸 만한 AI 주제 3개만 골라줘.
조회수 ceiling, 반복 리스크까지 같이.
```

### Full draft pack

```text
Anthropic 최신 이슈로 7슬라이드 쓰레드 써줘.
커버는 1차 출처 스샷 위주로 추천해줘.
팩트체크 위험한 부분은 표시해.
```

### Revision on same topic

```text
이 topic 유지하고
후킹만 더 세게 바꿔줘.
결론은 덜 빨리 드러나게.
```

### Performance diagnosis

```text
이 글 왜 약했는지 분석해줘.
후킹, topic ceiling, protagonist, close 기준으로.
```

## Standard output shape

For serious requests, Claude should return these sections in order:

1. `추천 주제 / 각도`
2. `왜 지금 이건지`
3. `검증 A 결과`
4. `검증 B 결과`
5. `최종 정합성 판단`
6. `관심도 / 구조 점검`
7. `7슬라이드 초안`
8. `핵심 근거 3개`
9. `추천 커버 / 스샷 아이디어`
10. `팩트체크 리스크`

## Double-check rule

The workflow is now designed so that:

1. one verifier checks source accuracy,
2. a second verifier checks the same topic independently,
3. a reconciler decides what survives,
4. a structural-interest review checks whether the framing is actually likely to attract broad attention.

If the two verifiers disagree on a core fact, that claim should not pass through silently.

If the interest review says the topic is structurally weak, the system should recommend changing the angle instead of forcing a draft.

## Review loop

Typical review replies:

- `이걸로 가자`
- `후킹만 다시`
- `너무 결론 빨리 나옴`
- `팩트 다시 봐`
- `Anthropic 또 나와서 피로함. 다른 topic으로`

Claude should treat these as direct editing instructions, not as invitations to restart the whole topic unless asked.

## Reference usage rule

Reference files are there to learn:

- hook shapes,
- pacing,
- reversal placement,
- close patterns,
- what low-ceiling topics look like.

Reference files are not there to be paraphrased line by line.

## File map

- `SOUL.md`: account identity and editorial rules
- `docs/DIRECT_CLAUDE_WORKFLOW.md`: direct creation pipeline
- `docs/PIPELINE_ARCHITECTURE_V1.md`: enforced dual-verification architecture
- `prompts/THREADS_PIPELINE_PROMPTS.md`: reusable prompt chain
- `schemas/thread_run_output.json`: structured output target
- `references/README.md`: reference ingestion and retrieval rules
- `DEPLOY.md`: remote OpenClaw flow
