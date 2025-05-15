import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# --- KONFIGURACE ---
RESULTS_FILE = Path("treti_experiment.json")   # upravte cestu k vašemu JSON
PDF_OUTPUT   = Path("3_plots_o4.pdf")
# --------------------

# 1) Načteme výsledky
with RESULTS_FILE.open('r', encoding='utf-8') as f:
    results = json.load(f)

# 2) Seskupíme bias a absolutní chyby podle otázky
bias_by_q    = {}
abs_err_by_q = {}
for itm in results:
    try:
        q = int(itm["questionNumber"])
        a = float(itm["actual_score"])
        p = float(itm["predicted_score"])
    except:
        continue
    bias_by_q.setdefault(q, []).append(p - a)
    abs_err_by_q.setdefault(q, []).append(abs(p - a))

START_Q = 5
END_Q   = 9
# 3) Pevné pořadí Q1–Q9 (nebo max podle vašich dat)
question_nums = [q for q in sorted(bias_by_q.keys()) if START_Q <= q <= END_Q]
labels        = [f"Q{q}" for q in question_nums]
n = len(labels)
y_pos = np.arange(n)[::-1]  # Q1 nahoře

# 4) Spočítáme metriky v tomhle pořadí
mean_bias   = [np.mean(bias_by_q.get(i, [0])) for i in question_nums]
data_abserr = [abs_err_by_q.get(i, [0])     for i in question_nums]

# 5) Barvy (červená = nadhodnocení, modrá = podhodnocení)
colors = ["steelblue" if b>0 else "steelblue" for b in mean_bias]

# 6) Vykreslíme dva panely se sdílenou osou Y
fig, (ax2, ax3) = plt.subplots(ncols=2, figsize=(14, 6), sharey=True)

# — Levý panel: Bias —
mx = max(abs(min(mean_bias)), abs(max(mean_bias)))
ax2.barh(y_pos, mean_bias, color=colors, align='center')
ax2.axvline(0, color="black", linewidth=1)
ax2.set_xlim(-mx*1.1, mx*1.1)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(labels)
ax2.set_ylabel("Question")
ax2.set_title("Bias per question")
ax2.set_xlabel("Mean bias\n(prediction – actual)")
ax2.invert_yaxis()

# — Pravý panel: Absolutní chyba —
ax3.boxplot(data_abserr,
            vert=False,
            positions=y_pos,
            widths=0.6)
ax3.set_yticks(y_pos); ax3.set_yticklabels([])  # necháme štítky jen vlevo
ax3.set_title("Absolute error distribution per question")
ax3.set_xlabel("Absolut error\n|prediction – actual|")
ax3.invert_yaxis()

fig.suptitle("Experiment 3 - o4-mini", fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])  # rezervuje prostor nahoře pro nadpis

plt.tight_layout()
plt.show()
fig.savefig(PDF_OUTPUT)
print(f" Grafy uloženy do {PDF_OUTPUT.resolve()}")
