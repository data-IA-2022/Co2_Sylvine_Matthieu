import pandas as pd
import numpy as np
import pickle

# fonction pour retourner prédiction individuelle
def makePredictionIndiv(numberofbuildings,numberoffloors,primarypropertytype,Gaz_bool, Vapeur_bool,propertygfabuilding_s):
  #mise en forme pour prédiction
  df_input = pd.DataFrame(data=[[numberofbuildings,numberoffloors,primarypropertytype,Gaz_bool, Vapeur_bool,propertygfabuilding_s]],
                      columns=["numberofbuildings","numberoffloors", "primarypropertytype","Gaz_bool", "Vapeur_bool", "propertygfabuilding_s"])
  #chargement modèle et prédiction
  loaded_model = pickle.load(open('best_model.pkl', 'rb'))
  Y_pred = loaded_model.predict(df_input)
  return(np.exp(Y_pred[0]))

# a = makePredictionIndiv(1, 12, 'Hotel', 'True', 'True', 88434)
# print("la predi pour le premier batiment, entré à la main = ", a)
# print("---------------------------------")

# fonction pour renvoyer des prédictions à partir d'un csv
def makePredictionCsv(csv_input):
  # charger le csv
  dataset = pd.read_csv(csv_input, sep =";")

  # modifier les noms de colonnes
  colNames =['osebuildingid', 'datayear', 'buildingtype', 'primarypropertytype', 'propertyname', 'address', 'city', 
          'state', 'zipcode', 'taxparcelidentificationnumber', 'councildistrictcode', 'neighborhood', 'latitude', 
          'longitude', 'yearbuilt', 'numberofbuildings', 'numberoffloors', 'propertygfatotal', 'propertygfaparking', 
          'propertygfabuilding_s', 'listofallpropertyusetypes', 'largestpropertyusetype', 'largestpropertyusetypegfa', 
          'secondlargestpropertyusetype', 'secondlargestpropertyuse', 'thirdlargestpropertyusetype', 'thirdlargestpropertyusetypegfa', 
          'yearsenergystarcertified', 'energystarscore', 'siteeui_kbtu_sf', 'siteeuiwn_kbtu_sf', 'sourceeui_kbtu_sf', 
          'sourceeuiwn_kbtu_sf', 'siteenergyuse_kbtu', 'siteenergyusewn_kbtu', 'steamuse_kbtu', 'electricity_kwh', 
          'electricity_kbtu', 'naturalgas_therms', 'naturalgas_kbtu', 'defaultdata', 'comments', 'compliancestatus', 'outlier',
          'totalghgemissions', 'ghgemissionsintensity']
  dataset.columns = colNames

  ## NETTOYAGE
  # Garder seulement quand compliant
  dataset = dataset[dataset['compliancestatus'] == 'Compliant']

  # corriger erreurs ponctuelles
  dataset['numberoffloors'] = dataset['numberoffloors'].replace(99, 1)
  dataset['numberoffloors'] = dataset['numberoffloors'].replace(0, 1)
  dataset['numberofbuildings'] = dataset['numberofbuildings'].replace(0, 1)

  ## RAJOUT DE COLONNES
  # rajouter les bool
  dataset['Gaz_bool'] = dataset['naturalgas_kbtu'].ne(0)
  dataset['Vapeur_bool'] = dataset['steamuse_kbtu'].ne(0)
 
  ## SELECTION UNIQUEMENT DES COLONNES D'INTERET POUR LE MODELE
  data = dataset[['osebuildingid', 'propertyname', 
                  "numberofbuildings","numberoffloors", "primarypropertytype","Gaz_bool", "Vapeur_bool", "propertygfabuilding_s"
                  # ,'totalghgemissions','totalghgemissions_log'
                  # ,'siteenergyuse_kbtu','siteenergyuse_kbtu_log'
                  ]]

  # drop les na sur ces colonnes
  data = data.dropna()

  # charger le pickle
  loaded_model = pickle.load(open('best_model.pkl', 'rb'))

  # déclarer le dataset de test
  X_test = data[["numberofbuildings","numberoffloors", "primarypropertytype","Gaz_bool", "Vapeur_bool", "propertygfabuilding_s"]]

  Y_pred = loaded_model.predict(X_test)
  # print("la predi pour le 1er batiment du csv: ",np.exp(Y_pred[0]))

  Y_exp = [[np.exp(x) for x in sublist] for sublist in Y_pred]
  df_exp = pd.DataFrame(Y_exp, columns=['predictedGhgEmissions', 'predictedEnergyConsumption'])

  df_combined = pd.concat([dataset, df_exp], axis=1)
  return(df_combined)

# b = makePredictionCsv("data/Template_Building_Energy_Benchmarking.csv")
# print(b)


