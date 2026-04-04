---
name: threads-poster
description: "Threads 콘텐츠 자동화 — 트렌드 리서치, 콘텐츠 생성, 리뷰 승인, 자동 게시. 사용 시점: (1) Threads 포스트 작성/게시 요청, (2) 트렌드 기반 콘텐츠 제안, (3) 게시물 성과 분석, (4) 콘텐츠 캘린더 관리"
metadata:
  openclaw:
    emoji: "🧵"
    requires:
      bins: ["python3", "curl"]
      os: ["linux", "darwin"]
---

# Threads 콘텐츠 자동화 스킬

Threads Graph API를 통해 콘텐츠를 생성하고 게시하는 스킬.
트렌드 리서치 → 초안 작성 → 사용자 승인 → 자동 게시 파이프라인.

## 환경 설정

### 필수 환경변수

`~/.openclaw/.env`에 설정:

```bash
export THREADS_ACCESS_TOKEN='your_long_lived_token'
export THREADS_USER_ID='your_threads_user_id'
```

### 선택 환경변수

```bash
export IMGUR_CLIENT_ID='your_imgur_client_id'  # 로컬 이미지 업로드용
```

## 콘텐츠 작성 규칙 (반드시 준수)

1. **500자 이내** (Threads 제한)
2. **첫 줄 = 훅** (숫자, 질문, 과감한 주장 중 택1)
3. **토픽 태그 1개** 반드시 포함 (마지막 줄)
4. **구체적 데이터/경험** 사용 — 막연한 표현 금지
5. **인게이지먼트 미끼 금지** ("좋아요 눌러주세요" 등)
6. **외부 링크는 본문에 넣지 않기** — 필요시 첫 답글에

### 포맷 우선순위 (인게이지먼트율 기준)
- 비디오 (5.55%) > 이미지 (4.55%) > 텍스트 (2.79%) > 링크 (2.34%)
- 가능하면 이미지를 동반할 것

### 포스트 유형 (로테이션)
1. 핫테이크 — 의견/관점, 대화 유도
2. 질문형 — 오픈 질문으로 답글 유도
3. 팁/방법론 — 실용적 가치 제공
4. 개인 이야기 — 구체적 경험, 진정성
5. 트렌드 코멘터리 — 뉴스에 내 관점 추가

## 게시 워크플로

### 텍스트 게시

```bash
python3 scripts/threads_api.py post --text "게시물 내용" --tag "토픽태그"
```

### 이미지 게시

```bash
python3 scripts/threads_api.py post --text "캡션" --image "https://public-url.com/img.jpg" --tag "태그"
```

### 캐러셀 게시 (2~20장)

```bash
python3 scripts/threads_api.py post --text "캡션" --images "url1,url2,url3" --tag "태그"
```

### 프로필 확인

```bash
python3 scripts/threads_api.py profile
```

### 최근 게시물 확인

```bash
python3 scripts/threads_api.py list --limit 5
```

### 게시물 인사이트

```bash
python3 scripts/threads_api.py insights --post-id "POST_ID"
```

### 게시 한도 확인

```bash
python3 scripts/threads_api.py quota
```

### 토큰 갱신

```bash
python3 scripts/threads_api.py refresh-token
```

## 승인 워크플로 (중요)

**절대 사용자 승인 없이 게시하지 말 것.**

1. 콘텐츠 초안을 사용자에게 보여준다
2. 다음 형식으로 제시:

```
🧵 Threads 초안

📝 내용:
[게시물 텍스트]

🏷️ 태그: [토픽태그]
📊 유형: [핫테이크/질문형/팁/이야기/트렌드]
⏰ 추천 게시 시간: [시간]

✅ 승인하시면 "올려줘"라고 답해주세요
✏️ 수정이 필요하면 알려주세요
```

3. 사용자가 승인하면 게시 실행
4. 게시 후 결과 (Post ID, 성공 여부) 보고

## 트렌드 리서치 방법

web-search 스킬을 사용해:
1. 사용자의 콘텐츠 필러 관련 최신 뉴스 검색
2. Threads에서 인기 토픽 확인
3. 경쟁 계정 최근 포스트 분석
4. 결과를 간결한 브리핑으로 정리

## 최적 게시 시간 (KST)

- 목요일 09:00 (전체 1위)
- 화~금 09:00~12:00 (피크)
- 저녁 18시 이후 피하기

## 주간 분석 리포트 형식

```
📈 주간 Threads 분석

📊 이번 주 성과:
- 총 게시: N개
- 최고 성과 포스트: [내용 요약] (좋아요 N, 답글 N)
- 최저 성과 포스트: [내용 요약] — 원인: [분석]

📈 트렌드: [개선/하락/안정]
💡 다음 주 추천: [전략 1가지]
```

## 에러 처리

- API 에러 시: 에러 메시지를 사용자에게 전달, 자동 재시도하지 않기
- 토큰 만료 시: 사용자에게 갱신 필요 알림
- 레이트 리밋 시: 남은 한도 확인 후 사용자에게 보고
