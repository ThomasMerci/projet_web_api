**﻿# project_web_scraping**


# Network:

docker network create network_project_scraping


# volume

docker volume create project_scraping


# Cassandra
cd cassandra


docker build -t cassandra_db .


docker run -p 9042:9042 --network=network_project_scraping --rm --name cassandra_db cassandra_db


docker start cassandra_db


ou:


docker run -p 9042:9042 --network=network_project_scraping --rm --name cassandra_db2 -d cassandra:3.11

docker run -p 9042:9042 --rm --name cassandra_db3 -d cassandra:3.11

cd ..

# mysql

mysql:

cd mysql

docker build -t mysql_db .

docker run -d -p 3306:3306 --network=network_project_scraping --name mysql_db -e MYSQL_ROOT_PASSWORD=supersecret mysql_db

docker start mysql_db

cd ..

# app

docker build --tag project_web_scraping:latest .



# run

docker run -it --network=network_project_scraping -v project_scraping:/app --name project_web_scraping project_web_scraping:latest

docker run -it --network=network_project_scraping -v project_scraping:/app --name project_web_scraping project_web_scraping:latest python app.py

docker run -it -v project_scraping:/app --name project_web_scraping project_web_scraping:latest

docker run -it --network=network_project_scraping -v project_scraping:/app --name project_web_scraping -e MYSQL_ROOT_PASSWORD=supersecret project_web_scraping:latest



# vérifier les données dans cassandra

docker exec -it cassandra_db cqlsh


DESCRIBE keyspaces;


USE jobs_scraping;


SELECT * FROM jobs LIMIT 10;
