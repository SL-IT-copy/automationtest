# Trigger Commands

Use these directly in Claude sessions.

These are not external API commands.
These are the actual in-session triggers for the workflow.

## 1. Full thread pack

```text
Anthropic 최신 이슈 글 써줘.
출처는 두 개 검증 에이전트가 따로 보고,
서로 안 맞는 건 정리한 뒤,
사람들이 구조적으로 관심 가질 만한지까지 체크해서
7슬라이드 초안 + 핵심 근거 + 추천 커버 스샷까지 한 번에 줘.
```

## 2. Topic scout first

```text
오늘 쓸 만한 AI 주제 3개만 골라줘.
출처는 이중 검증하고,
각 주제마다 viral ceiling이랑 same-company fatigue 리스크도 같이 줘.
```

## 3. Same topic, stronger framing

```text
이 topic 유지.
출처 다시 이중 검증하고,
후킹 더 세게,
결론은 덜 빨리 드러나게 다시 써줘.
```

## 4. Existing draft diagnosis

```text
이 초안 검토해줘.
출처 이중 검증,
정합성 확인,
그리고 이 구조가 왜 약한지까지 말해줘.
```

## Expected output shape

For a serious request, the result should contain:

1. 추천 주제 / 각도
2. 왜 지금 이건지
3. 검증 A 결과
4. 검증 B 결과
5. 최종 정합성 판단
6. 관심도 / 구조 점검
7. 7슬라이드 초안
8. 핵심 근거
9. 추천 커버 / 스샷 아이디어
10. 팩트체크 리스크
