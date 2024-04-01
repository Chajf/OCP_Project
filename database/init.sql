-- Create a new database
CREATE DATABASE IF NOT EXISTS sentiment_database;

-- Use the newly created database
USE sentiment_database;

-- Create a table
CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text_content TEXT
);

-- Create a table
CREATE TABLE IF NOT EXISTS sentiment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    label VARCHAR(255),
    val FLOAT
);