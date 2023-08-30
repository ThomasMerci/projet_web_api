#pip install cassandra-driver
import urllib.request
import json
from datetime import datetime
import json
import mysql.connector

def data_ville_fonct(ville):
    data_ville = [{'ville': 'Paris', 'pays': 'FR', 'ville_id': '2988507'},
                  {'ville': 'Bordeaux', 'pays': 'FR', 'ville_id': '5905868'},
                  {'ville': 'Monaco', 'pays': 'MC', 'ville_id': '2993458'}]

    for i in data_ville:
        if ville.lower() == i['ville'].lower():
            return i['ville'], i['pays'], i['ville_id']
        
    with open('./python/city.json', 'r') as f:
        city_data = json.load(f)
        for city in city_data:
            if ville.lower() == city['name'].lower():
                return city['name'], city['country'], str(city['_id'])

    return 'Paris', 'FR', '2988507'



def url_builder(ville, pays, ville_id):
    user_api =  '58d1efb0943d1d89316df09425339d11'
    unit = 'metric'
    if ville:
        api = 'http://api.openweathermap.org/data/2.5/weather?q='
        full_api_url = api + ville + ',' + pays + '&mode=json&units=' + unit + '&APPID=' + user_api
    else:
        api = 'http://api.openweathermap.org/data/2.5/weather?id='
        full_api_url = api + ville_id + '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url

def data_fetch(full_api_url):
    with urllib.request.urlopen(full_api_url) as url:
        data = json.loads(url.read().decode('utf-8'))
    return data

def time_converter(time):
    try:
        return datetime.fromtimestamp(int(time)).strftime('%H:%M:%S')
    except ValueError:
        return time
    
    

def data_organizer(raw_api_dict):
    data= {'city': raw_api_dict.get('name'),
        'country': raw_api_dict.get('sys').get('country'),
        'temp': raw_api_dict.get('main').get('temp'),
        'temp_max': raw_api_dict.get('main').get('temp_max'),
        'temp_min': raw_api_dict.get('main').get('temp_min'),
        'humidity': raw_api_dict.get('main').get('humidity'),
        'pressure': raw_api_dict.get('main').get('pressure'),
        'sky': raw_api_dict['weather'][0]['main'],
        'sunrise': time_converter(raw_api_dict.get('sys').get('sunrise')),
        'sunset': time_converter(raw_api_dict.get('sys').get('sunset')),
        'wind': raw_api_dict.get('wind').get('speed'),
        'wind_deg': raw_api_dict.get('wind').get('deg'),
        'dt': time_converter(raw_api_dict.get('dt')),
        'cloudiness': raw_api_dict.get('clouds').get('all')
    }
    return data

#ville
def ville_fonct(ville):
    ville, pays, ville_id =data_ville_fonct(ville)
    full_api_url = url_builder(ville, pays, ville_id)
    data = data_fetch(full_api_url)
    df = data_organizer(data)
    return df

def mysql_db_data(ville):
    try :
        df = ville_fonct(ville)
        connection = mysql.connector.connect( host='mysql_db', user='root', password='supersecret', database='weather_data')
        cursor = connection.cursor()

        cursor.execute("SHOW TABLES LIKE 'weather'")
        result = cursor.fetchone()
        if not result:
            create_table_query = """CREATE TABLE weather (id INT AUTO_INCREMENT PRIMARY KEY, city VARCHAR(255),
            country VARCHAR(255), temp DECIMAL(5,2), temp_max DECIMAL(5,2), temp_min DECIMAL(5,2), 
            humidity INT, pressure INT, sky VARCHAR(255), sunrise TIME,  sunset TIME, 
            wind DECIMAL(5,2),  wind_deg INT, dt TIME, cloudiness INT) """
            cursor.execute(create_table_query)

        query = """INSERT INTO weather (city, country, temp, temp_max, temp_min, humidity, pressure, sky, sunrise, sunset, wind, wind_deg, dt, cloudiness)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (df['city'], df['country'], df['temp'], df['temp_max'], df['temp_min'], df['humidity'], df['pressure'], df['sky'], time_converter(df['sunrise']), time_converter(df['sunset']), df['wind'], df['wind_deg'], time_converter(df['dt']), df['cloudiness'])
        cursor.execute(query, data)

        connection.commit()
        cursor.close()
        connection.close()
    except:
        print("mysql ne marche pas")



def mysql_database():
    connection = mysql.connector.connect(host='mysql_db', user='root', password='supersecret', database='weather_data')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS weather")
    create_table_query = """CREATE TABLE weather (id INT AUTO_INCREMENT PRIMARY KEY, 
        city VARCHAR(255),country VARCHAR(255), temp DECIMAL(5,2), temp_max DECIMAL(5,2),
        temp_min DECIMAL(5,2), humidity INT, pressure INT,sky VARCHAR(255),sunrise TIME, 
        sunset TIME,wind DECIMAL(5,2), wind_deg INT, dt TIME, cloudiness INT)"""
    cursor.execute(create_table_query)
    cursor.close()
    connection.close()



from cassandra.cluster import Cluster
import uuid

def cassandra_db_data(ville):
    try:
        df = ville_fonct(ville)
        cluster = Cluster(['cassandra_db'], port=9042)
        session = cluster.connect('weather_data')

        tables = session.execute("SELECT table_name FROM system_schema.tables WHERE keyspace_name='weather_data';")
        if 'weather' not in [table.table_name for table in tables]:
            create_table_query = """CREATE TABLE weather (id UUID PRIMARY KEY,
                city TEXT,country TEXT, temp DOUBLE, temp_max DOUBLE,temp_min DOUBLE, humidity INT, 
                pressure INT,sky TEXT,sunrise TIMESTAMP, sunset TIMESTAMP, wind DOUBLE, 
                wind_deg INT, dt TIMESTAMP, cloudiness INT)"""
            session.execute(create_table_query)

        query = """
        INSERT INTO weather (id, city, country, temp, temp_max, temp_min, humidity, pressure, sky, sunrise, sunset, wind, wind_deg, dt, cloudiness)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (uuid.uuid4(), df['city'], df['country'], df['temp'], df['temp_max'], df['temp_min'], df['humidity'], df['pressure'], df['sky'], time_converter(df['sunrise']), time_converter(df['sunset']), df['wind'], df['wind_deg'], time_converter(df['dt']), df['cloudiness'])
        session.execute(query, data)
        cluster.shutdown()
    except:
        print('Cassandra ne marche')