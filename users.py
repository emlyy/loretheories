from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db
import secrets

def logged_in():
    if session.get("username"):
        return True
    return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return True

def check_username(username):
    sql = text("SELECT username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return True
    return False

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    if logged_in():
        return False
    if check_password_hash(user[1], password):
        session["username"] = username
        session["user_id"] = user[0]
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False

def logout():
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
