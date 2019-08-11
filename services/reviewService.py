import json
from marshmallow import Schema, fields
from database import open_db_connection
from services.exceptionService import VOPException
from services.userService import is_user_present, UserNotFoundException


class ReviewSchema(Schema):
    title = fields.String()
    description = fields.String()
    videoUrl = fields.String()
    thumbnail = fields.String()
    afLink = fields.String()
    username = fields.String()


# ["title", "description", "videoUrl", "thumbnailUrl", "afLink", "username"]

def insert_review(review):
    if is_user_present(review["username"]):
        with open_db_connection(True) as cursor:
            cursor.execute('insert into reviews(title, description, videoUrl, thumbnailUrl, afLink, username)'
                           ' values(?, ?, ?, ?, ?, ?)', review['title'], review['description'], review['videoUrl']
                           , review['thumbnailUrl'], review['afLink'], review['username'])
        return json.dumps(review), 200
    else:
        raise UserNotFoundException(review["username"])


class ReviewAlreadyExistException(VOPException):
    code = 422
    name = "ReviewAlreadyExistException"
    message = None

    def __init__(self, video_url):
        self.message = "A review with the same video already exist " + video_url
