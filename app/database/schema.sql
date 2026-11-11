CREATE DATABASE starsea;
USE starsea;

-- TABELA DE USUÁRIOS

CREATE TABLE users
(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    user_password VARCHAR(255),
    spotify_id VARCHAR(255) UNIQUE,
    profile_image VARCHAR(500),
    country VARCHAR(10),
    city VARCHAR(100),
    state VARCHAR(100),
    latitude DOUBLE NULL,
    longitude DOUBLE NULL,
    notification_radius_km DOUBLE NOT NULL DEFAULT 50,
    nearby_notifications_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    personalized_notifications_only BOOLEAN NOT NULL DEFAULT FALSE,
    spotify_preferences_synced_at DATETIME NULL
);

-- TABELA DE ORGANIZADORES

CREATE TABLE organizers
(
    organizer_id   INT AUTO_INCREMENT PRIMARY KEY,
    organizer_name VARCHAR(255) NOT NULL
);

-- TABELA DE EVENTOS

CREATE TABLE events
(
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(150) NOT NULL,
    event_description VARCHAR(500),
    event_date DATE,
    ticket_link VARCHAR(255),
    event_location VARCHAR(255),
    latitude DOUBLE NULL,
    longitude DOUBLE NULL,
    organizer_id INT,

    FOREIGN KEY (organizer_id)
        REFERENCES organizers (organizer_id)
        ON DELETE CASCADE
);

-- TABELA DE ARTISTAS

CREATE TABLE artists
(
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    spotify_id VARCHAR(255) UNIQUE NULL
);

-- TABELA DE GÊNEROS

CREATE TABLE genres
(
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL
);

-- ASSOCIAÇÃO ENTRE EVENTOS E ARTISTAS

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

-- ASSOCIAÇÃO ENTRE USUÁRIOS E EVENTOS

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

-- ASSOCIAÇÃO ENTRE ARTISTAS E GÊNEROS

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

-- ASSOCIAÇÃO ENTRE USUÁRIOS E GÊNEROS

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

-- ARTISTAS ESCOLHIDOS PELO USUÁRIO OU IMPORTADOS DO SPOTIFY
CREATE TABLE music_preferences
(
    user_id INT NOT NULL,
    artist_id INT NOT NULL,
    source VARCHAR(30) NOT NULL,
    `rank` INT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (user_id, artist_id, source),
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES artists (artist_id) ON DELETE CASCADE
);

-- GÊNEROS DO SPOTIFY, SEPARADOS DOS CADASTRADOS MANUALMENTE EM artist_genre
CREATE TABLE artist_spotify_genre
(
    artist_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (artist_id, genre_id),
    FOREIGN KEY (artist_id) REFERENCES artists (artist_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres (genre_id) ON DELETE CASCADE
);

-- GÊNEROS RETORNADOS COM OS ARTISTAS PREFERIDOS EM CADA IMPORTAÇÃO DO USUÁRIO
CREATE TABLE music_preference_genre
(
    user_id INT NOT NULL,
    artist_id INT NOT NULL,
    source VARCHAR(30) NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (user_id, artist_id, source, genre_id),
    FOREIGN KEY (user_id, artist_id, source)
        REFERENCES music_preferences (user_id, artist_id, source) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres (genre_id) ON DELETE CASCADE
);

-- NOTIFICAÇÕES NA APLICAÇÃO: UM AVISO POR USUÁRIO E EVENTO
CREATE TABLE notifications
(
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    message VARCHAR(500) NOT NULL,
    distance_km DOUBLE NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL,
    CONSTRAINT uq_notification_user_event UNIQUE (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events (event_id) ON DELETE CASCADE,
    INDEX ix_notifications_user_id (user_id),
    INDEX ix_notifications_event_id (event_id)
);
