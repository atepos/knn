# KNN - Automatické hodnocení písemek ze SUI (CheckPoint odevzdání)
**Autoři**: xkaska01, xhemza05, xmagda03

**1. Odkaz na repozitář:**  
[https://github.com/atepos/knn.git](https://github.com/atepos/knn.git)

**2. Definice úlohy:**

Cílem je poloautomatizovat hodnocení písemných odpovědí studentů, které byly získány ze zkoušek SUI pomocí OCR. Vstupem do našeho systému jsou digitálně naskenované zkoušky, u nichž je text převeden do digitální podoby pomocí OCR, a zároveň máme k dispozici jednotlivé hodnocení úloh. Víme, že každá otázka je ohodnocena maximálně 4 body na základě manuálního hodnocení. Na rozdíl od některých přístupů, kde se využívají referenční odpovědi, v našem případě přímo využíváme konečné známky jako referenční měřítko.

Výstupem našeho systému bude automaticky generované hodnocení každé odpovědi, které se snaží co nejvěrněji napodobit manuální hodnocení. Například pokud model pomocí automatizovaných metod (např. na základě metriky kosinové podobnosti embeddingů nebo jiného přístupu) vyhodnotí odpověď s výsledkem 0,5, interpretuje se to jako přibližně 2 body z možných 4. Tímto způsobem můžeme experimentovat s různými metodami automatického hodnocení, přičemž manuálně udělené skóre slouží jako standard pro kalibraci a validaci výsledků.

**3. Krátký přehled existujících řešení:**

- **[e‑rater (ETS):](https://www.ets.org/erater.html)**  
  Využívají lingvistické a statistické metody pro hodnocení esejí. Přestože je primárně určen pro hodnocení esejí 

- **[ASAP Short Answer Scoring:](https://www.kaggle.com/competitions/asap-sas)**  
  Porovnává studentovy odpovědi s lidskými anotacemi pomocí statistických metod. Dosahuje výsledků srovnatelných s lidským hodnocením.

- **[Can Large Language Models Be an Alternative to Human Evaluations?](https://doi.org/10.48550/arXiv.2305.01937)**  
  Autoři ukazují, že hodnocení provedené LLM koreluje s výsledky expertů, což potvrzuje potenciál těchto modelů jako alternativy k manuálnímu hodnocení.

- **[Check-Eval: A Checklist-based Approach for Evaluating Text Quality](https://doi.org/10.48550/arXiv.2407.14467)**  
  Řešení využívá kontrolní seznamy (checklisty) k hodnocení kvality textu. Tento strukturovaný a interpretable přístup dosahuje vysoké korelace s lidskými hodnoceními a nabízí modulární způsob, jak automatizovat proces hodnocení.

**4. Trénovací Dataset:**


**5. Způsob vyhodnocení:**

Využijeme metriku založenou na kosinové podobnosti mezi embeddingy textu. 

**Definice a rozsah:** Metrika měří kosinovou podobnost mezi vektorovou reprezentací (embeddingem) studentovy odpovědi a referenční (ideální) odpovědi. Hodnoty se pohybují od 0 do 1, kde 1 znamená úplnou shodu (maximální podobnost) a 0 absolutní odlišnost.

**Optimalizace:** Cílem je maximalizovat tuto hodnotu – čím blíže je výsledek k 1, tím kvalitnější odpověď.

**Příklad:** Pokud dostaneme skóre 0.5, znamená to, že odpověď má přibližně 50 % shody s referencí. V praxi to obvykle indikuje střední kvalitu – odpověď není zcela správná, ale také není úplně mimo mísu. V závislosti na nastavených prahových hodnotách (například nad 0.7 = dobré, mezi 0.4 a 0.7 = průměrné, pod 0.4 = slabé) lze takové skóre interpretovat jako výsledek, který by mohl vyžadovat další revizi nebo doplnění.

**6. Baseline řešení:**

**7. Vyhodnocení Baseline:**

**8. Plán útoku:**


**Reference:**  
- ETS e‑rater: [https://www.ets.org/erater.html](https://www.ets.org/erater.html)  
- ASAP Short Answer Scoring: [https://www.kaggle.com/competitions/asap-sas](https://www.kaggle.com/competitions/asap-sas)  
- Can Large Language Models Be an Alternative to Human Evaluations?: [https://doi.org/10.48550/arXiv.2305.01937](https://doi.org/10.48550/arXiv.2305.01937)  
- Check-Eval: A Checklist-based Approach for Evaluating Text Quality: [https://doi.org/10.48550/arXiv.2407.14467](https://doi.org/10.48550/arXiv.2407.14467)