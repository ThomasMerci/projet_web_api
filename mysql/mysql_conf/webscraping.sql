Create Database weather_data;
use weather_data;
CREATE TABLE IF NOT EXISTS weather (
id INT AUTO_INCREMENT PRIMARY KEY, 
city VARCHAR(255),
country VARCHAR(255), 
temp DECIMAL(5,2), 
temp_max DECIMAL(5,2),
temp_min DECIMAL(5,2), 
humidity INT, 
pressure INT,
sky VARCHAR(255),
sunrise TIME, 
sunset TIME, 
wind DECIMAL(5,2), 
wind_deg INT, 
dt TIME, 
cloudiness INT);