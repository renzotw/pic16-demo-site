CREATE TABLE IF NOT EXISTS messages (
  id INT PRIMARY KEY AUTO_INCREMENT,
  handle TEXT UNIQUE NOT NULL,
  message TEXT NOT NULL
  );