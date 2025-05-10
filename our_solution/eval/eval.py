import sys
from datasets import load_dataset

# Zpracování argumentu z příkazové řádky
if len(sys.argv) != 2:
    print("Použití: python script.py <cesta_k_checkpointu>")
    sys.exit(1)

checkpoint_path = sys.argv[1]

# Preprocessing function
def preprocess_dataset(row):
    return {
            "prompt": f"Otázka: {row['questionText']}\nOdpověď: {row['answerText']}",
            "completion": f"{row['score']}"
    }

# Načítání datasetu a jeho předzpracování
# dataset = load_dataset("json", data_files="data.json")
# dataset = load_dataset("json", data_files="SUI_dataset_one_question.json")
dataset = load_dataset("json", data_files="SUI_dataset.json")
# dataset = load_dataset("json", data_files="data.json")
dataset = dataset.map(preprocess_dataset, remove_columns=dataset["train"].column_names)
# Rozdělení datasetu na trénovací a testovací část
dataset = dataset["train"].train_test_split(test_size=0.2, seed=42)

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch



# Načítání modelu s kvantizací
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    device_map="auto"
)

# from transformers import AutoTokenizer, AutoModelForCausalLM
# model = AutoModelForCausalLM.from_pretrained(OUTPUT_DIR, device_map="auto", quantization_config=bnb_config)
model = AutoModelForCausalLM.from_pretrained(checkpoint_path, device_map="auto", quantization_config=bnb_config)
tokenizer = AutoTokenizer.from_pretrained(checkpoint_path, padding_side='left')

from transformers import pipeline

pipe = pipeline("text-generation", model=model, return_full_text=False, tokenizer=tokenizer, pad_token_id=tokenizer.eos_token_id, max_new_tokens=100)
pipe.tokenizer.pad_token_id = model.config.eos_token_id

from sklearn.metrics import mean_absolute_error, mean_squared_error
from transformers.pipelines.pt_utils import KeyDataset
from tqdm.auto import tqdm

preds = []
targets = []

with open("inference_results.txt", "w") as f:
    for i, (sample, out) in enumerate(zip(dataset["test"], pipe(KeyDataset(dataset["test"], "prompt"), batch_size=8))):
        prompt = sample["prompt"]
        target_str = sample["completion"]
        output = out[0]["generated_text"]

        try:
            pred = float(output.strip())
            target = float(target_str.strip())
            preds.append(pred)
            targets.append(target)
            f.write(f"[{i}] Prompt: {prompt}\n")
            f.write(f"[{i}] Target: {target}, Prediction: {pred}\n\n")
        except ValueError:
            f.write(f"[{i}] Failed to parse: pred='{output.strip()}', target='{target_str.strip()}'\n\n")
            continue

    # Calculate metrics at the end
    mae = mean_absolute_error(targets, preds)
    mse = mean_squared_error(targets, preds)

    f.write("Final Results:\n")
    f.write(f"MAE: {mae:.4f}\n")
    f.write(f"MSE: {mse:.4f}\n")

# print(f"MAE: {mae:.4f}")
# print(f"MSE: {mse:.4f}")
print(f"{mae:.3f}   {mse:.3f}")


