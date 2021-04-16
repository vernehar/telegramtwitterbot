from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import databasecontrol
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
api = Api(app)
connection = databasecontrol.openConnection()


class influencers(Resource):
    def get(self):
        data = databasecontrol.getCurrentInfluencers()
        #data = data.to_dict()  # convert dataframe to dictionary
        return {'data': data}, 200  # return data and 200 OK code

class follows(Resource):
    def get(self):
        influencer = request.args.get('name')
        data = databasecontrol.getCurrentInfluencerFollows(influencer)
        return {'data': data}

class twitterHandleSearch(Resource):
    def get(self):
        handle = request.args.get('handle')
        data = databasecontrol.GetInfluencerFollowsByHandle(handle)
        return {'data':data}

class trending(Resource):
    def get(self):
        hours = request.args.get('hours')
        data = databasecontrol.trendingWithinTimePeriod(int(hours))
        return {'data':data}


    
api.add_resource(influencers, '/influencers')  # '/users' is our entry point for Users
api.add_resource(follows, '/follows')  # '/users' is our entry point for Users
api.add_resource(twitterHandleSearch, '/handlesearch')
api.add_resource(trending, '/trending')

if __name__ == '__main__':
    app.run()  # run our Flask app