CREATE TABLE index_points (
    id SERIAL PRIMARY KEY,
    day_start_points INT NOT NULL,
    day_end_points INT NOT NULL,
    market_date DATE NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
