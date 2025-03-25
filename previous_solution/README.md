# Automatic answer grading using transformers
## Authors: xmarti97, xharva03, xtizsa00

# Project structure
`fine_tunes` - results of the model training
`datasets` - extracted datasets with their transcriptions
`results` - evaluated model predictions, used
`pero_ocr` - ocr module from pero-ocr project, available publicly
`region_templates` - templates for each assigment to extract regions

## Scripts
createDataset.py - creates datased, which is ready to be trained with
questionSeparator.py - uses templates to extract transcriptions
regionsToTranscriptions.py - extracts output from questionSeparator, and creates raw dataset with paired grades, logins, and other metadata
createTrainingData.py - takes from data regionsToTranscriptions, and creates it monolytic json dataset containing prompt and completions
createTrainingDataForOpenAI.py - takes json training data, and creates complete promps
calculateLoss.py - creates .yaml results from OpenAI, which can be evaluated via resultVisualiser.py
answerSimilarityEval.py - uses bert for result evalation (instead of openai)
resultVisualiser.py - visualises results from calculateLoss and answerSimilarityEval.py
