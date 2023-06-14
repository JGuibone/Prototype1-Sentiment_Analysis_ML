import pdfkit
import matplotlib as plt
from flask import render_template, make_response

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


def PDFTEST():
    
    return 1