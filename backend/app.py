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

@app.route('/')
def hello_world():
    return "hello world"
    
if __name__ == "__main__":
    app.run()
