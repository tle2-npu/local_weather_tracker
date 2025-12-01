# Local Weather Tracker
A simple Python application that retrieves real-time weather data from the Open-Meteo API, stores observations in a PostgreSQL database, and exposes CRUD endpoints for managing those observations.

## Description 
This is an application allows users to:

- Search a city using the Open-Meteo Geocoding API
- Retrieve live weather data (temperature, windspeed, latitude, longitude, timestamp)
- Store observations in a PostgreSQL database
- Exposes a CRUD Web Service (create new observations, update temperature/windspeed, delete an observation)

## Prerequisites
Make sure you have the following installed:
- **Python**
- **PostgreSQL installed and running**
- **Git**
- **pip** 
- **VS Code** (recommended)

## Usage
### 1. Clone the repository 
`git clone GITHUB_URL_HERE`

`cd YOUR_REPO_NAME`

Open in VS Code: `code.`
### 2. Create and Activate Virtual Environment
- Create:

`python3 -m venv venv`
- Activate: 

`source .venv/bin/activate` for macOS / Linux

`.venv\Scripts\Activate.ps1` for Windows 
### 3. Install Dependencies
`pip install -r requirements.txt`
### 4. Set Up Environment Variables
Create `.env` file in the project root:
```python
DB_USER=postgres
DB_PASSWORD=12345678
DB_HOST=localhost
DB_PORT=5432
DB_NAME=databases_final_project
```
### 5. Initialize Database
Inside PostgreSQL:

1. Create table 
```python
CREATE TABLE weather_observations (
	city_id SERIAL PRIMARY KEY,
	city VARCHAR(50) UNIQUE NOT NULL,
	temperature NUMERIC(5,2),
	windspeed NUMERIC(5,2),
	latitude NUMERIC(10,5),
	longitude NUMERIC(10,5),
	observation_time TIMESTAMP DEFAULT NOW()	
);
```
2. Insert data
```python
INSERT INTO weather_observations (city, temperature, windspeed, latitude, longitude) VALUES 
('Chicago',4.9,9.9,41.85003,-87.65005),
('Boston',13.2,25.7,42.35843,-71.05977),
('Austin',6.7,4.7,30.26715,-97.74306),
('New York',10.9,24.0,40.71427,-74.00597),
('Atlanta',7.2,14.9,33.749,-84.38798),
('Washington',10.9,21.3,38.89511,-77.03637),
('San Diego',16.1,4.3,32.71571,-117.16472),
('Los Angeles',17.0,4.9,34.05223,-118.24368),
('Westminster',16.0,19.5,51.4975,-0.1357),
('Houston',10.5,3.6,29.76328,-95.36327);
```
3. Retrieve all observations
```python
SELECT * FROM weather_observations;
```
## Features
- Real-time weather retrieval using Open-Meteo
- PostgreSQL-backed storage
- CRUD routes:

    - Create new observation
    - View all observations
    - View observation by ID
    - Update weather values
    - Delete observation 
- Graceful error handling for database connection failures
- Clean database abstraction using a reusable `_execute()` method 

## Contribution 
Feel free to fork this repository and open a pull request.

Suggestions and improvements are always welcome!