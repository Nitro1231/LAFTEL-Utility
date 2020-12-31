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
    'Accept-Encoding':'gzip, deflate, br',
    'authority':'laftel.net',
    'accept':'application/json, text/plain, */*',
    'authorization':f'Token {token}',
    'laftel':'TeJava',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.108.15 Safari/537.36',
    'accept-language':'ko,en-US;q=0.9,en;q=0.8'
}

def getWishList(user_id):
    """
    Get wish items from the LAFTEL DB and return the JSON formatted list file.
     - ``user_id`` is a unique integer value that identifies the user.
     - Return ``JSON`` that includes the wish list.
    """
    response = requests.get(f'https://laftel.net/api/v1.0/users/{user_id}/rate/is_wish/', headers=headers)
    data = response.text
    wish = json.loads(data)
    return wish

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