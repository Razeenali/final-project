import requests
import spoonacular as sp

# API key:
# 4c93056742bb42a8a2536a91e6630495


def getRecipeFrom(query):
    api = sp.API("4c93056742bb42a8a2536a91e6630495")
    # Parse an ingredient
    content = requests.get(
        f"https://api.spoonacular.com/recipes/search?query={query}&number=10" + "&apiKey=" + "4c93056742bb42a8a2536a91e6630495")
    json_response = content.json()
    return json_response


def getTitle(query):
    json_response = getRecipeFrom(query)
    results = json_response['results']
    title_list = []
    for item in results:
        title_list.append(item['title'])
    return title_list


def getInfo(query):
    json_response = getRecipeFrom(query)
    title = json_response['title']
    timePrepMin = json_response['readyInMinutes']
    numServings = json_response['servings']
    image = json_response['image']

# def getPrepTime(query):
#     pass


# def getNumServings(query):
#     pass


# def getImage(query):
#     pass



