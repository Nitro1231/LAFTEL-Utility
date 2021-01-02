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
    'laftel':'TeJava',
    'authorization':f'Token {token}',
}

def getUserInfo():
    response = requests.get('https://laftel.net/api/v1.0/users/myinfo/', headers=headers)
    data = json.loads(response.text)
    return data

def getDailyItems():
    response = requests.get('https://laftel.net/api/search/v2/daily/', headers=headers)
    data = json.loads(response.text)
    return data

def searchAutoComplete(keyword):
    response = requests.get('https://laftel.net/api/search/v1/auto_complete/', headers=headers, params={ 'keyword': keyword })
    data = json.loads(response.text)
    return data

def searchItem(keyword):
    response = requests.get('https://laftel.net/api/search/v1/keyword/', headers=headers, params={ 'keyword': keyword })
    data = json.loads(response.text)
    return data

def getWishList(user_id):
    """
    Get wish items from the LAFTEL DB and return the JSON formatted list file.
     - ``user_id`` is a unique integer value that identifies the user.
     - Return ``JSON`` that includes the wish list.
    """
    response = requests.get(f'https://laftel.net/api/v1.0/users/{user_id}/rate/is_wish/', headers=headers)
    data = json.loads(response.text)
    return data

def editWishItem(item_id, wish):
    """
    Modify the status of the wish item.
     - ``item_id`` is a unique integer id value of an item (or Anime).
     - ``wish`` is a boolean type value that indicates the status of the item that you like to change. 
     - Return ``status code`` of the API request. 
    """
    response = requests.post(f'https://laftel.net/api/v1.0/items/{item_id}/wish/', headers=headers, data={ 'is_wish': wish })
    return response.status_code

def clearWishList(user_id):
    """
    Change the status of wish items in the user's wish lists to false.
     - ``user_id`` is a unique integer value that identifies the user.
    """
    wish = getWishList(user_id)
    for key, value in wish.items():
        if value:
            code = editWishItem(key, False)
            print(f'{key}:{code}')

def getItemDetail(item_id):
    response = requests.get(f'https://laftel.net/api/v1.0/items/{item_id}/detail/', headers=headers)
    data = json.loads(response.text)
    return data

def getItemEpisodes(item_id, limit=1000):
    params = {
        'item_id': item_id,
        'limit': limit
    }
    response = requests.get('https://laftel.net/api/episodes/v1/list/', headers=headers, params=params)
    data = json.loads(response.text)
    return data

def getRelatedItem(item_id):
    response = requests.get(f'https://laftel.net/api/v1.0/items/{item_id}/related/', headers=headers)
    data = json.loads(response.text)
    return data

def getDiscoverList():
    response = requests.get('https://laftel.net/api/v1.0/info/discover/', headers=headers)
    data = json.loads(response.text)
    return data

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
    return data

#print(getItem(['2021년 1분기', '2020년 4분기'], ['이세계'], ['학교'], ['판타지'], ['순정'], 'recent'))
#print(getItem())