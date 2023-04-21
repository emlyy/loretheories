from flask import session
from sqlalchemy.sql import text
from db import db

def check_if_liked(post_id, user_id):
    sql = text("SELECT * FROM likes WHERE post_id=:post_id AND user_id=:user_id")
    result = db.session.execute(sql, {"post_id":post_id, "user_id":user_id})
    likes = result.fetchone()
    if likes == None:
        return False
    return True

def like_post():
    post_id = session["post_id"]
    user_id = session["user_id"]
    if not check_if_liked(post_id, user_id):
        try:
            sql = text("INSERT INTO likes (post_id, user_id) VALUES (:post_id, :user_id)")
            db.session.execute(sql, {"post_id":post_id, "user_id":user_id})
            db.session.commit()
        except:
            return False
    else:
        try:
            sql = text("DELETE FROM likes WHERE post_id=:post_id AND user_id=:user_id")
            db.session.execute(sql, {"post_id":post_id, "user_id":user_id})
            db.session.commit()
        except:
            return False
    return True
