#py -3.11 -m pip install git+https://github.com/runpod/runpod-python.git
#import runpod
#from cassandra.cluster import Cluster
#from cassandra.auth import PlainTextAuthProvider
from flask import Blueprint
from flask import Flask, request, jsonify
from python.llama import retour_texte
from python.data import ville_fonct, mysql_db_data, cassandra_db_data
import pandas as pd
from datetime import datetime, timedelta
import mysql.connector

api = Blueprint('api', __name__)

#date et heure actuel
now = datetime.now()
date = now.strftime("%d-%m-%Y")
heure = now.strftime("%H:%M:%S")

#récupération des données dans mysql
def mysql_data():
    try: 
        connection = mysql.connector.connect(host='mysql_db', user='root', password='supersecret', database='weather_data')
        cursor = connection.cursor()
        cursor.execute("SELECT city FROM weather Order by Id DESC LIMIT 5")
        data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        dc = []
        for row in data:
            row = [str(item) if isinstance(item, timedelta) else item for item in row]
            dc.append(dict(zip(column_names, row)))
        cursor.close()
        connection.close()
        return dc
    except:
        return 'Pas de données disponible'

#api de récupération et d'envoi des données pour le front-end
@api.route('/message', methods=['GET', 'POST'])
def meteo():
    data = request.json 
    ville = data.get('ville')
    cle = data.get('cle')

    mysql_db_data(ville)
    #cassandra_db_data(ville)
    dt = ville_fonct(ville)
    
    reponse = retour_texte(f"Rédige un article détaillé comme un journaliste météorologique à la (date {date} et heure{heure}) dans la ville de {dt['city']}. "
    f"La température est actuellement de est de {dt['temp']}°C, avec un maximum de {dt['temp_max']}°C et un minimum de {dt['temp_min']}°C. "
    f"L'humidité est de {dt['humidity']}% avec une pression atmosphérique de {dt['pressure']} hPa. Le ciel est {dt['sky']} avec une couverture nuageuse de {dt['cloudiness']}%. "
    f"Le soleil s'est levé à {dt['sunrise']} et se couche à {dt['sunset']}. Le vent souffle à {dt['wind']} m/s en provenance de {dt['wind_deg']} degrés. Bonne jurnée à tous", cle, dt)

    reponse2 = f" {dt['city']}, {dt['temp']}°C, max {dt['temp_max']}°C,  min{dt['temp_min']}°C, humidité {dt['humidity']}%, pression{dt['pressure']} hPa, couverture nuageuse de {dt['cloudiness']}%, levé du soleil {dt['sunrise']}, vent de {dt['wind']} m/s"
    print(reponse2)

    print(mysql_data())
    db_data = mysql_data()
    if cle != '':
        return jsonify({"data": reponse, 'db_data': db_data})
    else:
        reponse = reponse2
        return jsonify({"data": reponse, 'db_data': db_data})





    





