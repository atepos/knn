# KNN - Automatické hodnocení písemek ze SUI (CheckPoint odevzdání)
**Autoři**: xkaska01, xhemza05, xmagda03

**1. Odkaz na repozitář:**  
[https://github.com/atepos/knn.git](https://github.com/atepos/knn.git)

**2. Definice úlohy:**

Cílem je poloautomatizovat hodnocení písemných odpovědí studentů, které byly získány ze zkoušek SUI pomocí OCR. 

Vstupem do našeho systému jsou digitálně naskenované zkoušky, u nichž je text převeden do digitální podoby pomocí OCR, a zároveň máme k dispozici jednotlivé hodnocení úloh. Víme, že každá otázka je ohodnocena maximálně 4 body na základě manuálního hodnocení. Na rozdíl od některých přístupů, kde se využívají referenční odpovědi, v našem případě přímo využíváme konečné známky jako referenční měřítko.

Výstupem našeho systému bude automaticky generované hodnocení každé odpovědi, které se snaží co nejvěrněji napodobit manuální hodnocení. Tímto způsobem budeme experimentovat s různými modeli dotrénovaných k automatickému hodnocení, přičemž manuálně udělené skóre slouží jako standard pro kalibraci a validaci výsledků.

**3. Krátký přehled existujících řešení:**

- **[e‑rater (ETS):](https://www.ets.org/erater.html)**  
  Využívají lingvistické a statistické metody pro hodnocení esejí. Přestože je primárně určen pro hodnocení esejí.

- **[ASAP Short Answer Scoring:](https://www.kaggle.com/competitions/asap-sas)**  
  Porovnává studentovy odpovědi s lidskými anotacemi pomocí statistických metod. Dosahuje výsledků srovnatelných s lidským hodnocením.

- **[Can Large Language Models Be an Alternative to Human Evaluations?](https://doi.org/10.48550/arXiv.2305.01937)**  
  Autoři ukazují, že hodnocení provedené LLM koreluje s výsledky expertů, což potvrzuje potenciál těchto modelů jako alternativy k manuálnímu hodnocení.

- **[Check-Eval: A Checklist-based Approach for Evaluating Text Quality](https://doi.org/10.48550/arXiv.2407.14467)**  
Tento článek jsme si vybrali i k prezentaci a tedy ho podrobněji rozebereme ve videu - Autoři v tomto článku představují nový rámec CHECK-EVAL určený k hodnocení textů. Vycházejí z předpokladu, že tradiční metriky (BLEU, ROUGE, METEOR) často nedostatečně korelují s lidským hodnocením, zejména u kreativních či nuančních úloh.

**4. Trénovací Dataset:**

Dataset jsme přejali od studentů z minulého roku, kteří pomocí OCR převedli ručně psané písemky na jejich .json podoby. My jsme následně pro přehlednost jejich dataset upravili a nahráli do repozitáře [zde](https://github.com/atepos/knn/tree/main/our_solution/datasets/parsed). Provedli jsme následující úpravy: 

Odstranili jsme z něj nepodstatné informace pro naše řešení jako (zahashovaný login studenta, rok vykonání zkoušky a zahashované ID otázky). Dále jsme upravili celkovou strukturu .jsonu, kdy v původním datasetu byly známky ke každé otázce v hlavičce a následovali jednotlivé pomíchané otázky s ukazatel k dané známce v hlavičce - my jsme známky z hlavičky vyjmuli a dali je ke každé otázce zvlášť. Dále bylo potřeba vyřešit chybějící otázky, tedy předchozí studenti špatně naparsovali data a např. v odpovědi se nacházel text k otázce i odpovědi zároveň - tyto případy jsme korektně separovali do `hodnot` náležitých `klíčů` v jsonu. Také bylo nutné opravit špatně namapované číslá otázek k náležitým otázkám. A tedy výsledná struktura datasetu je následující:

```
[
...
    {
        ...
    },
    {
        "questionNumber": číslo otázky,
        "questionText": Text zadané otázky,
        "answerTest": Odpověď studenta,
        "score": Získané skóre za opověď
    },
    {
        ...
    },
...
]
```

**5. Způsob vyhodnocení:**

V našem řešení hodnotíme kvalitu písemných odpovědí porovnáním výstupu modelu s manuálním hodnocením vyučujícího. Používáme metodu, která spočívá v tréninku modelu, aby na základě zadané otázky a odpovědi předpovídal bodové hodnocení, jež se co nejvíce blíží referenčnímu hodnocení udělenému lidským hodnotitelem.

- **Definice a hodnotový rozsah:**  
  Model předpovídá skóre, které je na škále například od 0 do 4 (0 – nejhorší, 4 – nejlepší). Alternativně může být výstup modelu normalizován na interval 0 až 1, kdy 1 značí úplnou shodu s ideálním hodnocením a 0 absolutní nesouhlas.

- **Optimalizace:**  
  V rámci tréninku se snažíme minimalizovat rozdíl mezi modelovým hodnocením a referenčním hodnocením. Jinými slovy, chceme, aby byl tento rozdíl co nejmenší – model tedy "minimalizuje chybu" a tím maximalizuje přesnost svého předpovězeného skóre.

- **Interpretace výsledků:**  
  Pokud model například vrátí skóre 0,5 (v normalizovaném intervalu), znamená to, že odpověď má přibližně 50 % shody s ideálním hodnocením. V praxi to typicky indikuje střední kvalitu odpovědi – odpověď není vynikající, ale ani úplně špatná. Prahové hodnoty mohou být dále definovány (např. nad 0,7 považujeme odpověď za dobrou, mezi 0,4 a 0,7 za průměrnou a pod 0,4 za slabou).

Takže budeme opakovatelně hodnotit písemné odpovědi studentů a postupně zlepšovat přesnost modelu tak, aby co nejlépe napodoboval lidské hodnocení.

**6. Baseline řešení:**

Jako Baseline jsme zvolili řešení našich předchůdců [odkaz na jejich repozitář s jejich výsledky](https://github.com/atepos/knn/blob/main/previous_solution). Jedná se o finetunované modely `Ada`, `Babbage`, `Curie` a `Davinci`. K tomuto kroku nás vedlon několik důvodů: 

1. Dle našeho názoru je jejich dataset docela "neučesaný" s množstvím chybějících hodnot a bloatů. Tak jsme zvědavy, zda například pouze úprava datasetu, na kterém byl model dotrénován povede k lepším výsledkům.

2. Jejich řešení je už přímo natrenované a vyhodnocené na jejich zmiňovaném datasetu. Tedy stojí nás to minimální úsilí a měli bychom mít nejlepší baseline, co můžeme sehnat. 

3. Zajímá nás jestli budeme schopni najít/dotrénovat lepší model a o kolik se naše dosažené výsledky budou lišit.


**7. Vyhodnocení Baseline:**

**8. Plán útoku:**


**Reference:**  
ETS e‑rater: [https://www.ets.org/erater.html](https://www.ets.org/erater.html)  
ASAP Short Answer Scoring: [https://www.kaggle.com/competitions/asap-sas](https://www.kaggle.com/competitions/asap-sas)  
Can Large Language Models Be an Alternative to Human Evaluations?: [https://doi.org/10.48550/arXiv.2305.01937](https://doi.org/10.48550/arXiv.2305.01937)  
Check-Eval: A Checklist-based Approach for Evaluating Text Quality: [https://doi.org/10.48550/arXiv.2407.14467](https://doi.org/10.48550/arXiv.2407.14467)