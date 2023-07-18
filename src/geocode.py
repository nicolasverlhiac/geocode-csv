import os
import geopy.geocoders
import pandas as pd

# Récupérer les clés d'API des différents fournisseurs à partir de variables d'environnement
google_api_key = os.getenv('GOOGLE_API_KEY')
mapbox_api_key = os.getenv('MAPBOX_API_KEY')
opencage_api_key = os.getenv('OPENCAGE_API_KEY')
maptiler_api_key = os.getenv('MAPTILER_API_KEY')
geoapify_api_key = os.getenv('GEOAPIFY_API_KEY')

# Liste des fournisseurs de géocodage à utiliser
providers = [
    ('Google Maps', google_api_key, 'googlev3'),
    ('MapBox', mapbox_api_key, 'mapbox'),
    ('OpenCage', opencage_api_key, 'opencage'),
    ('MapTiler', maptiler_api_key, 'maptiler'),
    ('Geoapify', geoapify_api_key, 'geoapify')
]

# Parcourir les fournisseurs de géocodage et configurer le fournisseur avec la clé d'API correspondante
geolocator = None
selected_provider = None
for provider, provider_key, provider_name in providers:
    if provider_key:
        if provider_name == 'googlev3':
            geolocator = geopy.geocoders.GoogleV3(api_key=provider_key)
        else:
            geolocator = geopy.geocoders.get_geocoder_for_service(provider_name)(api_key=provider_key)
        selected_provider = provider
        break

# Vérifier si un fournisseur de géocodage valide a été sélectionné
if selected_provider is None:
    print("Aucun fournisseur de géocodage valide n'a été sélectionné.")
    exit()

# Définir les colonnes du DataFrame contenant les adresses
address_columns = ['name', 'address', 'postcode', 'city', 'country']

# Charger votre fichier CSV en tant que DataFrame
input_file = '/app/csv/input.csv'
output_file = '/app/csv/output.csv'

# Charger votre fichier CSV en tant que DataFrame
df = pd.read_csv(input_file, delimiter=';')

# Ajouter les colonnes 'latitude' et 'longitude' au DataFrame si elles n'existent pas
if 'latitude' not in df.columns:
    df['latitude'] = None
if 'longitude' not in df.columns:
    df['longitude'] = None

# Parcourir les lignes du DataFrame et utiliser le fournisseur de géocodage sélectionné pour récupérer la latitude et la longitude
for index, row in df.iterrows():
    address = ' '.join(str(row[col]) for col in address_columns)
    location = geolocator.geocode(address)

    if location is not None:
        lat = round(location.latitude, 13)
        lng = round(location.longitude, 13)
        df.at[index, 'latitude'] = str(lat)[:13]
        df.at[index, 'longitude'] = str(lng)[:13]

        print(f"{address} ➡️ Latitude: {lat}, Longitude: {lng} (Provider: {selected_provider})")

# Sauvegarder les modifications dans votre fichier CSV
df.to_csv(output_file, sep=';', index=False)
