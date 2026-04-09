이 프로젝트는 JSup(@jisang0914)의 한국어 AI/테크 Threads 콘텐츠 생성 파이프라인임.

## 세션 시작 시 반드시 읽을 파일

1. `AGENTS.md` — 전체 운영 규칙, 파일 책임, hard boundaries
2. `CLAUDE.md` — Claude/OpenCode 세션 로더
3. `SOUL.md` — 계정 정체성, 보이스, hook 규칙, 포맷 규칙
4. `config/pipeline.yaml` — 기계적으로 읽는 파이프라인 설정
5. `config/sources.yaml` — 소스 우선순위
6. `config/xactions.yaml` — X 검색 설정
7. `config/autosave.yaml` — 자동 저장 규칙
8. relevant files in `checklists/` — hook / fact / pacing / final gate
9. `prompts/THREADS_PIPELINE_PROMPTS.md` — 11단계 프롬프트 체인
10. `references/reference_index.json` — 고성과 레퍼런스 인덱스
11. recent files in `content/published/` and `memory/cold/`

레퍼런스를 읽을 때는 `references/parsed/` 디렉토리의 실제 텍스트도 함께 읽을 것.
특히 상위 성과 글(306k, 215k, 201k, 200k, 109k)의 hook 구조, 줄바꿈 리듬, 반전 위치, 마감 패턴을 파악해둘 것.

## 핵심 운영 규칙

- 글 생성은 여기 Claude 세션 안에서 직접 수행
- OAuth는 Threads 게시/인증용. 콘텐츠 생성과는 무관
- `config/source_catalog.json`에 라이브 소스 목록 있음
- X 검색은 `scripts/x-search.sh`를 canonical entrypoint로 사용

## 강제 검증 체크리스트 (모든 실제 thread 요청에 적용)

글 생성 요청이 들어오면, 아래 순서를 반드시 따를 것.
순서를 건너뛰거나 축약하지 말 것.

### Step 0: 중복 / 피로도 체크
- `content/covered_topics.json` 확인
- 최근 2포스트와 같은 회사 / 같은 앵글이면 기본적으로 회피
- materially new angle 아니면 topic scout 단계에서 제외

### Step 1: 소스 수집
- web search로 현재 시점 소스 최소 3개 확보
- 가능하면 1차 출처(공식 블로그, 공식 발표, 원문 보도) 우선

### Step 2: 팩트팩 구성
- 핵심 사실을 claim / source / date / quote 형태로 정리
- 출처 없는 claim은 해석(interpretation)으로 분류하거나 제거

### Step 3: 검증 A
- 보수적 관점에서 팩트팩 감사
- stale 수치, mixed quarter, 근거 부족, 인과관계 과장 체크
- 결과: verified / caution / reject 판정

### Step 4: 검증 B
- A와 독립적으로 같은 팩트팩 재감사
- A가 놓칠 수 있는 반증, 출처 위계 문제, 숨은 모호성 체크
- 결과: verified / caution / reject 판정

### Step 5: 정합성 조정 (Reconciliation)
- A와 B 결과 비교
- 일치하면 유지
- 핵심 사실에서 충돌하면 disputed 표기 — 초안에 그냥 넣지 않음
- 최종 publishability 판정: pass / caution / fail

### Step 6: 구조/관심도 점검
- hook이 인지 부조화를 만드는가
- protagonist / antagonist 또는 승자 / 패자가 있는가
- 반전이나 escalation이 있는가
- broad audience ceiling이 충분한가
- same-company fatigue 리스크는 없는가
- 결과: proceed / revise_angle / abandon_topic

### Step 7: 레퍼런스 참조
- references/parsed/ 에서 가장 가까운 고성과 글 2~3개 읽기
- hook 패턴, 줄바꿈 리듬, 반전 위치, 마감 스타일만 참고
- 문장을 복사하지 않음

### Step 8: 초안 작성
- SOUL.md의 voice, formatting, quality gates 전부 적용
- 코드블록으로 슬라이드별 전달 (클릭 한 번 복사)
- 한 줄 14~20자 기준, 마침표에서 줄 끝, 길면 의미 단위 엔터
- 인물 인용 시 누구인지 한 줄 설명 또는 이름 생략
- 전문용어 풀어쓰기

### Step 9: 결과물 출력
아래 10개 섹션을 순서대로 빠짐없이 포함:

1. 추천 주제 / 각도
2. 왜 지금 이건지
3. 검증 A 결과
4. 검증 B 결과
5. 최종 정합성 판단
6. 관심도 / 구조 점검
7. 7슬라이드 초안 (코드블록, 슬라이드별)
8. 핵심 근거 (전체 URL 포함)
9. 추천 커버 / 스샷 아이디어 (전체 URL 포함)
10. 팩트체크 리스크

### Step 10: 자기 점검
초안 완성 후, 아래 체크리스트를 스스로 확인:

- [ ] 출처 없는 핵심 사실이 초안에 남아있지 않은가?
- [ ] 검증 A/B가 충돌한 사실이 초안에 그냥 들어가지 않았는가?
- [ ] 한 줄이 20자를 크게 넘는 곳은 없는가?
- [ ] 한 줄이 4~5자 미만으로 너무 짧은 곳은 없는가?
- [ ] 인물 이름이 설명 없이 등장하지 않는가?
- [ ] 전문용어가 풀어쓰기 없이 남아있지 않은가?
- [ ] 링크가 잘리거나 생략되지 않았는가?
- [ ] 코드블록으로 전달되어 클릭 복사가 가능한가?
- [ ] 이 글을 처음 보는 사람이 팔로우하고 싶어질 만한가?
- [ ] 이 주제가 구조적으로 100k+ 뷰를 넘을 수 있는가?

하나라도 실패하면 해당 부분을 수정한 뒤 최종본을 낼 것.
