import json
from pathlib import Path
from openai import OpenAI

# --- KONFIGURACE ---
OPENAI_API_KEY  = ""

MODEL          = "o4-mini"
ANSWERS_FILE   = Path("sui.json")   # JSON se studentskými odpověďmi
CRITERIA_FILE  = Path("unique_questions_skeleton.json")         
OUTPUT_FILE    = Path("treti_experiment.json")
# --------------------

client = OpenAI(api_key=OPENAI_API_KEY)

# Načíst data
answers  = json.loads(ANSWERS_FILE.read_text(encoding="utf-8"))
criteria = json.loads(CRITERIA_FILE.read_text(encoding="utf-8"))

crit_map = {c["questionNumber"]: c for c in criteria}

results = []
for ans in answers:
    qnum     = ans.get("questionNumber")
    question = ans.get("questionText", "").strip()
    answer   = ans.get("answerText", "").strip()
    actual   = ans.get("score")

    crit = crit_map.get(qnum, {})
    bod1 = crit.get("bod1", "")
    bod2 = crit.get("bod2", "")
    bod3 = crit.get("bod3", "")
    bod4 = crit.get("bod4", "")

    prompt = (
        f"Otázka:\n{question}\n\n"
        "Hodnotící kritéria:\n"
        f"1) {bod1}\n"
        f"2) {bod2}\n"
        f"3) {bod3}\n"
        f"4) {bod4}\n\n"
        f"Odpověď studenta:\n{answer}\n\n"
        "Prosím ohodnoťte kvalitu této odpovědi podle výše uvedených kritérií číslem 0–4. A ZKUS HODNOTIT VÍCE BODY, TEDA KDYŽ SI BUDEŠ MYSLET, ŽE JE TO ZA 1 BOD TAK DEJ 2 ATD ... PROSTĚ BUĎ HODNĚ HODNÝ"
        "(odpovězte pouze jediným číslem)."
    )

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
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
    json.dumps(results, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Hotovo – vyhodnoceno {len(results)} odpovědí, výsledky v {OUTPUT_FILE.resolve()}")