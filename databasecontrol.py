import sqlite3
import string
import time
import calendar

#open connection to database
def openConnection():
    connection = sqlite3.connect("influencers.db", check_same_thread=False)
    return connection

#When a new influencer is added, add it to table "influencers" and make two tables, one to hold all the followings over
#time of that influencer, another to hold followings since last update
def appendInfulencer(_name):
    connection = openConnection()
    connection.execute("INSERT OR IGNORE INTO influencers VALUES(?)", (_name,))
    _name = checkName(_name)
    connection.execute("CREATE TABLE IF NOT EXISTS "+_name+" (follows text UNIQUE, time int)")
    newFollowsTableName = _name + "newfollows"
    connection.execute("CREATE TABLE IF NOT EXISTS "+newFollowsTableName+" (follows text UNIQUE, time int)")
    connection.commit()
    connection.close()

#return list of currently followed influencers
def getCurrentInfluencers():
    connection = openConnection()
    currentInfluencers = []
    connection.row_factory = lambda cursor, row: row[0]
    c = connection.cursor()
    for row in c.execute("SELECT name FROM influencers"):
        currentInfluencers.append(row)
    return currentInfluencers

#Get the current follows of influencers followed
def getCurrentInfluencerFollows(_influencer):
    connection = openConnection()
    _influencer = checkName(_influencer)
    connection.row_factory = lambda cursor, row: row[0]
    c = connection.cursor()
    currentFollows = c.execute("SELECT follows FROM "+_influencer).fetchall()
    return currentFollows

#When a new follow is found it is added to both the influencer specific table containing all follows 
#and the temporary one holding the ones since last update. NewInfluencer is set to true if the influencer is just added
#to avoid a huge data dump to telegram, e.g. when a new follower is added the current follows by that account are not 
#considered new
def newFollow(_influencer, _newFollowing, newInfluencer = False):
    connection = openConnection()
    _influencer = checkName(_influencer)
    newtuple = []
    newtuple.append((_newFollowing, calendar.timegm(time.gmtime())))
    connection.executemany("INSERT OR IGNORE INTO "+_influencer+" VALUES(?,?)", newtuple)
    if not newInfluencer:
        connection.executemany("INSERT OR IGNORE INTO "+_influencer+"newfollows VALUES(?,?)", newtuple)
    connection.commit()


#empty the [influencer]newfollows tables when update is requested from tg
def emptyNewFollows():
    connection = openConnection()
    currentInfluencers = getCurrentInfluencers()
    print(currentInfluencers)
    for i in range(len(currentInfluencers)):
        currentInfluencers[i] = checkName(currentInfluencers[i])
        connection.execute("DELETE FROM "+currentInfluencers[i]+"newfollows")
    connection.commit()
    connection.close()

#dump new follows as a dict to for a message from these to telegram
def dumpNewFollows():
    connection = openConnection()
    newFollows = {}
    currentInfluencers = getCurrentInfluencers()
    for i in range(len(currentInfluencers)):
        currentInfluencers[i] = checkName(currentInfluencers[i])
        connection.row_factory = lambda cursor, row: row[0]
        c = connection.cursor()
        changeloglist = c.execute("SELECT follows FROM "+currentInfluencers[i]+"newfollows").fetchall()
        if changeloglist:
            currentInfluencers[i] = returnNameToNormal(currentInfluencers[i])
            newFollows.update({currentInfluencers[i]: changeloglist})
    emptyNewFollows()
    return newFollows

def trendingWithinTimePeriod(_hours):
    seconds = _hours * 3600
    connection = openConnection()
    all24hFollows = []
    trending = {}
    currentInf = getCurrentInfluencers()
    for i in range(len(currentInf)):
        connection.row_factory = lambda cursor, row: row[0]
        c = connection.cursor()
        currentInf[i] = checkName(currentInf[i])
        follows = c.execute("SELECT follows FROM "+currentInf[i]+" WHERE time>"+str(calendar.timegm(time.gmtime())-seconds)).fetchall()
        all24hFollows.extend(follows)

    for j in range(len(all24hFollows)):
        count = all24hFollows.count(all24hFollows[j])
        if count > 2:
            trending.update({all24hFollows[j]:count})
    return trending

#return the current influencers as a parsed string, not so database related
def getCurrentInfluencersString():
    currentInfluencers = getCurrentInfluencers()
    influencerString = "\n"
    for i in range(len(currentInfluencers)):
        influencerString = influencerString + currentInfluencers[i] + "\n"
    return influencerString

#check that the account name does not stat with a number, if it does, add prefix NUM to the name to avoid sql error
def checkName(_name):
    if _name[0].isdigit():
        _name = "NUM" + _name
    return _name


#Remove the prefix for printing purposes
def returnNameToNormal(_name):
    if "NUM" in _name[0:3]:
        _name = _name.replace("NUM","")
        return _name
    else:
        return _name



