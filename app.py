# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
import model


# -- Initialization section --
app = Flask(__name__)


# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/results', methods=['POST', 'GET'])
def results():
    recipe = model.getRecipeFrom(request.form['foodQ'])
    return render_template('results.html', recipe=recipe)
