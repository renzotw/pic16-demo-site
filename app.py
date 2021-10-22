from flask import Flask, render_template, request, g, Blueprint

import sqlite3
import click

import random 
import string

app = Flask(__name__)

@app.route("/")
# simplest possible approach
def main():
    return render_template("base.html") # Searches in template directory for main.html

@app.route("/submit/", methods = ["POST", "GET"])
def submit():
    if request.method == "GET":
        return render_template("submit.html")
    else:
        try:
            render_template("submit.html", 
                             name = request.form["name"],
                             student = request.form["student"])
        except:
            render_template("submit.html")

message_bp = Blueprint('message', __name__, url_prefix='/message')

def get_message_db():
    if 'db' not in g:
        g.message_db = sqlite3.connect('users.sqlite')

    with current_app.open_resource('init.sql') as f:
        g.message_db.executescript(f.read().decode('utf8'))

    return g.message_db



    
