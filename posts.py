from flask import session
from sqlalchemy.sql import text
from db import db

def get_all_posts():
    sql = text("SELECT title, message, posted_at FROM posts")
    result = db.session.execute(sql)
    posts = result.fetchall()
    return posts

def save_post(title, message):
    user_id = session["user_id"]
    #try:
    sql = text("INSERT INTO posts (user_id, title, message, posted_at) VALUES (:user_id, :title, :message, NOW())")
    db.session.execute(sql, {"user_id":user_id, "title":title, "message":message})
    db.session.commit()
    #except:
        #return False
    return True
