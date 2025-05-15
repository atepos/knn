import json
import os
import random
from pathlib import Path
from openai import OpenAI


GROUPED_FILE    = Path('sui.json')  
OUTPUT_FILE     = Path('druhy_experiment.json')
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


scores = sorted({str(item["score"]) for item in data}, key=lambda x: float(x))
reference_examples = []
for score in scores:
    candidates = [itm for itm in data if str(itm["score"]) == score]
    chosen = random.choice(candidates)
    reference_examples.append(chosen)


results = []
for item in data:
    qnum     = item["questionNumber"]
    question = item["questionText"]
    answer   = item["answerText"]
    actual   = item["score"]

    
    parts = []
    parts.append("Níže jsou uvedeny ukázkové odpovědi s patřičným skóre (0–4):")
    for ex in reference_examples:
        parts.append(f"Otázka: {ex['questionText']}")
        parts.append(f"Odpověď: {ex['answerText']}")
        parts.append(f"Skóre: {ex['score']}\n")
    parts.append("Nyní, prosím, na základě těchto příkladů ohodnoťte tuto odpověď:")
    parts.append(f"Otázka: {question}")
    parts.append(f"Odpověď: {answer}")
    parts.append("Odpovězte pouze číslem 0–4.")
    content = "\n".join(parts)


    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": content}]
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

