이 프로젝트는 JSup(@jisang0914)의 한국어 AI/테크 Threads 콘텐츠 생성 파이프라인임.

세션 시작 시 반드시 아래 파일들을 읽고 숙지할 것:

1. `SOUL.md` — 계정 정체성, 채널 원칙, hook 규칙, topic 피로도 규칙
2. `WORKFLOW.md` — 작동 방식, 트리거 명령어, 출력 형식
3. `docs/DIRECT_CLAUDE_WORKFLOW.md` — 전체 파이프라인 흐름
4. `docs/TRIGGER_COMMANDS.md` — 사용 가능한 트리거 명령어
5. `prompts/THREADS_PIPELINE_PROMPTS.md` — 11단계 프롬프트 체인
6. `references/reference_index.json` — 고성과 레퍼런스 인덱스

핵심 운영 규칙:

- 글 생성은 여기 Claude 세션 안에서 직접 수행
- 모든 serious request는 이중 검증(Verifier A + B) → 정합성 조정 → 구조/관심도 리뷰 후 초안 생성
- 출처 없는 핵심 사실은 초안에 넣지 않음
- 결과물은 항상 10개 섹션 포함: 추천 주제, 왜 지금, 검증A, 검증B, 정합성, 구조점검, 초안, 근거, 커버 추천, 리스크
- OAuth는 Threads 게시/인증용. 콘텐츠 생성과는 무관
- `config/source_catalog.json`에 라이브 소스 목록 있음 (HN, Reddit, Anthropic, OpenAI, arXiv 등)
- `references/parsed/`에 고성과 글 텍스트 있음 — 구조/패턴 참고용이지 복사용 아님
