import requests
import spoonacular as sp

# API key: 4c93056742bb42a8a2536a91e6630495


def getRecipeFrom(query):
    api = sp.API("4c93056742bb42a8a2536a91e6630495")
    num_results = 20
    content = requests.get(
        f"https://api.spoonacular.com/recipes/search?query={query}&number={num_results}&apiKey=4c93056742bb42a8a2536a91e6630495")
    json_response = content.json()
    return json_response


# def getListID(query):
#     json_response = getRecipeFrom(query)
#     list_ID = []
#     for dish in json_response['results']:
#         list_ID.append(dish['id'])
#     return list_ID


def getListDishes(query):
    json_response = getRecipeFrom(query)
    list_dishes = []
    for dish in json_response['results']:
        list_dishes.append(dish)
    return list_dishes


# Get Recipe Information
# def getInformation(query):
#     content = requests.get(f'https://api.spoonacular.com/recipes/{query}/information?apiKey=4c93056742bb42a8a2536a91e6630495&includeNutrition=false')
#     json_response = content.json()
#     return json_response

def getFavorite(iden):
    content = requests.get(f'https://api.spoonacular.com/recipes/{iden}/information?apiKey=4c93056742bb42a8a2536a91e6630495&includeNutrition=false')
    json_response = content.json()
    return json_response
