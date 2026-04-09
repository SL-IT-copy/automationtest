# Mercor 데이터 유출 — 4만 명의 얼굴, 음성, 신분증

- date: 2026-04-06
- status: published
- sources: https://www.wired.com/story/meta-pauses-work-with-mercor-after-data-breach-puts-ai-industry-secrets-at-risk/, https://fortune.com/2026/04/02/mercor-ai-startup-security-incident-10-billion/, https://www.theregister.com/2026/04/02/mercor_supply_chain_attack/, https://finance.yahoo.com/sectors/technology/article/twin-cybersecurity-incidents-leave-ai-industry-shaken-141850823.html, https://a16z.com/et-tu-agent-did-you-install-the-backdoor, https://www.digitaltoday.co.kr/news/articleView.html?idxno=653598, https://www.tokenpost.kr/news/breaking/346330

## Slides

```
3월 31일.
약 4만 명의 얼굴, 목소리, 이력서, 신분증이
한 폴더에 담겨 있었고
그 폴더가 통째로 새 나갔음.

새 나간 곳은
OpenAI, Anthropic, Meta가
모두 거래해온 그 회사.

기업 가치 14조 원.
```

```
회사 이름 Mercor.
미국 AI 학습 데이터 공급 회사.
계약직 약 4만 명 이상.

OpenAI와 Anthropic이
이 회사한테서 사람의 답변과
사람의 얼굴을 사왔음.

Meta도 작업 중이었음.

"AI가 똑똑해지는 데 쓰인 사람의 말과 영상."
이게 전부 한 곳에 모여 있었음.
```

```
새어 나간 폴더에 들어 있던 것.

영상 면접.
얼굴, 표정, 미세 움직임.
목소리, 억양, 발음.
이력서, 학력, 경력.
신분증 사본.

진짜 사람의 진짜 얼굴과 음성을
대규모로 라벨링해둔 데이터셋.

딥페이크 학습용으로
바로 쓸 수 있는 형태.
```

```
어떻게 새어 나갔는가.

해커 그룹 TeamPCP의
2단계 공급망 공격.

1단계: Trivy.
전 세계 개발자가 보안 점검에 쓰는
오픈소스 보안 스캐너.
이걸 먼저 감염시킴.

2단계: LiteLLM.
AI 회사들이 여러 모델을
갈아끼울 때 쓰는 오픈소스 라이브러리.
감염된 Trivy를 통해 악성 코드 삽입.

Mercor는 LiteLLM을 쓰고 있었음.

세계 개발자가 신뢰하던 보안 도구가
그 신뢰로
회사를 뚫은 사건.
```

```
가장 먼저 움직인 건 Meta.
Mercor와의 모든 작업을
무기한 중단한다고 발표.

같은 주.
실리콘밸리에서 가장 큰
AI 투자 회사를 만든 Marc Andreessen이
X에 글을 올림.

"이번 주에 Anthropic 코드 유출.
지금 Mercor 유출.
'AI 안전'을 '잠가두면 된다'는 식으로 하던 시대는
완전히 죽었다."
```

```
이게 한국이랑 무슨 상관이냐.

지난주 한국 X 사용자가 올린 글에
좋아요 1,500개.

"Mercor 시험만 응시했는데도
22만원 입금받음.
온라인 AI 부업 추천."

한국에서도 이 회사에
얼굴, 목소리, 이력서, 신분증을
이미 넘긴 사람들이 있다는 뜻.

그 사람들 데이터도
같은 폴더 안에 있을 가능성.
```

```
"AI는 데이터로 똑똑해진다"
는 말의 진짜 의미.

4만 명이 자기 얼굴과 목소리를
일자리 대가로 회사에 넘겼고,
그 회사는 보안에 실패했고,
그 데이터는 지금 어딘가에 떠 있음.

AI 안전 논의가 모델 안전을 말하는 동안
사람의 얼굴이 새 나가고 있음.

🔗 https://fortune.com/2026/04/02/mercor-ai-startup-security-incident-10-billion/

AI 업계 흐름, 계속 정리해서 올릴 예정.
팔로우 해두면 놓치지 않음.
```
