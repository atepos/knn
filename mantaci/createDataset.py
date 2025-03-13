from regionsToTranscriptions import extractRegions
from createTrainingData import trainingDataFromTranscriptions
from createTrainingForOpenAI import getOpenAITrainingData
import sys
import json
import random

OPENAI_DATASET = True

if __name__ == "__main__":
    datasetsYamlFolder = sys.argv[1]
    ocrFolder = sys.argv[2]
    anonymizedFolder = sys.argv[3]
    filenameExported = sys.argv[4]
    regionTranscriptions = extractRegions(datasetsYamlFolder, ocrFolder, anonymizedFolder)
    dataset = trainingDataFromTranscriptions(regionTranscriptions)
    random.shuffle(dataset)
    trainingCnt = int(len(dataset) * 0.9)
    trainingData = dataset[:trainingCnt]
    testData = dataset[trainingCnt:]
    if OPENAI_DATASET:
        trainingData = getOpenAITrainingData(trainingData)

    with open(filenameExported + ".test.json", 'w', encoding='utf8') as f:
        json.dump(testData, f, ensure_ascii=False, indent=4)
    with open(filenameExported + ".train.json", 'w', encoding='utf8') as f:
        json.dump(trainingData, f, ensure_ascii=False, indent=4)
    print("Done")
