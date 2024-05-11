CREATE TABLE users (
    username TEXT PRIMARY KEY,
    phone TEXT NOT NULL UNIQUE,
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
    week INTEGER NOT NULL,
    year INTEGER NOT NULL
);