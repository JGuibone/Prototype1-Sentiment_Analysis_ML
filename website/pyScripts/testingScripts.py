from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
from pathlib import Path
# from transformers import logging as hf_logging

MODEL = f"Model/twitter-roberta-base-sentiment-2022"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)



def stringSentement(text):
    resultScore = []
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    print(text)
    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]
        resultScore.append(f"{i + 1}) {l} {np.round(float(s), 4)}")
    return resultScore

def documentInjest():

    return True

import csv
import numpy as np

def generate_numpy_table(csv_file):
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    table = np.array(data)
    return table

# Usage example
csv_file_path = 'website/testData/testData.csv'
numpy_table = generate_numpy_table(csv_file_path)
print(numpy_table)

def sameContentChecker(csv_file):

    return True


import numpy as np

def check_and_remove_same_content(table):
    # Convert the table elements to strings (if not already)
    str_table = np.char.asarray(table)

    # Check if all elements are equal to the first element
    same_content = np.all(np.char.equal(str_table, str_table[0]))

    # Remove duplicates
    unique_table = np.unique(str_table)

    return same_content, unique_table

# Usage example
table = np.array([['apple', 'apple', 'apple'],
                  ['apple', 'apple', 'apple'],
                  ['apple', 'apple', 'apple']])

same_content, unique_table = check_and_remove_same_content(table)
print("Same content:", same_content)  # Output: True
print("Unique table:")
print(unique_table)