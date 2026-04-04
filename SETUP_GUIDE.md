# Threads API 초기 설정 가이드

이 가이드를 한 번만 따라하면 OpenClaw(또는 Claude Code)에서 Threads에 게시할 수 있습니다.

## Step 1: Meta 개발자 앱 생성

1. https://developers.facebook.com 접속 → 로그인
2. **My Apps** → **Create App**
3. Use case: **Other** 선택
4. App type: **Business** 선택
5. 앱 이름 입력 (예: "My Threads Bot")

## Step 2: Threads API 제품 추가

1. 앱 대시보드 → **Add Product** → **Threads API** 선택
2. **Settings** → App ID와 App Secret 메모

## Step 3: 액세스 토큰 발급

### 개발용 (즉시 사용 가능, 자기 계정만)

1. https://developers.facebook.com/tools/explorer/ 접속
2. 상단에서 만든 앱 선택
3. **Permissions** 에서 추가:
   - `threads_basic`
   - `threads_content_publish`
   - `threads_manage_insights`
4. **Generate Access Token** 클릭
5. Threads 계정 로그인 & 권한 허용
6. 발급된 토큰 복사 (이것이 short-lived token)

### 장기 토큰으로 교환 (60일 유효)

터미널에서 실행:

```bash
curl -s "https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=YOUR_APP_SECRET&access_token=YOUR_SHORT_TOKEN"
```

응답에서 `access_token` 값이 장기 토큰입니다.

## Step 4: User ID 확인

```bash
curl -s "https://graph.threads.net/v1.0/me?access_token=YOUR_LONG_TOKEN" | python3 -m json.tool
```

응답의 `id` 값이 Threads User ID입니다.

## Step 5: 프로젝트에 크레덴셜 저장

```bash
cp config/.env.example config/.env
```

`config/.env` 파일을 열고 실제 값으로 교체:

```
THREADS_ACCESS_TOKEN=여기에_장기_토큰
THREADS_USER_ID=여기에_유저_ID
```

## Step 6: 테스트

```bash
pip install -r requirements.txt
python scripts/threads_api.py profile
```

프로필 정보가 출력되면 설정 완료!

## 토큰 갱신 (60일마다)

토큰 만료 전에 실행:

```bash
python scripts/threads_api.py refresh-token
```

자동으로 `config/.env` 파일이 업데이트됩니다.

## 프로덕션 (타인 계정 게시 시에만 필요)

자기 계정에만 게시한다면 앱 리뷰 불필요. 타인 계정 게시가 필요한 경우:

1. 앱 대시보드 → **App Review** → 각 권한별 제출
2. 스크린캐스트 녹화 필요 (각 권한의 사용 흐름 시연)
3. 심사 기간: 2~4주

## (선택) Imgur 이미지 호스팅

Threads API는 공개 URL의 이미지만 받습니다. 로컬 이미지를 올리려면:

1. https://api.imgur.com/oauth2/addclient 에서 앱 등록
2. **Client ID** 발급
3. `config/.env`에 추가:
   ```
   IMGUR_CLIENT_ID=여기에_클라이언트_ID
   ```
