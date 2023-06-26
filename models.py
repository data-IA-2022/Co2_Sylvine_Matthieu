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
        best_model = grid_search.best_estimator_

# Enregistrer le meilleur modèle
with open('best_model.pkl', 'wb') as file:
    pickle.dump(best_model, file)

for result in results:
    print(f"Model: {result['model']}")
    print(f"Best parameters: {result['best_params']}")
    print(f"Best CV score: {result['best_cv_score']}")
    print(f"R2 score on test data: {result['r2_score']}")
    print(f"RMSE on test data: {result['rmse']}")
    print()

loaded_model = pickle.load(open("best_model.pkl","rb"))
loaded_model.predict(X)