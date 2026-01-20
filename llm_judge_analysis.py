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

# Save as a single combined file for easier reading
output = {"aphorisms": []}

for num in range(1, 51):
    aph = {"number": num, "translations": {}}
    for name in ["Gutenberg", "Kaufmann", "Hollingdale", "Norman", "Faber", "Zimmern"]:
        text = translations[name].get(num)
        if text is not None:
            aph["translations"][name] = text
        else:
            aph["translations"][name] = None
    output["aphorisms"].append(aph)

# Create output directory
os.makedirs("llm_judge/full_analysis", exist_ok=True)

# Save combined translations
with open("llm_judge/combined_1_50.json", "w") as fp:
    json.dump(output, fp, indent=2, ensure_ascii=False)

print(f"Saved {len(output['aphorisms'])} aphorisms to llm_judge/combined_1_50.json")

# Print summary of what's available
for aph in output["aphorisms"]:
    available = [k for k, v in aph["translations"].items() if v is not None]
    missing = [k for k, v in aph["translations"].items() if v is None]
    print(f"Aphorism {aph['number']}: {len(available)} translations available, missing: {missing if missing else 'none'}")
