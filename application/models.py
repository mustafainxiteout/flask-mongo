import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class users(db.Document):
    user_id=db.IntField(unique=True)
    name=db.StringField(max_length=50)
    email=db.StringField(max_length=50,unique=True)
    password=db.StringField()
    verified=db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow())

    def set_password(self, password):
        self.password=generate_password_hash(method='pbkdf2:sha512:150000',password=password)
    
    def get_password(self,password):
        return check_password_hash(self.password, password)
    
class courses(db.Document):
    courseID=db.StringField(unique=True)
    title=db.StringField(max_length=100)
    description=db.StringField(max_length=255)
    credits=db.IntField()
    term=db.StringField(max_length=25)