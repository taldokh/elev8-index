CREATE TABLE equities (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    quarter DATE NOT NULL,
    weight INT NOT NULL CHECK (weight >= 0 AND weight <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
