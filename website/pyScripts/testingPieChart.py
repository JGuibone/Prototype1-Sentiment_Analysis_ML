import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
from transformers import pipeline
import pandas as pd
from pathlib import Path
from os.path import dirname, join



csv_file_path = 'website/testData/Survey Questions - Techono Event.csv'

def csvPrep(csv_file):
    # No Error Checking.
    pdtable = pd.read_csv(csv_file)
    pdtable.shift()[1:]
    # pdtable.rename(columns={})
    pd_data = pdtable.iloc[:, 1:]
    return pd_data

def columnSelector(Dataframe: pd.DataFrame, columnNumber):
    return Dataframe.iloc[:, columnNumber]

def SentimentTwitterBase(pd_series):
    #returns a pandas dataframe from processing the sentiment
    sentiment = pd.DataFrame(columns=['Sentence','Label','Score'])
    sentiment_task = pipeline("sentiment-analysis", model=f"Model/twitter-roberta-base-sentiment-2022", tokenizer=f"Model/twitter-roberta-base-sentiment-2022")
    Sentence = []
    Label = []
    Score = []
    for item in pd_series:
        sentimentResult = sentiment_task(item)
        Sentence.append(item)
        Label.append(f"{sentimentResult[0]['label']}")
        Score.append(f"{format(sentimentResult[0]['score'], '.4f')}")
    sentiment['Sentence'] = pd.Series(Sentence)
    sentiment['Label'] = pd.Series(Label)
    sentiment['Score'] = pd.Series(Score)
    return sentiment

def SentimentGPT2(pd_series):
    #returns a pandas dataframe from processing the sentiment
    sentiment = pd.DataFrame(columns=['Sentence','Label','Score'])
    sentiment_task = pipeline("text-classification", model=f"Model/gpt2-medium-finetuned-sst2-sentiment", tokenizer=f"Model/gpt2-medium-finetuned-sst2-sentiment")
    Sentence = []
    Label = []
    Score = []
    for item in pd_series:
        sentimentResult = sentiment_task(item)
        Sentence.append(item)
        Label.append(f"{sentimentResult[0]['label'].lower()}")
        Score.append(f"{format(sentimentResult[0]['score'], '.4f')}")
    sentiment['Sentence'] = pd.Series(Sentence, dtype=str)
    sentiment['Label'] = pd.Series(Label, dtype=str)
    sentiment['Score'] = pd.Series(Score, dtype=float)
    return sentiment


def DataToPie(Data :pd.Series):
    numColumn = Data.nunique()
    if numColumn == 3:
        Positive = 0
        Neutral = 0
        Negative = 0
        for item in Data:
            if str(item).lower() == 'positive':
                Positive += 1
            elif str(item).lower() == 'neutral':
                Neutral += 1
            else:
                Negative += 1
        return {'Positive': Positive, 'Neutral': Neutral, 'Negative': Negative}
    else:
        Positive = 0
        Negative = 0
        for item in Data:
            if str(item).lower() == 'positive':
                Positive += 1
            else:
                Negative += 1
        return {'Positive': Positive, 'Negative': Negative}

def GeneratePie(Data :dict):
    numElem = len(Data)
    if numElem == 3:
        x = list(Data.values())
        labels = list(Data.keys())
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(x, labels=labels, autopct='%.1f%%')
        ax.set_title('Sentiment Base on Feedback \n Using Twitter roberta base')
        plt.tight_layout()
        plt.savefig('website/PieChartImgs/SentimentTwitter.png')
        return True
    else:
        x = list(Data.values())
        labels = list(Data.keys())
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(x, labels=labels, autopct='%.1f%%')
        ax.set_title('Sentiment Base on Feedback \n Using GPT-2 Model')
        plt.tight_layout()
        plt.savefig('website/PieChartImgs/SentimentGPT2.png')
        return True

def GeneratePie2(Data :dict):
    pltpie = plt
    numElem = len(Data)
    x = list(Data.values())
    labels = list(Data.keys())
    if numElem == 3:
        pltpie.pie(x, labels=labels, autopct='%.1f%%', wedgeprops={'edgecolor': 'black'})
        pltpie.title('Sentiment Base on Feedback \n Using Twitter roberta base')
        pltpie.savefig('website/PieChartImgs/SentimentTwitter.png')
        pltpie.close()
    else:
        pltpie.pie(x, labels=labels, autopct='%.1f%%', wedgeprops={'edgecolor': 'black'})
        pltpie.title('Sentiment Base on Feedback \n Using GPT-2 Model')
        pltpie.savefig('website/PieChartImgs/SentimentGPT2.png')
        pltpie.close()




# data = columnSelector(csvPrep(csv_file_path),0)
# TwitterModel = SentimentTwitterBase(data)['Label']
# GPT2Model = SentimentGPT2(data)['Label']
# GeneratePie(DataToPie(TwitterModel))
# GeneratePie(DataToPie(GPT2Model))

# MainDict = dict.fromkeys(['Sentiment-TwitterModel','Sentiment-GPT2','Summary'])
# CurrentData = csvPrep(csv_file_path)
# Sentiment = columnSelector(CurrentData, 0)
# MainDict['Sentiment-TwitterModel'] = SentimentTwitterBase(Sentiment)
# MainDict['Sentiment-GPT2'] = SentimentGPT2(Sentiment)

# print(MainDict['Sentiment-TwitterModel']['Label'])
# print("*****************")
# print(MainDict['Sentiment-GPT2']['Label'])
# print(DataToPie(MainDict['Sentiment-TwitterModel']['Label']))
# print("*****************")
# print(DataToPie(MainDict['Sentiment-GPT2']['Label']))
# GeneratePie2(DataToPie(MainDict['Sentiment-TwitterModel']['Label']))
# GeneratePie2(DataToPie(MainDict['Sentiment-GPT2']['Label']))


# UPLOAD = "website/PieChartImgs"
# projectroot = dirname(__file__)
# fileLoc = join(projectroot, 'SentimentGPT2.png')

# print(fileLoc)

# print(Path(UPLOAD,"SentimentGPT2.png"))

#https://www.pythoncharts.com/matplotlib/pie-chart-matplotlib/