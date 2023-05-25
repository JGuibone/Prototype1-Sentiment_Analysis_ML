from flask import request
from flask import Flask, render_template
from website.pyScripts.SentimentFunctions import stringSentement, document2Array, sentimentV2
from pathlib import Path
import numpy as np


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
        # return 'testing route'
        if request.method == 'POST':
            files = request.files.getlist('file')
            for file in files:
                if 'file' not in request.files or file.filename == '':
                    continue
                if allowed_file(file.filename) == True:
                    table = sentimentV2(document2Array(file))
                    print(table)

        return render_template('results.html')

    @app.route("/test")
    def testroute():
        return 'testroute'

    return app