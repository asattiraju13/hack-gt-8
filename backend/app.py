from flask import Flask, request, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import url_for
import sqlalchemy.dialects.sqlite
import hashlib

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

    users = db.relationship('User',secondary=user_to_classes, backref=db.backref('user_to_classes_backref', lazy='dynamic'))
    
    def __init__(self, name, notes, users, posts):
        self.name = name
        self.notes = notes
        self.users = users
        self.posts = posts

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    text = db.Column(db.String)
    vote_count = db.Column(db.Integer)

    classes = db.relationship('Class',secondary=class_to_posts, backref=db.backref('class_to_posts_backref', lazy='dynamic'))

    def __init__(self, title, text, vote_count):
        self.title = title
        self.text = text
        self.vote_count = vote_count

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
        fields = ('title','text','vote_count')

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

@app.route('/signup',methods=['POST'])
def signup_info():
    if request.method == "POST":
        email = request.form.get("uname")
        psw = request.form.get("psw")
        psw = hashlib.sha256(psw.encode())
        classes = request.form.get("classes")

        # add to database
    

@app.route('/login',methods=['POST'])
def login_info(var = None):
    if request.method == "POST":
        email = request.form.get("uname")
        psw = request.form.get("psw")
        psw = hashlib.sha256(psw.encode())
        user = User.query.get({'email':email})

        # fetch classes
        Class.query.filter(Class.users.any(user_id=user.id)).all()

        if user.__dict__['password'] == psw:
            resp = make_response(render_template('dashboard.html'))
            resp.set_cookie('classes', Class.query.filter(Class.users.any(user_id=user.id)).all())
            return resp #dashboard
        else:
            var = "error"
            return url_for('login_info', variable = var)

@app.route('/get_user/<user>', methods=['GET'])
def get_classes(user):
    return User.query.get({'classes':user})

@app.route('/dashboard', methods='GET')
def dashboard():
    classes = request.cookies.get('classes')
    return render_template('dashboard.htmml', variable = classes)
        
if __name__ == "__main__":
    app.run(debug=True)