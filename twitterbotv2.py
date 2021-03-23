import tweepy
from tweepy import OAuthHandler
from tweepy import API
import json
import time
import os

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


def twitterupdate():

    api = twitterapi()

    #find users
    influencers = []
    influencers = open("influencers.txt","r").readlines()
    newFollows = {} #new dict that is returnet from function
    print(influencers)
    for j in range(len(influencers)):
        print(j)
        user = api.get_user(influencers[j].rstrip())
        print(api.rate_limit_status)

        try:
            userfile = open(influencers[j].rstrip() + ".txt","r")
        except IOError:
            userfile = open(influencers[j].rstrip() + ".txt","w+")
            userfile.close()
        userfile = open(influencers[j].rstrip() + ".txt","r")
        userfollows = userfile.readlines()

        userfile.close()

        #Get current accounts that the user follows
        currentfriends = []
        for friend in user.friends():
            currentfriends.append(friend.screen_name)
        
        print(currentfriends)

    #print(currentfriends)

        open(influencers[j].rstrip()+"newfollowings.txt", 'w').close()

        #Check if there are friends new followings and append them to list
        changeloglist = []
        for i in range(len(currentfriends)):
            if (currentfriends[i]+"\n" not in userfollows):
                changelog = open(influencers[j].rstrip()+"newfollowings.txt","a")
                userfile = open(influencers[j].rstrip()+".txt","a")
                changelog.writelines(currentfriends[i] + "\n")
                userfile.writelines(currentfriends[i] + "\n")
                changeloglist.append(currentfriends[i])

        if changeloglist: #If changeloglist is empty (no new followers for this influencer) then don't append to dict
            newFollows.update({influencers[j].rstrip(): changeloglist})
    
    return newFollows


def checkTwitterUser(userName, api):
    try:
        print("OK1")
        api.get_user(userName)

        currentInfluencers = [line.rstrip() for line in open('influencers.txt')]
        print(currentInfluencers)
        if userName not in currentInfluencers:
            print("OK2")
            return True
        else:
            return False
    except:
        return False

def appendUserToList(userName):
    api = twitterapi()
    if checkTwitterUser(userName, api):
        try:
            open("influencers.txt","a").writelines(userName + "\n")

            newInfluencer = api.get_user(userName)

            newInfluencerFile = open(userName + ".txt","w")
            newInfluencerNewFollowings = open(userName + "newfollowings.txt","w")

            for friend in newInfluencer.friends():
                newInfluencerFile.writelines(friend.screen_name + "\n")
                newInfluencerNewFollowings.writelines(friend.screen_name + "\n")
            
            newInfluencerFile.close()
            newInfluencerNewFollowings.close()
            return True
        except:
            return False
    else:
        return False

def getCurrentInfluencers():
    currentInfluencers = [line.rstrip() for line in open('influencers.txt')]
    influencerString = "\n"
    for i in range(len(currentInfluencers)):
        influencerString = influencerString + currentInfluencers[i] + "\n"
    return influencerString
