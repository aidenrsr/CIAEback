DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS badges;
DROP TABLE IF EXISTS user_point;
DROP TABLE IF EXISTS user_badges;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS book_page;
DROP TABLE IF EXISTS messages;

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  username TEXT UNIQUE,  -- Optional, as OAuth may not require a username
  email TEXT UNIQUE NOT NULL,  -- OAuth usually provides an email
  password TEXT,  -- Optional for OAuth users
  oauth_provider TEXT,  -- Name of the OAuth provider (e.g., Google, Facebook)
  oauth_user_id TEXT UNIQUE,  -- OAuth provider's unique user ID
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  -- Please add 
);

CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL REFERENCES users(username),
    text TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_book_interaction (
  interaction_id SERIAL PRIMARY KEY,
  user_id SERIAL REFERENCES users(user_id),
  book_id SERIAL REFERENCES books(book_id),
  status INTEGER NOT NULL,
  score INTEGER NOT NULL,
  last_interacted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE badges (
  badge_id SERIAL PRIMARY KEY,
  badge_name TEXT NOT NULL,
  badge_image TEXT NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE user_point (
  user_id INTEGER REFERENCES users(user_id),
  points INTEGER NOT NULL,
  PRIMARY KEY (user_id)
);

CREATE TABLE user_badges (
  user_id INTEGER REFERENCES users(user_id),
  badge_id INTEGER REFERENCES badges(badge_id),
  PRIMARY KEY (user_id, badge_id)  -- Composite primary key
);

CREATE TABLE books (
  book_id SERIAL PRIMARY KEY,
  book_name TEXT NOT NULL,
  book_author TEXT NOT NULL,
  book_page_num INTEGER NOT NULL,
  content TEXT NOT NULL,
  date_added DATE DEFAULT CURRENT_DATE
);

CREATE TABLE book_page (
  book_id INTEGER REFERENCES book(book_id),
  page_num INTEGER NOT NULL,
  page_text TEXT NOT NULL,
  page_pdf TEXT NOT NULL,
  PRIMARY KEY (book_id, page_num)  -- Composite primary key
);

CREATE TABLE chapter_page (
  chapter_id SERIAL PRIMARY KEY,
  book_id INTEGER REFERENCES book(book_id),
  start_page INTEGER NOT NULL,
  end_page INTEGER NOT NULL
);


CREATE TABLE score (
  identification_score INTEGER NOT NULL,
  catharsis_score INTEGER NOT NULL,
  insight_score INTEGER NOT NULL,
  score_total INTEGER NOT NULL
);