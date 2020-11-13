CREATE TABLE users(
    first_name text,
    last_name text,
    userID text primary key,
    hashcode int
);

CREATE TABLE posts(
    post_id text primary key,
    title text,
    content text,
    create_time text,
    vote_count int,
    voted_userID text,
    userID text,
    FOREIGN KEY (userID)
        REFERENCES users (userID)
);