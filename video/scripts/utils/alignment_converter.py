from __future__ import annotations

from typing import Any


def _flush_word(
    buffer: list[tuple[str, float, float]], captions: list[dict[str, Any]]
) -> None:
    if not buffer:
        return
    text = "".join(char for char, _, _ in buffer)
    if not text:
        buffer.clear()
        return
    start_ms = int(round(buffer[0][1] * 1000))
    end_ms = int(round(buffer[-1][2] * 1000))
    captions.append(
        {
            "text": text,
            "startMs": start_ms,
            "endMs": end_ms,
            "timestampMs": start_ms,
            "confidence": None,
        }
    )
    buffer.clear()


def chars_to_word_captions(alignment: dict) -> list[dict]:
    if not alignment:
        return []

    characters = alignment.get("characters") or []
    starts = alignment.get("character_start_times_seconds") or []
    ends = alignment.get("character_end_times_seconds") or []

    if not (len(characters) == len(starts) == len(ends)):
        raise ValueError("Alignment arrays must have matching lengths")

    captions: list[dict[str, Any]] = []
    buffer: list[tuple[str, float, float]] = []

    for char, start, end in zip(characters, starts, ends):
        if char in {" ", "\n", "\r", "\t"}:
            _flush_word(buffer, captions)
            continue
        if char == "":
            continue
        buffer.append((char, float(start), float(end)))

    _flush_word(buffer, captions)
    return captions
