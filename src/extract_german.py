"""
Specialized extractor for the German Gutenberg BGE PDF.
This is the ground truth — every aphorism must be captured.
"""

import fitz
import re
import json
from pathlib import Path


def extract_full_text(pdf_path: str) -> str:
    """Extract all text from PDF."""
    doc = fitz.open(pdf_path)
    pages = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(pages)


def clean_gutenberg_boilerplate(text: str) -> str:
    """Remove Project Gutenberg header/footer."""
    # Find start of actual content
    start_markers = ["Vorrede.", "VORREDE"]
    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[idx:]
            break

    # Find end of content
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG",
        "End of the Project Gutenberg",
        "*** END OF THIS PROJECT GUTENBERG"
    ]
    for marker in end_markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
            break

    return text


def extract_aphorisms(text: str) -> list[dict]:
    """
    Extract all 296 aphorisms from German BGE.

    Structure in Gutenberg PDF:
    - Numbers appear as "1." or "1.\n" followed by text
    - Some numbers are on their own line, some inline
    - Chapter headings like "Erstes Hauptstück:" appear between
    """
    aphorisms = []

    # Pattern: number (1-296) followed by period, then content until next number
    # The (?=...) is a lookahead to stop at the next aphorism number
    pattern = r'(?:^|\n)\s*(\d{1,3})\.\s*\n?(.*?)(?=\n\s*\d{1,3}\.\s*\n|\n\s*\d{1,3}\.\s*[A-Z]|$)'

    # First pass: try to get everything
    matches = re.findall(pattern, text, re.DOTALL)

    for num_str, content in matches:
        num = int(num_str)
        if 1 <= num <= 296:
            # Clean up the content
            content = content.strip()
            # Remove chapter headings that got included
            content = re.sub(r'^.*Hauptstück:.*$', '', content, flags=re.MULTILINE)
            content = content.strip()

            if len(content) > 20:  # Must have actual content
                aphorisms.append({"number": num, "text": content})

    # Deduplicate by number, keeping longest version
    by_number = {}
    for aph in aphorisms:
        num = aph["number"]
        if num not in by_number or len(aph["text"]) > len(by_number[num]["text"]):
            by_number[num] = aph

    return sorted(by_number.values(), key=lambda x: x["number"])


def extract_with_split_method(text: str) -> list[dict]:
    """
    Alternative method: split on aphorism numbers.
    More robust for this specific PDF.
    """
    aphorisms = []

    # Split text on aphorism number pattern
    # Match: newline(s), number, period, space or newline
    parts = re.split(r'\n\s*(\d{1,3})\.\s*\n?', text)

    # parts[0] is before first number
    # parts[1] is first number, parts[2] is its content
    # parts[3] is second number, parts[4] is its content, etc.

    i = 1
    while i < len(parts) - 1:
        try:
            num = int(parts[i])
            content = parts[i + 1] if i + 1 < len(parts) else ""

            if 1 <= num <= 296 and len(content.strip()) > 20:
                # Clean content: remove chapter headings
                content = re.sub(
                    r'(Erstes|Zweites|Drittes|Viertes|Fünftes|Sechstes|Siebentes|Achtes|Neuntes)\s+Hauptstück:.*?(?=\n|$)',
                    '',
                    content,
                    flags=re.DOTALL
                )
                content = re.sub(r'Aus hohen Bergen\..*', '', content, flags=re.DOTALL)
                content = content.strip()

                if len(content) > 20:
                    aphorisms.append({"number": num, "text": content})
        except ValueError:
            pass
        i += 2

    # Deduplicate
    by_number = {}
    for aph in aphorisms:
        num = aph["number"]
        if num not in by_number or len(aph["text"]) > len(by_number[num]["text"]):
            by_number[num] = aph

    return sorted(by_number.values(), key=lambda x: x["number"])


def validate_extraction(aphorisms: list[dict]) -> dict:
    """Check which aphorisms are missing."""
    found = {a["number"] for a in aphorisms}
    expected = set(range(1, 297))
    missing = sorted(expected - found)

    return {
        "total_found": len(aphorisms),
        "total_expected": 296,
        "missing_count": len(missing),
        "missing_numbers": missing,
        "complete": len(missing) == 0
    }


def process_german_gutenberg(pdf_path: str = "BGE_Gutenberg.pdf") -> dict:
    """
    Full pipeline for German Gutenberg PDF.
    Tries multiple methods to ensure completeness.
    """
    print(f"Extracting from {pdf_path}...")

    raw = extract_full_text(pdf_path)
    cleaned = clean_gutenberg_boilerplate(raw)

    print(f"  Raw text: {len(raw):,} chars")
    print(f"  Cleaned:  {len(cleaned):,} chars")

    # Try both methods
    method1 = extract_aphorisms(cleaned)
    method2 = extract_with_split_method(cleaned)

    # Use whichever got more
    if len(method2) > len(method1):
        aphorisms = method2
        method_used = "split"
    else:
        aphorisms = method1
        method_used = "regex"

    print(f"  Method used: {method_used}")

    # Validate
    validation = validate_extraction(aphorisms)
    print(f"  Found: {validation['total_found']}/296")

    if validation["missing_count"] > 0:
        print(f"  Missing: {validation['missing_numbers'][:10]}{'...' if len(validation['missing_numbers']) > 10 else ''}")

    return {
        "name": "Gutenberg",
        "language": "de",
        "aphorisms": aphorisms,
        "aphorism_count": len(aphorisms),
        "validation": validation,
        "raw_text": cleaned
    }


def save_result(result: dict, output_path: str = "corpus/aligned/gutenberg.json"):
    """Save extraction result."""
    output = {k: v for k, v in result.items() if k != "raw_text"}
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    result = process_german_gutenberg()

    # Show sample
    print("\n--- SAMPLE APHORISMS ---")
    for aph in result["aphorisms"][:3]:
        preview = aph["text"][:200].replace("\n", " ")
        print(f"\n{aph['number']}. {preview}...")

    # Save
    save_result(result)

    # Final report
    v = result["validation"]
    if v["complete"]:
        print("\n✓ All 296 aphorisms extracted!")
    else:
        print(f"\n✗ Missing {v['missing_count']} aphorisms: {v['missing_numbers']}")
