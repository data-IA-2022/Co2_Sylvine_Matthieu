import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score
import utils
import pickle

## CHARGEMENT DATA DEPUIS BDD
# création connexion
print("Creation connexion ...")
engine = utils.get_engine()

# Spécifier le nom de la table que vous souhaitez exporter
table_name = '"dataco2cv"'

# Exécuter une requête SQL pour sélectionner les données de la table
query = f"SELECT * FROM {table_name}"

# Lire les résultats de la requête dans un DataFrame pandas
print("Récupération table depuis la BDD ...")
data = pd.read_sql_query(query, engine)

## CHARGEMENT DATA DEPUIS CSV LOCAL
# # Charger les données (supposons qu'elles soient dans un DataFrame pandas)
# data = pd.read_csv('dataset_prepared2.csv')

## PREPROCESSING
print("Préprocessing en cours ...")
# drop la ligne avec le bullit center si on prend en log
data = data[data['osebuildingid'] != 49784]
print(data.shape)
# nettoyage d'autres outliers au cas où
data = data[data['siteeuiwn_kbtu_sf'] < 600] # retire 5
print(data.shape)

data = data[data['buildingtype'] != 'Nonresidential WA']
print(data.shape)


# rajout log des deux targets "brutes"
data['siteenergyuse_kbtu_log'] = np.log(data['siteenergyuse_kbtu'])
data['totalghgemissions_log'] = np.log(data['totalghgemissions'])

# Listes de features pour réutilisation
listOfAllUses = ['adult education', 'automobile dealership', 'bank branch', 'bar/nightclub', 'college/university', 
                 'convenience store without gas station', 'courthouse', 'data center', 'distribution center', 
                 'enclosed mall', 'energy/power station', 'fast food restaurant', 'financial office', 'fire station', 
                 'fitness center/health club/gym', 'food sales', 'food service', 'hospital', 'hotel', 'k-12 school', 'laboratory', 
                 'library', 'lifestyle center', 'manufacturing/industrial plant', 'medical office', 'movie theater', 'multifamily housing', 
                 'museum', 'non-refrigerated warehouse', 'office', 'other', 'other - education', 'other - entertainment/public assembly', 
                 'other - lodging/residential', 'other - mall', 'other - public services', 'other - recreation', 'other - restaurant/bar', 
                 'ot/home/sylvine/Documents/Projets/Projet9_CO2/azureml_AutoML_4c588bca-a6ed-458a-afb2-58a8e9cd1c89_40_output_mlflow_log_model_1310009553 (1)/model.pklher - services', 'other - technology/science', 'other - utility', 'other/specialty hospital', 
                 'outpatient rehabilitation/physical therapy', 'parking', 'performing arts', 'personal services', 'police station', 
                 'pre-school/daycare', 'prison/incarceration', 'refrigerated warehouse', 'repair services', 'residence hall/dormitory', 
                 'residential care facility', 'restaurant', 'retail store', 'self-storage facility', 'senior care community', 
                 'single family home', 'social/meeting hall', 'strip mall', 'supermarket/grocery store', 'swimming pool', 
                 'urgent care/clinic/other outpatient', 'vocational school', 'wholesale club/supercenter', 'worship facility']

listOfAllUsesGfa = ['adult education_gfa', 'automobile dealership_gfa', 'bank branch_gfa', 'bar/nightclub_gfa', 
                    'college/university_gfa', 'convenience store without gas station_gfa', 'courthouse_gfa', 'data center_gfa', 
                    'distribution center_gfa', 'enclosed mall_gfa', 'energy/power station_gfa', 'fast food restaurant_gfa', 
                    'financial office_gfa', 'fire station_gfa', 'fitness center/health club/gym_gfa', 'food sales_gfa', 
                    'food service_gfa', 'hospital_gfa', 'hotel_gfa', 'k-12 school_gfa', 'laboratory_gfa', 'library_gfa', 
                    'lifestyle center_gfa', 'manufacturing/industrial plant_gfa', 'medical office_gfa', 'movie theater_gfa', 
                    'multifamily housing_gfa', 'museum_gfa', 'non-refrigerated warehouse_gfa', 'office_gfa', 'other_gfa', 
                    'other - education_gfa', 'other - entertainment/public assembly_gfa', 'other - lodging/residential_gfa', 
                    'other - mall_gfa', 'other - public services_gfa', 'other - recreation_gfa', 'other - restaurant/bar_gfa', 
                    'other - services_gfa', 'other - technology/science_gfa', 'other - utility_gfa', 'other/specialty hospital_gfa', 
                    'outpatient rehabilitation/physical therapy_gfa', 'parking_gfa', 'performing arts_gfa', 'personal services_gfa', 
                    'police station_gfa', 'pre-school/daycare_gfa', 'prison/incarceration_gfa', 'refrigerated warehouse_gfa', 
                    'repair services_gfa', 'residence hall/dormitory_gfa', 'residential care facility_gfa', 'restaurant_gfa', 
                    'retail store_gfa', 'self-storage facility_gfa', 'senior care community_gfa', 'single family home_gfa', 
                    'social/meeting hall_gfa', 'strip mall_gfa', 'supermarket/grocery store_gfa', 'swimming pool_gfa', 
                    'urgent care/clinic/other outpatient_gfa', 'vocational school_gfa', 'wholesale club/supercenter_gfa', 'worship facility_gfa']

# Séparer les caractéristiques (features) et la variable cible
# X = data.drop(['ghgemissionsintensity', 'siteeuiwn_kbtu_sf','osebuildingid','propertyname',
#        'neighborhood', 'latitude', 'longitude', 'yearbuilt','propertygfatotal', 'listofallpropertyusetypes', 'largestpropertyusetypegfa',
#        'secondlargestpropertyuse', 'secondlargestpropertyusetype', 'thirdlargestpropertyusetype', 'largestpropertyusetypegfa_log',
#        'thirdlargestpropertyusetypegfa', 'energystarscore', 'siteeui_kbtu_sf', 'sourceeui_kbtu_sf', 'secondlargestpropertyuse_log',
#        'sourceeuiwn_kbtu_sf', 'siteenergyuse_kbtu', 'siteenergyusewn_kbtu', 'certif2016', 'propertygfabuilding_s_log',
#        'steamuse_kbtu','electricity_kbtu', 'naturalgas_kbtu', 'propertygfatotal_log','propertygfaparking_log',
#        'totalghgemissions', 'yearsenergystarcertified', 'geopoint','Electricite_bool','thirdlargestpropertyusetypegfa_log','steamuse_kbtu_log',
#        'electricity_kbtu_log','naturalgas_kbtu_log', 'siteeuiwn_kbtu_sf_log', 'ghgemissionsintensity_log'], axis=1)

X = data[['primarypropertytype',"largestpropertyusetype", "Gaz_bool", "Vapeur_bool"]]
# y = data[['ghgemissionsintensity_log', 'siteeuiwn_kbtu_sf_log']]
# y = data['ghgemissionsintensity_log']
y = data['totalghgemissions_log']

print(X.columns)
print(X.shape)
# quit()

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Extraire les colonnes numériques et catégorielles
# numeric_features = X.select_dtypes(include=[int, float]).columns.tolist()
# categorical_features = X.select_dtypes(include=[object]).columns.tolist()
# numeric_features = ["propertygfabuilding_s","numberoffloors"] + listOfAllUsesGfa
categorical_features = ["primarypropertytype", "largestpropertyusetype"]

# Créer les transformateurs pour les données numériques et catégorielles
numeric_transformer = RobustScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Créer le préprocesseur de colonnes
preprocessor = ColumnTransformer(
    transformers=[
        # ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# CREATION DU MODELE
print("Creation du modèle en cours ...")
# Créer le modèle RandomForest multi-target
# base_estimator = RandomForestRegressor()
# model = MultiOutputRegressor(base_estimator)
model = GradientBoostingRegressor()


# Définir les paramètres de la grille de recherche pour le modèle
# param_grid = {
#     'estimator__estimator__n_estimators': [100, 500],
#     'estimator__estimator__max_depth': [None, 5, 10]
# }
param_grid = {
    'estimator__n_estimators': [100, 300, 500],
    'estimator__max_depth': [None, 5, 10, 15]
}


# Créer la pipeline complète
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('estimator', model)
])


# ENTRAINEMENT
# Effectuer la recherche de grille
print("gridsearch en cours ...")
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='r2')
grid_search.fit(X_train, y_train)

# EVALUATION DU MODELE
print("Evaluation en cours ...")
# Prédire les valeurs sur l'ensemble de test
y_pred = grid_search.predict(X_test)

# Calculer le coefficient de détermination (R2 score)
r2 = r2_score(y_test, y_pred)

# Afficher les résultats
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV score: {grid_search.best_score_}")
print(f"R2 score on test data: {r2}")


filename = 'model_totalghglog.sav'
# pickle.dump(grid_search.best_estimator_, open(filename, 'wb'))