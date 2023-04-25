from flask import request
from flask import Flask, render_template
from pyScripts.SentimentFunctions import stringSentement

app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def my_form_post():

    if request.method == 'POST':
        text = request.form['text']
        results = stringSentement(text)
        return render_template('index.html', variable=results)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(port='8088', threaded=False, debug=True)