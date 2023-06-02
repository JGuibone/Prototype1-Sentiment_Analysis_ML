from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
import pandas as pd
from scipy.special import softmax
from pathlib import Path
import csv as csv
# from transformers import logging as hf_logging

MODEL = f"Model/twitter-roberta-base-sentiment-2022"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)



def stringSentement(text):
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    # scores = output[0][0].detach().numpy()
    scores = softmax(output[0][0].detach().numpy())
    ranking = scores.argsort()[::-1]
    # ranking = np.argsort(scores)
    # ranking = ranking[::-1]
    l = config.id2label[ranking[0]]
    s = scores[ranking[0]]
    result = f"{l} {np.round(float(s), 4)}"
    return result

def documentInjest():

    return True

import csv
import numpy as np

def document2Array(csv_file):
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    table = np.array(data)
    return table[:,1:]


csv_file_path = 'website/testData/testData.csv'

# pdtable = pd.read_csv(csv_file_path)
# numpyarray = pdtable.to_numpy()
# numpyarray = numpyarray[:,1:]
# # print(numpyarray[:,1:])

def combineArray(numpyArray):

    return True
def sentimentV2(numpyArray):
    pylist = numpyarray.tolist()
    for x in range(numpyArray.shape[0]):
        result = stringSentement(numpyArray[x][0])
        pylist[x].append(result)
    nparr = np.array(pylist)
    return nparr

# print(pdtable.columns)
# pdtable.columns = ['column1','column2','column3']
# print(pdtable.columns)

def CSVToStr(csv_file):
    #Function is used for injesting form POST from user.
    pdtable = pd.read_csv(csv_file)
    pddata = pdtable.iloc[:,1]
    convo = '\n'.join(list(pddata))
    print(convo)



def document2Array(csv_file):
    #remove header parementer if you dont want to include the header of the csv document in converting to numpy array
    pdtable = pd.read_csv(csv_file)
    nptable = pdtable.to_numpy()[:,1]
    return nptable

# testingfunction()

CSVToStr(csv_file_path)

# print(len('birds'))

# print(pdtable.shape)
# print(pdtable.iloc[:[0]])
# print(numpyarray[1])
# print(sentimentV2(numpyarray))


# stringSentement('we need aircon to hot and wifi')
# print(stringSentement('the event was a huge failure'))

# nparray = np.array([1,3,2])
# ranking = (-nparray).argsort()
# print(ranking)
