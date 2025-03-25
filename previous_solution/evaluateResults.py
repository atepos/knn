import openai
import json
import numpy as np
import sys
from sklearn.metrics import mean_squared_error
from createTrainingForOpenAI import parseItem

def loadJson(file):
    with open(file, 'r', encoding="utf8") as json_file:
        data = json.load(json_file)
        return data
v1 = "ada:ft-personal-2023-05-11-20-50-52"
v2 = "babbage:ft-personal-2023-05-13-18-58-37"
v3 = "babbage:ft-personal-2023-05-14-13-09-58"
v4 = "babbage:ft-personal-2023-05-14-14-29-04"
v5 = "babbage:ft-personal-2023-05-14-18-14-51"
model = v1

data = loadJson(sys.argv[1])

import os
openai.api_key = os.environ["OPENAI_API_KEY"] 

y_true = []
y_pred = []
res = {}

def dumpRes():
    with open("final2022-ALL-babbage-v1.yaml", 'w', encoding='utf8') as f:
        import yaml
        yaml.dump(res, f, allow_unicode=True)

import signal
def handler(signum, frame):
    print("\nMSE:", mean_squared_error(y_true, y_pred))
    dumpRes()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

def queryModel(prompt):
    return openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=1,
            logprobs=5,
    )

if __name__ == "__main__":
    i = 0
    # import random
    # random.shuffle(data)
    # data = data[:500]
    for row in data:
        item = parseItem(row["questionTextRaw"], row["promptRaw"], row["completion"], row)
        prompt = item["prompt"] + "\n\n###\n\n"
        login = row["login"]
        promptRaw = row["promptRaw"].strip(";")
        questionNum = row["questionNum"]

        if row["completion"] == "???":
            continue

        key = row["year"] + "-" + row["test"]
        if not res.get(key):
            res[key] = {}
        if not res[key].get(login):
            res[key][login] = {}

        i += 1

        completion = queryModel(prompt)
        choice = completion["choices"][0]["text"]
        # choice = "2"
        if len(choice) != 2:
            pred = "INVALID"
        choice = choice[0]
        if not choice.isnumeric():
            pred = "INVALID"
        else:
            pred = int(choice)
        true = int(float(row["completion"]))
        res[key][login][questionNum] = {"truth": true, "pred": pred, "text": promptRaw}

        # if abs(pred - true) > 2:
        #     print("expected:", row["completion"], "got:" , completion["choices"][0]["text"])
        #     print("answer:", row["prompt"])
        if pred == "INVALID":
            continue
        y_pred.append(pred)
        y_true.append(true)

        if i % 10 == 0:
            print("MSE:", mean_squared_error(y_true, y_pred))
    dumpRes()
    print("MSE:", mean_squared_error(y_true, y_pred))
