import requests
import spoonacular as sp

# API key:
# 4c93056742bb42a8a2536a91e6630495


def getRecipeFrom(query):
    api = sp.API("4c93056742bb42a8a2536a91e6630495")

    num_results = 20

    # Parse an ingredient
    content = requests.get(
        f"https://api.spoonacular.com/recipes/search?query={query}&number={num_results}" + "&apiKey=" + "4c93056742bb42a8a2536a91e6630495")
    json_response = content.json()
    return json_response


# def getTitle(query):
#     json_response = getRecipeFrom(query)
#     results = json_response['results']
#     title_list = []
#     print(type(json_response))
#     for item in results:
#         title_list.append(item['title'])
#     return title_list

# def getPrepTime(query):
#     json_response = getRecipeFrom(query)
#     results = json_response['results']
#     prepTime_list = []
#     for item in results:
#         prepTime_list.append('{}{}{}'.format('Prep Time: ', item['readyInMinutes'], ' minutes'))
#     return prepTime_list


def getInfo(query):
    json_response = getRecipeFrom(query)
    list_dishes = []
    for dish in json_response['results']:
        list_dishes.append(dish)
    # print(list_dishes)
    return list_dishes
