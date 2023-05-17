from flask import request
from flask import Flask, render_template
from website.pyScripts.SentimentFunctions import stringSentement


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'EO0UzmL6NVcL!t2&HlkW*@$h7dHfbjCIl*K*jSjZP@RX*UTM2$vGBV^hBQ*^I5FD'

    # @app.route('/', methods=['POST','GET'])
    # def my_form_post():

    #     if request.method == 'POST':
    #         text = request.form['text']
    #         results = stringSentement(text)
    #         return render_template('index.html', variable=results)
    #     else:
    #         return render_template('index.html')

    @app.route("/", methods=['POST','GET'])
    def index():
        # return 'testing route'
        return render_template('home.html')
    
    @app.route("/results")
    def results():
        # return 'testing route'
        return render_template('results.html')

    @app.route("/test")
    def testroute():
        return 'testroute'

    return app