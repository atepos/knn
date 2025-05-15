import json
import os
import random
from pathlib import Path
from openai import OpenAI

GROUPED_FILE    = Path('sui.json')  
OUTPUT_FILE     = Path('prvni_experiment.json')
OPENAI_API_KEY = ""
MODEL           = 'o4-mini'


client = OpenAI(api_key=OPENAI_API_KEY)


data = json.loads(GROUPED_FILE.read_text(encoding="utf-8"))


first_words = []
for item in data:
    fw = item["questionText"].split()[0]
    if fw not in first_words:
        first_words.append(fw)
for item in data:
    fw = item["questionText"].split()[0]
    item["questionNumber"] = first_words.index(fw) + 1

results = []
for item in data:
    qnum  = item["questionNumber"]
    question = item["questionText"]
    answer   = item["answerText"]
    actual   = item["score"]

    content = (
        f"Otázka:\n{question}\n\n"
        f"Odpověď studenta:\n{answer}\n\n"
        "Na základě výše uvedeného ohodnoťte prosím kvalitu této odpovědi "
        "číslem 0–4 (odpovězte pouze tímto číslem)."
    )

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role":"user","content":content}]
        )
        pred = resp.choices[0].message.content.strip()
    except Exception as e:
        pred = f"ERROR: {e}"

    results.append({
        "questionNumber":   qnum,
        "actual_score":     actual,
        "predicted_score":  pred
    })

OUTPUT_FILE.write_text(
    json.dumps(results, ensure_ascii=False, indent=4),
    encoding="utf-8"
)
