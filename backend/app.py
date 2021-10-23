#Flask App

from flask import Flask, request, jsonify, render_template
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

user_to_classes = db.Table('user_to_classes',
                          db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
                          db.Column('class_id', db.Integer, db.ForeignKey('class.class_id')))

class_to_posts = db.Table('class_to_posts',
                         db.Column('class_id',db.Integer, db.ForeignKey('class.class_id')),
                         db.Column('post_id', db.Integer, db.ForeignKey('post.post_id')))

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    classes = db.relationship('Class', backref='user', lazy='dynamic', secondary=user_to_classes)

    def __init__(self, email, password, classes):
        self.email = email
        self.password = password
        self.classes = classes

class Class(db.Model):
    class_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True)
    #notes = db.relationship('Note', backref='class', lazy=True, uselist=False)
    
    def __init__(self, name, notes, posts):
        self.name = name
        self.notes = notes
        self.users = users
        self.posts = posts

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    text = db.Column(db.String)
    classes = db.relationship('Class',secondary=class_to_posts, backref=db.backref('class_to_posts_backref', lazy='dynamic'))

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.classes = classes

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

class UserSchema(ma.Schema):
    class Meta:
        fields = ('email','classes')

class ClassSchema(ma.Schema):
    class Meta:
        fields = ('name',)

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

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/')
def hello_world():
    return "hello world"

@app.route('/login',methods=['POST'])
def login_info():

    if request.method == "POST":
        email = request.form.get("uname")
        psw = request.form.get("psw")
        
        user = User.query({'email':email})

        user.__dict__['password']

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)