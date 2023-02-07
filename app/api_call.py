from app import apiKey
import requests
import json

def api_data(searchKeys):
    try:
        url = "https://api.spoonacular.com/recipes/findByIngredients"

        params = {'ingredients':f'{searchKeys}',
                'apiKey':f'{apiKey}'      
                }
        rsp = requests.get(url,params=params)
        data = rsp.json()
        with open('./JSON/api_data.json', "w") as outfile:
            json.dump(data, outfile)
        status = 'DONE'
    except:
        status = 'ERROR'
    return status
