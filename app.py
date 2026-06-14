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
    posts=db.relationship("Post",back_populates="author")
    def __repr__(self):
        return f"<User id={self.id},username={self.username},email={self.email}>"
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50))
    body=db.Column(db.String(120))
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    author=db.relationship("User",back_populates="posts")
    def __repr__(self):
        return f"<Post id={self.id},user_id={self.user_id},title={self.title},body={self.body},author={self.author.username if self.author else None}>"
@app.shell_context_processor
def make_shell_contect():
    return {
        "db":db,
        "User":User,
        "Post":Post
    }
