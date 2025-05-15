import json
from pathlib import Path
import re

# --- KONFIGURACE ---
INPUT_FILE = Path("sui.json")  # Váš JSON soubor sáznamy
OUTPUT_FILE = Path("unique_questions_skeleton.json")
# --------------------

# Načtení dat
data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

# Seskupení unikátních otázek dle čísla a textu
unique = {}
for entry in data:
    qnum = entry.get("questionNumber")
    qtext = entry.get("questionText", "").strip()
    # zachovej pouze první výskyt každé otázky (stejné questionNumber)
    if qnum not in unique:
        unique[qnum] = qtext

# Vytvoření seznamu se skeletonem bodů
output = []
for qnum in sorted(unique.keys()):
    output.append({
        "questionNumber": qnum,
        "questionText": unique[qnum],
        "bod1": "",
        "bod2": "",
        "bod3": "",
        "bod4": ""
    })

# Uložení do JSON
with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✅ Vygenerováno {len(output)} unikátních otázek do {OUTPUT_FILE.resolve()}")
