CREATE DATABASE starsea;
USE starsea;

-- USERS TABLE

CREATE TABLE users
(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    spotify_id VARCHAR(255) UNIQUE,
    profile_image VARCHAR(500),
    country VARCHAR(10)
);

-- ORGANIZERS TABLE

CREATE TABLE organizers
(
    organizer_id   INT AUTO_INCREMENT PRIMARY KEY,
    organizer_name VARCHAR(255) NOT NULL
);

-- EVENTS TABLE

CREATE TABLE events
(
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(150) NOT NULL,
    event_description VARCHAR(500),
    event_date DATE,
    ticket_link VARCHAR(255),
    event_location VARCHAR(255),
    organizer_id INT,

    FOREIGN KEY (organizer_id)
        REFERENCES organizers (organizer_id)
        ON DELETE CASCADE
);

-- ARTISTS TABLE

CREATE TABLE artists
(
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL
);

-- GENRES TABLE

CREATE TABLE genres
(
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL
);

-- EVENT <-> ARTIST RELATIONSHIP

CREATE TABLE event_artist
(
    event_id  INT,
    artist_id INT,

    PRIMARY KEY (event_id, artist_id),

    FOREIGN KEY (event_id)
        REFERENCES events (event_id)
        ON DELETE CASCADE,

    FOREIGN KEY (artist_id)
        REFERENCES artists (artist_id)
        ON DELETE CASCADE
);

-- USER <-> EVENT RELATIONSHIP

CREATE TABLE user_event
(
    user_id  INT,
    event_id INT,

    PRIMARY KEY (user_id, event_id),

    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (event_id)
        REFERENCES events (event_id)
        ON DELETE CASCADE
);

-- ARTIST <-> GENRE RELATIONSHIP

CREATE TABLE artist_genre
(
    artist_id INT,
    genre_id  INT,

    PRIMARY KEY (artist_id, genre_id),

    FOREIGN KEY (artist_id)
        REFERENCES artists (artist_id)
        ON DELETE CASCADE,

    FOREIGN KEY (genre_id)
        REFERENCES genres (genre_id)
        ON DELETE CASCADE
);

-- USER <-> GENRE RELATIONSHIP

CREATE TABLE user_genre
(
    user_id  INT,
    genre_id INT,

    PRIMARY KEY (user_id, genre_id),

    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (genre_id)
        REFERENCES genres (genre_id)
        ON DELETE CASCADE
);