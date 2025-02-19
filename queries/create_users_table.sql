-- Step 1: Create the ENUM type for the role
CREATE TYPE user_role AS ENUM ('guest', 'subscriber');

-- Step 2: Create the users table
CREATE TABLE users
(
    id         SERIAL PRIMARY KEY,
    first_name VARCHAR(50)        NOT NULL,
    last_name  VARCHAR(50)        NOT NULL,
    role       user_role          NOT NULL,
    username   VARCHAR(50) UNIQUE NOT NULL,
    password   TEXT               NOT NULL, -- Consider hashing passwords for security
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);