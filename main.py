# This uses python 3.* and DO NOT support python 2.*
# This project requires tweepy, urllib, google.cloud, PILLOW and ffmpeg libraries.
# Setting up authentication for Google Cloud is REQUIRED before running this program
import tweepy
#Ref:https://github.com/tweepy/tweepy
from urllib import request
import os
import io
from google.cloud import vision
from google.cloud.vision import types
#Ref:https://cloud.google.com/vision/docs/libraries#client-libraries-install-python
from PIL import Image, ImageDraw, ImageFont
#Ref:https://pillow.readthedocs.io/en/5.2.x/#
import ffmpeg
#Ref:https://github.com/kkroening/ffmpeg-python

# Input your keys and secrets of twiiter API, so that the program can use it to access to the api
consumer_key = YOUR_consumer_key
consumer_secret = YOUR_consumer_secret
access_key = YOUR_access_key
access_secret = YOUR_access_secret

# Input the direction of your fonts here
fonts = YOUR_FONTS

def download_tweets(Name):
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


def get_labels():
    # Setup to access to the Google Vision API
    client = vision.ImageAnnotatorClient()
    i = 1
    print('Getting labels from google and printing labels on it')
    while(1):
        # Check if there are pictures inside the folder
        if os.path.exists('./PICS/'+str(i)+'.jpg') == True:
            file_name = os.path.join(os.path.dirname(__file__),'./PICS/'+str(i)+'.jpg')
            # Read the pictures and get ready to push it to Google
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()
        
            image = types.Image(content=content)
		
            # Get the labels from Google Vision
            response = client.label_detection(image=image)
            labels = response.label_annotations
            # Setup PILLOW to put labels into the picture
            im = Image.open('./PICS/'+str(i)+'.jpg')
            draw = ImageDraw.Draw(im)
            myfont = ImageFont.truetype(fonts, size=35)
            fillcolor = 'red'
            # Put labels into the picture
            m = 0
            for label in labels:
                m = m + 1
                draw.text((40, 40*m), label.description, font=myfont, fill=fillcolor)
                if m > 2:
                    break
            im.save('./PICS/'+str(i)+'.jpg', 'JPEG')
            i = i + 1
        # Print the total number of the pictures
        else:
            print(str(i - 1)+' pictures completed')
            break

def Put_to_video():
    # Use ffmpeg to convert the pictures into a video
    os.system("ffmpeg -framerate 1 -pattern_type glob -i './PICS/*.jpg' -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4")

def Delect_Files():
    # Delect the pictures downloaded in order to save storage space of the computer
    i = 1
    while(1):
        # Check if the path has pictures inside
        if os.path.exists('./PICS/'+str(i)+'.jpg'):
            os.remove('./PICS/'+str(i)+'.jpg')
            i = i + 1
        else:
            break
    os.removedirs('./PICS')

if __name__ == '__main__':
    Name = input("input Screen Name :")
    download_tweets(Name)
    if os.path.exists('./PICS/1.jpg') == True:
            get_labels()
            Put_to_video()
            Delect_Files()
            print('Output is completed')
    else:
        print('Error: no picture is downloaded from this twitter account')

