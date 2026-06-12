from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
load_dotenv()
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URL")
db=SQLAlchemy(app)



#user table
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20))
    email=db.Column(db.String(100))
    def __repr__(self):
        return f"<User id={self.id},username={self.username},email={self.email}>"

@app.shell_context_processor
def make_shell_contect():
    return {
        "db":db,
        "User":User
    }
