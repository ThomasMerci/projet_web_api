**﻿# project_web_scraping**


# Après téléchargement lancer

docker-compose build


docker-compose up


docker start mysql_db



# Projet

Le but du projet est de mettre en œuvre les connaissances en du web scraping. Pour ce projet, il a été choisi d'utiliser avec l'api de http://api.openweathermap.org/. Cette api fournit des informations météorologiques actualisées qui détient aussi une grosse base de données sur toutes les villes du monde entier.

Une fois les données récupérées, elles sont stockées dans Cassandra et MySQL, cela donne une garanti ainsi que la persistance des données.

Après avoir enregistré les informations, je les transmets à l'api d'OpenAI pour les transformer en un article de presse. Au début, j'avais opté pour le modèle Llama 2 pour effectuer cette transformation en presse. toutefois, le coût en GPU est assez élevé.

Après récupération de l'article, les données sont envoyées en api au font-end, le JS met en forme les données pour la page en html.

