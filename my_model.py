import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Respondents(db.Model):
    __tablename__ = 'people'

    person_id =  db.Column('person_id', db.Integer, primary_key=True, autoincrement=True)

    mothername = db.Column('mothername', db.Text)

    age = db.Column('age', db.Integer)

    height = db.Column('height', db.Integer)


class Answers(db.Model):
    __tablename__ = 'answers'
    
    person_id = db.Column('person_id', db.Integer, ForeignKey('people.person_id'), primary_key=True)

    assistant = db.Column('assistant', db.Integer)

    check = db.Column('checking', db.Integer)

    likes = db.Column('likes', db.Integer)

    extent = db.Column('extent', db.Text)

    design = db.Column('design', db.Integer)

    content = db.Column('content', db.Integer)

    author = db.Column('author', db.Integer)

    author_name = db.Column('author_name', db.Text)

    impression = db.Column('impression', db.Integer)


