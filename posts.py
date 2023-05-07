from flask import session
from sqlalchemy.sql import text
from db import db

def get_post_id(title, message):
    user_id = session["user_id"]
    sql = text("SELECT p.id FROM posts p WHERE p.user_id=:user_id AND"
    " p.message=:message AND p.title=:title")
    result = db.session.execute(sql, {"user_id":user_id, "message":message, "title":title})
    post_id = result.fetchall()
    return post_id[-1][0]

def get_all_posts():
    sql = text("SELECT u.username, p.user_id, p.id, p.title, p.message,"
    "p.posted_at, (SELECT COUNT(l.user_id) FROM likes l WHERE "
    "p.id=l.post_id) FROM users u, posts p WHERE u.id=p.user_id"
    " ORDER BY p.posted_at DESC")
    result = db.session.execute(sql)
    posts = result.fetchall()
    return posts

def save_post(title, message, category):
    user_id = session["user_id"]
    sql = text("INSERT INTO posts (user_id, title, message,"
        "category, posted_at) VALUES (:user_id, :title, :message,"
        " :category, NOW())")
    db.session.execute(sql, {"user_id":user_id, "title":title,
        "message":message, "category":category})
    db.session.commit()
    return True

def save_tags(tags, post_id):
    tags_list = list(tags.split(" "))
    if len(tags) == 0:
        return True
    for tag in tags_list:
        sql = text("INSERT INTO tags (post_id, tag) VALUES (:post_id, :tag)")
        db.session.execute(sql, {"post_id":post_id, "tag":tag})
        db.session.commit()
    return True

def search_posts(search_word):
    sql = text("SELECT u.username, p.user_id, p.id, p.title, p.message,"
    "p.posted_at, (SELECT COUNT(l.user_id) FROM likes l WHERE"
    " p.id=l.post_id) FROM users u, posts p WHERE u.id=p.user_id AND"
    " (p.message ILIKE :search_word OR p.title ILIKE :search_word)"
    "ORDER BY p.posted_at DESC")
    result = db.session.execute(sql, {"search_word":"%"+search_word+"%"})
    posts = result.fetchall()
    return posts

def posts_by_category():
    category = session["category"]
    sql = text("SELECT u.username, p.user_id, p.id, p.title, p.message,"
    " p.posted_at, (SELECT COUNT(l.user_id) FROM likes l "
    "WHERE p.id=l.post_id) FROM users u, posts p WHERE "
    "u.id=p.user_id AND p.category=:category ORDER BY p.posted_at DESC")
    result = db.session.execute(sql, {"category":category})
    posts = result.fetchall()
    return posts

def posts_by_tag():
    tag = session["tag"]
    sql = text("SELECT u.username, p.user_id, p.id, p.title, p.message,"
    " p.posted_at, (SELECT COUNT(l.user_id) FROM likes l "
    "WHERE p.id=l.post_id) FROM users u JOIN posts p ON u.id=p.user_id "
    "JOIN tags t ON p.id=t.post_id WHERE t.tag LIKE :tag ORDER BY p.posted_at DESC")
    result = db.session.execute(sql, {"tag":tag})
    posts = result.fetchall()
    return posts

def tags():
    sql = text("SELECT DISTINCT tag FROM tags ORDER BY tag ASC")
    result = db.session.execute(sql)
    tags = result.fetchall()
    return tags

def delete(id):
    sql = text("DELETE FROM tags WHERE post_id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    sql = text("DELETE FROM comments WHERE post_id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    sql = text("DELETE FROM likes WHERE post_id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    sql = text("DELETE FROM posts WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
