"""
Threads API 래퍼 — OpenClaw 스킬 및 Claude Code에서 호출용

사용법:
    # 텍스트 게시
    python scripts/threads_api.py post --text "게시물 내용" --tag "토픽태그"

    # 이미지 게시
    python scripts/threads_api.py post --text "캡션" --image "https://example.com/img.jpg"

    # 캐러셀 게시 (이미지 2~20장)
    python scripts/threads_api.py post --text "캡션" --images "url1,url2,url3"

    # 프로필 조회
    python scripts/threads_api.py profile

    # 최근 게시물 조회
    python scripts/threads_api.py list

    # 게시물 인사이트
    python scripts/threads_api.py insights --post-id "POST_ID"

    # 게시 한도 확인
    python scripts/threads_api.py quota

    # 토큰 갱신
    python scripts/threads_api.py refresh-token
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OPENCLAW_HOME = Path.home() / ".openclaw"

ENV_SEARCH_PATHS = [
    PROJECT_ROOT / "config" / ".env",
    PROJECT_ROOT / ".env",
    OPENCLAW_HOME / ".env",
    OPENCLAW_HOME / "skills" / "threads-poster" / ".env",
]

for env_path in ENV_SEARCH_PATHS:
    if env_path.exists():
        load_dotenv(env_path)
        break

BASE_URL = "https://graph.threads.net/v1.0"


def get_credentials():
    """환경변수에서 크레덴셜 로드"""
    token = os.getenv("THREADS_ACCESS_TOKEN")
    user_id = os.getenv("THREADS_USER_ID")
    if not token or not user_id:
        print("❌ 크레덴셜이 설정되지 않았습니다.")
        print(
            "   config/.env 파일에 THREADS_ACCESS_TOKEN과 THREADS_USER_ID를 설정하세요."
        )
        print("   설정 가이드: SETUP_GUIDE.md 참고")
        sys.exit(1)
    return token, user_id


def api_request(method, endpoint, params=None, data=None):
    """Threads API 요청 헬퍼"""
    token, _ = get_credentials()
    url = f"{BASE_URL}/{endpoint}"

    if params is None:
        params = {}
    params["access_token"] = token

    try:
        if method == "GET":
            resp = requests.get(url, params=params, timeout=30)
        elif method == "POST":
            resp = requests.post(url, params=params, data=data, timeout=30)
        elif method == "DELETE":
            resp = requests.delete(url, params=params, timeout=30)
        else:
            raise ValueError(f"지원하지 않는 메서드: {method}")

        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"❌ API 에러 ({resp.status_code}):")
            try:
                error_data = resp.json()
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except Exception:
                print(resp.text)
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"❌ 네트워크 에러: {e}")
        sys.exit(1)


# ─────────────────────────────────────────────
# 게시 관련
# ─────────────────────────────────────────────


def create_text_container(
    user_id, text, topic_tag=None, reply_to_id=None, reply_control=None
):
    """텍스트 게시물 컨테이너 생성"""
    params = {
        "media_type": "TEXT",
        "text": text,
    }
    if topic_tag:
        params["topic_tag"] = topic_tag
    if reply_to_id:
        params["reply_to_id"] = reply_to_id
    if reply_control:
        params["reply_control"] = reply_control

    result = api_request("POST", f"{user_id}/threads", params=params)
    return result.get("id")


def create_image_container(
    user_id, text, image_url, topic_tag=None, is_carousel_item=False
):
    """이미지 게시물 컨테이너 생성"""
    params = {
        "media_type": "IMAGE",
        "image_url": image_url,
        "text": text,
    }
    if topic_tag:
        params["topic_tag"] = topic_tag
    if is_carousel_item:
        params["is_carousel_item"] = "true"
        params.pop("text", None)

    result = api_request("POST", f"{user_id}/threads", params=params)
    return result.get("id")


def create_video_container(user_id, text, video_url, topic_tag=None):
    """비디오 게시물 컨테이너 생성"""
    params = {
        "media_type": "VIDEO",
        "video_url": video_url,
        "text": text,
    }
    if topic_tag:
        params["topic_tag"] = topic_tag

    result = api_request("POST", f"{user_id}/threads", params=params)
    return result.get("id")


def create_carousel_container(user_id, text, children_ids, topic_tag=None):
    """캐러셀 게시물 컨테이너 생성"""
    params = {
        "media_type": "CAROUSEL",
        "children": ",".join(children_ids),
        "text": text,
    }
    if topic_tag:
        params["topic_tag"] = topic_tag

    result = api_request("POST", f"{user_id}/threads", params=params)
    return result.get("id")


def publish_container(user_id, container_id):
    """컨테이너 게시 (발행)"""
    params = {"creation_id": container_id}
    result = api_request("POST", f"{user_id}/threads_publish", params=params)
    return result.get("id")


def check_container_status(container_id):
    """컨테이너 처리 상태 확인 (비디오 등)"""
    params = {"fields": "status,error_message"}
    return api_request("GET", container_id, params=params)


def post_text(text, topic_tag=None, reply_to_id=None):
    """텍스트 게시물 발행"""
    _, user_id = get_credentials()

    if len(text) > 500:
        print(f"⚠️  텍스트가 {len(text)}자입니다. Threads 제한은 500자.")
        print("   자동으로 500자에서 자릅니다.")
        text = text[:500]

    print(f"📝 컨테이너 생성 중...")
    container_id = create_text_container(user_id, text, topic_tag, reply_to_id)

    if not container_id:
        print("❌ 컨테이너 생성 실패")
        return None

    print(f"📤 게시 중...")
    post_id = publish_container(user_id, container_id)

    if post_id:
        print(f"✅ 게시 완료!")
        print(f"   Post ID: {post_id}")
        print(f"   내용: {text[:100]}{'...' if len(text) > 100 else ''}")
        if topic_tag:
            print(f"   태그: {topic_tag}")

        save_published(post_id, text, topic_tag)
        return post_id
    return None


def post_image(text, image_url, topic_tag=None):
    """이미지 게시물 발행"""
    _, user_id = get_credentials()

    print(f"🖼️  이미지 컨테이너 생성 중...")
    container_id = create_image_container(user_id, text, image_url, topic_tag)

    if not container_id:
        print("❌ 컨테이너 생성 실패")
        return None

    print("⏳ 미디어 처리 대기 (5초)...")
    time.sleep(5)

    print(f"📤 게시 중...")
    post_id = publish_container(user_id, container_id)

    if post_id:
        print(f"✅ 이미지 게시 완료!")
        print(f"   Post ID: {post_id}")
        save_published(post_id, text, topic_tag, image_url=image_url)
        return post_id
    return None


def post_carousel(text, image_urls, topic_tag=None):
    """캐러셀 게시물 발행 (이미지 2~20장)"""
    _, user_id = get_credentials()

    if len(image_urls) < 2:
        print("❌ 캐러셀은 최소 2장의 이미지가 필요합니다.")
        return None
    if len(image_urls) > 20:
        print("❌ 캐러셀은 최대 20장의 이미지만 가능합니다.")
        return None

    children_ids = []
    for i, url in enumerate(image_urls):
        print(f"🖼️  이미지 {i + 1}/{len(image_urls)} 컨테이너 생성...")
        item_id = create_image_container(user_id, text, url, is_carousel_item=True)
        if item_id:
            children_ids.append(item_id)
        else:
            print(f"❌ 이미지 {i + 1} 컨테이너 생성 실패")
            return None

    print("📦 캐러셀 컨테이너 생성 중...")
    carousel_id = create_carousel_container(user_id, text, children_ids, topic_tag)

    if not carousel_id:
        print("❌ 캐러셀 컨테이너 생성 실패")
        return None

    print("⏳ 미디어 처리 대기 (10초)...")
    time.sleep(10)

    print("📤 게시 중...")
    post_id = publish_container(user_id, carousel_id)

    if post_id:
        print(f"✅ 캐러셀 게시 완료! ({len(image_urls)}장)")
        print(f"   Post ID: {post_id}")
        save_published(post_id, text, topic_tag, image_urls=image_urls)
        return post_id
    return None


# ─────────────────────────────────────────────
# 조회 관련
# ─────────────────────────────────────────────


def get_profile():
    """프로필 정보 조회"""
    _, user_id = get_credentials()
    params = {
        "fields": "id,username,name,threads_profile_picture_url,threads_biography"
    }
    result = api_request("GET", user_id, params=params)

    print("👤 프로필 정보:")
    print(f"   이름: {result.get('name', 'N/A')}")
    print(f"   사용자명: @{result.get('username', 'N/A')}")
    print(f"   바이오: {result.get('threads_biography', 'N/A')}")
    return result


def get_posts(limit=10):
    """최근 게시물 조회"""
    _, user_id = get_credentials()
    params = {
        "fields": "id,text,timestamp,media_type,shortcode,permalink",
        "limit": limit,
    }
    result = api_request("GET", f"{user_id}/threads", params=params)

    posts = result.get("data", [])
    print(f"📋 최근 게시물 ({len(posts)}개):\n")
    for i, post in enumerate(posts, 1):
        text = post.get("text", "(미디어 전용)")
        ts = post.get("timestamp", "")
        media = post.get("media_type", "TEXT")
        permalink = post.get("permalink", "")
        print(f"  {i}. [{media}] {text[:80]}{'...' if len(text) > 80 else ''}")
        print(f"     시간: {ts}")
        print(f"     ID: {post.get('id', '')}")
        if permalink:
            print(f"     링크: {permalink}")
        print()

    return posts


def get_insights(post_id):
    """게시물 인사이트 조회"""
    params = {"metric": "views,likes,replies,reposts,quotes"}
    result = api_request("GET", f"{post_id}/insights", params=params)

    print(f"📊 게시물 인사이트 (ID: {post_id}):\n")
    for metric in result.get("data", []):
        name = metric.get("name", "")
        value = metric.get("values", [{}])[0].get("value", 0)
        print(f"   {name}: {value}")

    return result


def get_quota():
    """게시 한도 확인"""
    _, user_id = get_credentials()
    params = {"fields": "quota_usage,config"}
    result = api_request("GET", f"{user_id}/threads_publishing_limit", params=params)

    data = result.get("data", [{}])[0]
    usage = data.get("quota_usage", 0)
    config = data.get("config", {})
    limit = config.get("quota_total", 250)
    duration = config.get("quota_duration", 86400)

    remaining = limit - usage
    print(f"📊 게시 한도:")
    print(f"   사용: {usage}/{limit} ({duration // 3600}시간 기준)")
    print(f"   남은 횟수: {remaining}")

    return {"used": usage, "limit": limit, "remaining": remaining}


# ─────────────────────────────────────────────
# 토큰 관련
# ─────────────────────────────────────────────


def refresh_token():
    """장기 토큰 갱신 (60일 만료 전에 실행)"""
    token = os.getenv("THREADS_ACCESS_TOKEN")
    if not token:
        print("❌ THREADS_ACCESS_TOKEN이 설정되지 않았습니다.")
        sys.exit(1)

    url = f"{BASE_URL}/refresh_access_token"
    params = {
        "grant_type": "th_refresh_token",
        "access_token": token,
    }

    try:
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            new_token = data.get("access_token")
            expires_in = data.get("expires_in", 0)

            if new_token:
                env_path = PROJECT_ROOT / "config" / ".env"
                if env_path.exists():
                    content = env_path.read_text()
                    content = content.replace(token, new_token)
                    env_path.write_text(content)
                    print(f"✅ 토큰 갱신 완료!")
                    print(f"   만료까지: {expires_in // 86400}일")
                    print(f"   config/.env 파일이 업데이트되었습니다.")
                else:
                    print(f"✅ 새 토큰: {new_token[:20]}...")
                    print(f"   만료까지: {expires_in // 86400}일")
                    print("   ⚠️  config/.env 파일을 직접 업데이트하세요.")
                return new_token
            else:
                print("❌ 토큰 갱신 실패: 응답에 access_token 없음")
        else:
            print(f"❌ 토큰 갱신 실패 ({resp.status_code}):")
            print(resp.text)
    except requests.exceptions.RequestException as e:
        print(f"❌ 네트워크 에러: {e}")

    return None


# ─────────────────────────────────────────────
# 유틸리티
# ─────────────────────────────────────────────


def save_published(post_id, text, topic_tag=None, image_url=None, image_urls=None):
    """게시 완료된 콘텐츠 아카이브"""
    from datetime import datetime

    published_dir = PROJECT_ROOT / "content" / "published"
    published_dir.mkdir(parents=True, exist_ok=True)

    record = {
        "post_id": post_id,
        "text": text,
        "topic_tag": topic_tag,
        "image_url": image_url,
        "image_urls": image_urls,
        "published_at": datetime.now().isoformat(),
    }

    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{post_id}.json"
    filepath = published_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Threads API CLI — Claude Code용")
    subparsers = parser.add_subparsers(dest="command", help="명령어")

    post_parser = subparsers.add_parser("post", help="게시물 발행")
    post_parser.add_argument(
        "--text", "-t", required=True, help="게시물 텍스트 (500자 이내)"
    )
    post_parser.add_argument("--tag", help="토픽 태그 (1개)")
    post_parser.add_argument("--image", help="이미지 URL (단일)")
    post_parser.add_argument("--images", help="이미지 URL 목록 (쉼표 구분, 캐러셀)")
    post_parser.add_argument("--video", help="비디오 URL")
    post_parser.add_argument("--reply-to", help="답글 대상 포스트 ID")

    subparsers.add_parser("profile", help="프로필 조회")

    list_parser = subparsers.add_parser("list", help="최근 게시물 조회")
    list_parser.add_argument("--limit", "-n", type=int, default=10, help="조회 개수")

    insights_parser = subparsers.add_parser("insights", help="게시물 인사이트")
    insights_parser.add_argument("--post-id", required=True, help="게시물 ID")

    subparsers.add_parser("quota", help="게시 한도 확인")

    subparsers.add_parser("refresh-token", help="액세스 토큰 갱신")

    args = parser.parse_args()

    if args.command == "post":
        if args.images:
            urls = [u.strip() for u in args.images.split(",")]
            post_carousel(args.text, urls, args.tag)
        elif args.image:
            post_image(args.text, args.image, args.tag)
        elif args.video:
            _, user_id = get_credentials()
            container_id = create_video_container(
                user_id, args.text, args.video, args.tag
            )
            if container_id:
                print("⏳ 비디오 처리 대기 (30초)...")
                time.sleep(30)
                post_id = publish_container(user_id, container_id)
                if post_id:
                    print(f"✅ 비디오 게시 완료! Post ID: {post_id}")
                    save_published(post_id, args.text, args.tag)
        else:
            post_text(args.text, args.tag, args.reply_to)
    elif args.command == "profile":
        get_profile()
    elif args.command == "list":
        get_posts(args.limit)
    elif args.command == "insights":
        get_insights(args.post_id)
    elif args.command == "quota":
        get_quota()
    elif args.command == "refresh-token":
        refresh_token()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
