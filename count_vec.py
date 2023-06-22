import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import CountVectorizer
import utils

# # Définir les informations de connexion à la base de données
# db_user = 'adminCO2'
# db_password = 'Seattle-2023'
# db_host = 'serveur-co2-sylvine-matthieu.postgres.database.azure.com'
# db_port = '5432'  # Remplacez-le par le port approprié
# db_name = 'BDDCO2'

# # Créer l'URL de connexion à la base de données
# db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# # Créer une connexion à la base de données
# engine = create_engine(db_url)

# création connexion
engine = utils.get_engine()

# Spécifier le nom de la table que vous souhaitez exporter
# table_name = '"CO2_dataco2_prepared"'
table_name = '"CO2_dataco2_prepared2"'

# Exécuter une requête SQL pour sélectionner les données de la table
query = f"SELECT * FROM {table_name}"

# Lire les résultats de la requête dans un DataFrame pandas
df = pd.read_sql_query(query, engine)



# countvectorizer pour avoir une col par usetype
df.dropna(subset=['listofallpropertyusetypes'], inplace=True)
df.reset_index(drop=True, inplace=True)
df['listofallpropertyusetypes'] = df['listofallpropertyusetypes'].str.replace(r'\s*\([^)]*\)', '', regex=True)
df['largestpropertyusetype'] = df['largestpropertyusetype'].str.replace(r'\s*\([^)]*\)', '', regex=True)
df['secondlargestpropertyusetype'] = df['secondlargestpropertyusetype'].str.replace(r'\s*\([^)]*\)', '', regex=True)
df['thirdlargestpropertyusetype'] = df['thirdlargestpropertyusetype'].str.replace(r'\s*\([^)]*\)', '', regex=True)

vectorizer = CountVectorizer(tokenizer=lambda x: x.split(', '))
count_matrix = vectorizer.fit_transform(df['listofallpropertyusetypes'])
encoded_df = pd.DataFrame(count_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# Concaténation du DataFrame encodé avec le DataFrame d'origine
df = pd.concat([df, encoded_df], axis=1)

## creer la liste des noms pour les nouvelles colonnes 
noms = vectorizer.get_feature_names_out()

##Début de création du df 

#Création de nouveau nom de colonnes
noms_gfa = []
for i in noms:
  j = i+"_gfa"
  noms_gfa.append(j)
colonnes_a_dupliquer = noms
nouveaux_noms_colonnes = noms_gfa
for colonne, nouveau_nom in zip(colonnes_a_dupliquer, nouveaux_noms_colonnes):
    df[nouveau_nom] = df[colonne].copy()
  
#multiplication du nombre dans la colonne 

df['largestpropertyusetype'] = df['largestpropertyusetype'].str.lower()
df['secondlargestpropertyusetype'] = df['secondlargestpropertyusetype'].str.lower()
df['thirdlargestpropertyusetype'] = df['thirdlargestpropertyusetype'].str.lower()

for colonne in noms_gfa:
    for index, row in df.iterrows():
        if row['secondlargestpropertyusetype'] is not None:
            if row['largestpropertyusetype'] + "_gfa" == colonne:
                df.loc[index, colonne] *= row['largestpropertyusetypegfa']
        if row['secondlargestpropertyusetype'] is not None:
            if row['secondlargestpropertyusetype'] + "_gfa"   == colonne:
                df.loc[index, colonne] *= row['secondlargestpropertyuse']
        if row['thirdlargestpropertyusetype'] is not None:       
            if row['thirdlargestpropertyusetype'] + "_gfa" == colonne:
                df.loc[index, colonne] *= row['thirdlargestpropertyusetypegfa']


df[noms_gfa] = df[noms_gfa].applymap(lambda x: 0 if x == 1 else x)
df['nombre_utilisation_differente'] = df[noms].apply(lambda row: row.astype(str).str.count('1').sum(), axis=1)
table_name = 'dataco2cv'

df = df[(df['osebuildingid'] != 496) & (df['osebuildingid'] != 27966)]

for index, row in df.iterrows():
    if pd.isnull(row["largestpropertyusetype"]) or row["largestpropertyusetype"] == "null":
        df.at[index, "largestpropertyusetype"] = row["listofallpropertyusetypes"]
        df.at[index, "largestpropertyusetypegfa"] = row["propertygfatotal"]
        

# for cellule in df['listofallpropertyusetypes']:
#     nombre_de_use = cellule.count(',') + 1
    

# Importez votre DataFrame dans la base de données
df.to_sql(table_name, con=engine, if_exists='replace', index=False)
df.to_csv('dataset_prepared2.csv', index=False)
