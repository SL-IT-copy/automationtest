from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from utils.spec_validator import validate_spec


DEFAULT_BACKGROUND_MUSIC = "ambient_loop.mp3"
DEFAULT_HANDLE = "@jisang0914"


def sanitize_id(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or "video-spec"


def parse_json_slides(input_path: Path) -> list[str]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        slides = payload.get("slides")
    elif isinstance(payload, list):
        slides = payload
    else:
        raise ValueError("Unsupported JSON input format")

    if not isinstance(slides, list) or not slides:
        raise ValueError("JSON input must contain a non-empty slides array")

    normalized = []
    for index, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            raise ValueError(f"Slide {index} must be an object")
        text = slide.get("text") or slide.get("content") or slide.get("body") or ""
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"Slide {index} is missing text")
        slide_number = slide.get("slide_number", index)
        normalized.append((int(slide_number), text.strip()))

    normalized.sort(key=lambda item: item[0])
    return [text for _, text in normalized]


def parse_markdown_slides(input_path: Path) -> list[str]:
    content = input_path.read_text(encoding="utf-8")
    blocks = re.findall(r"```(?:[^\n`]*)\n(.*?)```", content, flags=re.DOTALL)
    slides = [block.strip() for block in blocks if block.strip()]
    if not slides:
        raise ValueError("Markdown input must contain at least one fenced code block")
    return slides


def load_slides(input_path: Path) -> list[str]:
    suffix = input_path.suffix.lower()
    if suffix == ".json":
        return parse_json_slides(input_path)
    if suffix == ".md":
        return parse_markdown_slides(input_path)
    raise ValueError("Input file must be .json or .md")


def build_description(slides: list[str]) -> str:
    slide_body = "\n\n".join(slides)
    description = f"{slide_body}\n\n{DEFAULT_HANDLE}\n\n#AI #Tech #뉴스"
    return description[:5000]


def build_title(first_slide: str) -> str:
    first_line = next(
        (line.strip() for line in first_slide.splitlines() if line.strip()),
        first_slide.strip(),
    )
    title = first_line[:100]
    return title or "JSup AI/Tech Update"


def build_spec(input_path: Path, theme: str) -> dict:
    slides_text = load_slides(input_path)
    spec_id = sanitize_id(input_path.stem)
    title = build_title(slides_text[0])
    total_slides = len(slides_text)

    spec = {
        "id": spec_id,
        "title": title,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "settings": {
            "width": 1080,
            "height": 1920,
            "fps": 30,
            "theme": theme,
            "background_music": DEFAULT_BACKGROUND_MUSIC,
            "background_music_volume": 0.08,
            "transition_duration_frames": 15,
        },
        "intro": {
            "duration_seconds": 0.5,
            "handle": DEFAULT_HANDLE,
            "logo_text": "JSup",
        },
        "outro": {
            "duration_seconds": 2.0,
            "cta_text": "AI 업계 흐름, 계속 정리해서 올릴 예정.\n팔로우 해두면 놓치지 않음.",
            "handle": DEFAULT_HANDLE,
        },
        "slides": [
            {
                "slide_number": index,
                "total_slides": total_slides,
                "text": text,
                "audio_file": f"{spec_id}/slide_{index:02d}.mp3",
                "captions_file": f"{spec_id}/slide_{index:02d}_captions.json",
                "duration_ms": None,
                "theme_override": None,
            }
            for index, text in enumerate(slides_text, start=1)
        ],
        "youtube": {
            "title": title,
            "description": build_description(slides_text),
            "tags": ["AI", "Tech", "AI뉴스", "테크뉴스", "JSup"],
            "category_id": "28",
            "default_language": "ko",
            "playlist_id": None,
            "contains_synthetic_media": True,
        },
    }
    validate_spec(spec)
    return spec


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("--theme", default="dark")
    parser.add_argument("--output-dir", default="video/output/")
    args = parser.parse_args()

    input_path = Path(args.input_path).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    spec = build_spec(input_path, args.theme)
    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "video_spec.json"
    output_path.write_text(
        json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(output_path)


if __name__ == "__main__":
    main()
