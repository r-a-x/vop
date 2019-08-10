from flask import Flask, request
from webargs import fields, flaskparser
import json, os

from services.reviewService import insert_review
from services.userService import signup_user, login_user
from video import get_video_feed

app = Flask(__name__)

parser = flaskparser.FlaskParser()


class CustomError(Exception):
    pass


@parser.error_handler
def handle_error(error, req, schema, status_code, headers):
    print(error, req, schema, status_code, headers)
    return {}, 200
    # raise CustomError(error.messages)


class CustomError(Exception):
    pass


def throw_error(code, success, message):
    return json.dumps({
        code: code,
        success: success,
        message: message
    }), 500


# "title": "string",
# "description": "string",
# "videourl": "String",
# "thumbnailurl": "String",
# "aflink": "string",
# "uid": "string",
# "username": "string"

# review = {"title": fields.Str(required=True),
#           "description": fields.Str(required=True),
#           "videoUrl": fields.Str(required=True),
#           "thumbnailUrl": fields.Str(required=True),
#           "afLink": fields.Str(required=True),
#           "username": fields.Str(required=True)}


@app.route("/")
def hello():
    return "Hello There!!"


def check_for_params(request_json, params=[]):
    for param in params:
        if param not in request_json or request_json[param] is None:
            return False, json.dumps({
                "error": param + " is not present in the request"
            }), 400
    return True, None


# Every user can create more than one
review_params = ["title", "description", "videoUrl", "thumbnailUrl", "afLink", "username"]


@app.route("/review", methods=['POST'])
def review():
    is_request_well_formed, response = check_for_params(request.json, review_params
                                                        )
    if not is_request_well_formed:
        return response
    return insert_review(request.json)


signup_params = ["username", "password", "name"]


@app.route("/signup", methods=['POST'])
def signup():
    is_request_well_formed, response = check_for_params(request.json, signup_params)
    if not is_request_well_formed:
        return response
    return signup_user(request.json)


login_params = ["username", "password"]


@app.route("/login", methods=['POST'])
def login():
    is_request_well_formed, response = check_for_params(request.json, login_params)
    if not is_request_well_formed:
        return response
    return login_user(request.json)


@app.route("/feed")
def feed():
    return json.dumps(get_video_feed())


if __name__ == "__main__":
    app.run(debug=True)
