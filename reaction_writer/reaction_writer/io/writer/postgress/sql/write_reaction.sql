INSERT INTO user_reaction (username, reaction, timestamp)
VALUES ($1, $2, to_timestamp($3));
