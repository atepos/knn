from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import sys
import numpy as np
import yaml
import time

def loadTranscriptions(file):
    with open(file, 'r', encoding="utf-8") as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded

def prepareBaseAnswers(data, model):
    baseAnswers = {}
    for pageId in data:
        for answerId in data[pageId]['answers']:
            # skip incorrect answers with empty questions
            if not data[pageId]['questions'][answerId]:
                continue
            login = data[pageId]['login']
            answerText = data[pageId]['answers'][answerId]
            if len(data[pageId]['points']) > answerId:
                if data[pageId]['points'][answerId].isnumeric():
                    answerPoints = round(float(data[pageId]['points'][answerId]))
                    if answerPoints > 4:
                        answerPoints = 4
                else:
                    answerPoints = 0
            else:
                answerPoints = 0

            if answerId not in baseAnswers:
                baseAnswers[answerId] = {0: [], 1: [], 2: [], 3:[], 4: []}

            if len(baseAnswers[answerId][answerPoints]) <= 8:
                mergedAnswers = [answerText]
                for questionBaseAnswer in baseAnswers[answerId][answerPoints]:
                    mergedAnswers.append(questionBaseAnswer['text'])
                sen_embeddings = model.encode(mergedAnswers)
                ratings = cos_sim(np.array([sen_embeddings[0]]), np.array(sen_embeddings[1:]))
                ratings = ratings[0]
                ratings = ratings.numpy()
                print(ratings.shape)
                if ratings.shape[0] > 0:
                    minSim = np.amin(ratings)
                else:
                    minSim = 0
                if(minSim < 0.6):
                    baseAnswers[answerId][answerPoints].append({'text': answerText, 'truth': answerPoints})
                #     if questionBaseAnswers['baseRating'] == answerPoints:
                #         sameRating = True
                #         break
                # if not sameRating:
                #     baseAnswers[answerId].append({'text': answerText, 'baseRating': answerPoints})
                #     continue
    return baseAnswers

def prepareAnswersForRating(data):
    notRatedAnswers = {}
    for pageId in data:
        for answerId in data[pageId]['answers']:
            # skip incorrect answers with empty questions
            if not data[pageId]['questions'][answerId]:
                continue
            login = data[pageId]['login']
            answerText = data[pageId]['answers'][answerId]
            if len(data[pageId]['points']) > answerId:
                if data[pageId]['points'][answerId].isnumeric():
                    answerPoints = round(float(data[pageId]['points'][answerId]))
                else:
                    answerPoints = 0
            else:
                answerPoints = 0

            if login not in notRatedAnswers:
                notRatedAnswers[login] = {}
            notRatedAnswers[login][answerId] = {'text': answerText, 'pred': 0, 'truth': answerPoints}
    return notRatedAnswers

def rateAnswers(model,  baseAnswers, notRatedAnswers):
    questionCount = len(notRatedAnswers)
    ratedCount = 0
    for login in notRatedAnswers:
        for answerId in notRatedAnswers[login]:
            notRatedAnswer = notRatedAnswers[login][answerId]['text']
            mergedAnswers = [notRatedAnswer]
            for rating in baseAnswers[answerId]:
                for baseAnswer in baseAnswers[answerId][rating]:
                    mergedAnswers.append(baseAnswer['text'])
            sen_embeddings = model.encode(mergedAnswers)
            ratings = cos_sim(np.array([sen_embeddings[0]]), np.array(sen_embeddings[1:]))
            ratings = ratings[0]
            ratings = ratings.numpy()
            # bestIndex = np.argmax(ratings)
            # currentIndex = 0
            # classSimSum = []
            # for rating in baseAnswers[answerId]:
            #     currentIndex += len(baseAnswers[answerId][rating])
            #     if bestIndex < currentIndex:
            #         bestRatingClass = rating
            #         break
            # notRatedAnswers[login][answerId]['pred'] = bestRatingClass
            maxRating = 0
            maxRatingClass = 0
            itemCnt = 0
            for rating in baseAnswers[answerId]:
                currentSum = 0
                currentClass = 0
                for baseAnswer in baseAnswers[answerId][rating]:
                    currentSum += ratings[itemCnt]
                    itemCnt += 1
                    currentClass = baseAnswer['truth']
                if len(baseAnswers[answerId][rating]) > 0:
                    currentSum /= len(baseAnswers[answerId][rating])
                #print(currentClass, len(baseAnswers[answerId][rating]))
                if currentSum > maxRating:
                    maxRating = currentSum
                    maxRatingClass = currentClass
            #print(ratings)
            #print(maxRatingClass)
            #print(baseAnswers[answerId])
            #return None
            notRatedAnswers[login][answerId]['pred'] = maxRatingClass
        print(ratedCount,'/',questionCount)
        ratedCount += 1
    return notRatedAnswers

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Incorrect args")

    # model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    #model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
    # model = SentenceTransformer('use-cmlm-multilingual')
    start = time.time() * 1000
    data = loadTranscriptions(sys.argv[1])
    baseAnswers = prepareBaseAnswers(data, model)
    notRatedAnswers = prepareAnswersForRating(data)
    ratedAnswers = rateAnswers(model, baseAnswers, notRatedAnswers)

    with open(sys.argv[2],'w') as yamlfile:
        dump = yaml.dump(ratedAnswers)
        yamlfile.write(dump)
    end = time.time() * 1000
    print(end - start)