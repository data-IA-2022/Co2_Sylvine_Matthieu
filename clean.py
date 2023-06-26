# make sure to install these packages before running:
import pandas as pd
from sodapy import Socrata
import utils
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import text
# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.seattle.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.seattle.gov,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("2bpz-gwpy", limit=50000)
results = client.get("2bpz-gwpy", limit=50000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

print(results_df.head())
print("shape avant cleaning: ", results_df.shape)

print(results_df.columns)

# CLEANING
# retirer les colonnes non souhaitées
results_df.drop(columns=["datayear",
                        "address",
                        "city",
                        "state",
                        "zipcode",
                        "taxparcelidentificationnumber",
                        "councildistrictcode"                    
                        ], inplace = True)

results_df["energystarscore"] = results_df["energystarscore"].replace("NULL", np.nan)

print("--------------------------------")
print(results_df["energystarscore"].unique())

# chargement db
print("chargement db")
engine = utils.get_engine()
engine = utils.get_engine()

results_df.to_sql("dataco2", engine, if_exists="replace")
results_df.to_sql("dataco2", engine, if_exists="replace")

####################
# Instructions SQL pour modifier la table a posteriori
print("modif database")
sql_statements = [
    "ALTER TABLE public.dataco2 ALTER COLUMN osebuildingid TYPE int USING osebuildingid::int;",
    "ALTER TABLE public.dataco2 ALTER COLUMN buildingtype TYPE varchar(50) USING buildingtype::varchar;",
    "ALTER TABLE public.dataco2 ALTER COLUMN primarypropertytype TYPE varchar(50) USING primarypropertytype::varchar;",
    "ALTER TABLE public.dataco2 ALTER COLUMN propertyname TYPE varchar(100) USING propertyname::varchar;",
    "ALTER TABLE public.dataco2 ALTER COLUMN neighborhood TYPE varchar(50) USING neighborhood::varchar;",
    "ALTER TABLE public.dataco2 ALTER COLUMN latitude TYPE numeric USING latitude::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN longitude TYPE numeric USING longitude::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN yearbuilt TYPE int USING yearbuilt::int;",
    "ALTER TABLE public.dataco2 ALTER COLUMN numberofbuildings TYPE int USING numberofbuildings::int;",
    "ALTER TABLE public.dataco2 ALTER COLUMN numberoffloors TYPE int USING numberoffloors::int;",
    "ALTER TABLE public.dataco2 ALTER COLUMN propertygfatotal TYPE int USING propertygfatotal::int;",
    "ALTER TABLE public.dataco2 ALTER COLUMN propertygfaparking TYPE int USING propertygfaparking::int;",
    "ALTER TABLE public.dataco2 ALTER COLUMN propertygfabuilding_s TYPE int USING propertygfabuilding_s::int;",
    "ALTER TABLE public.dataco2 ALTER COLUMN largestpropertyusetype TYPE varchar(75) USING largestpropertyusetype::varchar;",
    "ALTER TABLE public.dataco2 ALTER COLUMN largestpropertyusetypegfa TYPE varchar(75) USING largestpropertyusetypegfa::varchar;",
    "ALTER TABLE public.dataco2 ALTER COLUMN energystarscore TYPE numeric USING energystarscore::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN siteeui_kbtu_sf TYPE numeric USING siteeui_kbtu_sf::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN siteeuiwn_kbtu_sf TYPE numeric USING siteeuiwn_kbtu_sf::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN sourceeui_kbtu_sf TYPE numeric USING sourceeui_kbtu_sf::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN sourceeuiwn_kbtu_sf TYPE numeric USING sourceeuiwn_kbtu_sf::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN siteenergyuse_kbtu TYPE numeric USING siteenergyuse_kbtu::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN siteenergyusewn_kbtu TYPE numeric USING siteenergyusewn_kbtu::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN steamuse_kbtu TYPE numeric USING steamuse_kbtu::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN electricity_kwh TYPE numeric USING electricity_kwh::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN electricity_kbtu TYPE numeric USING electricity_kbtu::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN naturalgas_therms TYPE numeric USING naturalgas_therms::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN naturalgas_kbtu TYPE numeric USING naturalgas_kbtu::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN compliancestatus TYPE varchar(100) USING compliancestatus::varchar;",
    "ALTER TABLE public.dataco2 ALTER COLUMN totalghgemissions TYPE numeric USING totalghgemissions::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN ghgemissionsintensity TYPE numeric USING ghgemissionsintensity::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN secondlargestpropertyusetype TYPE varchar(100) USING secondlargestpropertyusetype::varchar;",
    "ALTER TABLE public.dataco2 ALTER COLUMN secondlargestpropertyuse TYPE numeric USING secondlargestpropertyuse::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN thirdlargestpropertyusetype TYPE varchar(100) USING thirdlargestpropertyusetype::varchar;",
    "ALTER TABLE public.dataco2 ALTER COLUMN thirdlargestpropertyusetypegfa TYPE numeric USING thirdlargestpropertyusetypegfa::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN yearsenergystarcertified TYPE numeric USING yearsenergystarcertified::numeric;",
    "ALTER TABLE public.dataco2 ALTER COLUMN outlier TYPE varchar(20) USING outlier::varchar;"
]

# Exécuter les instructions SQL
with engine.connect() as conn:
       conn.execute("ALTER TABLE public.dataco2 ALTER COLUMN osebuildingid TYPE int USING osebuildingid::int;")




print("database modifiée les champions =)")

conn.close()
