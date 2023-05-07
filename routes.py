from flask import Flask
from flask import render_template, redirect, request, session
from app import app
import users, posts, comments, likes, sessions

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
            return render_template("login.html", message="Incorrect username or password. Please try again.")
        return redirect("/")

@app.route("/logout")
def logout():
    if users.logged_in:
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
        error_message = None
        if len(username) < 1:
            error_message = "username cannot be empty"
        if not users.check_username(username):
            error_message = "username already taken"
        if len(password_1) < 6:
            error_message = "password must be atleast 6 characters long"
        if password_1 != password_2:
            error_message = "passwords do not match"
        if not error_message:
            if users.register(username, password_1):
                return redirect("/login")
            else:
                error_message = "there was a problem try again"
        return render_template("register.html", message=error_message)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        title = request.form["title"]
        message = request.form["message"]
        category = request.form["category"]
        tags = request.form["tags"]
        if len(title) == 0:
            return render_template("create.html", error="title cannot be empty")
        if len(message) == 0:
            return render_template("create.html", error="cannot post an empty theory")
        if not posts.save_post(title, message, category):
            return render_template("create.html", error="there was a problem try again")
        post_id = posts.get_post_id(title, message)
        if not posts.save_tags(tags, post_id):
            return render_template("create.html", error="there was a problem with adding the tags, however your theory was still posted")
    return redirect("/all_posts")

@app.route("/all_posts", methods=["GET"])
def all_posts():
    likes.check_if_liked
    sessions.save_previous("all")
    posts_list = posts.get_all_posts()
    return render_template("posts.html", posts=posts_list, header="All Shared Theories")

@app.route("/categories", methods=["GET"])
def categories():
    tags = posts.tags()
    return render_template("categories.html", tags=tags)

@app.route("/category/<id>")
def categoryy(id):
    sessions.save_category(id)
    sessions.save_previous("category")
    return redirect("/category")

@app.route("/category", methods=["GET"])
def category():
    likes.check_if_liked
    posts_list = posts.posts_by_category()
    if len(posts_list) != 0:
        return render_template("posts.html", posts=posts_list, header="All shared theories in "+session["category"])
    else:
        return render_template("posts.html", posts=posts_list, header="No shared theories in "+session["category"])

@app.route("/tag/<id>")
def tagg(id):
    sessions.save_tag(id)
    sessions.save_previous("tags")
    return redirect("/tag")

@app.route("/tag", methods=["GET"])
def tag():
    likes.check_if_liked
    posts_list = posts.posts_by_tag()
    if len(posts_list) != 0:
        return render_template("posts.html", posts=posts_list, header="All shared theories with tag: "+session["tag"])
    return render_template("posts.html", posts=posts_list, header="No shared theories with tag "+session["tag"])

@app.route("/search", methods=["GET"])
def search():
    return render_template("search.html")

@app.route("/result", methods=["GET"])
def result():
    search_word = request.args["query"]
    if search_word == "":
        return render_template("search.html")
    sessions.save_previous("result")
    sessions.save_search(search_word)
    posts_list = posts.search_posts(search_word)
    if len(posts_list) != 0:
        likes.check_if_liked
        return render_template("search.html", posts=posts_list, header="Results for search: "+search_word)
    return render_template("search.html", header="No results for search:"+search_word)

@app.route("/comments/<int:id>", methods=["GET"])
def commentss(id):
    sessions.save_post(id)
    return redirect("/comment")

@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "GET":
        comments_list = comments.get_comments()
        if len(comments_list) != 0:
            return render_template("comments.html", comments=comments_list)
        return render_template("comments.html", message="There are no commnets, be the first to commnent.")
    if request.method == "POST":
        comment = request.form["message"]
        error = "Comment cannot be empty!"
        if len(comment) != 0:
            if comments.post_comment(comment):
                return redirect("/comment")
            error = "Could not post comment."
        comments_list = comments.get_comments()
        return render_template("comments.html", comments=comments_list, message=error)

@app.route("/like/<int:id>", methods=["POST"])
def likess(id):
    if users.logged_in():
        sessions.save_post(id)
        return redirect("/like")
    return redirect("/login")

@app.route("/like")
def like():
    if users.logged_in():
        likes.like_post()
    if session["previous"] == "result":
        url = "/result?query="+session["search"]
        return redirect(url)
    elif session["previous"] == "category":
        return redirect("/category")
    elif session["previous"] == "tags":
        return redirect("/tag")
    return redirect("all_posts")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if users.logged_in():
        posts.delete(id)
    if session["previous"] == "result":
        url = "/result?query="+session["search"]
        return redirect(url)
    elif session["previous"] == "category":
        return redirect("/category")
    elif session["previous"] == "tags":
        return redirect("/tag")
    return redirect("/all_posts")

@app.route("/comment/delete/<int:id>", methods=["POST"])
def delete_comment(id):
    if users.logged_in():
        comments.delete(id)
    return redirect("/comment")
