from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import csv
import pandas as pd
from transformers import pipeline

MODEL = f"Model/twitter-roberta-base-sentiment-2022"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def stringSentement(text):
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = softmax(output[0][0].detach().numpy())
    ranking = scores.argsort()[::-1]
    l = config.id2label[ranking[0]]
    s = scores[ranking[0]]
    result = f"{l} {np.round(float(s), 4)}"
    return result

def document2Array(csv_file):
    #remove header parementer if you dont want to include the header of the csv document in converting to numpy array
    pdtable = pd.read_csv(csv_file)
    nptable = pdtable.to_numpy()[:,1:]
    return nptable

def sentimentV2(numpyArray):
    pylist = numpyArray.tolist()
    for x in range(numpyArray.shape[0]):
        result = stringSentement(numpyArray[x][0])
        pylist[x].append(result)
    nparr = np.array(pylist)
    return nparr

#output

# nparr = [[string,string,string],
        # [string,string,string],
        # [string,string,string],
        # [string,string,string]]


#================================= TESTING Remove any un-commented code below this line when done ========================================

# csv_file_path = 'website/testData/testData.csv'

# pdtable = pd.read_csv(csv_file_path)

