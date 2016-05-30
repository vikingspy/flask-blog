# -*- coding: utf-8 -*-
# blog.py - controller

# To start local http server, from command line:
# python http.server [port (opt)]
# do this from the directory where the files are

"""blog.py acts as the application controller. Flask
works with a client-server model. The server receives HTTP requests from the
client (i.e., the web browser), then returns content back to the client in 
the form of a response. 
NOTE: HTTP is the method used for all web-based communications; the
‘http://’ that prefixes URLs designates an HTTP request. Literally everything
you see in your browser is transferred to you via HTTP."""

# imports
from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
import sqlite3
from functools import wraps

# configuration
DATABASE = "blog.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = "hard2guess"

app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

# function used for connecting to database
def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

# keeps users from accessing main.html without logging in
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            #flash("Already logged in.")
            return test(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for("login"))
    return wrap

# this section compares the username and password entered
# against those from the configuration section. If the correct username
# and password are entered, the user is redirected to the main page
# and the session key, 'logged_in', is set to True.
# Otherwise, an error message is shown.
@app.route('/', methods=["GET", "POST"])    
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"] or \
                request.form["password"] != app.config["PASSWORD"]:
                    error = "Invalid credentials. Please try again."
        else:
            session["logged_in"] = True
            # url_for() function generates a URL to the given endpoint
            return redirect(url_for("main"))
    return render_template("login.html", error=error)

# function to add new posts
@app.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form["title"]
    post = request.form["post"]
    if not title or not post:
        flash("All fields are required. Please try again.")
        return redirect(url_for("main"))
    else:
        g.db = connect_db()
        g.db.execute("insert into posts (title, post) values (?,?)",
                     [request.form["title"], request.form["post"]])
        g.db.commit()
        g.db.close()
        flash("New entry was successfully posted!")
        return redirect(url_for("main"))

# when a GET request is sent to access main.html, this @ decorator momentarily replaces main()
@app.route('/main') 
@login_required 
def main():
    g.db = connect_db()
    cur = g.db.execute("select * from posts")
    posts = [dict(title=row[0], post=row[1]) for row in
             cur.fetchall()]
    g.db.close()
    return render_template("main.html", posts=posts)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
