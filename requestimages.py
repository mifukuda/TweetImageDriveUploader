import os
import requests
from requests.models import HTTPError
from pydrive.auth import GoogleAuth


# function for retreiving liked tweet images
def get_images():
    # BEARER_TOKEN stored as environment variable (re-enter every use)
    BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
    headers = {'Authorization' : f'Bearer {BEARER_TOKEN}', 'User-Agent' : 'v2LikedTweetsPython'}
    params = {'max_results' : '5', 'expansions' : 'attachments.media_keys', 'media.fields' : 'url'}
    url = 'https://api.twitter.com/2/users/756179614154756096/liked_tweets'
    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        for media in res.json()['includes']['media']:
            img_url = media['url']
            img = requests.get(img_url)
            img.raise_for_status
            with open(os.path.join('images', os.path.basename(img_url)), 'wb') as imageFile:
                for chunk in img.iter_content(100000):
                    imageFile.write(chunk)
    except HTTPError as err:
        print(err)

def upload_images():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

get_images()