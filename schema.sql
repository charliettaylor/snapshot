CREATE TABLE users (
    username TEXT PRIMARY KEY,
    phone TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    -- bool
    active INTEGER NOT NULL
);

CREATE TABLE registrations (
    phone TEXT PRIMARY KEY,
    username TEXT NULL,
    -- 0 start, 1 username, 2 retry username, 3 complete
    state INTEGER NOT NULL
);

CREATE TABLE prompts (
    id INTEGER PRIMARY KEY,
    prompt TEXT NOT NULL,
    date DATE NOT NULL
);

CREATE TABLE pics (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL,
    prompt INTEGER NOT NULL,
    user TEXT NOT NULL,
    winner INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(prompt) REFERENCES prompts(id),
    FOREIGN KEY(user) REFERENCES users(username)
);
