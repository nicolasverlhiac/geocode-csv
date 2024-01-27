from geopy.exc import GeopyError
from geopy.geocoders import get_geocoder_for_service, GoogleV3
import pandas as pd
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

# Constants
ADDRESS_COLUMNS = ["name", "address", "postcode", "city", "country"]
INPUT_FILE = os.environ.get("INPUT_CSV", "/app/csv/input.csv")
OUTPUT_FILE = os.environ.get("OUTPUT_CSV", "/app/csv/output.csv")
CSV_DELIMITER = ";"


def load_api_keys():
    """Charge les clés d'API à partir des variables d'environnement."""
    keys = {
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "MAPBOX_API_KEY": os.getenv("MAPBOX_API_KEY"),
        "OPENCAGE_API_KEY": os.getenv("OPENCAGE_API_KEY"),
        "MAPTILER_API_KEY": os.getenv("MAPTILER_API_KEY"),
        "GEOAPIFY_API_KEY": os.getenv("GEOAPIFY_API_KEY"),
    }
    return keys


def select_geolocator(api_keys):
    """Sélectionne le fournisseur de géocodage basé sur les clés d'API disponibles."""
    providers = [
        ("Google Maps", api_keys["GOOGLE_API_KEY"], "googlev3"),
        ("MapBox", api_keys["MAPBOX_API_KEY"], "mapbox"),
        ("OpenCage", api_keys["OPENCAGE_API_KEY"], "opencage"),
        ("MapTiler", api_keys["MAPTILER_API_KEY"], "maptiler"),
        ("Geoapify", api_keys["GEOAPIFY_API_KEY"], "geoapify"),
    ]
    for provider, key, service in providers:
        if key:
            if service == "googlev3":
                return GoogleV3(api_key=key), provider
            return get_geocoder_for_service(service)(api_key=key), provider
    return None, None


def geocode_addresses(df, geolocator, provider):
    """Géocode les adresses en utilisant le géolocalisateur sélectionné."""
    if geolocator is None:
        logging.error("Aucun fournisseur de géocodage n'a été sélectionné.")
        sys.exit(1)

    for index, row in df.iterrows():
        address = " ".join(str(row[col]) for col in ADDRESS_COLUMNS)
        try:
            location = geolocator.geocode(address)
            if location:
                lat = round(location.latitude, 7)
                lng = round(location.longitude, 7)
                df.at[index, "latitude"] = lat
                df.at[index, "longitude"] = lng
                logging.info(
                    f"(Provider: {provider}) | {address} ➡️ Latitude: {lat}, Longitude: {lng}"
                )
        except GeopyError as e:
            logging.error(f"Erreur lors de la géocodage de l'adresse '{address}': {e}")


def main():
    api_keys = load_api_keys()
    geolocator, provider = select_geolocator(api_keys)

    try:
        df = pd.read_csv(INPUT_FILE, delimiter=CSV_DELIMITER)
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier {INPUT_FILE}: {e}")
        sys.exit(1)

    df["latitude"] = df.get("latitude", pd.Series(dtype=object))
    df["longitude"] = df.get("longitude", pd.Series(dtype=object))

    geocode_addresses(df, geolocator, provider)

    try:
        df.to_csv(OUTPUT_FILE, sep=CSV_DELIMITER, index=False)
        logging.info(f"Les données géocodées ont été sauvegardées dans {OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"Erreur lors de l'écriture du fichier {OUTPUT_FILE}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
