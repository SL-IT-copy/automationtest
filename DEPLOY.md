# 별도 맥에 OpenClaw + Threads 자동화 배포

이 가이드를 따라 별도 맥(서버)에 OpenClaw를 설치하고,
자동으로 Threads 콘텐츠를 생성 → Telegram으로 리뷰 요청 → 승인 시 자동 게시 파이프라인을 구축합니다.

---

## 전제조건

- macOS가 설치된 별도 Mac (24시간 켜둘 수 있는 것)
- 인터넷 연결
- Anthropic API 키 (https://console.anthropic.com 에서 발급)
- Threads 계정 (Instagram 계정 필요)
- Telegram 계정

## Step 0: 이 프로젝트를 별도 맥으로 옮기기

아래 중 편한 방법 하나 선택:

**방법 A: AirDrop (가장 간단)**
1. Finder에서 `threadautomationplan` 폴더 우클릭 → 압축
2. AirDrop으로 별도 맥에 전송
3. 별도 맥에서 압축 풀기

**방법 B: USB/외장 드라이브**
1. USB에 `threadautomationplan` 폴더 복사
2. 별도 맥에 붙여넣기

**방법 C: GitHub (권장 — 버전관리 가능)**
```bash
# 현재 맥에서
cd threadautomationplan
git init && git add -A && git commit -m "initial setup"
gh repo create threads-automation --private --source=. --push

# 별도 맥에서
git clone https://github.com/YOUR_USERNAME/threads-automation.git
cd threads-automation
```

**방법 D: scp (네트워크)**
```bash
# 현재 맥에서 (별도 맥의 IP를 알 때)
scp -r threadautomationplan user@REMOTE_MAC_IP:~/
```

별도 맥에 프로젝트가 옮겨졌으면 다음 단계로.

## Step 0.5: 자동 설치 (setup.sh)

별도 맥에서 프로젝트 폴더로 이동 후:

```bash
cd threadautomationplan
./setup.sh
```

이 스크립트가 자동으로:
- Python 의존성 설치
- OpenClaw 설치 (없으면)
- threads-poster 스킬 복사
- SOUL.md 복사
- 크레덴셜 입력 안내
- 연결 테스트

**setup.sh가 모두 완료되면 Step 2(Telegram)부터 진행하세요.**
수동으로 하나씩 하고 싶으면 아래 Step 1부터 따라하세요.

---

## 전체 플로우

```
[별도 맥 - 24시간 실행]

OpenClaw (크론으로 자동 실행)
  ├─ 매일 아침: 트렌드 리서치 + 콘텐츠 초안 생성
  ├─ Telegram으로 초안 전송 → 사용자 리뷰
  ├─ 사용자 "올려줘" → Threads API로 자동 게시
  └─ 매주 금요일: 성과 분석 리포트 전송
         │
         ▼
  [내 폰의 Telegram] ← 여기서 리뷰/승인
```

---

## Step 1: OpenClaw 설치 (별도 맥에서)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

설치 중 선택사항:
- **LLM**: Anthropic Claude 선택 → API 키 입력
- **Chat Channel**: Telegram 선택

## Step 2: Telegram 봇 설정

### 2.1 봇 생성

1. Telegram에서 **@BotFather** 검색
2. `/newbot` 입력
3. 봇 이름 입력 (예: "My Threads Bot")
4. **Bot Token** 복사 (형식: `123456:ABC-DEF...`)

### 2.2 Chat ID 확인

1. 방금 만든 봇에게 아무 메시지 보내기
2. 브라우저에서 열기:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
3. 응답에서 `"chat":{"id": 123456789}` 확인 → 이것이 Chat ID

### 2.3 OpenClaw에 Telegram 연결

OpenClaw 설치 시 Telegram을 선택했으면 자동 설정됨.
수동 설정이 필요하면:

```bash
openclaw channel configure telegram
# Bot Token과 Chat ID 입력
```

## Step 3: Threads API 크레덴셜 설정

`SETUP_GUIDE.md`를 따라 Meta 앱 생성 & 토큰 발급 후:

```bash
# OpenClaw 환경변수에 추가
cat >> ~/.openclaw/.env << 'EOF'
export THREADS_ACCESS_TOKEN='your_long_lived_token'
export THREADS_USER_ID='your_threads_user_id'
EOF
```

## Step 4: 스킬 & 스크립트 설치

### 4.1 필요 스킬 설치

```bash
openclaw skill install web-search
```

### 4.2 커스텀 스킬 복사

이 프로젝트의 스킬 파일을 OpenClaw 스킬 디렉토리로 복사:

```bash
# threads-poster 스킬 복사
cp -r skills/threads-poster ~/.openclaw/skills/

# Python 의존성 설치
pip3 install requests python-dotenv
```

### 4.3 SOUL.md 복사

```bash
cp SOUL.md ~/.openclaw/SOUL.md
```

SOUL.md를 본인의 콘텐츠 주제에 맞게 수정하세요.

## Step 5: 크론잡 설정 (자동화 파이프라인)

### 5.1 매일 아침 — 트렌드 리서치 + 콘텐츠 생성

```bash
openclaw cron add threads-daily \
  --cron "0 8 * * 1-5" \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "오늘 Threads에 올릴 콘텐츠를 준비해줘.

1단계 - 리서치:
- web-search로 내 콘텐츠 필러 관련 오늘의 트렌드 조사
- 인기 있는 Threads 토픽 확인

2단계 - 초안 작성:
- SOUL.md 가이드라인에 맞춰 포스트 2개 초안 작성
- 각 초안에 추천 게시 시간과 토픽 태그 포함
- threads-poster 스킬의 승인 워크플로 형식으로 제시

내가 리뷰하고 승인하면 그때 올려줘." \
  --channel telegram
```

### 5.2 인게이지먼트 체크 (선택)

```bash
openclaw cron add threads-engagement \
  --cron "0 18 * * 1-5" \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "오늘 올린 Threads 포스트 성과를 확인해줘.
threads-poster 스킬로 최근 게시물 인사이트를 조회하고,
답글이 달렸으면 답글 초안도 제안해줘.
특이사항 없으면 메시지 보내지 마." \
  --channel telegram
```

### 5.3 주간 분석 리포트

```bash
openclaw cron add threads-weekly \
  --cron "0 17 * * 5" \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "이번 주 Threads 성과 분석 리포트를 만들어줘.
threads-poster 스킬의 주간 분석 리포트 형식으로 작성.
최고/최저 성과 포스트, 트렌드, 다음 주 추천 포함." \
  --channel telegram
```

### 5.4 토큰 자동 갱신 (45일마다)

```bash
openclaw cron add token-refresh \
  --every 45d \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "Threads 액세스 토큰을 갱신해줘.
python3 ~/.openclaw/skills/threads-poster/scripts/threads_api.py refresh-token 실행.
결과를 알려줘." \
  --channel telegram
```

## Step 6: 테스트

### 수동 테스트

```bash
# OpenClaw에 직접 메시지 보내기
openclaw chat "내 Threads 프로필 정보 보여줘"
```

또는 Telegram에서 봇에게:
```
Threads 프로필 확인해줘
```

### 크론잡 확인

```bash
openclaw cron list
```

## Step 7: 맥이 꺼지지 않게 설정

### 자동 로그인 + 잠자기 방지

1. **시스템 설정 → 에너지 절약**
   - "디스플레이가 꺼진 상태에서도 자동 잠자기 방지" 체크
   - 또는 `caffeinate` 사용:
   ```bash
   caffeinate -s &
   ```

2. **OpenClaw 자동 시작** (재부팅 시)
   ```bash
   # LaunchAgent 등록
   cat > ~/Library/LaunchAgents/com.openclaw.gateway.plist << 'EOF'
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
     <key>Label</key>
     <string>com.openclaw.gateway</string>
     <key>ProgramArguments</key>
     <array>
       <string>/usr/local/bin/openclaw</string>
       <string>start</string>
     </array>
     <key>RunAtLoad</key>
     <true/>
     <key>KeepAlive</key>
     <true/>
     <key>StandardOutPath</key>
     <string>/tmp/openclaw.log</string>
     <key>StandardErrorPath</key>
     <string>/tmp/openclaw-error.log</string>
   </dict>
   </plist>
   EOF

   launchctl load ~/Library/LaunchAgents/com.openclaw.gateway.plist
   ```

---

## 일상 사용법

모든 상호작용은 **Telegram**에서:

| 상황 | 하는 일 |
|------|---------|
| 아침에 초안 도착 | 읽고 "올려줘" 또는 "수정해줘: [내용]" |
| 즉석 포스트 | "이것에 대한 스레드 써줘: [주제]" |
| 성과 궁금 | "오늘 포스트 성과 어때?" |
| 아이디어 | "이 주제로 포스트 3개 초안 만들어줘" |
| 토큰 문제 | "토큰 갱신해줘" |

### 승인 플로우 예시

```
🤖 봇:
🧵 Threads 초안

📝 내용:
GPT-5 발표 후 24시간이 지났다.

솔직한 감상: 데모는 인상적이었지만,
실제로 내 작업 방식을 바꿀 건 "커스텀 에이전트" 기능이다.

코딩보다 "지시"가 중요한 시대가 진짜 온 것 같다.

여러분은 어떤 기능이 가장 기대되나요?

🏷️ 태그: AI
📊 유형: 트렌드 코멘터리
⏰ 추천: 오늘 09:00

✅ 승인하시면 "올려줘"라고 답해주세요

👤 나: 올려줘

🤖 봇: ✅ 게시 완료! Post ID: 12345678
```

---

## 문제 해결

| 문제 | 해결 |
|------|------|
| 봇이 메시지 안 보냄 | `openclaw status` 확인, Gateway 재시작 |
| API 에러 | `python3 scripts/threads_api.py profile` 로 토큰 유효 확인 |
| 크론잡 안 돌아감 | `openclaw cron list`로 확인, `openclaw cron logs` |
| 토큰 만료 | Telegram에서 "토큰 갱신해줘" |
| 맥 재부팅 후 | LaunchAgent가 자동 시작 (Step 7 설정 시) |
