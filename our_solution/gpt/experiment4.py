import json
import os
import random
from pathlib import Path
from openai import OpenAI


GROUPED_FILE    = Path('sui.json')  
OUTPUT_FILE     = Path('ctvrty_experiment.json')
OPENAI_API_KEY = ""
MODEL           = 'o4-mini'

client = OpenAI(api_key=OPENAI_API_KEY)

data = json.loads(GROUPED_FILE.read_text(encoding="utf-8"))

first_words = []
for itm in data:
    fw = itm["questionText"].split()[0]
    if fw not in first_words:
        first_words.append(fw)
for itm in data:
    fw = itm["questionText"].split()[0]
    itm["questionNumber"] = first_words.index(fw) + 1


groups = {}
for itm in data:
    qnum = itm["questionNumber"]
    groups.setdefault(qnum, []).append(itm)

results = []


for qnum, items in groups.items():
    
    unique_scores = sorted({str(it["score"]) for it in items}, key=float)

  
    if len(unique_scores) < 2:
        continue


    hidden = {}
    for sc in unique_scores:
        candidates = [it for it in items if str(it["score"]) == sc]
        hidden[sc] = random.choice(candidates)


    refs = [it for it in items if it not in hidden.values()]

  
    for sc, hid in hidden.items():
     
        prompt_lines = [
            f"Aktuální otázka č. {qnum}:",
            hid["questionText"],
            "",
            "Níže jsou referenční příklady (score 0–4):"
        ]
        for r in refs:
            prompt_lines.append(f"- Skóre {r['score']}: {r['answerText']}")
        prompt_lines += [
            "",
            "Nyní, prosím, podle výše uvedených ukázek HONOĎTE následující skrytou odpověď:",
            f"\"{hid['answerText']}\"",
            "Odpovězte **pouze** číslem 0–4."
        ]
        content = "\n".join(prompt_lines)


        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role":"user","content":content}]
            )
            pred = resp.choices[0].message.content.strip()
        except Exception as e:
            pred = f"ERROR: {e}"

        results.append({
            "questionNumber":  qnum,
            "actual_score":    hid["score"],
            "predicted_score": pred,
            "hidden_answer":   hid["answerText"]
        })

OUTPUT_FILE.write_text(
    json.dumps(results, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
