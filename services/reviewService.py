import json

from database import open_db_connection
from services.userService import is_user_present


# ["title", "description", "videoUrl", "thumbnailUrl", "afLink", "username"]

def insert_review(review):
    if is_user_present(review["username"]):
        with open_db_connection(True) as cursor:
            cursor.execute('insert into reviews(title, description, videoUrl, thumbnailUrl, afLink, username)'
                           ' values(?, ?, ?, ?, ?, ?)', review['title'], review['description'], review['videoUrl']
                           , review['thumbnailUrl'], review['afLink'], review['username'])
        return json.dumps(review), 200
    else:
        return json.dumps({
            "error": "Please signup before posting the review",
        }), 400
