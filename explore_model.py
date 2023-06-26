import pickle
import numpy as np
import pandas as pd
import plotly.express as px

# load modele
loaded_model = pickle.load(open('best_model.pkl', 'rb'))
truc = loaded_model.named_steps['estimator']

print(truc)
truc.estimators_[0]
truc.estimators_[1]

# Get Feature importance data using feature_importances_ attribute
GHG = truc.estimators_[0] # récup du modele sur les ghg
energy = truc.estimators_[1] # recup du modele sur la consommation
feature_names = loaded_model.named_steps['preprocessor'].get_feature_names_out()  # récupération des feature names

def plot_feature_importance(modele):
  if modele == GHG:
    titre = "GHG"
  else :
    titre = "energy consumption"
  feature_importance = pd.Series({feature_names[i] : modele.feature_importances_[i] for i in range(len(modele.feature_importances_))})

  df_feat_imp = pd.DataFrame.from_dict(feature_importance.sort_values(ascending=False))

  fig = px.histogram(df_feat_imp, x=df_feat_imp.index, y=0, title=titre)
  fig.show()

plot_feature_importance(GHG)
plot_feature_importance(energy)