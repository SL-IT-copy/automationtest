import json
import re
import zipfile
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
PARSED_DIR = ROOT / "references" / "parsed"
INDEX_PATH = ROOT / "references" / "reference_index.json"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def parse_views(name: str) -> Optional[int]:
    match = re.search(r"(\d+(?:\.\d+)?)\s*k", name.lower())
    if not match:
        return None
    return int(float(match.group(1)) * 1000)


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraphs = []
    for paragraph in root.findall(".//w:p", NS):
        parts = [node.text for node in paragraph.findall(".//w:t", NS) if node.text]
        line = "".join(parts).strip()
        if line:
            paragraphs.append(line)
    return "\n".join(paragraphs)


def first_lines(text: str, count: int = 12) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[:count]


def infer_mode(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for index in range(len(lines) - 2):
        if (
            lines[index].isdigit()
            and lines[index + 1] == "/"
            and lines[index + 2].isdigit()
        ):
            return "thread"
    compact = text.replace(" ", "")
    if any(
        token in compact for token in ["1/7", "2/7", "3/7", "1/6", "2/6", "1/5", "1/8"]
    ):
        return "thread"
    return "post_or_thread"


def record_for(path: Path) -> dict:
    text = docx_text(path)
    return {
        "file": path.name,
        "views": parse_views(path.stem),
        "mode_hint": infer_mode(text),
        "char_count": len(text),
        "line_count": len([line for line in text.splitlines() if line.strip()]),
        "hook_preview": first_lines(text, 4),
        "first_lines": first_lines(text, 12),
        "parsed_text_file": f"references/parsed/{path.stem}.txt",
    }, text


def main() -> None:
    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    for path in sorted(ROOT.glob("*.docx")):
        record, text = record_for(path)
        parsed_path = PARSED_DIR / f"{path.stem}.txt"
        parsed_path.write_text(text, encoding="utf-8")
        items.append(record)
    items.sort(key=lambda item: item.get("views") or 0, reverse=True)
    INDEX_PATH.write_text(
        json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"indexed {len(items)} reference files")
    print(INDEX_PATH)


if __name__ == "__main__":
    main()
