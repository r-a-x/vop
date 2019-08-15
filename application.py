import os

from flask import Flask, url_for
from flask_restplus import Api, Resource, fields

from services.reviewService import insert_review
from services.userService import UserNotFoundException, signup_user, UserAlreadyExistException, \
    InvalidLoginDetailsException, login_user


app = Flask(__name__)
if os.environ.get('AZURE'):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')
    Api.specs_url = specs_url

api = Api(app, version='1.0', title='VOP Api',
          description='A Basic VOP API',
          )

error_model = api.model('ErrorModel', {
    "success": fields.String,
    "errorType": fields.String,
    "errorMessage": fields.String
})


# @app.errorhandler(Exception)
# @app.errorhandler(RequiredParametersMissingException)
# @app.errorhandler(ReviewAlreadyExistException)
@api.errorhandler(UserAlreadyExistException)
@api.errorhandler(UserNotFoundException)
@api.errorhandler(InvalidLoginDetailsException)
# @marshal_with(ErrorSchema, 500)
@api.marshal_with(error_model)
def handle_error_util(error):
    code = error.code
    success = False
    response = {
        'success': success,
        'errorType': error.name,
        'errorMessage': error.message
    }
    return response, code


ns_conf = api.namespace('reviews', description='Info about Review api')

# model = api.model('ReviewModel', {
#     'name': fields.String,
#     'address': fields.String,
#     'date_updated': fields.DateTime(dt_format='rfc822'),
# })
review_model = api.model('ReviewModel', {
    "title": fields.String,
    "description": fields.String,
    "videoUrl": fields.String,
    "thumbnailUrl": fields.String,
    "afLink": fields.String,
    "username": fields.String
})


@ns_conf.route("")
class Reviews(Resource):
    @api.marshal_with(review_model)
    def get(self):
        pass

    @api.marshal_with(review_model)
    @api.expect(review_model)
    def post(self):
        return insert_review(api.payload)


user_model = api.model('UserModel', {
    "username": fields.String,
    "password": fields.String
})

ns_conf = api.namespace('users', description='Info about Review api')


# @ns_conf.route("")
class Users(Resource):
    # @api.marshal_with()
    def get(self):
        pass

    # @api.marshal_with()
    @api.expect(user_model)
    def post(self):
        pass


login_model = api.model('LoginModel', {
    'username': fields.String,
    'password': fields.String
})

ns_conf = api.namespace('login', description='Login Api')


@ns_conf.route('')
# @api.expect(login_model)
# @api.marshal_with()
class Login(Resource):
    # @api.marshal_with()
    @api.expect(login_model)
    def post(self):
        return login_user(api.payload)


ns_conf = api.namespace('signup', description='Signup Api')
signup_model = api.model('SignupModel', {
    'name': fields.String,
    'username': fields.String,
    'password': fields.String
})


@ns_conf.route('')
# @api.expect(login_model)
# @api.marshal_with()
class Signup(Resource):
    # @api.marshal_with()
    @api.expect(signup_model)
    def post(self):
        return signup_user(api.payload)
        # print(api.payload)


# # review_params = ["title", "description", "videoUrl", "thumbnailUrl", "afLink", "username"]
# review_params = {
#     "title": fields.Str(required=True),
#     "description": fields.Str(required=True),
#     "videoUrl": fields.Str(required=True),
#     "thumbnailUrl": fields.Str(required=True),
#     "afLink": fields.Str(required=True),
#     "username": fields.Str(required=True)
# }
#
#
# @app.route("/review", methods=['POST'])
# @parser.use_args(review_params, locations=("json"))
# def review():
#     return insert_review(request.json)
# docs.register(review)
#
# # signup_params = ["username", "password", "name"]
# signup_params = {
#     "username": fields.Str(required=True),
#     "password": fields.Str(required=True),
#     "name": fields.Str(required=True)
# }
#
# # docs.register("review")
# @app.route("/signup", methods=['POST'])
# @parser.use_args(signup_params, locations=('json'))
# # @marshal_with( code=200)
# def signup(args):
#     return signup_user(args)
#
#
# # login_params = ["username", "password"]
#
# login_params = {
#     "username": fields.Str(required=True),
#     "password": fields.Str(required=True)
# }
#
#
# @app.route("/login", methods=['POST'])
# @parser.use_args(login_params, locations=('json'))
# def login(args):
#     return login_user(args)
#
#
# @app.route("/feed")
# def feed():
#     pass
#     # return json.dumps(get_video_feed())

if __name__ == "__main__":
    app.run(debug=True)
