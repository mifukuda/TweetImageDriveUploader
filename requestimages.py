import os
import requests
from requests.models import HTTPError
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil

# Function for retreiving liked tweet images
def get_images():
    # BEARER_TOKEN stored as environment variable (re-enter every use)
    BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
    # Creating request URL
    headers = {'Authorization' : f'Bearer {BEARER_TOKEN}', 'User-Agent' : 'v2LikedTweetsPython'}
    # Info: https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-users-id-liked_tweets
    params = {'max_results' : '5', 'expansions' : 'attachments.media_keys', 'media.fields' : 'url'}
    url = 'https://api.twitter.com/2/users/756179614154756096/liked_tweets'
    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        print('Downloading files...')
        # Convert response to JSON and download image from each tweet
        for media in res.json()['includes']['media']:
            img_url = media['url']
            img = requests.get(img_url)
            img.raise_for_status
            # Write image data to file in binary
            with open(os.path.join('images', os.path.basename(img_url)), 'wb') as imageFile:
                for chunk in img.iter_content(100000):
                    imageFile.write(chunk)
    except HTTPError as err:
        print(err)

# Uploading downloaded images to Google Drive folder
# Documentation: https://pythonhosted.org/PyDrive/quickstart.html#authentication
def upload_images():
    print('Uploading files...')
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    # Upload files
    for file_name in os.listdir('images'):
        file = drive.CreateFile({'parents': [{'id': '1nsQen_n5t5c6mrLQbDr6742zN4qTmDy_'}]})
        file.SetContentFile(os.path.join('images', file_name))
        file.Upload()
        file = None

# Delete images once uploaded
def cleanup():
    print('Cleaning up...')
    shutil.rmtree('images')
    os.mkdir('images')

get_images()
upload_images()
cleanup()