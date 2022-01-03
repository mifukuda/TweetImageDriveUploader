import os
import requests

BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
r = {'Authorization' : f'Bearer {BEARER_TOKEN}', 'User-Agent' : 'v2LikedTweetsPython'}
print(r['Authorization'])
print(r['User-Agent'])
url = 'https://api.twitter.com/2/users/756179614154756096/liked_tweets'
