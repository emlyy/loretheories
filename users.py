from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    except:
        return False
    return True

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    if check_password_hash(user[1], password):
        session["username"] = username
        session["user_id"] = user[0]
        return True
    return False

def logout():
    del session["username"]
    del session["user_id"]
