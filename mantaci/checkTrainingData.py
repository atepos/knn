import pandas as pd # data analysis package
# Two-dimensional, size-mutable, potentially heterogeneous tabular data.
import json

def loadJson(file):
    with open(file) as f:
        data = json.load(f)
        return data
dataset = loadJson("trainingDataOPENAI.json")        
df = pd.DataFrame(dataset, columns = ['completion'])
print(df["completion"].unique())
df.head()
