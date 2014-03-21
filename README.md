api
===

This is the api for the form apps

CREATE DATABASE api

CREATE TABLE users (id INT(10) NOT NULL AUTO_INCREMENT, username VARCHAR(100), password VARCHAR(100), unique_id VARCHAR(200), PRIMARY KEY (id))
CREATE TABLE form 

CREATE TABLE form (id INT(10) NOT NULL AUTO_INCREMENT, unique_id VARCHAR(200), full_name VARCHAR(200), food VARCHAR(600), music VARCHAR(600), movie VARCHAR(600), book VARCHAR(600), poem VARCHAR(600), quote VARCHAR(600), PRIMARY KEY (id))
