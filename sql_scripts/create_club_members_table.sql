CREATE TABLE IF NOT EXISTS club_members(
    id BIGSERIAL PRIMARY KEY,
    season TEXT,
    player_tag TEXT,
    player_name TEXT,
    trophies INT
);
