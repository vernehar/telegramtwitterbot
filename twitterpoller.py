import twitterbotv3
import databasecontrol
import time

init = False

if not init:
    try:
        api = twitterbotv3.twitterapi()
        init = True
    except:
        time.sleep(60)
        api = twitterbotv3.twitterapi()
        init = True

#find users
influencers = []
influencers = databasecontrol.getCurrentInfluencers()
newFollows = {} #new dict that is returnet from function

#poll twitter api indefinately
print(influencers)
while True:
    for j in range(len(influencers)):
        try:
            print(j)
            time.sleep(60) #API has request limits, wait one minute between polls
            user = api.get_user(influencers[j])
            print(api.rate_limit_status)

            userfollows = databasecontrol.getCurrentInfluencerFollows(influencers[j])

            #Get current accounts that the user follows
            currentfriends = []
            for friend in user.friends():
                currentfriends.append(friend.screen_name)
                    
            print(currentfriends)

            #Check if there are friends new followings and append them to list
            changeloglist = []
            for i in range(len(currentfriends)):
                if (currentfriends[i] not in userfollows):
                    databasecontrol.newFollow(influencers[j], currentfriends[i], False)
        except:
            time.sleep(60)
