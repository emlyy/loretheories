CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE posts (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, title TEXT, message TEXT, category TEXT, posted_at TIMESTAMP);
CREATE TABLE comments (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, message TEXT, post_id INTEGER REFERENCES posts, posted_at TIMESTAMP);
CREATE TABLE tags (post_id INTEGER REFERENCES posts, tag TEXT);
CREATE TABLE likes (post_id INTEGER REFERENCES posts, user_id INTEGER REFERENCES users);
