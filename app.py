from flask import Flask, request, abort
from github_webhook import Webhook
import os
from pathlib import Path
from hmac import HMAC
from hashlib import sha256

secret = os.environ.get("SECRET").encode()
app = Flask(__name__)

def verify(rq):
    sign = "sha256=" + HMAC(key=secret, msg=rq.get_data(), digestmod=sha256).hexdigest()
    recv = rq.headers.get("X-Hub-Signature-256")
    return sign == recv

@app.route("/postreceive", methods=["POST"])
def on_push():
    if not verify(request):
        abort(403)
    Path("/flags/reload").touch()
    return "ok sent"
