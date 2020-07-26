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


@app.route('/recipes', methods=['POST', 'GET'])
def recipes():
    list_dishes = model.getListDishes(request.form['foodQ'])
    return render_template('recipes.html', list_dishes=list_dishes)


@app.route('/ingredients', methods=['POST', 'GET'])
def ingredients():
    information = model.getInformation(request.form['dishID'])
    return render_template('ingredients.html', information=information)
