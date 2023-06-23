import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score, mean_squared_error

# Charger les données (supposons qu'elles soient dans un DataFrame pandas)
data = pd.read_csv('dataset_prepared2.csv')

data = data[data["osebuildingid"] != 49784]

data["totalghgemissions_log"] = np.log(data['totalghgemissions'])
data ["siteenergyuse_kbtu_log"] = np.log(data['siteenergyuse_kbtu'])

listOfAllUses = ['adult education', 'automobile dealership', 'bank branch', 'bar/nightclub', 'college/university', 
                 'convenience store without gas station', 'courthouse', 'data center', 'distribution center', 
                 'enclosed mall', 'energy/power station', 'fast food restaurant', 'financial office', 'fire station', 
                 'fitness center/health club/gym', 'food sales', 'food service', 'hospital', 'hotel', 'k-12 school', 'laboratory', 
                 'library', 'lifestyle center', 'manufacturing/industrial plant', 'medical office', 'movie theater', 'multifamily housing', 
                 'museum', 'non-refrigerated warehouse', 'office', 'other', 'other - education', 'other - entertainment/public assembly', 
                 'other - lodging/residential', 'other - mall', 'other - public services', 'other - recreation', 'other - restaurant/bar', 
                 'other - services', 'other - technology/science', 'other - utility', 'other/specialty hospital', 
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
X = data[[ "numberofbuildings","numberoffloors", "primarypropertytype",
                "Gaz_bool", "Vapeur_bool", "propertygfabuilding_s"]]



y = data[['totalghgemissions_log', 'siteenergyuse_kbtu_log']]

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Extraire les colonnes numériques et catégorielles
numeric_features = X.select_dtypes(exclude=[object, bool])
categorical_features =  X.select_dtypes(include=[object, bool])



# Créer le préprocesseur de colonnes
preprocessor = ColumnTransformer(transformers=[
    ('cat', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), categorical_features.columns),
    ('num', StandardScaler(), numeric_features.columns),
])

# Définir les modèles à tester avec leurs paramètres
models = [
    {
        'estimator': RandomForestRegressor(),
        'params': {
            'estimator__estimator__n_estimators': [100, 200, 500],
            'estimator__estimator__max_depth': [None, 5, 10]
        }
    },
    {
        'estimator': GradientBoostingRegressor(),
        'params': {
            'estimator__estimator__n_estimators': [100, 200, 500],
            'estimator__estimator__max_depth': [3, 5, 10]
        }
    },
    {
        'estimator': LinearRegression(),
        'params': {}
    },
    {
        'estimator': SVR(),
        'params': {
            'estimator__estimator__C': [0.1, 1, 10],
            'estimator__estimator__kernel': ['linear', 'rbf']
        }
    },
    {
        'estimator': ExtraTreesRegressor(),
        'params': {
            'estimator__estimator__n_estimators': [100, 200, 500],
            'estimator__estimator__max_depth': [None, 5, 10]
        }
    }
]

import pickle

results = []
best_score = float('-inf')
best_model = None

# Parcourir chaque modèle et effectuer la recherche de grille
for model_info in models:
    estimator = model_info['estimator']
    param_grid = model_info['params']

    # Créer le modèle MultiOutputRegressor avec l'estimateur approprié
    model = MultiOutputRegressor(estimator)

    # Créer la pipeline complète
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('estimator', model)
    ])

    # Effectuer la recherche de grille
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='r2')
    grid_search.fit(X_train, y_train)

    # Prédire les valeurs sur l'ensemble de test
    y_pred = grid_search.predict(X_test)

    # Calculer le coefficient de détermination (R2 score)
    r2 = r2_score(y_test, y_pred)

    # Calculer la racine carrée de l'erreur quadratique moyenne (RMSE)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # Enregistrer les résultats
    result = {
        'model': estimator.__class__.__name__,
        'best_params': grid_search.best_params_,
        'best_cv_score': grid_search.best_score_,
        'r2_score': r2,
        'rmse': rmse
    }
    results.append(result)

    # Mettre à jour le meilleur score et le meilleur modèle si nécessaire
    if grid_search.best_score_ > best_score:
        best_score = grid_search.best_score_
        best_model = pipeline

# Enregistrer le meilleur modèle
with open('modelv1.pkl', 'wb') as file:
    pickle.dump(best_model, file)

# Afficher les résultats
for result in results:
    print(f"Model: {result['model']}")
    print(f"Best parameters: {result['best_params']}")
    print(f"Best CV score: {result['best_cv_score']}")
    print(f"R2 score on test data: {result['r2_score']}")
    print(f"RMSE on test data: {result['rmse']}")
    print()
