from __future__ import annotations

import base64
import time
from typing import Any

import requests


API_URL_TEMPLATE = (
    "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
)
TRANSIENT_STATUS_CODES = {429, 500, 502, 503}
IMMEDIATE_ERROR_STATUS_CODES = {400, 401}


def tts_with_timestamps(
    text: str,
    voice_id: str,
    api_key: str,
    *,
    model_id: str = "eleven_multilingual_v2",
    language_code: str = "ko",
    stability: float = 0.55,
    similarity_boost: float = 0.75,
    speed: float = 0.9,
    apply_language_text_normalization: bool = True,
    timeout: int = 120,
    max_retries: int = 3,
) -> tuple[bytes, dict[str, Any]]:
    if not text or not text.strip():
        raise ValueError("text must not be empty")
    if not voice_id:
        raise ValueError("voice_id is required")
    if not api_key:
        raise ValueError("api_key is required")

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "language_code": language_code,
        "apply_language_text_normalization": apply_language_text_normalization,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "speed": speed,
        },
    }

    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                API_URL_TEMPLATE.format(voice_id=voice_id),
                headers=headers,
                json=payload,
                timeout=timeout,
            )
        except requests.RequestException as error:
            last_error = error
            if attempt == max_retries:
                break
            time.sleep(2 ** (attempt - 1))
            continue

        if response.status_code in IMMEDIATE_ERROR_STATUS_CODES:
            raise RuntimeError(
                f"ElevenLabs request failed ({response.status_code}): {response.text}"
            )

        if response.status_code in TRANSIENT_STATUS_CODES:
            last_error = RuntimeError(
                f"ElevenLabs transient error ({response.status_code}): {response.text}"
            )
            if attempt == max_retries:
                break
            time.sleep(2 ** (attempt - 1))
            continue

        try:
            response.raise_for_status()
            data = response.json()
        except (requests.HTTPError, ValueError) as error:
            raise RuntimeError(f"Invalid ElevenLabs response: {error}") from error

        audio_base64 = data.get("audio_base64")
        if not audio_base64:
            raise RuntimeError("ElevenLabs response missing audio_base64")

        alignment_key = (
            "normalized_alignment" if apply_language_text_normalization else "alignment"
        )
        alignment = data.get(alignment_key)
        if not isinstance(alignment, dict):
            raise RuntimeError(f"ElevenLabs response missing {alignment_key}")

        try:
            audio_bytes = base64.b64decode(audio_base64)
        except ValueError as error:
            raise RuntimeError("Invalid ElevenLabs audio payload") from error

        return audio_bytes, alignment

    if last_error is not None:
        raise RuntimeError(
            f"ElevenLabs request failed after {max_retries} attempts"
        ) from last_error
    raise RuntimeError("ElevenLabs request failed")
