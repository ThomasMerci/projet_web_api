CREATE KEYSPACE IF NOT EXISTS weather_data WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
USE weather_data;

CREATE TABLE IF NOT EXISTS weather(
    id UUID PRIMARY KEY,
    city TEXT,
    country TEXT,
    temp DECIMAL,
    temp_max DECIMAL,
    temp_min DECIMAL,
    humidity INT,
    pressure DECIMAL,
    sky TEXT,
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    wind DECIMAL,
    wind_deg INT,
    dt TIMESTAMP,
    cloudiness INT
);


