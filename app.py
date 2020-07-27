# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo
import model


# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'user_information'

# database user: admin
# password: B6ZboUGoYAC0RVeq

# URI of database
# mongodb+srv://admin:<password>@cluster0.34ojx.mongodb.net/<dbname>?retryWrites=true&w=majority
app.config['MONGO_URI'] = 'mongodb+srv://admin:B6ZboUGoYAC0RVeq@cluster0.34ojx.mongodb.net/user_information?retryWrites=true&w=majority'

mongo = PyMongo(app)


# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    collection = mongo.db.events
    events = collection.find({})
    return render_template('index.html', events=events)

@app.route('/user_information', methods = ['GET', 'POST'])
def user_information():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        user_email = request.form['user_email']

        collection = mongo.db.events
        collection.insert({"email": user_email})
        user_information = collection.find({})
        return render_template('successSignUp.html', user_information=user_information)

@app.route('/recipes', methods=['POST', 'GET'])
def recipes():
    list_dishes = model.getListDishes(request.form['foodQ'])
    return render_template('recipes.html', list_dishes=list_dishes)


@app.route('/ingredients', methods=['POST', 'GET'])
def ingredients():
    information = model.getInformation(request.form['dishID'])
    return render_template('ingredients.html', information=information)
