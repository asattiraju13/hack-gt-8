#Flask App

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import url_for
import sqlalchemy.dialects.sqlite

from flask_sqlalchemy.model import Model

import os
from markupsafe import escape

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Class(db.Model):
    class_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True)
    notes = db.relationship('Note', backref='class', lazy=True, uselist=False)
    posts = db.relationship('Post', backref='class', lazy=True, uselist=False)
    user = db.relationship('User', backref='class', lazy=True)

    def __init__(self, name, notes, posts):
        self.name = name
        self.notes = notes
        self.posts = posts

class Note(db.Model):
    note_id = db.Column(db.Integer, primary_key = True)
    class_name = db.Column(db.String, db.ForeignKey('class.name'))
    lecture = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String)
    imgs = db.Column(db.PickleType)

    def __init__(self, class_name, lecture, text, imgs):
        self.class_name = class_name
        self.lecture = lecture
        self.text = text
        self.imgs = imgs

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key = True)
    class_name = db.Column(db.String, db.ForeignKey('class.name'))
    title = db.Column(db.String)
    text = db.Column(db.String)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.class_name = class_name

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String)
    classes = db.Column(db)

class ClassSchema(ma.Schema):
    class Meta:
        fields = ('name')

class NoteSchema(ma.Schema):
    class Meta:
        fields = ('class_name','lecture','text','img')

class PostSchema(ma.Schema):
    class Meta:
        fields = ('title','text')

class_schema = ClassSchema()
classes_schema = ClassSchema(many=True)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@app.route('/')
def hello_world():
    return "hello world"
    
if __name__ == "__main__":
    app.run()
