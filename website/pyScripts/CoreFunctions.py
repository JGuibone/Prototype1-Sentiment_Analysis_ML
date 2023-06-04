import pandas as pd
from transformers import pipeline


#output

# nparr = [[string,string,string],
        # [string,string,string],
        # [string,string,string],
        # [string,string,string]]


#================================= TESTING Remove any un-commented code below this line when done ========================================

def csvPrep(csv_file, column_num):
    # No Error Checking.
    pdtable = pd.read_csv(csv_file)
    pd_data = pdtable.iloc[:,column_num]
    return pd_data

def pandasToSummarize(pd_series):
    #uses HuggingFace Transformers pipeline Library, No Error Checking.
    summarizer = pipeline("summarization", model="Model/bart-large-cnn-samsum")
    convo = '\n'.join(list(pd_series))
    result = summarizer(convo)[0]['summary_text']
    return result
    

def pandasToSentiment(pd_series):
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
