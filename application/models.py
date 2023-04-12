import flask
from application import db
    
class courses(db.Document):
    courseID=db.StringField(unique=True)
    title=db.StringField(max_length=100)
    description=db.StringField(max_length=255)
    credits=db.IntField()
    term=db.StringField(max_length=25)