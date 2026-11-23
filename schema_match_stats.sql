-- ========================================================
-- Schema: Tournament Teams Players & Match Events
-- For Pannangala Panthers Sports Club
-- ========================================================

-- 1. Table: Tournament Team Players (Team Rosters)
CREATE TABLE IF NOT EXISTS tournament_team_players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL,
    player_name VARCHAR(100) NOT NULL,
    jersey_number INT NULL,
    position VARCHAR(50) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES tournament_teams(id) ON DELETE CASCADE
);

CREATE INDEX idx_tournament_team_players_team_id ON tournament_team_players(team_id);


-- 2. Table: Match Events (Goals & Cards)
CREATE TABLE IF NOT EXISTS match_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    team_id INT NOT NULL,
    player_name VARCHAR(100) NOT NULL,
    event_type ENUM('goal', 'green_card', 'yellow_card', 'red_card') NOT NULL,
    minute INT NULL,
    notes VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES tournament_matches(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES tournament_teams(id) ON DELETE CASCADE
);

CREATE INDEX idx_match_events_match_id ON match_events(match_id);


-- ========================================================
-- Example Sample Data (Optional testing)
-- ========================================================
-- Sample Team Players:
-- INSERT INTO tournament_team_players (team_id, player_name, jersey_number, position) VALUES
-- (1, 'Bopanna', 10, 'Forward'),
-- (1, 'Vinay Poovanna', 7, 'Midfielder'),
-- (1, 'Vivek Ponnanna', 4, 'Defender');

-- Sample Match Goals & Cards:
-- INSERT INTO match_events (match_id, team_id, player_name, event_type) VALUES
-- (1, 1, 'Bopanna', 'goal'),
-- (1, 1, 'Vinay Poovanna', 'goal'),
-- (1, 1, 'Vivek Ponnanna', 'green_card'),
-- (1, 2, 'Rival Striker', 'goal'),
-- (1, 2, 'Rival Defender', 'yellow_card');
