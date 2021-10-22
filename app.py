from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
# simplest possible approach
def main():
    return "hi there!"
