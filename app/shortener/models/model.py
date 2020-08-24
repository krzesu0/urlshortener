from . import db

class Link(db.Model):
    """Database model for storing links"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(30), unique=True, nullable=False, index=True)
    url = db.Column(db.String, nullable=False)
