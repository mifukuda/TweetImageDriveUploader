import os
import requests
from requests.models import HTTPError
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil

# Must have 'cache.txt', 'client_secrets.json', and 'images' folder in cwd

# Function for retreiving liked tweet images
def get_images():
    # BEARER_TOKEN stored as environment variable (re-enter every use)
    BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
    # Creating request URL
    headers = {'Authorization' : f'Bearer {BEARER_TOKEN}', 'User-Agent' : 'v2LikedTweetsPython'}
    # Info: https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-users-id-liked_tweets
    url = 'https://api.twitter.com/2/users/756179614154756096/liked_tweets'
    pagination_token = None
    download_active = True
    # Set counter <= n, where n is the number (in hundreds) of image requests
    counter = 1
    while(download_active and counter <= 3):
        # Alter max results if less required (max = 100)
        params = {'max_results' : '100', 'expansions' : 'attachments.media_keys', 'media.fields' : 'url', 'pagination_token' : pagination_token}
        try:
            # GET images
            res = requests.get(url, headers=headers, params=params)
            res.raise_for_status()
            res_json = res.json()
            print('Downloading files...')
            # Convert response to JSON and download image from each tweet
            for media in res_json['includes']['media']:
                # No image URL for tweet
                if 'url' not in media:
                    continue
                img_url = media['url']
                # Check if image has already been downloaded/uploaded in cache
                with open('cache.txt', 'r+') as cache_file:
                    if img_url not in cache_file.read():
                        # Download image
                        img = requests.get(img_url)
                        img.raise_for_status
                        # Write image data to file in binary
                        with open(os.path.join('images', os.path.basename(img_url)), 'wb') as imageFile:
                            for chunk in img.iter_content(100000):
                                imageFile.write(chunk)
                        # Cache image url
                        cache_file.write(img_url)
                        cache_file.write('\n')
            if 'next_token' in res_json['meta']:
                pagination_token = res_json['meta']['next_token']
                counter += 1
            else:
                print('No more images to download.')
                download_active = False
        except HTTPError as err:
            print(err)
        except KeyError:
            print("No images in current batch of liked tweets.")

# Uploading downloaded images to Google Drive folder
# Documentation: https://pythonhosted.org/PyDrive/quickstart.html#authentication
def upload_images():
    print('Authenticating...')
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    # Upload files
    print('Uploading files...')
    for file_name in os.listdir('images'):
        file = drive.CreateFile({'title': file_name, 'parents': [{'id': '1nsQen_n5t5c6mrLQbDr6742zN4qTmDy_'}]})
        file.SetContentFile(os.path.join('images', file_name))
        file.Upload()
        file = None

# Delete images once uploaded
def cleanup():
    print('Cleaning up...')
    shutil.rmtree('images')
    os.mkdir('images')

def main():
    get_images()
    if len(os.listdir('images')) == 0:
        print("No new files to upload.")
        return
    upload_images()
    cleanup()

if __name__ == "__main__":
    main()
