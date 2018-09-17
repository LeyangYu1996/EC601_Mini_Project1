import tweepy
# Ref:https://github.com/tweepy/tweepy
import json
from urllib import request
import os

def download_tweets(Name):
    # Set the keys and secrets, so that we can use it to access to the api
    consumer_key = YOUR_KEY
    consumer_secret = YOUR_SECRET
    access_key = YOUR_CONSUMER_KEY
    access_secret = YOUR_CONSUMER_SECRET
    # Put the screen name into this part
    screenname = Name
    # Use the keys and secrets to access to the api
    auth = tweepy.OAuthHandler( consumer_key, consumer_secret)
    auth.set_access_token( access_key, access_secret)
    api = tweepy.API(auth)
    # Download first set of status
    print('Getting tweets')
    public_tweets = api.user_timeline(screen_name = screenname, count = 200)
    # Check if there is no tweets downloaded
    if(len(public_tweets) == 0):
        print('No Tweets found')
    else:
        # Get the urls of all pictures and save them into a list
        picurl = set()
        for status in public_tweets:
            media = status.entities.get('media', [])
            if(len(media) > 0):
                picurl.add(media[0]['media_url'])
        # Check if NO media files was found
        if(len(picurl) == 0):
            print('No Pictures Found or you inputed a wrong SCREEN NAME')
        # If there is media files, use urltrieve to download the urls
        else:
            if os.path.exists('./PICS') == False:
                os.makedirs('./PICS')
            i=0
            print('Downloading Pictures')
            for media_file in picurl:
                i=i+1
                path_name = os.path.join('./PICS/', str(i)+'.jpg')
                request.urlretrieve(media_file, path_name)


if __name__ == '__main__':
	download_tweets()
