from flask import Blueprint, current_app, g, render_template, redirect, request, flash, url_for, session, Flask

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
                             message = request.form["message"])
        except:
            render_template("submit.html")

    if request.method == "POST":
        insert_message(request)
        return render_template("submit.html")


def get_message_db():
    if 'db' not in g:
        g.message_db = sqlite3.connect('message_db.sqlite')
        
    conn = g.message_db
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (ID INTEGER PRIMARY KEY AUTOINCREMENT, messages TEXT, name TEXT)")
    return g.message_db   


def insert_message(request):
    message = request.form["message"]
    name = request.form["name"]

    db = get_message_db()

    db.execute(
                'INSERT INTO message (messages, name) VALUES (?, ?)',
                (username, salt, generate_password_hash(password + salt))
            )

    db.commit()

    conn.close()






# Miscellaneous

message_bp = Blueprint('message', __name__, url_prefix='/message')

@app.route("/submit/", methods = ["POST", "GET"])
def get_message_db():
    if 'db' not in g:
        g.message_db = sqlite3.connect('users.sqlite')

    with current_app.open_resource('init.sql') as f:
        g.message_db.executescript(f.read().decode('utf8'))

    return g.message_db

def insert_message(request):
    if request.method == 'POST':
        message = request.form["message"]
        name = request.form["name"]
        db = get_message_db()
        error = None
        user = db.execute(
            "INSERT INTO messages (id, message, name) VALUES (?,?,?)"
        )
        db.commit()
        flash("Message submitted successfully!")
    flash(error)
   



    
