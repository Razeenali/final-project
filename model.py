import requests
import spoonacular as sp
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("api_key")


def getRecipeFrom(query):
    api = sp.API({API_KEY})
    num_results = 20
    content = requests.get(
        f"https://api.spoonacular.com/recipes/search?query={query}&number={num_results}&apiKey={API_KEY}")
    json_response = content.json()
    return json_response


def getListDishes(query):
    json_response = getRecipeFrom(query)
    list_dishes = []
    for dish in json_response['results']:
        list_dishes.append(dish)
    return list_dishes


def getFavorite(iden):
    content = requests.get(f'https://api.spoonacular.com/recipes/{iden}/information?apiKey={API_KEY}&includeNutrition=false')
    json_response = content.json()
    return json_response
