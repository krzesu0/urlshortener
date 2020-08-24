"""Main view handler"""
import random
import string
import re
from flask import Blueprint, redirect, url_for, request, render_template
from flask_json import json_response
from ..models import Link, db

page = Blueprint("serve", __name__, static_folder="static")

REGEX = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+") # pylint: disable=anomalous-backslash-in-string

@page.route("/", methods=["GET"])
def index():
    """Render website"""
    return render_template("index.html")

@page.route("/<string:text>")
def redirect_to_page(text):
    """Redirect handler"""
    query = Link.query.filter_by(text=text).first()
    if query is None:
        return redirect(url_for("serve.index"))
    return redirect(query.url)

@page.route("/", methods=["POST"])
def add_new():
    """Add new url to database"""
    # we need two things, the url and optionally text
    data = request.get_json(force=True, silent=True)
    try:
        # check for url, if its not in the posted json then quit to index
        url = data["url"]
        if not REGEX.match(url):
            raise SyntaxError
    except (KeyError, TypeError):
        return json_response(status="URL missing.", error=True)

    except SyntaxError:
        return json_response(status="Illegal URL.", error=True)

    try:
        # we dont need text so just pass the exception
        text = data["text"]
        if not re.match("^[a-zA-Z0-9]*$", text):
            raise SyntaxError
        if len(text) < 1:
            raise KeyError
    except KeyError:
        text = "".join(random.choice(string.ascii_letters) for _ in range(5))
    except SyntaxError:
        return json_response(status="Illegal character used.", error=True)
    # quick check whether text was used before
    query = Link.query.filter_by(text=text).first()
    if query:
        return json_response(status=f"{text} is already taken.", error=True)
    new = Link(url=url, text=text)

    db.session.add(new)
    db.session.commit()

    return json_response(status="ok", text=text, error=False)
