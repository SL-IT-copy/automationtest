# pyright: reportMissingImports=false
from __future__ import annotations

import argparse
import json
import os
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv
from mutagen.mp3 import MP3

from utils.alignment_converter import chars_to_word_captions
from utils.elevenlabs_client import tts_with_timestamps
from utils.spec_validator import validate_spec


DEFAULT_VOICE_ID = "juMJXUAec27cMjEBdGCR"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PUBLIC_AUDIO_ROOT = PROJECT_ROOT / "video" / "remotion" / "public" / "audio"


def load_spec(spec_path: Path) -> dict:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    validate_spec(spec)
    return spec


def get_mp3_duration_ms(audio_bytes: bytes) -> int:
    return int(round(MP3(BytesIO(audio_bytes)).info.length * 1000))


def main() -> None:
    load_dotenv(PROJECT_ROOT / ".env")

    parser = argparse.ArgumentParser()
    parser.add_argument("spec_path")
    parser.add_argument(
        "--voice-id", default=os.getenv("ELEVENLABS_VOICE_ID") or DEFAULT_VOICE_ID
    )
    args = parser.parse_args()

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise EnvironmentError("ELEVENLABS_API_KEY is required")

    spec_path = Path(args.spec_path).expanduser().resolve()
    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")

    spec = load_spec(spec_path)
    spec_id = spec["id"]
    audio_dir = PUBLIC_AUDIO_ROOT / spec_id
    audio_dir.mkdir(parents=True, exist_ok=True)

    for slide in spec["slides"]:
        slide_number = int(slide["slide_number"])
        audio_bytes, alignment = tts_with_timestamps(
            slide["text"],
            args.voice_id,
            api_key,
        )

        audio_filename = f"slide_{slide_number:02d}.mp3"
        captions_filename = f"slide_{slide_number:02d}_captions.json"
        audio_path = audio_dir / audio_filename
        captions_path = audio_dir / captions_filename

        audio_path.write_bytes(audio_bytes)
        captions = chars_to_word_captions(alignment)
        captions_path.write_text(
            json.dumps(captions, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        slide["audio_file"] = f"{spec_id}/{audio_filename}"
        slide["captions_file"] = f"{spec_id}/{captions_filename}"
        slide["duration_ms"] = get_mp3_duration_ms(audio_bytes)

    validate_spec(spec)
    spec_path.write_text(
        json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(spec_path)


if __name__ == "__main__":
    main()
