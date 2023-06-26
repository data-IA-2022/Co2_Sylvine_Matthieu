import utils
import pandas as pd

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


print(data.shape)
## DROP LES VALEURS NON INTERESSANTE
# drop bullitt center
data = data[data['osebuildingid'] != 49784]

cols = ['buildingtype', 'primarypropertytype', 'numberofbuildings', 'numberoffloors', 'propertygfatotal', 
        'propertygfaparking', 'propertygfabuilding_s', 'largestpropertyusetype', 'largestpropertyusetypegfa', 
        'siteeui_kbtu_sf', 'siteeuiwn_kbtu_sf', 'sourceeui_kbtu_sf', 'sourceeuiwn_kbtu_sf', 'siteenergyuse_kbtu', 
        'siteenergyusewn_kbtu', 'totalghgemissions', 'ghgemissionsintensity','Gaz_bool', 'Vapeur_bool',
        'adult education', 'automobile dealership', 'bank branch', 'bar/nightclub', 'college/university', 
        'convenience store without gas station', 'courthouse', 'data center', 'distribution center', 'enclosed mall',
          'energy/power station', 'fast food restaurant', 'financial office', 'fire station', 'fitness center/health club/gym', 
          'food sales', 'food service', 'hospital', 'hotel', 'k-12 school', 'laboratory', 'library', 'lifestyle center', 
          'manufacturing/industrial plant', 'medical office', 'movie theater', 'multifamily housing', 'museum', 
          'non-refrigerated warehouse', 'office', 'other', 'other - education', 'other - entertainment/public assembly', 
          'other - lodging/residential', 'other - mall', 'other - public services', 'other - recreation', 'other - restaurant/bar', 
          'other - services', 'other - technology/science', 'other - utility', 'other/specialty hospital', 
          'outpatient rehabilitation/physical therapy', 'parking', 'performing arts', 'personal services', 
          'police station', 'pre-school/daycare', 'prison/incarceration', 'refrigerated warehouse', 
          'repair services', 'residence hall/dormitory', 'residential care facility', 'restaurant', 'retail store', 
          'self-storage facility', 'senior care community', 'single family home', 'social/meeting hall', 'strip mall', 
          'supermarket/grocery store', 'swimming pool', 'urgent care/clinic/other outpatient', 'vocational school', 
          'wholesale club/supercenter', 'worship facility', 'adult education_gfa', 'automobile dealership_gfa', 
          'bank branch_gfa', 'bar/nightclub_gfa', 'college/university_gfa', 'convenience store without gas station_gfa', 
          'courthouse_gfa', 'data center_gfa', 'distribution center_gfa', 'enclosed mall_gfa', 'energy/power station_gfa', 
          'fast food restaurant_gfa', 'financial office_gfa', 'fire station_gfa', 'fitness center/health club/gym_gfa', 
          'food sales_gfa', 'food service_gfa', 'hospital_gfa', 'hotel_gfa', 'k-12 school_gfa', 'laboratory_gfa', 'library_gfa', 
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
          'urgent care/clinic/other outpatient_gfa', 'vocational school_gfa', 'wholesale club/supercenter_gfa', 
          'worship facility_gfa', 'nombre_utilisation_differente']


data = data[cols]

# data.drop(['osebuildingid', 'propertyname', 'neighborhood', 'latitude', 'longitude', 'yearbuilt', 
#            'listofallpropertyusetypes', 'largestpropertyusetypegfa', 'Electricite_bool',
#            'propertygfatotal_log',  'propertygfaparking_log', 'propertygfabuilding_s_log', 
#            'largestpropertyusetypegfa_log', 'siteeuiwn_kbtu_sf_log', 'ghgemissionsintensity_log'], 
#            axis=1, inplace = True)
print(data.shape)


## écrire dans BDD
# Importez votre DataFrame dans la base de données
data.to_sql('azure', con=engine, if_exists='replace', index=False)