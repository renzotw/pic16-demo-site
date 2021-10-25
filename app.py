from flask import Flask, g, render_template, request

import sqlite3
import click

import random 
import string

app = Flask(__name__)

# Route to home page
@app.route("/")
def main():
    """
    Function to render the home page 
    """
    return render_template("base.html") # Searches in template directory for main.html

# Route to submit page
@app.route("/submit/", methods = ["POST", "GET"])
def submit():
    """
    Function for submitting messages
    """
    if request.method == "GET":
        return render_template("submit.html")
    else:
        try:
            insert_message(request) # Run insert_message() to write to sql database
            return render_template("submit.html", name=request.form['name'], message=request.form['message']) # Return submit html with successful submission message
        except:
            return render_template("submit.html")

def get_message_db():
    """
    Function to initialize database and return open connection
    If database exists simply return the connection
    """
    if 'db' not in g:
        g.message_db = sqlite3.connect('message_db.sqlite')

    conn = g.message_db
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (ID INTEGER PRIMARY KEY AUTOINCREMENT, handle TEXT, message TEXT);")
    
    return g.message_db   


def insert_message(request):
    """
    Funciton to return the inputted name and message and write to sql database
    """
    message = request.form["message"]
    handle = request.form["name"]

    db = get_message_db() # Open connection to database
    error = None

    # Error cases
    if not message:
        error = "message is required."
    elif not handle:
        error = "name is required."

    if error is None:
        db.execute("INSERT INTO messages (handle, message) VALUES (?,?)", (handle, message)) # Query to write to database
        db.commit() # Commit changes to database

    db.close() # Close connection to database when done

    return message, handle

# Route to view page
@app.route('/view/')
def view():
    """
    Function to view up to as many messages as stated in limit
    """
    limit = 5 # Cap of how many messages to display
    mylist = random_messages(limit) # Run random_messages() to get a list of tuples of random messages
    return render_template('view.html', message_list=mylist)

def random_messages(n):
    """
    Function to return a random list of messages
    """

    db = get_message_db()

    cursor = db.cursor()

    cursor.execute("SELECT message, handle FROM messages ORDER BY RANDOM() LIMIT (?)", (n,))
    messages = cursor.fetchall() # List of tuples of messages and names

    db.close()  # Close connection when done

    return messages

    