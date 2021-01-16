import codecs
import configparser
import json
import requests

# User Info
config = configparser.ConfigParser()
config.read('./config.ini', encoding='utf-8')
token = config.get('LAFTEL', 'token')
user_id = config.get('LAFTEL', 'user_id')

headers = {
    'laftel': 'TeJava',
    'authorization': f'Token {token}',
}

def getUserInfo():
    response = requests.get('https://laftel.net/api/v1.0/users/myinfo/', headers=headers)
    data = json.loads(response.text)
    return data, response.status_code

def getDailyItems():
    response = requests.get('https://laftel.net/api/search/v2/daily/', headers=headers)
    data = json.loads(response.text)
    return data, response.status_code

def searchAutoComplete(keyword):
    response = requests.get('https://laftel.net/api/search/v1/auto_complete/', headers=headers, params={ 'keyword': keyword })
    data = json.loads(response.text)
    return data, response.status_code

def searchItem(keyword):
    response = requests.get('https://laftel.net/api/search/v1/keyword/', headers=headers, params={ 'keyword': keyword })
    data = json.loads(response.text)
    return data, response.status_code

def getWishList(user_id):
    """
    Get wish list from the LAFTEL API and return the JSON object.
     - ``user_id`` is a unique integer value that identifies the user.
     - Return ``JSON`` that includes the wish list.
     - Return ``status code`` of the API request.
    """
    response = requests.get(f'https://laftel.net/api/v1.0/users/{user_id}/rate/is_wish/', headers=headers)
    data = json.loads(response.text)
    return data, response.status_code

def editWishItem(item_id, wish):
    """
    Modify the status of the wish item.
     - ``item_id`` is a unique integer id value of an item.
     - ``wish`` is a boolean type value that indicates the status of the item that you like to change.
     - Return ``status code`` of the API request.
    """
    response = requests.post(f'https://laftel.net/api/v1.0/items/{item_id}/wish/', headers=headers, data={ 'is_wish': wish })
    return response.status_code

def clearWishList(user_id, log=True):
    """
    Change the status of wish items in the user's wish lists to false.
     - ``user_id`` is a unique integer value that identifies the user.
     - If ``log`` is True, the function will print the item id and status code.
    """
    wish = getWishList(user_id)
    for key, value in wish.items():
        if value:
            code = editWishItem(key, False)
            if log: print(f'{key}:{code}')

def getItemDetail(item_id):
    """
    Get detailed information about the item.
     - ``item_id`` is a unique integer id value of an item.
     - Return ``JSON`` that includes detailed information about the item.
     - Return ``status code`` of the API request. 
    """
    response = requests.get(f'https://laftel.net/api/v1.0/items/{item_id}/detail/', headers=headers)
    data = json.loads(response.text)
    return data, response.status_code

def getItemEpisodes(item_id, limit=1000):
    """
    Get an episode list of an item that includes detailed information about each episode.
     - ``item_id`` is a unique integer id value of an item.
     - ``limit`` is the maximum number of the episode that will be returned.
     - Return ``JSON`` that includes detailed episode information about the item.
     - Return ``status code`` of the API request. 
    """
    params = {
        'item_id': item_id,
        'limit': limit
    }
    response = requests.get('https://laftel.net/api/episodes/v1/list/', headers=headers, params=params)
    data = json.loads(response.text)
    return data, response.status_code

def getRelatedItem(item_id):
    """
    Get a list of a related item. This includes the series of the current item or the item that has similar characteristics.
     - ``item_id`` is a unique integer id value of an item.
     - Return ``JSON`` that includes detailed episode information about the item.
     - Return ``status code`` of the API request. 
    """
    response = requests.get(f'https://laftel.net/api/v1.0/items/{item_id}/related/', headers=headers)
    data = json.loads(response.text)
    return data, response.status_code

def getDiscoverList():
    response = requests.get('https://laftel.net/api/v1.0/info/discover/', headers=headers)
    data = json.loads(response.text)
    return data, response.status_code

def getItem(years=[], tags=[], exclude_tags=[], genres=[], exclude_genres=[], sort='rank', viewable=None, svod=None, ending=None):
    params = {
        'years': (','.join(years)),
        'tags': (','.join(tags)),
        'exclude_tags': (','.join(exclude_tags)),
        'genres': (','.join(genres)),
        'exclude_genres': (','.join(exclude_genres)),
        'sort': sort,
        'viewable': viewable,
        'svod': svod,
        'ending': ending
    }
    response = requests.get('https://laftel.net/api/search/v1/discover/', headers=headers, params=params)
    data = json.loads(response.text)
    return data, response.status_code

#print(getItem(['2021년 1분기', '2020년 4분기'], ['이세계'], ['학교'], ['판타지'], ['순정'], 'recent'))
#print(getItem())