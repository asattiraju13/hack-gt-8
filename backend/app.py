from flask import Flask, request, jsonify, render_template, make_response, redirect, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import url_for
import sqlalchemy.dialects.sqlite
import hashlib

import PyPDF2

from flask_sqlalchemy.model import Model

import os
from markupsafe import escape

import re
import math
import numpy as np

import nltk
from stop_words import get_stop_words

# from nltk.corpus import stopwords
# stopwords.words('english')

from model import NotesDoc

UPLOAD_FOLDER = '/pdf'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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

    def __init__(self, class_name, lecture, text):
        self.class_name = class_name
        self.lecture = lecture
        self.text = text

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

# note_schema = NoteSchema()
# notes_schema = NoteSchema(many=True)

# post_schema = PostSchema()
# posts_schema = PostSchema(many=True)

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)

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
                print(user.classes)
                return render_template('dashboard.html', variable = user.classes)

            else:
                return redirect(url_for('login_info'))
    
    return render_template('login.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    classes = request.cookies.get('classes')
    return render_template('dashboard.html', variable = classes)


@app.route('/get_user/<user>', methods=['GET'])
def get_classes(user):
    return User.query.get({'classes':user})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/<classname>/notes',methods=['GET','POST'])
def notess(classname):
    if request.method == 'POST':
        lecture = request.form.get("lecture")
        files = request.files["file"]

        app.config['UPLOAD_FOLDER'] = "pdf"
        app.config['MAX_CONTENT_PATH'] = 1000000000000

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("pdf", file.filename))
            return redirect(url_for('dashboard', name=filename))

    notes = Note.query.filter_by(class_name = classname).all()
    return render_template('notes.html', classname=classname, notes = notes)

    #     # FIND THE PD



    #     pdffileobj=open('1.pdf','rb')

    #     pdfreader=PyPDF2.PdfFileReader(pdffileobj)
    #     x=pdfreader.numPages

    #     text = ""
    #     for i in range(x):
    #         pageobj = pdfreader.getPage(i)
    #         text += pageobj.extractText()


        

    #    

    #     for note in notes:
    #         if lecture == int(note.lecture):
    #             return

    #         # else:

    #             #new_note = Note(classname, lecture, text)

        
    #     # add link to html text of notes in the final render template

    # # return


@app.route('/<classname>/posts', methods=['GET','POST'])
def postss(classname):
    if request.method == 'POST':
        title = request.form.get("title")
        text = request.form.get("text")

        new_post = Post(title, text, 0, classname)

        db.session.add(new_post)
        db.session.commit()

        posts = Post.query.filter_by(class_name = classname).all()
        posts = sorted(posts, key = lambda x: x.vote_count, reverse=True)    
    return render_template('posts.html')
        
if __name__ == "__main__":
    app.run(debug=True)
