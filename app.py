from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response
from bson import ObjectId
import openai
# from db_operations import get_db

app = Flask(__name__)
CORS(app)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text =request.get_json().get("message")
    #todo: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

# @app.route("/get_fullname/<userName>", methods=["GET"])
# def get_fullname_by_username(userName):
#     try:
#         user_data = Collection.find_one({"userName": userName})

#         if user_data:
#             full_name = user_data.get("fullName", "User")  
#             return f"Full name for username {userName}: {full_name}"
#         else:
#             return f"No user found with username {userName}"

#     except Exception as e:
#         return f"Error retrieving user data: {str(e)}"
    
if __name__ == "__main__":
    app.run(debug=True)