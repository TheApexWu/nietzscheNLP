import json
import os

# Load combined file
with open("llm_judge/combined_1_50.json") as fp:
    data = json.load(fp)

# Split into individual files
os.makedirs("llm_judge/aphorisms", exist_ok=True)

for aph in data["aphorisms"]:
    num = aph["number"]
    with open(f"llm_judge/aphorisms/aph_{num:02d}.json", "w") as fp:
        json.dump(aph, fp, indent=2, ensure_ascii=False)
    print(f"Saved aphorism {num}")

# Also create batches of 5 for easier reading
for batch_start in range(1, 51, 5):
    batch_end = min(batch_start + 4, 50)
    batch_aphs = [a for a in data["aphorisms"] if batch_start <= a["number"] <= batch_end]
    with open(f"llm_judge/aphorisms/batch_{batch_start:02d}_{batch_end:02d}.json", "w") as fp:
        json.dump({"aphorisms": batch_aphs}, fp, indent=2, ensure_ascii=False)
    print(f"Saved batch {batch_start}-{batch_end}")
