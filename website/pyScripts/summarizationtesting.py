from transformers import pipeline
import pandas as pd

csv_file_path = 'website/testData/Survey Questions - Techono Event.csv'

pdtable = pd.read_csv(csv_file_path)

def csvPrep(csv_file, column_num):
    # No Error Checking.
    pdtable = pd.read_csv(csv_file)
    pd_data = pdtable.iloc[:,column_num]
    return pd_data

def pandasToSummarize(pd_series):
    #uses HuggingFace Transformers pipeline Library, No Error Checking.
    summarizer = pipeline("summarization", model="Model/bart-large-cnn-samsum")
    convo = '\n'.join(list(pd_series))
    return summarizer(convo)[0]['summary_text']
    

def pandasToSentiment(pd_series):
    nptable = pd_series.to_numpy()
    print(nptable)
    print(type(nptable))

pandasToSentiment(csvPrep(csv_file_path,2))


# result = summarizer(CSVToStr(csv_file_path))
# print(type(result))
# print(result[0]['summary_text'])
# print(CSVToStr(csv_file_path))