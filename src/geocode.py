import os
import googlemaps
import pandas as pd

# Récupérer les clés d'API Google Maps à partir de votre compte Google Cloud Console
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API_KEY'))

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



# Parcourir les lignes du DataFrame et utiliser Google Maps pour récupérer la latitude et la longitude
for index, row in df.iterrows():
    address = ' '.join(str(row[col]) for col in address_columns)
    geocode_result = gmaps.geocode(address)

    if len(geocode_result) > 0:
        location = geocode_result[0]['geometry']['location']
        lat = round(location['lat'], 13)
        lng = round(location['lng'], 13)
        df.at[index, 'latitude'] = str(lat)[:13]
        df.at[index, 'longitude'] = str(lng)[:13]

        print(f"{address} ➡️ Latitude: {lat}, Longitude: {lng}")

# Sauvegarder les modifications dans votre fichier CSV
df.to_csv(output_file, sep=';', index=False)
