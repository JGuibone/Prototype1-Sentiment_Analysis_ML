import pandas as pd
import matplotlib.pyplot as plt
import pdfkit
from transformers import pipeline
from flask import render_template, make_response


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
    summarizer = pipeline("summarization", model="Model/bart-large-cnn-samsum")
    convo = '\n'.join(list(pd_series))
    result = summarizer(convo)[0]['summary_text']
    return result

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

def generatePDF(Data: dict):
    config = pdfkit.configuration(wkhtmltopdf = f'wkhtmltox/bin/wkhtmltopdf.exe')
    rendered = render_template('results.html', 
                               data=Data, 
                               SentimentTwitterTable=[Data['Sentiment-TwitterModel'].to_html(classes='data')], 
                               SentimentTwitterTitle=Data['Sentiment-TwitterModel'].columns.values,
                               SentimentGPT2Table=[Data['Sentiment-GPT2'].to_html(classes='data')], 
                               SentimentGPT2Title=Data['Sentiment-GPT2'].columns.values
                               
                               )
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename=output.pdf'

    return response

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
    else:
        x = list(Data.values())
        labels = list(Data.keys())
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(x, labels=labels, autopct='%.1f%%')
        ax.set_title('Sentiment Base on Feedback \n Using GPT-2 Model')
        plt.tight_layout()
        plt.savefig('website/PieChartImgs/SentimentGPT2.png')


#================================= TESTING Remove any un-commented code below this line when done ========================================