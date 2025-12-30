CREATE TABLE users (
    tg_id BIGINT PRIMARY KEY,
    nickname TEXT,
    player_tag TEXT UNIQUE,
    balance NUMERIC DEFAULT 0,
    referrer_id BIGINT,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    mode TEXT,
    creator_id BIGINT,
    max_players INT,
    status TEXT,
    lobby_code TEXT,
    started_at TIMESTAMP,
    winner_id BIGINT
);

CREATE TABLE match_players (
    match_id INT,
    tg_id BIGINT,
    PRIMARY KEY (match_id, tg_id)
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    tg_id BIGINT,
    amount NUMERIC,
    status TEXT
);