import codecs
import configparser
import json
import requests
from urllib import parse

# User Info
config = configparser.ConfigParser()
config.read('./config.ini', encoding='utf-8')
token = config.get('LAFTEL', 'token')
user_id = config.get('LAFTEL', 'user_id')

headers = {
    'laftel':'TeJava',
    'authorization':f'Token {token}',
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

def getItemByYears(years, sort='rank'):
    year = parse.quote(','.join(years))
    response = requests.get(f'https://laftel.net/api/search/v1/discover/?sort={sort}&years={year}', headers=headers)
    data = json.loads(response.text)
    return data

def getItemByTags(tags, exclude_tags=[], sort='rank'):
    tag = parse.quote(','.join(tags))
    exclude_tag = parse.quote(','.join(exclude_tags))
    response = requests.get(f'https://laftel.net/api/search/v1/discover/?sort={sort}&tags={tag}&exclude_tags={exclude_tag}', headers=headers)
    data = json.loads(response.text)
    return data

def getItemByGenres(genres, exclude_genres=[], sort='rank'):
    genre = parse.quote(','.join(genres))
    exclude_genre = parse.quote(','.join(exclude_genres))
    response = requests.get(f'https://laftel.net/api/search/v1/discover/?sort={sort}&genres={genre}&exclude_genres={exclude_genre}', headers=headers)
    data = json.loads(response.text)
    return data

def getItem(years=[], tags=[], exclude_tags=[], genres=[], exclude_genres=[], sort='rank'):
    year = parse.quote(','.join(years))
    tag = parse.quote(','.join(tags))
    exclude_tag = parse.quote(','.join(exclude_tags))
    genre = parse.quote(','.join(genres))
    exclude_genre = parse.quote(','.join(exclude_genres))

    response = requests.get(f'https://laftel.net/api/search/v1/discover/?sort={sort}&years={year}&tags={tag}&exclude_tags={exclude_tag}&genres={genre}&exclude_genres={exclude_genre}', headers=headers)
    data = json.loads(response.text)
    return data

#print(getItemByYears([]))
#print(getItemByYears(['2020년 1분기', '2020년 2분기']))
#print(getItemByTags(['먼치킨', '이세계'], ['역하렘']))
#print(getItemByTags([], ['게임']))
#print(getItemByGenres(['판타지', '로맨스'], ['액션']))
#print(getItem(['2021년 1분기', '2020년 4분기'], ['이세계'], ['학교'], ['판타지'], ['순정'], 'recent'))