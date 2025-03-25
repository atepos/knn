import yaml
import json
import sys

def loadTranscriptions(file):
     with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data

def getTranscriptionPointPair(page, questionsCount = 14):
    if len(page["points"]) != questionsCount:
        print(Exception("Error, invalid number of points:", page["points"]))
        return
    res = []
    for idx in iter(page["answers"]):
        if page["questions"][idx] == "":
            continue
        if page["answers"][idx] == "":
            page["points"][idx] = "0"
        if page["year"] == "2022" and page["test"] == "1":
            if idx+1 == 2 or idx+1 == 7:
                continue
        if page["year"] == "2022" and page["test"] == "3":
            if idx+1 == 4:
                continue
        x = {"questionNum": idx+1, "promptRaw":  page["answers"][idx], "completion": page["points"][idx], "login": page["login"], "year": page["year"], "test": page["test"], "questionTextRaw": page["questions"][idx]}
        res.append(x)
    return res

def trainingDataFromTranscriptions(transcriptions):
    trainingDatas = []
    for key in transcriptions:
        page = transcriptions[key]
        pageTranscriptions = getTranscriptionPointPair(page)
        if pageTranscriptions:
            trainingDatas.append(pageTranscriptions)
    return [item for sublist in trainingDatas for item in sublist]

if __name__ == "__main__":
    transcriptions = loadTranscriptions(sys.argv[1])
    trainingData = trainingDataFromTranscriptions(transcriptions)
    with open("trainingData.json", 'w', encoding='utf8') as f:
        json.dump(trainingData, f, ensure_ascii=False)
    print("Done")
