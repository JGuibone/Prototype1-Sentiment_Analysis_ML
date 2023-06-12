from flask import Flask, render_template, request, make_response
from website.pyScripts.CoreFunctions import csvPrep, pandasToSummarize, SentimentTwitterBase, SentimentGPT2, generatePDF, columnSelector
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
                    # print(summaryval)
                    # print(f"{sentiment} \n {summaryval}")
                    # print(type(summaryval))
            # print(MainDict['Sentiment'])
            return generatePDF(MainDict)

        else:
            return 404

    @app.route("/test")
    def testroute():
        config = pdfkit.configuration(wkhtmltopdf = f'wkhtmltox/bin/wkhtmltopdf.exe')
        rendered = render_template('test.html', value1='Hello', value2='Word')
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        
        

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