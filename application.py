from flask import Flask, request
from webargs import fields, flaskparser
from services.exceptionService import RequiredParametersMissingException, ErrorSchema
from services.reviewService import insert_review, ReviewAlreadyExistException
from services.userService import signup_user, login_user, UserAlreadyExistException, UserNotFoundException, \
    InvalidLoginDetailsException
from flask_apispec import use_kwargs, marshal_with
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from video import get_video_feed

app = Flask(__name__)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='pets',
        version='v1',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})
docs = FlaskApiSpec(app)
# app.config.update(
#     APISPEC_SWAGGER_URL='/swagger',
#     APISPEC_SWAGGER_UI_URL='/swagger-ui'
# )
# docs = FlaskApiSpec(app)
parser = flaskparser.FlaskParser()


@parser.error_handler
def handle_error(error, req, schema, code, headers):
    raise RequiredParametersMissingException("Certain parameters like """.join(error.messages.keys()) + 'are missing ')


@app.errorhandler(Exception)
@app.errorhandler(RequiredParametersMissingException)
@app.errorhandler(ReviewAlreadyExistException)
@app.errorhandler(UserAlreadyExistException)
@app.errorhandler(UserNotFoundException)
@app.errorhandler(InvalidLoginDetailsException)
@marshal_with(ErrorSchema, 500)
def handle_error_util(error):
    code = error.code
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.name,
            'message': error.description
        }

    }
    return response, code


@app.route("/")
def hello():
    return "Hello World!!"


# def check_for_params(request_json, params=[]):
#     for param in params:
#         if param not in request_json or request_json[param] is None:
#             return False, json.dumps({
#                 "error": param + " is not present in the request"
#             }), 400
#     return True, None


# review_params = ["title", "description", "videoUrl", "thumbnailUrl", "afLink", "username"]
review_params = {
    "title": fields.Str(required=True),
    "description": fields.Str(required=True),
    "videoUrl": fields.Str(required=True),
    "thumbnailUrl": fields.Str(required=True),
    "afLink": fields.Str(required=True),
    "username": fields.Str(required=True)
}


@app.route("/review", methods=['POST'])
@parser.use_args(review_params, locations=("json"))
def review():
    return insert_review(request.json)
docs.register(review)

# signup_params = ["username", "password", "name"]
signup_params = {
    "username": fields.Str(required=True),
    "password": fields.Str(required=True),
    "name": fields.Str(required=True)
}

# docs.register("review")
@app.route("/signup", methods=['POST'])
@parser.use_args(signup_params, locations=('json'))
# @marshal_with( code=200)
def signup(args):
    return signup_user(args)


# login_params = ["username", "password"]

login_params = {
    "username": fields.Str(required=True),
    "password": fields.Str(required=True)
}


@app.route("/login", methods=['POST'])
@parser.use_args(login_params, locations=('json'))
def login(args):
    return login_user(args)


@app.route("/feed")
def feed():
    pass
    # return json.dumps(get_video_feed())


if __name__ == "__main__":
    app.run(debug=True)
