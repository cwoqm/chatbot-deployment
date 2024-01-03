#db_operations.py
from flask import Flask, request, jsonify
import requests
import pymongo
from bs4 import BeautifulSoup

mongo_url = "mongodb+srv://admin:admin@cluster0.uksugso.mongodb.net/dictation"

try:
    client = pymongo.MongoClient(mongo_url)
    if client.server_info():
        print("Connected to MongoDB successfully!")
    db = client.dictation
    Collection = db.user_google
    Collection2 = db.user
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}")

userName = "user1969"

# https://dictation2-cjedgb.5sc6y6-4.usa-e2.cloudhub.io/api/users/author

# def get_user_name():
#     url = "https://dictation2-cjedgb.5sc6y6-4.usa-e2.cloudhub.io/api/users/author"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         user_name = data.get("userName")
#         return user_name
#     except requests.exceptions.RequestException as e:
#         print(f"Error during request: {e}")
#         return "not found"
# userName = get_user_name()

def get_user_full_name():
    try:
        # user_full_name = Collection.find_one({"userName": userName})["fullName"]
        # return user_full_name
        user_google_document = Collection.find_one({"userName": userName})

        if user_google_document:
            user_full_name = user_google_document["fullName"]
            return user_full_name

        # If not found in user_google collection, try the user collection
        user_document = Collection2.find_one({"userName": userName})

        if user_document:
            user_full_name = user_document["fullName"]
            return user_full_name
    except Exception as e:
        print(f"Error retrieving user name: {str(e)}")
        return "Not Found"
    
def get_score():
    try:
        user_scores = db.score.find({"userName": userName}).sort("time", -1).limit(1)
        scores_list = [score["score"] for score in user_scores]
        return scores_list
        # user_scores = db.score.find({"userName": userName}).sort("time", -1).limit(3)
        # # scores_list = [(score["time"], score["score"]) for score in user_scores]
        # scores_list = [score["score"] for score in user_scores]
        # return f"3 latest scores: {scores_list}"
    except Exception as e:
        return "Not Found"