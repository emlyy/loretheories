CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE posts (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, title TEXT, message TEXT, posted_at TIMESTAMP);
