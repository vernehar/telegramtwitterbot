import tweepy
from tweepy import OAuthHandler
from tweepy import API
import json
import time

def twitterupdate():
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