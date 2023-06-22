import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import r2_score

# charger le csv
dataset = pd.read_csv("data/2017_Building_Energy_Benchmarking.csv")

# modifier les noms de colonnes
# print(dataset.columns.to_list())
colNames =['osebuildingid', 'datayear', 'buildingtype', 'primarypropertytype', 'propertyname', 'address', 'city', 
           'state', 'zipcode', 'taxparcelidentificationnumber', 'councildistrictcode', 'neighborhood', 'latitude', 
           'longitude', 'yearbuilt', 'numberofbuildings', 'numberoffloors', 'propertygfatotal', 'propertygfaparking', 
           'propertygfabuilding_s', 'listofallpropertyusetypes', 'largestpropertyusetype', 'largestpropertyusetypegfa', 
           'secondlargestpropertyusetype', 'secondlargestpropertyuse', 'thirdlargestpropertyusetype', 'thirdlargestpropertyusetypegfa', 
           'yearsenergystarcertified', 'energystarscore', 'siteeui_kbtu_sf', 'siteeuiwn_kbtu_sf', 'sourceeui_kbtu_sf', 
           'sourceeuiwn_kbtu_sf', 'siteenergyuse_kbtu', 'siteenergyusewn_kbtu', 'steamuse_kbtu', 'electricity_kwh', 
           'electricity_kbtu', 'naturalgas_therms', 'naturalgas_kbtu','totalghgemissions', 'ghgemissionsintensity',
           'defaultdata', 'compliancestatus','outlier']

dataset.columns = colNames

## NETTOYAGE
# Garder seulement quand compliant
dataset = dataset[dataset['compliancestatus'] == 'Compliant']

# enlever les cas où les targets sont de 0
dataset = dataset[dataset['siteenergyuse_kbtu'] > 0.0] 
dataset = dataset[dataset['totalghgemissions'] > 0.0] 

# virer ose 49967 université outlier
dataset = dataset[dataset['osebuildingid'] != 49967]
# drop la ligne avec le bullit center si on prend en log
dataset = dataset[dataset['osebuildingid'] != 49784]

# corriger erreurs ponctuelles
dataset['numberoffloors'] = dataset['numberoffloors'].replace(99, 1)
dataset['numberoffloors'] = dataset['numberoffloors'].replace(0, 1)
dataset['numberofbuildings'] = dataset['numberofbuildings'].replace(0, 1)

# # nettoyage sur quartiers
# dataset.loc[dataset['propertyname'] == "Chief Seattle Club/Monterey Lofts" , 'neighborhood'] = 'downtown'
# dataset.loc[dataset['propertyname'] == "INScape" , 'neighborhood'] = 'greater duwamish'
# dataset.loc[dataset['propertyname'] == "High Point Community Center" , 'neighborhood'] = 'delridge'
# # capitaliser neighborhhod pour homogénéité
# dataset['neighborhood'] = dataset['neighborhood'].str.upper()

# Eventuellement d'autres tris 

## RAJOUT DE COLONNES
# rajouter les bool
dataset['Gaz_bool'] = dataset['naturalgas_kbtu'].ne(0)
dataset['Vapeur_bool'] = dataset['steamuse_kbtu'].ne(0)

# rajout log des deux targets "brutes"
dataset['siteenergyuse_kbtu_log'] = np.log(dataset['siteenergyuse_kbtu'])
dataset['totalghgemissions_log'] = np.log(dataset['totalghgemissions'])

# + faire le countvect? si nécessaire

## SELECTION UNIQUEMENT DES COLONNES D'INTERET POUR LE MODELE
data = dataset[['primarypropertytype',"largestpropertyusetype", "Gaz_bool", "Vapeur_bool",'totalghgemissions_log']]

# drop les na sur ces colonnes
data = data.dropna()

## EVALUATION DU MODELE
# charger le pickle
loaded_model = pickle.load(open('model_totalghglog.sav', 'rb'))

# déclarer les jeux x et y
X_test = data[['primarypropertytype',"largestpropertyusetype", "Gaz_bool", "Vapeur_bool"]]
Y_test = data['totalghgemissions_log']

# Prédire les valeurs sur l'ensemble de test
Y_pred = loaded_model.predict(X_test)

# Calculer le coefficient de détermination (R2 score)
r2 = r2_score(Y_test, Y_pred)

print("r2 score calculé a la mano", r2)