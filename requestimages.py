import os
import requests
from requests.models import HTTPError
from pydrive.auth import GoogleAuth

def get_images():
    BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
    headers = {'Authorization' : f'Bearer {BEARER_TOKEN}', 'User-Agent' : 'v2LikedTweetsPython'}
    params = {'max_results' : '5', 'expansions' : 'attachments.media_keys', 'media.fields' : 'url'}
    url = 'https://api.twitter.com/2/users/756179614154756096/liked_tweets'
    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        print(res.json()['includes'])
        return res.json()['includes']
    except HTTPError as err:
        print(err)

def upload_images():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() 

upload_images()