from flask import Flask, g, render_template, request

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
            return render_template("submit.html", name = request.form["name"], message = request.form["message"])
        except:
            return render_template("submit.html")



def get_message_db():
    if 'db' not in g:
        g.message_db = sqlite3.connect('message_db.sqlite')

    conn = g.message_db
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (ID INTEGER PRIMARY KEY AUTOINCREMENT, handle TEXT, message TEXT);")
    
    return g.message_db   


def insert_message(request):
    message = request.form["message"]
    handle = request.form["name"]

    db = get_message_db()

    db.execute("INSERT INTO messages (handle, message) VALUES (?,?);")
    db.commit()

    conn.close()

    return message, handle






# Miscellaneous

# message_bp = Blueprint('message', __name__, url_prefix='/message')

# @app.route("/submit/", methods = ["POST", "GET"])
# def get_message_db():
#     if 'db' not in g:
#         g.message_db = sqlite3.connect('users.sqlite')

#     with current_app.open_resource('init.sql') as f:
#         g.message_db.executescript(f.read().decode('utf8'))

#     return g.message_db

# def insert_message(request):
#     if request.method == 'POST':
#         message = request.form["message"]
#         name = request.form["name"]
#         db = get_message_db()
#         error = None
#         user = db.execute(
#             "INSERT INTO messages (id, message, name) VALUES (?,?,?)"
#         )
#         db.commit()
#         flash("Message submitted successfully!")
#     flash(error)
   



    
