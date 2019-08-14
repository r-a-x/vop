import json
from database import open_db_connection
from services.exceptionService import VOPException
from services.userService import is_user_present, UserNotFoundException


# ["title", "description", "videoUrl", "thumbnailUrl", "afLink", "username"]

def insert_review(review):
    if is_user_present(review["username"]):
        with open_db_connection(True) as cursor:
            cursor.execute('insert into reviews(title, description, videoUrl, thumbnailUrl, afLink, username)'
                           ' values(?, ?, ?, ?, ?, ?)', review['title'], review['description'], review['videoUrl']
                           , review['thumbnailUrl'], review['afLink'], review['username'])
        return review, 200
    else:
        raise UserNotFoundException()


class ReviewAlreadyExistException(VOPException):
    code = 422
    name = "ReviewAlreadyExistException"
    message = None

    def __init__(self, video_url):
        self.message = "A review with the same video already exist " + video_url
