from flask import Flask, render_template, request, make_response, redirect
from website.pyScripts.CoreFunctions import *
from pathlib import Path
from os.path import dirname, join
import pdfkit



def create_app():
    UPLOAD_FOLDER = Path("website/uploads")
    ALLOWED_EXTENSIONS = ['csv']

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'EO0UzmL6NVcL!t2&HlkW*@$h7dHfbjCIl*K*jSjZP@RX*UTM2$vGBV^hBQ*^I5FD'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        


    def allowed_file(filename):
        print(filename.rsplit('.', 1)[1].lower())
        return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route("/", methods=['GET','POST'])
    def index():
        return render_template('home.html')
        
    
    @app.route("/results", methods=['POST'])
    def results():
        if request.method == 'POST':
            files = request.files.getlist('file')
            MainDict = dict.fromkeys(['Sentiment-TwitterModel','Sentiment-GPT2','Summary', 'img1', 'img2'])
            for file in files:
                if 'file' not in request.files or file.filename == '':
                    continue
                if allowed_file(file.filename) == True:
                    CurrentData = csvPrep(file)
                    Sentiment = columnSelector(CurrentData, 0)
                    Summary = columnSelector(CurrentData, 1)
                    MainDict['Sentiment-TwitterModel'] = SentimentTwitterBase(Sentiment)
                    MainDict['Sentiment-GPT2'] = SentimentGPT2(Sentiment)
                    MainDict['Summary'] = pandasToSummarize(Summary)
                    MainDict['img1'] = GeneratePie(DataToPie(MainDict['Sentiment-TwitterModel']['Label']))
                    MainDict['img2'] = GeneratePie(DataToPie(MainDict['Sentiment-GPT2']['Label']))
            # return MainDict['img2']
                else:
                    
                    return redirect("/")
            return generatePDF(MainDict)
            # return "Generated"
        else:
            return 404
    return app