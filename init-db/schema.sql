CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    total_tickets INTEGER NOT NULL,
    available_tickets INTEGER NOT NULL,
    version INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    seat_number INTEGER NOT NULL,
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, seat_number)
);

-- Insert Seed Data only if the table is empty
-- This prevents duplicate rows on every restart
INSERT INTO events (name, total_tickets, available_tickets)
SELECT 'System Design Workshop', 100, 100
WHERE NOT EXISTS (SELECT 1 FROM events WHERE name = 'System Design Workshop');

INSERT INTO users (username, email)
SELECT 'paawan_dev', 'paawan@gmail.com'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'paawan_dev');