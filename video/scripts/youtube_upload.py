from __future__ import annotations

import argparse
import json
import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from utils.spec_validator import validate_spec
from utils.youtube_auth import get_authenticated_service


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RETRIABLE_STATUS_CODES = {500, 502, 503, 504}
_SERVICE = None


def _service():
    global _SERVICE
    if _SERVICE is None:
        _SERVICE = get_authenticated_service()
    return _SERVICE


def upload_video(
    spec_path: str | Path, mp4_path: str | Path, public: bool = False
) -> str:
    spec_file = Path(spec_path).expanduser().resolve()
    video_file = Path(mp4_path).expanduser().resolve()

    if not spec_file.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_file}")
    if not video_file.exists():
        raise FileNotFoundError(f"MP4 file not found: {video_file}")

    spec = json.loads(spec_file.read_text(encoding="utf-8"))
    validate_spec(spec)
    youtube = spec["youtube"]

    body = {
        "snippet": {
            "title": youtube["title"],
            "description": youtube["description"],
            "tags": youtube.get("tags", []),
            "categoryId": youtube.get("category_id", "28"),
            "defaultLanguage": youtube.get("default_language", "ko"),
            "defaultAudioLanguage": youtube.get("default_language", "ko"),
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True,
        },
    }

    media = MediaFileUpload(
        str(video_file), chunksize=5 * 1024 * 1024, resumable=True, mimetype="video/mp4"
    )
    request = (
        _service().videos().insert(part="snippet,status", body=body, media_body=media)
    )

    response = None
    retry = 0
    while response is None:
        try:
            _, response = request.next_chunk()
        except HttpError as error:
            if error.resp.status not in RETRIABLE_STATUS_CODES or retry >= 5:
                raise
            time.sleep((2**retry) + random.random())
            retry += 1
        except OSError:
            if retry >= 5:
                raise
            time.sleep((2**retry) + random.random())
            retry += 1

    video_id = response.get("id")
    if not video_id:
        raise RuntimeError("YouTube upload completed without returning a video ID")

    playlist_id = youtube.get("playlist_id")
    if playlist_id:
        _service().playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }
            },
        ).execute()

    if public:
        make_public(video_id)

    print(f"https://www.youtube.com/watch?v={video_id}")
    return video_id


def make_public(video_id: str) -> None:
    if not video_id:
        raise ValueError("video_id is required")
    _service().videos().update(
        part="status",
        body={
            "id": video_id,
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
                "containsSyntheticMedia": True,
            },
        },
    ).execute()


def main() -> None:
    load_dotenv(PROJECT_ROOT / ".env")

    parser = argparse.ArgumentParser()
    parser.add_argument("spec_path")
    parser.add_argument("mp4_path")
    parser.add_argument("--public", action="store_true")
    args = parser.parse_args()

    upload_video(args.spec_path, args.mp4_path, public=args.public)


if __name__ == "__main__":
    main()
