import urllib2
import json
import time
from flask import Flask


app = Flask(__name__) # instantiate Flask

# loop through participants
def getParticipants():

    file = open('participants.json', "r")
    jsonText =  file.read()
    response = json.loads(jsonText)
    return response

# get user stats using Gerrit API
def getUserStats(username):
    
    if username!="":
        # concatenate url
        url = "https://gerrit.wikimedia.org/r/changes/?q=owner:" + username;
        
        request = urllib2.Request(url)
        result = urllib2.urlopen(request)
        jsonArray = result.read()

        jsonArray = jsonArray.replace(")]}'", ""); # Fix this error in headers of json tree
        return json.loads(jsonArray);

# create json file for monthly stats
def createJsonFile(jsonArray):
    filename = getCurrentMonth()
    with open('stats/' + filename + '.json', 'w') as f:
        f.write(str(jsonArray))  # convert result to string ad save it

# get current month
def getCurrentMonth():
    currentMonth = time.strftime("%Y-%m"); # eg: ./stats/2018-02.json 
    return currentMonth   

# cron job for fetching and saving stats
def cronTask():
    # load and save participants stats
    participants = getParticipants()

    monthlyStats = []
    for participant in participants:

        username = participant['username']
        patches = getUserStats(username)

        participant_patches = []; 

        for patch in patches:
            participant_patches.append(patch)   

        monthlyStats.append([username, participant_patches])


    # convert from array to json
    createJsonFile(json.dumps(monthlyStats))