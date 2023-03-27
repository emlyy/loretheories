from flask import Flask
from flask import render_template, redirect, request, session
from app import app
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if not users.login(username, password):
        return render_template("index.html", message="Incorrect username or password :/ Please try again.")
    return redirect("/login_success")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/login_success")
def login_success():
    return render_template("logged.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password_1 = request.form["password_1"]
        password_2 = request.form["password_2"]
        if password_1 != password_2:
            return render_template("register_error.html", message="passwords do not match")
        if users.register(username, password_1):
            return redirect("/")
        else:
            return render_template("register_error.html", message="there was a problem try again")


@app.route("/create")
def create():
    return render_template("create")
