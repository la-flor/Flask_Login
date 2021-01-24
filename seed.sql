DROP DATABASE IF EXISTS flask_login;

CREATE DATABASE flask_login;

\c flask_login;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR (25) UNIQUE NOT NULL,
    password VARCHAR (25) UNIQUE NOT NULL
);

INSERT INTO users (username, password)
VALUES ('PracticeUsername', 'PracticePassword1593');