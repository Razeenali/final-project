# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_pymongo import PyMongo
import model
import bcrypt


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
@app.route('/')
@app.route('/index')
def index():
    # collection = mongo.db.events
    # events = collection.find({})
    if request.method == 'POST':
        session.clear()
        return render_template('index.html')
    return render_template('index.html')


# CONNECT TO DB, ADD DATA
# Allows login user to see their custom set of favorite foods
# For a given collection called 'user' inside the database 'user_favorites'
# add to collection that contains key value pairs
@app.route('/user_favorites', methods=['POST', 'GET'])
def user_favorites():
    username = session["username"]
    # list of ingredients for chosen favorite dish to add
    user_fav_ingredients = []
    if 'username' in session:
        if request.method == 'GET':
            collection = mongo.db.users
            user_document = list(collection.find({'username':username}))
            return render_template('user_favorites.html', fav_foods=user_document[0]['favFood'])
        else:
            dishID = request.form['dishID']
            # print('Type of DishID: ' + type(dishID))
            # list of dictionaries representing ingredients
            ingredients = model.getFavorite(dishID)['extendedIngredients']
            # obtain string description from each ingredient dictionary
            # and add to user_fav_ingredients list
            for ing in ingredients:
                user_fav_ingredients.append(ing['originalString'])
            # users collection
            collection = mongo.db.users
            # specific session user document with given username
            # Add list of favorite dish information to session user document
            # if dish not yet marked favorite
            # print("Type of: collection.find({'username':username}))" + type(collection.find({'username':username})))
            test = False
            for dish_item in list(collection.find({'username':username}))[0]['favFood']:
                if dish_item['Dish ID'] == dishID:
                    test = True
            if not test:
                collection.update_one({'username': username}, { '$push': {"favFood": {"Dish ID": dishID, "Dish title": model.getFavorite(dishID)['title'], "ingredients": user_fav_ingredients}}})
                user_document = list(collection.find({'username':username}))
                print(user_document)
                return render_template('user_favorites.html', fav_foods=user_document[0]['favFood'], username=username)
            return 'Dish already exists'
    else:
        return "You are not logged in! Go to <a href='/index'>home</a>."


@app.route('/loginsignup', methods=['GET', 'POST'])
def loginsignup():
    session.clear()
    if request.method == 'GET':
        return render_template('loginsignup.html')
    else:
        array = []
        username = request.form["username"]
        password = request.form["password"]
        collection = mongo.db.users
        user = list(collection.find({"username":username}))
        # if username does not exist already
        if len(user) == 0:
            collection.insert_one({"username": username, "password": str(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()), 'utf-8'), "favFood": array})
            session["username"] = username
            return render_template('loginsignup.html')
        elif bcrypt.hashpw(password.encode('utf-8'), user[0]['password'].encode('utf-8')) == user[0]['password'].encode('utf-8'):
            session["username"] = username
            return render_template('loginsignup.html')
        else:
            return render_template('loginsignup.html')
        return "Sorry, username already exists. Please try again! <a href='/index'>home</a>"


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


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')
