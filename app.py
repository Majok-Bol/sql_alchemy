from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
import os
load_dotenv()
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URL")
db=SQLAlchemy(app)
migrate=Migrate(app,db)

#one-to-many relationship
#one user can have many posts
#but each post has one user
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
#video game characters and their weapons
#one character can carry many weapons ie one-to-many relationship
class Character(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30))#'link'
    level=db.Column(db.Integer)#eg 10
    weapons=db.relationship("Weapon",back_populates="owner")
    def __repr__(self):
        return f"<Character id={self.id},name={self.name},level={self.level}>"

#Weapon blueprint
class Weapon(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30))# eg 'Master Sword'
    damage=db.Column(db.Integer)# 50
    character_id=db.Column(db.Integer,db.ForeignKey("character.id"))
    owner=db.relationship("Character",back_populates="weapons")
    def __repr__(self):
        return f"<Weapon id={self.id},name={self.name},character_id={self.character_id},owner={self.owner.name if self.owner else None}>"



#one to one relationship
#means one thing=one other thing
#eg like a person and their passport.One person has exactly one passport
#one passport belongs to exactly one person
class Person(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30))
    passport=db.relationship("Passport",back_populates="owner",uselist=False) #uselist means only one and not a list
    def __repr__(self):
        return f"<Person id={self.id},name={self.name}>"

class Passport(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    number=db.Column(db.String(20))
    #connect passport table to person table
    person_id=db.Column(db.Integer,db.ForeignKey("person.id"))
    owner=db.relationship("Person",back_populates="passport")
    def __repr__(self):
        return f"<Passport id={self.id},number={self.number},person_id={self.person_id},owner={self.owner.name if self.owner else None}>"


#many-to-many relationships
#many things connect to many things
#the middleman table
pizza_topping=db.Table("pizza_topping",
db.Column("pizza_id",db.Integer,
db.ForeignKey("pizza.id")),
db.Column("topping_id",db.Integer,db.ForeignKey("topping.id")))
class Pizza(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30))
    price=db.Column(db.Float)
    toppings=db.relationship("Topping",secondary=pizza_topping,back_populates="pizzas")

class Topping(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    is_vegetarian=db.Column(db.Boolean)#false
    pizzas=db.relationship("Pizza",secondary=pizza_topping,back_populates="toppings")

#other example of many to many relationship
actor_movie=db.Table(
    "actor_movie",
    db.Column("actor_id",db.Integer,
    db.ForeignKey("actors.id")),
    db.Column("movie_id",db.Integer,db.ForeignKey("movies.id"))

)
class Actors(db.Model):
    __tablename__="actors"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    movies=db.relationship("Movies",secondary=actor_movie,back_populates="actors")
    def __repr__(self):
        return f"<Actor {self.name}>"
class Movies(db.Model):
    __tablename__="movies"
    id=db.Column(db.Integer,primary_key=True)
    movie_name=db.Column(db.String(50))
    actors=db.relationship("Actors",secondary=actor_movie,back_populates="movies")
    def __repr__(self):
        return f"<Movie {self.movie_name}>"
@app.shell_context_processor
def make_shell_contect():
    return {
        "db":db,
        "User":User,
        "Post":Post,
        "Character":Character,
        "Weapon":Weapon,
        "Person":Person,
        "Passport":Passport,
        "Pizza":Pizza,
        "Topping":Topping,
        "pizza_topping":pizza_topping,
        "Actors":Actors,
        "Movies":Movies,
        "actor_movie":actor_movie
    }
