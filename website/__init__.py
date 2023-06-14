from flask import Flask, render_template, request, make_response
from website.pyScripts.CoreFunctions import *
from pathlib import Path
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
            MainDict = dict.fromkeys(['Sentiment-TwitterModel','Sentiment-GPT2','Summary'])
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
                    GeneratePie(DataToPie(MainDict['Sentiment-TwitterModel']['Label']))
                    GeneratePie(DataToPie(MainDict['Sentiment-GPT2']['Label']))
            return generatePDF(MainDict)

        else:
            return 404

    @app.route("/test")
    def testroute():
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
        rendered = render_template('test.html', value1='Hello', value2='Word')
        pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
        
        

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline;filename=output.pdf'

        return response
        # pdfkit.from_url('http://google.com', 'out.pdf')
        # return 1

    @app.route("/test2", methods=['GET'])
    def testroute2():

        return 'Hello World'

    return app