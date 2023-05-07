from flask import session
from sqlalchemy.sql import text
from db import db

def get_comments():
    post_id = session["post_id"]
    sql = text("SELECT u.username, c.message, c.posted_at, c.id, c.user_id, p.title "
    "FROM users u JOIN comments c ON c.user_id=u.id JOIN posts p ON c.post_id=p.id  "
    "WHERE c.post_id=:post_id")
    result = db.session.execute(sql, {"post_id":post_id})
    comments = result.fetchall()
    return comments

def post_comment(message):
    post_id = session["post_id"]
    user_id = session["user_id"]
    try:
        sql = text("INSERT INTO comments (user_id, message, post_id, posted_at) "
        "VALUES (:user_id, :message, :post_id, NOW())")
        db.session.execute(sql, {"user_id":user_id, "message":message, "post_id":post_id})
        db.session.commit()
    except:
        return False
    return True

def delete(comment_id):
    sql = text("DELETE FROM comments WHERE id=:id")
    db.session.execute(sql, {"id":comment_id})
    db.session.commit()
