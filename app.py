from flask import Flask, render_template, request
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
    
