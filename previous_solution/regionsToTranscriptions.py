from pero_ocr.document_ocr.layout import PageLayout
import yaml
import sys
import os

def getRegions(file):
    layout = PageLayout(file=file)
    return layout.regions

def getAnswersAndQuestions(data, folder, filename):
    answers = data[filename]['answers']
    questions = data[filename]['questions']

    regions = getRegions(os.path.join(folder, filename))

    answerText = {}
    questionText = {}

    for answerNum in iter(answers):
        answerRegions = answers[answerNum]

        texts = []
        for regionId in answerRegions:
            region = filter(lambda x: x.id == regionId, regions)
            if sum(1 for _ in region) != 1:
                raise Exception("Error, duplicate answer regions found:", list(region))
            region = next(filter(lambda x: x.id == regionId, regions))
            texts.append(region.get_region_transcription())
        answerText[answerNum] = ";".join(texts)

    for questionNum in iter(questions):
        questionRegions = questions[questionNum]

        texts = []
        for regionId in questionRegions:
            region = filter(lambda x: x.id == regionId, regions)
            if sum(1 for _ in region) != 1:
                raise Exception("Error, duplicate question regions found")
            region = next(filter(lambda x: x.id == regionId, regions))
            texts.append(region.get_region_transcription())
        questionText[questionNum] = ";".join(texts)
    return answerText, questionText

def getPoints(year, test, annFolder):
    fileAnnName = "body-{}_{}.txt.uniform.anon".format(year, test)
    annFile = os.path.join(annFolder, fileAnnName)
    with open(annFile) as f:
        lines = f.readlines()
        points = {}
        for line in lines:
            line = line.split()
            if year == "2022" and test == "1":
                points[line[0]] = line[2:]
            else:
                points[line[0]] = line[1:]
        return points

allPoints = {}

def parseYaml(datasetFilepath, xmlTranscriptionsFolder, annFolder):
    with open(datasetFilepath) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    
    res = {}

    dataIt = iter(data)
    for file in dataIt:
        answerText, questionText = getAnswersAndQuestions(data, xmlTranscriptionsFolder, file)
        year = data[file]["year"]
        test = data[file]["test"]
        if not year+test in allPoints:
            allPoints[year+test] = getPoints(year, test, annFolder)
        login = data[file]["login"]
        if login in allPoints[year+test]:
            points = allPoints[year+test][login]
        else:
            points = []
        res[file] = {
                "answers": answerText,
                "questions": questionText,
                "points": points,
                "year": year,
                "test": test,
                "login": login,
            }
    return res

def Merge(dict1, dict2):
    return(dict2.update(dict1))

def extractRegions(yamlFolder, xmlTranscriptionsFolder, annFolder):
    yamlData = {}
    for file in os.listdir(yamlFolder):
        if file[:3] != "202":
            continue
        newDict = parseYaml(os.path.join(yamlFolder, file), xmlTranscriptionsFolder, annFolder)
        Merge(yamlData, newDict)
        yamlData = newDict
    return yamlData

if __name__ == '__main__':
    yamlData = extractRegions(sys.argv[1], sys.argv[2], sys.argv[3])
    yamlOutputName = sys.argv[1] + 'transcripted.yaml'
    with open(yamlOutputName,'w') as yamlfile:
        yaml.dump(yamlData, yamlfile, default_flow_style=False, allow_unicode=True)
    print("Done")
