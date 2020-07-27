# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo
import model
from flask import session
import bcrypt
from flask import redirect, url_for


# -- Initialization section --
app = Flask(__name__)

app.secret_key = "eka23l2j1jkasd"

# name of database
# Stores user email signups (footer)
app.config['MONGO_DBNAME'] = 'user_information'
# Stores user login information
app.config['MONGO_DBNAME'] = 'user_favorites'

# database user: admin
# password: B6ZboUGoYAC0RVeq

# URI of database
# mongodb+srv://admin:<password>@cluster0.34ojx.mongodb.net/<dbname>?retryWrites=true&w=majority
app.config['MONGO_URI'] = 'mongodb+srv://admin:B6ZboUGoYAC0RVeq@cluster0.34ojx.mongodb.net/user_information?retryWrites=true&w=majority'
app.config['MONGO_URI'] = 'mongodb+srv://admin:B6ZboUGoYAC0RVeq@cluster0.34ojx.mongodb.net/user_favorites?retryWrites=true&w=majority'

mongo = PyMongo(app)


# -- Routes section --
# index or Home page
# @app.route('/')
# @app.route('/index')
# def index():
#     collection = mongo.db.events
#     events = collection.find({})
#     return render_template('index.html', events=events)
@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():

    collection = mongo.db.events
    events = collection.find({})
    if request.method == 'GET':
        return render_template('index.html', events=events)
    else:
        username = request.form["username"]
        password = request.form["password"]
        collection = mongo.db.users
        user = list(collection.find({"username":username}))
        if len(user) == 0:
            collection.insert_one({"username": username, "password": str(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()), 'utf-8')})
            session["username"] = username
            # return "You are logged in.  Go to <a href='/index'>home</a>."
            return render_template('index.html', events=events)
        elif bcrypt.hashpw(password.encode('utf-8'), user[0]['password'].encode('utf-8')) == user[0]['password'].encode('utf-8'):
            session["username"] = username
            print(session["username"])
            print(session)
            # return "Welcome back  Go to <a href='/index'>home</a>."
            return render_template('index.html', events=events)
        else:
            return "Error"


# User email signup, adds user email to database 'user_information' and 
# redirects to successSignUp.html to show successful signup
@app.route('/user_information', methods=['GET', 'POST'])
def user_information():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        user_email = request.form['user_email']

        collection = mongo.db.events
        collection.insert({"email": user_email})
        user_information = collection.find({})
        return render_template('successSignUp.html', user_information=user_information)


# returns a list of dishes from API given a key word
@app.route('/recipes', methods=['POST', 'GET'])
def recipes():
    list_dishes = model.getListDishes(request.form['foodQ'])
    if 'username' in session:
        print('hello')
        return render_template('loggedInRecipes.html', list_dishes=list_dishes)
    return render_template('recipes.html', list_dishes=list_dishes)


# returns dict of ingredients given a dish ID
@app.route('/ingredients', methods=['POST', 'GET'])
def ingredients():
    information = model.getInformation(request.form['dishID'])
    print(type(information))
    return render_template('ingredients.html', information=information)


# Allows login user to see their custom set of favorite foods
@app.route('/user_favorites', methods=['POST', 'GET'])
def user_favorites():
    user_fav_ingredients = []
    if 'username' in session:
        collection = mongo.db.foods
        dishID = request.form['dishID']
        ingredients = model.getFavorite(dishID)['extendedIngredients']
        for ing in ingredients:
            user_fav_ingredients.append(ing['originalString'])
        collection.insert({"Dish ID": dishID, "Dish title:": model.getFavorite(dishID)['title'], "ingredients": user_fav_ingredients})
        foods = collection.find({})
        return render_template('user_favorites.html', dishID=dishID, ingredients=ingredients, foods=foods, user_fav_ingredients=user_fav_ingredients)
    return 'error'

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')
