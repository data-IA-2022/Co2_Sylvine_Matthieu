# -*- coding: utf-8 -*-
#from sqlalchemy.types import Integer
import pandas as pd
import numpy as np
import utils
from urllib import request
import json
import psycopg2

# lien api vers data
api_url = "https://data.seattle.gov/resource/2bpz-gwpy.json?$query=SELECT%0A%20%20%60osebuildingid%60%2C%0A%20%20%60datayear%60%2C%0A%20%20%60buildingtype%60%2C%0A%20%20%60primarypropertytype%60%2C%0A%20%20%60propertyname%60%2C%0A%20%20%60address%60%2C%0A%20%20%60city%60%2C%0A%20%20%60state%60%2C%0A%20%20%60zipcode%60%2C%0A%20%20%60taxparcelidentificationnumber%60%2C%0A%20%20%60councildistrictcode%60%2C%0A%20%20%60neighborhood%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60yearbuilt%60%2C%0A%20%20%60numberofbuildings%60%2C%0A%20%20%60numberoffloors%60%2C%0A%20%20%60propertygfatotal%60%2C%0A%20%20%60propertygfaparking%60%2C%0A%20%20%60propertygfabuilding_s%60%2C%0A%20%20%60listofallpropertyusetypes%60%2C%0A%20%20%60largestpropertyusetype%60%2C%0A%20%20%60largestpropertyusetypegfa%60%2C%0A%20%20%60secondlargestpropertyusetype%60%2C%0A%20%20%60secondlargestpropertyuse%60%2C%0A%20%20%60thirdlargestpropertyusetype%60%2C%0A%20%20%60thirdlargestpropertyusetypegfa%60%2C%0A%20%20%60yearsenergystarcertified%60%2C%0A%20%20%60energystarscore%60%2C%0A%20%20%60siteeui_kbtu_sf%60%2C%0A%20%20%60siteeuiwn_kbtu_sf%60%2C%0A%20%20%60sourceeui_kbtu_sf%60%2C%0A%20%20%60sourceeuiwn_kbtu_sf%60%2C%0A%20%20%60siteenergyuse_kbtu%60%2C%0A%20%20%60siteenergyusewn_kbtu%60%2C%0A%20%20%60steamuse_kbtu%60%2C%0A%20%20%60electricity_kwh%60%2C%0A%20%20%60electricity_kbtu%60%2C%0A%20%20%60naturalgas_therms%60%2C%0A%20%20%60naturalgas_kbtu%60%2C%0A%20%20%60defaultdata%60%2C%0A%20%20%60comments%60%2C%0A%20%20%60compliancestatus%60%2C%0A%20%20%60outlier%60%2C%0A%20%20%60totalghgemissions%60%2C%0A%20%20%60ghgemissionsintensity%60"

csv_file_path = "https://data.seattle.gov/resource/2bpz-gwpy.csv?$query=SELECT%0A%20%20%60osebuildingid%60%2C%0A%20%20%60datayear%60%2C%0A%20%20%60buildingtype%60%2C%0A%20%20%60primarypropertytype%60%2C%0A%20%20%60propertyname%60%2C%0A%20%20%60address%60%2C%0A%20%20%60city%60%2C%0A%20%20%60state%60%2C%0A%20%20%60zipcode%60%2C%0A%20%20%60taxparcelidentificationnumber%60%2C%0A%20%20%60councildistrictcode%60%2C%0A%20%20%60neighborhood%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60yearbuilt%60%2C%0A%20%20%60numberofbuildings%60%2C%0A%20%20%60numberoffloors%60%2C%0A%20%20%60propertygfatotal%60%2C%0A%20%20%60propertygfaparking%60%2C%0A%20%20%60propertygfabuilding_s%60%2C%0A%20%20%60listofallpropertyusetypes%60%2C%0A%20%20%60largestpropertyusetype%60%2C%0A%20%20%60largestpropertyusetypegfa%60%2C%0A%20%20%60secondlargestpropertyusetype%60%2C%0A%20%20%60secondlargestpropertyuse%60%2C%0A%20%20%60thirdlargestpropertyusetype%60%2C%0A%20%20%60thirdlargestpropertyusetypegfa%60%2C%0A%20%20%60yearsenergystarcertified%60%2C%0A%20%20%60energystarscore%60%2C%0A%20%20%60siteeui_kbtu_sf%60%2C%0A%20%20%60siteeuiwn_kbtu_sf%60%2C%0A%20%20%60sourceeui_kbtu_sf%60%2C%0A%20%20%60sourceeuiwn_kbtu_sf%60%2C%0A%20%20%60siteenergyuse_kbtu%60%2C%0A%20%20%60siteenergyusewn_kbtu%60%2C%0A%20%20%60steamuse_kbtu%60%2C%0A%20%20%60electricity_kwh%60%2C%0A%20%20%60electricity_kbtu%60%2C%0A%20%20%60naturalgas_therms%60%2C%0A%20%20%60naturalgas_kbtu%60%2C%0A%20%20%60defaultdata%60%2C%0A%20%20%60comments%60%2C%0A%20%20%60compliancestatus%60%2C%0A%20%20%60outlier%60%2C%0A%20%20%60totalghgemissions%60%2C%0A%20%20%60ghgemissionsintensity%60"

# Établir la connexion à la base de données
conn = psycopg2.connect(
    host="serveur-co2-sylvine-matthieu.postgres.database.azure.com",
    database="BDDCO2",
    user="adminCO2",
    password="Seattle-2023"
)

# conn = psycopg2.connect(utils.get_config()) # a debuguer pour garder tout secret



cur = conn.cursor()

# Récupérer les données de l'API
response = request.urlopen(api_url)
data = json.loads(response.read())

# Définir le schéma dynamiquement en fonction des clés présentes dans les données
def define_schema():
    create_table_query = "CREATE TABLE ma_table ("
    keys = data[0].keys() if data else []
    for key in keys:
        create_table_query += f"{key} VARCHAR(255),"
    create_table_query = create_table_query[:-1] + ")"
    cur.execute(create_table_query)
    conn.commit()

# Vérifier si la table existe déjà dans la base de données
# Si elle n'existe pas, définir le schéma
cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'ma_table')")
table_exists = cur.fetchone()[0]
if not table_exists:
    define_schema()


# Charger les données du fichier CSV dans la base de données
def load_data_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)

        # Définir le schéma si la table n'existe pas
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'ma_table')")
        table_exists = cur.fetchone()[0]
        if not table_exists:
            define_schema(headers)

        # Insérer les données dans la table
        insert_query = f"INSERT INTO ma_table ({', '.join(headers)}) VALUES ({', '.join(['%s'] * len(headers))})"
        for row in csv_reader:
            cur.execute(insert_query, row)
            conn.commit()

# Charger les données du fichier CSV dans la base de données
load_data_from_csv(csv_file_path)

# Fermer le curseur et la connexion à la base de données
cur.close()
conn.close()