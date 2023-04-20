from flask import Flask
from flask import render_template, redirect, request, session
from app import app
import users, posts, comments

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("login.html", message="Incorrect username or password :/ Please try again.")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password_1 = request.form["password_1"]
        password_2 = request.form["password_2"]
        if password_1 != password_2:
            return render_template("register.html", message="passwords do not match")
        if users.register(username, password_1):
            return redirect("/")
        else:
            return render_template("register.html", message="there was a problem try again")


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        title = request.form["title"]
        message = request.form["message"]
        # add tags and such
        if not posts.save_post(title, message):
            return render_template("create.html", error="there was a problem try again")
    return redirect("/all_posts")

@app.route("/all_posts", methods=["GET"])
def all_posts():
    posts_list = posts.get_all_posts()
    return render_template("posts.html", posts=posts_list)

@app.route("/categories", methods=["GET"])
def categories():
    return render_template("categories.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    if request.method == "POST":
        posts_list = posts.search_posts(search_word)
        return render_template("posts.html", posts=posts_list)

@app.route("/comments/<int:id>", methods=["GET"])
def commentss(id):
    comments.save_session(id)
    return redirect("/comment")

@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "GET":
        comments_list = comments.get_comments()
        if len(comments_list) != 0:
            return render_template("comments.html", comments=comments_list)
        else:
            return render_template("comments.html", message="There are no commnets, be the first to commnent.")
    if request.method == "POST":
        comment = request.form["message"]
        if not comments.post_comment(comment):
            return render_template("comments.html", message="could not post comment")
    return redirect("/comment")
