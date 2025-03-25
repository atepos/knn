import json
import sys
import random

PICK_ZERO_OTHER_CNT = 2
QUESTIONS_EACH_COUNT = -1

def loadJson(file):
     with open(file) as f:
        data = json.load(f)
        return data

def getRandomOtherThen(questionNum, data):
    if PICK_ZERO_OTHER_CNT == 0:
        return -1
    res = []
    while len(res) < PICK_ZERO_OTHER_CNT:
        item = random.choice(data)
        if item["questionNum"] != questionNum:
            res.append(item)
    return res

def getRandomNOfQuestion(data, questionNum, n):
    data = list(filter(lambda x: x["questionNum"] == questionNum, data))
    dataWithoutZero = list(filter(lambda x: x["completion"] != "???" and int(float(x["completion"])), data))
    dataWithZero = list(filter(lambda x: x["completion"] != "???" and int(float(x["completion"])) == 0, data))
    if not dataWithoutZero:
        return -1
    if n == -1:
        return data
    random.shuffle(dataWithoutZero)
    random.shuffle(dataWithZero)
    newData = dataWithoutZero[:n]
    if(len(dataWithZero) != 0):
        newData.append(dataWithZero[0]) 
    return newData

def parseItem(question, answer, completion, item):
    answer = answer.strip(";")
    question = question.strip(";")
    prompt = "For question: " + question + " , grade answer (from 0 to 4): " + answer
    meta = "{}-{}-{}-{}".format(item["year"], item["test"], item["questionNum"], item["login"])
    return {"prompt": prompt, "completion": completion, "meta": meta}

def getOpenAITrainingData(data):
    final = []
    for i in range(1, 20):
        randomQuestions = getRandomNOfQuestion(data, i, QUESTIONS_EACH_COUNT)
        # print(randomQuestions)
        if randomQuestions == -1:
            break
        for item in randomQuestions:
            if item["completion"] == "???":
                continue
            item["completion"] = str(int(float(item["completion"])))
            final.append(parseItem(item["questionTextRaw"], item["promptRaw"], item["completion"], item))
            others = getRandomOtherThen(item["questionNum"], data)
            if others == -1:
                continue
            for other in others:
                final.append(parseItem(item["questionTextRaw"], other["promptRaw"], "0", item))
    return final

if __name__ == "__main__":
    data = loadJson(sys.argv[1])
    openaiDataset = getOpenAITrainingData(data)
    with open("trainingDataOPENAI_2022_3.json", 'w', encoding='utf8') as f:
        json.dump(openaiDataset, f, ensure_ascii=False)
    print("Done")
