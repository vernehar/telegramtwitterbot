import tweepy
from tweepy import OAuthHandler
from tweepy import API
import json
import time
import os
import databasecontrol

def twitterapi():

    print("updating..")
    #read twitter api credentials and declare them to variables
    creds = [line.rstrip() for line in open('credentials.txt')]

    consumer_key = creds[0]
    consumer_secret = creds[1]
    access_token = creds[2]
    access_secret = creds[3]

    #authorize twitter api use
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth,wait_on_rate_limit=True)
    print(api.rate_limit_status)
    
    return api


#def twitterupdate():

api = twitterapi()

#find users
influencers = []
influencers = databasecontrol.getCurrentInfluencers()
newFollows = {} #new dict that is returnet from function

print(influencers)

#Check if such account exists in twitter
def checkTwitterUser(userName, api):
    try:
        print("OK1")
        api.get_user(userName)

        currentInfluencers = databasecontrol.getCurrentInfluencers()
        print(currentInfluencers)
        if userName not in currentInfluencers:
            print("OK2")
            return True
        else:
            return False
    except:
        return False

#append user to influencer list and get current follows
def appendUserToList(userName):
    api = twitterapi()
    try:
        if checkTwitterUser(userName, api):
            newInfluencer = api.get_user(userName)
            databasecontrol.appendInfulencer(newInfluencer.screen_name)
            for friend in newInfluencer.friends():
                print(friend.screen_name)
                databasecontrol.newFollow(userName, friend.screen_name, True)
        return True
    except:
        return False
        
    else:
        return False

