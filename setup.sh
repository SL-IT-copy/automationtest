#!/bin/bash
set -e

echo "============================================"
echo "  Threads 자동화 — OpenClaw 설정 스크립트"
echo "============================================"
echo ""

OPENCLAW_HOME="$HOME/.openclaw"
SKILL_DIR="$OPENCLAW_HOME/skills/threads-poster"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── 1. 전제조건 확인 ──────────────────────────

echo "[1/7] 전제조건 확인..."

if ! command -v python3 &>/dev/null; then
    echo "❌ python3이 설치되어 있지 않습니다."
    echo "   brew install python3 또는 https://python.org 에서 설치하세요."
    exit 1
fi

if ! command -v pip3 &>/dev/null; then
    echo "❌ pip3이 설치되어 있지 않습니다."
    echo "   python3 -m ensurepip --upgrade 실행하세요."
    exit 1
fi

if ! command -v curl &>/dev/null; then
    echo "❌ curl이 설치되어 있지 않습니다."
    exit 1
fi

echo "   ✅ python3, pip3, curl 확인 완료"

# ── 2. Python 의존성 설치 ─────────────────────

echo "[2/7] Python 의존성 설치..."
pip3 install --quiet requests python-dotenv
echo "   ✅ requests, python-dotenv 설치 완료"

# ── 3. OpenClaw 확인 ─────────────────────────

echo "[3/7] OpenClaw 확인..."

if command -v openclaw &>/dev/null; then
    echo "   ✅ OpenClaw 이미 설치됨"
else
    echo "   ⚠️  OpenClaw가 설치되어 있지 않습니다."
    echo ""
    read -p "   지금 설치하시겠습니까? (y/n): " install_openclaw
    if [[ "$install_openclaw" == "y" || "$install_openclaw" == "Y" ]]; then
        echo "   OpenClaw 설치 중..."
        curl -fsSL https://openclaw.ai/install.sh | bash
        echo "   ✅ OpenClaw 설치 완료"
    else
        echo "   ⏭️  건너뜀 — 나중에 수동 설치하세요: curl -fsSL https://openclaw.ai/install.sh | bash"
    fi
fi

# ── 4. 스킬 복사 ────────────────────────────

echo "[4/7] threads-poster 스킬 설치..."

mkdir -p "$SKILL_DIR/scripts"
cp "$SCRIPT_DIR/skills/threads-poster/SKILL.md" "$SKILL_DIR/SKILL.md"
cp "$SCRIPT_DIR/skills/threads-poster/scripts/threads_api.py" "$SKILL_DIR/scripts/threads_api.py"

echo "   ✅ 스킬 설치 완료: $SKILL_DIR"

# ── 5. SOUL.md 복사 ─────────────────────────

echo "[5/7] SOUL.md 복사..."

if [[ -f "$OPENCLAW_HOME/SOUL.md" ]]; then
    echo "   ⚠️  SOUL.md가 이미 존재합니다. 덮어쓰지 않습니다."
    echo "   필요하면 수동 복사: cp $SCRIPT_DIR/SOUL.md $OPENCLAW_HOME/SOUL.md"
else
    cp "$SCRIPT_DIR/SOUL.md" "$OPENCLAW_HOME/SOUL.md"
    echo "   ✅ SOUL.md 복사 완료"
    echo "   ⚠️  반드시 $OPENCLAW_HOME/SOUL.md를 본인에 맞게 수정하세요!"
fi

# ── 6. 크레덴셜 확인 ────────────────────────

echo "[6/7] Threads API 크레덴셜 확인..."

ENV_FILE="$OPENCLAW_HOME/.env"

if [[ -f "$ENV_FILE" ]] && grep -q "THREADS_ACCESS_TOKEN" "$ENV_FILE"; then
    echo "   ✅ Threads 크레덴셜이 이미 설정되어 있습니다."
else
    echo "   ⚠️  Threads API 크레덴셜이 설정되지 않았습니다."
    echo ""
    echo "   다음 중 하나를 선택하세요:"
    echo "   (1) 지금 토큰 입력"
    echo "   (2) 나중에 수동 설정 (SETUP_GUIDE.md 참고)"
    echo ""
    read -p "   선택 (1/2): " cred_choice

    if [[ "$cred_choice" == "1" ]]; then
        echo ""
        read -p "   THREADS_ACCESS_TOKEN: " threads_token
        read -p "   THREADS_USER_ID: " threads_user_id

        if [[ -n "$threads_token" && -n "$threads_user_id" ]]; then
            touch "$ENV_FILE"
            echo "export THREADS_ACCESS_TOKEN='$threads_token'" >> "$ENV_FILE"
            echo "export THREADS_USER_ID='$threads_user_id'" >> "$ENV_FILE"
            echo "   ✅ 크레덴셜 저장 완료: $ENV_FILE"
        else
            echo "   ❌ 값이 비어있습니다. 나중에 수동 설정하세요."
        fi
    else
        echo "   ⏭️  건너뜀 — SETUP_GUIDE.md를 참고하여 수동 설정하세요."
    fi
fi

# ── 7. 연결 테스트 ──────────────────────────

echo "[7/7] 연결 테스트..."

if [[ -f "$ENV_FILE" ]] && grep -q "THREADS_ACCESS_TOKEN" "$ENV_FILE"; then
    source "$ENV_FILE" 2>/dev/null || true
    if python3 "$SKILL_DIR/scripts/threads_api.py" profile 2>/dev/null; then
        echo ""
        echo "   ✅ Threads API 연결 성공!"
    else
        echo "   ⚠️  API 연결 실패 — 토큰을 확인하세요."
    fi
else
    echo "   ⏭️  크레덴셜 미설정 — 테스트 건너뜀"
fi

# ── 완료 ─────────────────────────────────────

echo ""
echo "============================================"
echo "  설치 완료!"
echo "============================================"
echo ""
echo "다음 단계:"
echo ""
echo "  1. SOUL.md 수정: nano $OPENCLAW_HOME/SOUL.md"
echo "     → 콘텐츠 필러(주제)를 본인에 맞게 채우세요"
echo ""
echo "  2. 크론잡 설정 (DEPLOY.md의 Step 5 참고):"
echo "     → openclaw cron add threads-daily ..."
echo ""
echo "  3. Telegram 봇 설정 (아직 안 했으면):"
echo "     → DEPLOY.md의 Step 2 참고"
echo ""
echo "  4. 테스트: Telegram에서 봇에게 '내 Threads 프로필 보여줘'"
echo ""
