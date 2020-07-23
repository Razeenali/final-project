import requests
import spoonacular as sp

# API key:
# 4c93056742bb42a8a2536a91e6630495


def getRecipeFrom(query):
    api = sp.API("4c93056742bb42a8a2536a91e6630495")
    # Parse an ingredient
    content = requests.get(
        f"https://api.spoonacular.com/recipes/search?query={query}&number=5" + "&apiKey=" + "4c93056742bb42a8a2536a91e6630495")
    json_response = content.json()
    print(json_response)


# print(getRecipeFrom('beef'))
