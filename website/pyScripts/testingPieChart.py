import matplotlib.pyplot as plt
from transformers import pipeline
import pandas as pd



csv_file_path = 'website/testData/Survey Questions - Techono Event.csv'

pdtable = pd.read_csv(csv_file_path)

def csvPrep(csv_file, column_num):
    # No Error Checking.
    pdtable = pd.read_csv(csv_file)
    pd_data = pdtable.iloc[:,column_num]
    return pd_data

def pandasToSentimentV2(pd_series):
    #returns a pandas dataframe from processing the sentiment
    sentiment = pd.DataFrame(columns=['Sentence','Label','Score'])
    sentiment_task = pipeline("text-classification", model=f"Model/twitter-roberta-base-sentiment-2022", tokenizer=f"Model/twitter-roberta-base-sentiment-2022")
    Sentence = []
    Label = []
    Score = []
    for item in pd_series:
        sentimentResult = sentiment_task(item)
        Sentence.append(item)
        Label.append(f"{sentimentResult[0]['label']}")
        Score.append(f"{format(sentimentResult[0]['score'], '.4f')}")
    sentiment['Sentence'] = pd.Series(Sentence, dtype=str)
    sentiment['Label'] = pd.Series(Label, dtype=str)
    sentiment['Score'] = pd.Series(Score, dtype=float)
    return sentiment


def pandasToSentiment(pd_series):
    #returns a pandas dataframe from processing the sentiment
    sentiment = pd.DataFrame(columns=['Sentence','Label','Score'])
    sentiment_task = pipeline("text-classification", model=f"Model/gpt2-medium-finetuned-sst2-sentiment", tokenizer=f"Model/gpt2-medium-finetuned-sst2-sentiment")
    Sentence = []
    Label = []
    Score = []
    for item in pd_series:
        sentimentResult = sentiment_task(item)
        Sentence.append(item)
        Label.append(f"{sentimentResult[0]['label']}")
        Score.append(f"{format(sentimentResult[0]['score'], '.4f')}")
    sentiment['Sentence'] = pd.Series(Sentence, dtype=str)
    sentiment['Label'] = pd.Series(Label, dtype=str)
    sentiment['Score'] = pd.Series(Score, dtype=float)
    return sentiment

def processDataForPieV2(data: pd.Series):
    Possitive = 0
    Negative = 0
    Neutral = 0
    for label in data:
        if label == 'positive' or label ==  'POSITIVE':
            Possitive += 1
        elif label == 'neutral' or label ==  'NEUTRAL':
            Neutral += 1
        else:
            Negative +=1
    pieVal = {'Positive': Possitive, 'Neutral': Neutral, 'Negative': Negative}
    return pieVal

def processDataForPie(data: pd.Series):
    Possitive = 0
    Negative = 0
    for label in data:
        if label == 'positive' or label ==  'POSITIVE':
            Possitive += 1
        else:
            Negative +=1
    pieVal = {'Positive': Possitive, 'Negative': Negative}
    return pieVal

LabVal = pandasToSentiment(csvPrep(csv_file_path,1))['Label']
LabVal2 = pandasToSentimentV2(csvPrep(csv_file_path,1))['Label']
print(LabVal)
print(LabVal2)


print(processDataForPie(LabVal))
print(processDataForPieV2(LabVal2))

# x = list(piedata.values())
# labels = list(piedata.keys())

# fig, ax = plt.subplots(figsize=(6, 6))
# ax.pie(x, labels=labels, autopct='%.1f%%')
# ax.set_title('Sentiment Base on Feedback')
# plt.tight_layout()
# plt.show()



#https://www.pythoncharts.com/matplotlib/pie-chart-matplotlib/