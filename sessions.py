from flask import session
from sqlalchemy.sql import text
from db import db

def save_post(post_id):
    session["post_id"] = post_id

def save_category(category):
    session["category"] = category

def save_previous(previous):
    session["previous"] = previous

def save_search(word):
    session["search"] = word

def save_tag(tag):
    session["tag"] = tag
