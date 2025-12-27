"""
PDF text extraction for Nietzsche translations.
"""

import fitz
import re
import json
from pathlib import Path


def extract_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF."""
    doc = fitz.open(pdf_path)
    text = "\n\n".join(page.get_text() for page in doc)
    doc.close()
    return text


def clean_archive_artifacts(text: str) -> str:
    """Remove Internet Archive boilerplate."""
    # Skip everything before actual content starts
    markers = [
        "PREFACE",
        "Preface",
        "VORREDE",
        "Vorrede",
        "BEYOND GOOD AND EVIL",
        "Beyond Good and Evil",
        "JENSEITS VON GUT UND BÖSE",
    ]

    for marker in markers:
        idx = text.find(marker)
        if idx != -1 and idx < len(text) // 3:  # Must be in first third
            return text[idx:]

    return text


def parse_aphorisms(text: str) -> list[dict]:
    """
    Extract numbered aphorisms from BGE text.
    Returns list of {number, text} dicts.
    """
    # BGE has 296 aphorisms, numbered 1-296
    # Pattern: number at start of line, followed by content
    pattern = r'(?:^|\n)\s*(\d{1,3})\s*\n(.+?)(?=\n\s*\d{1,3}\s*\n|$)'

    matches = re.findall(pattern, text, re.DOTALL)

    aphorisms = []
    for num_str, content in matches:
        num = int(num_str)
        if 1 <= num <= 296:
            aphorisms.append({
                "number": num,
                "text": content.strip()
            })

    # Sort by number, deduplicate
    seen = set()
    unique = []
    for aph in sorted(aphorisms, key=lambda x: x["number"]):
        if aph["number"] not in seen:
            seen.add(aph["number"])
            unique.append(aph)

    return unique


def detect_language(text: str) -> str:
    """Detect German vs English."""
    german_words = {"und", "der", "die", "das", "ist", "nicht", "sich", "mit"}
    words = text.lower().split()[:200]
    german_count = sum(1 for w in words if w in german_words)
    return "de" if german_count > len(words) * 0.1 else "en"


def process_translation(pdf_path: str) -> dict:
    """
    Full pipeline: extract, clean, parse.
    Returns {name, language, aphorisms, raw_text}.
    """
    path = Path(pdf_path)
    name = path.stem.replace("BGE_", "").replace("_", " ")

    raw = extract_pdf(pdf_path)
    cleaned = clean_archive_artifacts(raw)
    aphorisms = parse_aphorisms(cleaned)
    language = detect_language(cleaned)

    return {
        "name": name,
        "language": language,
        "aphorisms": aphorisms,
        "aphorism_count": len(aphorisms),
        "raw_text": cleaned
    }


def process_all(pdf_dir: str = ".") -> dict:
    """Process all BGE PDFs in directory."""
    results = {}

    for pdf_path in sorted(Path(pdf_dir).glob("BGE_*.pdf")):
        print(f"Processing {pdf_path.name}...")
        result = process_translation(str(pdf_path))
        results[result["name"]] = result
        print(f"  → {result['aphorism_count']} aphorisms ({result['language']})")

    return results


if __name__ == "__main__":
    results = process_all()

    # Save to corpus/aligned
    output_dir = Path("corpus/aligned")
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, data in results.items():
        # Save without raw_text (too large)
        clean_data = {k: v for k, v in data.items() if k != "raw_text"}
        out_path = output_dir / f"{name.replace(' ', '_').lower()}.json"
        with open(out_path, "w") as f:
            json.dump(clean_data, f, indent=2, ensure_ascii=False)
        print(f"Saved {out_path}")
