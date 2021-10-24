from flask import Flask, request, jsonify, render_template, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import url_for
import sqlalchemy.dialects.sqlite
import hashlib

from flask_sqlalchemy.model import Model

import os
from markupsafe import escape

#Init app
# Share ports
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    classes = db.Column(db.String)

    def __init__(self, email, password, classes):
        self.email = email
        self.password = password
        self.classes = classes

# class Class(db.Model):  # for the list of classes
#     __tablename__ = 'class'
#     class_id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String, unique = True)
    
#     def __init__(self, name):
#         self.name = name

class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    text = db.Column(db.String)
    vote_count = db.Column(db.Integer)
    class_name = db.Column(db.String)

    def __init__(self, title, text, vote_count, class_name):
        self.title = title
        self.text = text
        self.vote_count = vote_count
        self.class_name = class_name
    
    def __lt__(self, post):
        self.vote_count > post.vote_count

class Note(db.Model):
    __tablename__ = 'note'
    note_id = db.Column(db.Integer, primary_key = True)
    class_name = db.Column(db.String)
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
        fields = ('email','password','classes')

# class ClassSchema(ma.Schema):
#     class Meta:
#         fields = ('name',)

class NoteSchema(ma.Schema):
    class Meta:
        fields = ('class_name','lecture','text','img')

class PostSchema(ma.Schema):
    class Meta:
        fields = ('title','text','vote_count')

# class_schema = ClassSchema()
# classes_schema = ClassSchema(many=True)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

db.create_all()

@app.route('/')
def login():
    return redirect(url_for('login_info'))

@app.route('/signup',methods=['POST','GET'])
def signup_info():
    if request.method == "POST":
        email = request.form.get("uname")
        psw = request.form.get("psw")
        psw = hashlib.sha256(psw.encode('utf-8')).hexdigest()

        classes = request.form.get("classes")

        #User params: email, password, classes
        new_user = User(email = email, password = psw, classes = classes)
        db.session.add(new_user)
        db.session.commit()

        resp = make_response(render_template('dashboard.html', variable = classes))
        resp.set_cookie('classes', classes)
        return resp

    return render_template('signup.html')

@app.route('/login',methods=['POST', 'GET'])
def login_info():
    if request.method == 'POST':
        email = request.form.get("uname")
        psw = request.form.get("psw")
        psw = hashlib.sha256(psw.encode('utf-8')).hexdigest()

        user = User.query.filter_by(email=email).first()

        if user is not None:

            if user.password == psw:
                return render_template('dashboard.html', variable = user.classes)

            else:
                return redirect(url_for('login_info'))
    
    return render_template('login.html')

@app.route('/get_user/<user>', methods=['GET'])
def get_classes(user):
    return User.query.get({'classes':user})

@app.route('/dashboard', methods=['GET'])
def dashboard():
    classes = request.cookies.get('classes')
    return render_template('dashboard.html', variable = classes)

@app.route('/<classname>/posts', methods=['GET'])
def posts(classname):
    posts = Post.query.filter_by(class_name = classname).all()

    return posts
    #return render_template('posts.html', variable = posts)

    # IMPLEMENTING SORT


        
if __name__ == "__main__":
    app.run(debug=True)
