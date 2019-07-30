from flask import Flask, request
import json

from video import get_video_feed

app = Flask(__name__)


def throw_error(code, success, message):
    return json.dumps({
        code: code,
        success: success,
        message: message
    }), 500


@app.route("/")
def hello():
    return "Hello There!!"


@app.route("/feed")
def feed():
    return json.dumps(get_video_feed())


if __name__ == "__main__":
    app.run()
