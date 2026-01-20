import json
import os

# Load all translations
files = {
    "Gutenberg": "corpus/aligned/gutenberg.json",
    "Kaufmann": "corpus/aligned/walter_kaufman.json",
    "Hollingdale": "corpus/aligned/rj_hollingdale.json",
    "Norman": "corpus/aligned/judith_norman.json",
    "Faber": "corpus/aligned/marion_faber.json",
    "Zimmern": "corpus/aligned/helen_zimmern.json"
}

translations = {}
for name, f in files.items():
    with open(f) as fp:
        data = json.load(fp)
        translations[name] = {a["number"]: a["text"] for a in data["aphorisms"]}

# Extract aphorisms 1-50
for num in range(1, 51):
    print(f"=== APHORISM {num} ===")
    for name in ["Gutenberg", "Kaufmann", "Hollingdale", "Norman", "Faber", "Zimmern"]:
        text = translations[name].get(num, "MISSING")
        if text is not None and text != "MISSING":
            preview = text[:500].replace("\n", " ")
            print(f"{name}: {preview}...")
        else:
            print(f"{name}: MISSING")
    print()
