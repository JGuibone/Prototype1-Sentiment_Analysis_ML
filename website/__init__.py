from flask import Flask, render_template, request, make_response
from website.pyScripts.CoreFunctions import *
from pathlib import Path
from os.path import dirname, join
import pdfkit



def create_app():
    UPLOAD_FOLDER = Path("website/uploads")
    ALLOWED_EXTENSIONS = 'csv'

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'EO0UzmL6NVcL!t2&HlkW*@$h7dHfbjCIl*K*jSjZP@RX*UTM2$vGBV^hBQ*^I5FD'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def allowed_file(filename):
        return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route("/", methods=['GET'])
    def index():
        # return 'testing route'
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

            return generatePDF(MainDict)
            # return "Generated"

        else:
            return 404

    @app.route("/test")
    def testroute():
        rootdir = dirname(dirname(__file__))
        css = "website/css/result.css"
        Data = {'img1': f"{Path(rootdir, 'website/PieChartImgs/SentimentGPT2.png')}", 'img2': r"C:\Users\johan\Documents\GitHub\School Work\Practicum\Prototype1-Sentiment_Analysis_ML\website\PieChartImgs\SentimentTwitter.png", 'validation': 'Data is pressent'}
        config = pdfkit.configuration(wkhtmltopdf = f'wkhtmltox/bin/wkhtmltopdf.exe')
        options = {
            "enable-local-file-access": True,
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None
                    }
        rendered = render_template('test.html', value1='Hello', value2='Word', data=Data)
        pdf = pdfkit.from_string(rendered, False, configuration=config, options=options, css=css)
        
        

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline;filename=output.pdf'
        # print(response)
        return response
        # pdfkit.from_url('http://google.com', 'out.pdf')
        # return 1


    return app