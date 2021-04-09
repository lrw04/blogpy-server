from flask import Flask
from github_webhook import Webhook
import os
from pathlib import Path

app = Flask(__name__)
webhook = Webhook(app, endpoint="/postreceive", secret=os.environ.get("SECRET"))


@webhook.hook()
def on_push(data):
    Path("/flags/reload").touch()
