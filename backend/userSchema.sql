DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  username TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  userpassword TEXT NOT NULL  
);