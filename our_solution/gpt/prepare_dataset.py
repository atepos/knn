import json
from pathlib import Path

PARSED_DIR = Path('../datasets/parsed')
OUTPUT_DIR = Path('processed')
QUESTION_NUMBER = 11  # číslo otázky, kterou chceme vyfiltrovat pro všechny soubory

# Vytvoříme výstupní adresář, pokud neexistuje
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def process_file(input_path: Path, question_number: int):
    """
    Pro daný soubor provede:
      1) Filtrování otázek s questionNumber == question_number
      2) Seskupení odpovědí podle score (vybere první nenulovou odpověď)
      3) Uloží oba výstupy do OUTPUT_DIR
    """
    with input_path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    # Filtrování podle čísla otázky
    filtered = [item for item in data if item.get('questionNumber') == question_number]

    # Uložení filtrovaných otázek
    filtered_file = OUTPUT_DIR / f"{input_path.stem}_q{question_number}_filtered.json"
    with filtered_file.open('w', encoding='utf-8') as f:
        json.dump(filtered, f, indent=4, ensure_ascii=False)

    # Seskupení odpovědí podle score, vybere první nenulovou odpověď
    grouped = {}
    for score in sorted({item.get('score') for item in filtered}):
        # najdi první nenulovou odpověď pro toto score
        answer = ''
        for item in filtered:
            if item.get('score') == score:
                txt = item.get('answerText', '').strip()
                if txt:
                    answer = txt
                    break
        grouped[score] = answer

    # Příprava struktury pro zápis
    question_text = filtered[0].get('questionText') if filtered else ''
    output_data = {
        'questionNumber': question_number,
        'questionText': question_text,
        'answersByScore': []
    }

    for score, answer in grouped.items():
        output_data['answersByScore'].append({
            'score': score,
            'answers': [answer]
        })

    # Uložení seskupených odpovědí
    score_file = OUTPUT_DIR / f"{input_path.stem}_q{question_number}_grouped.json"
    with score_file.open('w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

    print(f"Zpracováno: {input_path.name} -> {filtered_file.name}, {score_file.name}")


if __name__ == '__main__':
    for input_file in PARSED_DIR.glob('*.json'):
        process_file(input_file, QUESTION_NUMBER)
