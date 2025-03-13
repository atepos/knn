import yaml
import sys
import os
import re
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def loadTranscriptions(file):
    with open(file, 'r', encoding="utf-8") as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded

def plotQuestionPoints(data, questionNum, ax):
    xArr = []
    yArr = []
    yArr2 = []
    cnt = 0
    for login in data:
        if questionNum in data[login]:
            xArr.append(cnt)
            yArr.append(float(data[login][questionNum]['truth']))
            yArr2.append(data[login][questionNum]['pred'])
            cnt += 1
    ax.plot(xArr, yArr, color='blue')
    ax.plot(xArr, yArr2, color='red')
            

def compareMSE(data):

    trueScore = []
    predictionScore = []
    mseValues = []

    for questionNum in range(1, 15):
        for login in data:
            #print(questionNum)
            if questionNum in data[login]:
                trueScore.append(float(data[login][questionNum]['truth']))
                predictionScore.append(data[login][questionNum]['pred'])
        if not len(trueScore) or not len(predictionScore):
            mseValues.append(0)
            continue 
        mseValues.append(mean_squared_error(trueScore, predictionScore))
       
        questionNum +=1
    return mseValues


def getTestScoreMSE(data):

    trueTestScores = []
    predictionTestScores = []

    for login in data:
        trueScore = 0
        predictionScore = 0
        for questionNum in range(1, 15):
            if questionNum in data[login]:
                trueScore += float(data[login][questionNum]['truth'])
                predictionScore += data[login][questionNum]['pred']
        #print("truth: ", trueScore)
        #print("prediction:  ", predictionScore)
        trueTestScores.append(trueScore)
        predictionTestScores.append(predictionScore)
    return mean_squared_error(trueTestScores, predictionTestScores)
            
def plotTestPoints(data, ax):
    xArr = []
    yArr = []
    yArr2 = []
    cnt = 0
    for login in data:
        baseRatingSum = 0
        ratingSum = 0
        for questionNum in data[login]:
            baseRatingSum += float(data[login][questionNum]['truth'])
            ratingSum += data[login][questionNum]['pred']

        xArr.append(cnt)
        yArr.append(baseRatingSum)
        yArr2.append(ratingSum)
        cnt += 1
    ax.plot(xArr, yArr, color='blue')
    ax.plot(xArr, yArr2, color='red')

def calcTotalMseError(data):
    xArr = []
    yArr = []
    for login in data:
        for questionNum in data[login]:
            xArr.append(float(data[login][questionNum]['pred']))
            yArr.append(data[login][questionNum]['truth'])
    return mean_squared_error(xArr, yArr)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Incorrect args")

    data1 = loadTranscriptions(sys.argv[1])
    data2 = loadTranscriptions(sys.argv[2])
    data3 = loadTranscriptions(sys.argv[3])
    data4 = loadTranscriptions(sys.argv[4])
    data5 = loadTranscriptions(sys.argv[5])
    data6 = loadTranscriptions(sys.argv[6])
    data7 = loadTranscriptions(sys.argv[7])
    data8 = loadTranscriptions(sys.argv[8])
    data9 = loadTranscriptions(sys.argv[9])


    mseVals1 = compareMSE(data1)
    mseVals2 = compareMSE(data2)
    mseVals3 = compareMSE(data3)
    mseVals4 = compareMSE(data4)
    mseVals5 = compareMSE(data5)
    mseVals6 = compareMSE(data6)
    mseVals7 = compareMSE(data7)
    mseVals8 = compareMSE(data8)
    mseVals9 = compareMSE(data9)

    X = [1,2,3,4,5,6,7,8,9,10,11,12,13, 14]
    figure, axis = plt.subplots(3,3)
    figure.tight_layout()



    axis[0, 0].plot(X, mseVals1,'--o',color='blue')
    axisTitle  = os.path.basename(sys.argv[1])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[0, 0].set_title("Model 1 -- {} MSE".format(axisTitle))
    axis[0, 0].set_ylim(0,6)
    
    axis[0, 1].plot(X, mseVals2,'--o',color='red')
    axisTitle  = os.path.basename(sys.argv[2])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[0, 1].set_title("Model 2 -- {} MSE".format(axisTitle))
    axis[0, 1].set_ylim(0,6)

    axis[0, 2].plot(X, mseVals3 ,'--o',color='green')
    axisTitle  = os.path.basename(sys.argv[3])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[0, 2].set_title("Model 3 -- {} MSE".format(axisTitle))
    axis[0, 2].set_ylim(0,6)
    
    axis[1, 0].plot(X, mseVals4,'--o',color='orange')
    axisTitle  = os.path.basename(sys.argv[4])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[1, 0].set_title("Model 4 -- {} MSE".format(axisTitle))
    axis[1, 0].set_ylim(0,6)
    
    axis[1, 1].plot(X, mseVals5 ,'--o',color='black')
    axisTitle  = os.path.basename(sys.argv[5])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[1, 1].set_title("Model 5 -- {} MSE".format(axisTitle))
    axis[1, 1].set_ylim(0,6)

    axis[1, 2].plot(X, mseVals6 ,'--o',color='purple')
    axisTitle  = os.path.basename(sys.argv[6])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[1, 2].set_title("Model 6 -- {} MSE".format(axisTitle))
    axis[1, 2].set_ylim(0,6)

    axis[2, 0].plot(X, mseVals7 ,'--o',color='pink')
    axisTitle  = os.path.basename(sys.argv[7])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[2, 0].set_title("Model 7 -- {} MSE".format(axisTitle))
    axis[2, 0].set_ylim(0,6)

    axis[2, 1].plot(X, mseVals8 ,'--o',color='brown')
    axisTitle  = os.path.basename(sys.argv[8])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[2, 1].set_title("Model 8 -- {} MSE".format(axisTitle))
    axis[2, 1].set_ylim(0,6)

    axis[2, 2].plot(X, mseVals9 ,'--o',color='teal')
    axisTitle  = os.path.basename(sys.argv[9])
    axisTitle = axisTitle.split('.yaml')[0]
    axis[2, 2].set_title("Model 9 -- {} MSE".format(axisTitle))
    axis[2, 2].set_ylim(0,6)



    testMse1 = getTestScoreMSE(data1)
    testMse2 = getTestScoreMSE(data2)
    testMse3 = getTestScoreMSE(data3)
    testMse4 = getTestScoreMSE(data4)
    testMse5 = getTestScoreMSE(data5)
    testMse6 = getTestScoreMSE(data6)
    testMse7 = getTestScoreMSE(data7)
    testMse8 = getTestScoreMSE(data8)
    testMse9 = getTestScoreMSE(data9)

    wholeTestMSE = []
    wholeTestMSE.append(testMse1)
    wholeTestMSE.append(testMse2)
    wholeTestMSE.append(testMse3)
    wholeTestMSE.append(testMse4)
    wholeTestMSE.append(testMse5)
    wholeTestMSE.append(testMse6)
    wholeTestMSE.append(testMse7)
    wholeTestMSE.append(testMse8)
    
    plt.figure(2)
    plt.plot(X, mseVals1,'--o',color='blue', label=os.path.basename(sys.argv[1]).split('.yaml')[0])
    plt.plot(X, mseVals2,'--o',color='red', label=os.path.basename(sys.argv[2]).split('.yaml')[0])
    plt.plot(X, mseVals3,'--o',color='green', label=os.path.basename(sys.argv[3]).split('.yaml')[0])
    plt.plot(X, mseVals4,'--o',color='orange', label=os.path.basename(sys.argv[4]).split('.yaml')[0])
    plt.plot(X, mseVals5,'--o',color='black', label=os.path.basename(sys.argv[5]).split('.yaml')[0])
    plt.plot(X, mseVals6,'--o',color='purple',label=os.path.basename(sys.argv[6]).split('.yaml')[0])
    plt.plot(X, mseVals7,'--o',color='pink', label=os.path.basename(sys.argv[7]).split('.yaml')[0])
    plt.plot(X, mseVals8,'--o',color='brown', label=os.path.basename(sys.argv[8]).split('.yaml')[0])
    plt.plot(X, mseVals9,'--o',color='teal', label=os.path.basename(sys.argv[9]).split('.yaml')[0])
    plt.legend()
    plt.title("Comparison of models, regarding MSE of each question")

    plt.figure(3)
    plt.plot('model1', testMse1 ,'o',color='blue', label=os.path.basename(sys.argv[1]).split('.yaml')[0])
    plt.plot('model2', testMse2 ,'o',color='red', label=os.path.basename(sys.argv[2]).split('.yaml')[0])
    plt.legend()
    plt.title("MSE for different models on the whole test score - BERT")

    plt.figure(4)
    plt.plot('model3', testMse3 ,'o',color='green', label=os.path.basename(sys.argv[3]).split('.yaml')[0])
    plt.plot('model4', testMse4 ,'o',color='orange', label=os.path.basename(sys.argv[4]).split('.yaml')[0])
    plt.plot('model5', testMse5 ,'o',color='black', label=os.path.basename(sys.argv[5]).split('.yaml')[0])
    plt.plot('model6', testMse6 ,'o',color='purple', label=os.path.basename(sys.argv[6]).split('.yaml')[0])
    plt.plot('model7', testMse7 ,'o',color='pink', label=os.path.basename(sys.argv[7]).split('.yaml')[0])
    plt.plot('model8', testMse8 ,'o',color='brown', label=os.path.basename(sys.argv[8]).split('.yaml')[0])
    plt.plot('model9', testMse9 ,'o',color='teal', label=os.path.basename(sys.argv[9]).split('.yaml')[0])
    plt.legend()
    plt.title("MSE for different models on the whole test score - OPENAI")



    plt.show()

    #how to run script
    #python .\resultVisualiser.py .\results\2022-1-bert-paraphrase-miniLM-final.yaml .\results\2022-1-bert-distiluse-final.yaml .\results\2022-1-ALL-three-answers.yaml .\results\2022-1-ALL-two-answers.yaml  .\results\2022-1-final-babbage-v1.yaml .\results\2022-1-final-babbage-v2.yaml .\results\2022-1-final-babbage-v3.yaml .\results\2022-1-final-babbage-v4.yaml .\results\2022-1-final-babbage-v5.yaml 

    #python .\resultVisualiser.py .\results\2022-2-bert-paraphrase-miniLM-final.yaml .\results\2022-2-bert-distiluse-final.yaml .\results\2022-2-ALL-three-answers.yaml .\results\2022-2-ALL-two-answers.yaml  .\results\2022-2-final-babbage-v1.yaml .\results\2022-2-final-babbage-v2.yaml .\results\2022-2-final-babbage-v3.yaml .\results\2022-2-final-babbage-v4.yaml .\results\2022-2-final-babbage-v5.yaml 

    #python .\resultVisualiser.py .\results\2022-3-bert-paraphrase-miniLM-final.yaml .\results\2022-3-bert-distiluse-final.yaml .\results\2022-3-ALL-three-answers.yaml .\results\2022-3-ALL-two-answers.yaml  .\results\2022-3-final-babbage-v1.yaml .\results\2022-3-final-babbage-v2.yaml .\results\2022-3-final-babbage-v3.yaml .\results\2022-3-final-babbage-v4.yaml .\results\2022-3-final-babbage-v5.yaml 

    #python .\resultVisualiser.py .\results\2022-1-A-bert-distiluse-final.yaml .\results\2022-1-A-bert-paraphrase-miniLM-final.yaml .\results\2022-1-ALL-three-answers.yaml .\results\2022-1-ALL-two-answers.yaml  .\results\2022-1-final-babbage-v1.yaml .\results\2022-1-final-babbage-v2.yaml .\results\2022-1-final-babbage-v3.yaml .\results\2022-1-final-babbage-v4.yaml .\results\2022-1-final-babbage-v5.yaml

    #python .\resultVisualiser.py .\results\2022-1-B-bert-distiluse-final.yaml .\results\2022-1-B-bert-paraphrase-miniLM-final.yaml .\results\2022-1-ALL-three-answers.yaml .\results\2022-1-ALL-two-answers.yaml  .\results\2022-1-final-babbage-v1.yaml .\results\2022-1-final-babbage-v2.yaml .\results\2022-1-final-babbage-v3.yaml .\results\2022-1-final-babbage-v4.yaml .\results\2022-1-final-babbage-v5.yaml