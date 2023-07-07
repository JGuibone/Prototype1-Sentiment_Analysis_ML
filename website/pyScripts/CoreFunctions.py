import pandas as pd
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import pdfkit
from transformers import pipeline
from flask import render_template, make_response
from os.path import dirname, join
from pathlib import Path

bartLocalPath = "Model/bart-large-cnn-samsum"
twitterLocalPath = f"Model/twitter-roberta-base-sentiment-2022"
gpt2LocalPath = f"Model/gpt2-medium-finetuned-sst2-sentiment"



def csvPrep(csv_file):
    # No Error Checking.
    pdtable = pd.read_csv(csv_file)
    pdtable.shift()[1:]
    # pdtable.rename(columns={})
    pd_data = pdtable.iloc[:, 1:]
    return pd_data

def columnSelector(Dataframe: pd.DataFrame, columnNumber):
    return Dataframe.iloc[:, columnNumber]

def pandasToSummarize(pd_series):
    #uses HuggingFace Transformers pipeline Library, No Error Checking.
    huggingFace = "philschmid/bart-large-cnn-samsum"
    if bartLocalPath != "":
        huggingFace = bartLocalPath
    summarizer = pipeline("summarization", model=huggingFace)
    convo = '\n'.join(list(pd_series))
    result = summarizer(convo)[0]['summary_text']
    return result

def SentimentTwitterBase(pd_series):
    #returns a pandas dataframe from processing the sentiment
    huggingFace = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
    if twitterLocalPath != "":
        huggingFace = twitterLocalPath
    sentiment = pd.DataFrame(columns=['Sentence','Label','Score'])
    sentiment_task = pipeline("sentiment-analysis", model=huggingFace, tokenizer=huggingFace)
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
    huggingFace = f"michelecafagna26/gpt2-medium-finetuned-sst2-sentiment"
    if twitterLocalPath != "":
        huggingFace = twitterLocalPath
    sentiment = pd.DataFrame(columns=['Sentence','Label','Score'])
    sentiment_task = pipeline("text-classification", model=huggingFace, tokenizer=huggingFace)
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

def generatePDF(Data: dict):
    css = "website/css/result.css"
    # imageLoc = 
    # pltPie = {}
    config = pdfkit.configuration(wkhtmltopdf = f'wkhtmltox/bin/wkhtmltopdf.exe')
    options = {
            "enable-local-file-access": True,
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None
            }
    summarize = render_template('summarize.html', 
                               data=Data, 
                               SentimentTwitterTable=[Data['Sentiment-TwitterModel'].to_html(classes='data')], 
                               SentimentTwitterTitle=Data['Sentiment-TwitterModel'].columns.values,
                               SentimentGPT2Table=[Data['Sentiment-GPT2'].to_html(classes='data')], 
                               SentimentGPT2Title=Data['Sentiment-GPT2'].columns.values
                               )
    pdf = pdfkit.from_string(summarize, False, configuration=config, options=options,css=css)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename=output.pdf'
    return response

def GeneratePie(Data :dict):
    rootdir = dirname(dirname(dirname(__file__)))
    twitterModel = Path('website/PieChartImgs/SentimentTwitter.png')
    GPT2Model = Path('website/PieChartImgs/SentimentGPT2.png')
    pltpie = plt
    numElem = len(Data)
    x = list(Data.values())
    labels = list(Data.keys())
    if numElem == 3:
        pltpie.pie(x, labels=labels, autopct='%.1f%%', wedgeprops={'edgecolor': 'black'})
        pltpie.title('Sentiment Base on Feedback \n Using Twitter roberta base')
        pltpie.savefig(twitterModel)
        pltpie.close()
        return join(rootdir,twitterModel)
    else:
        pltpie.pie(x, labels=labels, autopct='%.1f%%', wedgeprops={'edgecolor': 'black'})
        pltpie.title('Sentiment Base on Feedback \n Using GPT-2 Model')
        pltpie.savefig(GPT2Model)
        pltpie.close()
        return join(rootdir,GPT2Model)
    


#================================= TESTING Remove any un-commented code below this line when done ========================================