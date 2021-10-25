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
            insert_message(request)
            return render_template("submit.html", name=request.form['name'], message=request.form['message'])
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
    error = None

    if not message:
        error = "message is required."
    elif not handle:
        error = "name is required."

    if error is None:
        db.execute("INSERT INTO messages (handle, message) VALUES (?,?)", (handle, message))
        db.commit()

    db.close()

    return message, handle



# DON'T DELETE ANYTHING ABOVE

@app.route('/view/')
def view():
    limit = 5
    mylist = random_messages(limit)
    return render_template('view.html', message_list=mylist)

def random_messages(n):

    db = get_message_db()

    cursor = db.cursor()

    cursor.execute("SELECT message, handle FROM messages ORDER BY RANDOM() LIMIT (?)", (n,))
    messages = cursor.fetchall()

    db.close()

    return messages

    