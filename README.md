# Geocode CSV using Multiple Geocoding Providers

This repository provides a geocoding solution for CSV files containing contact addresses using multiple geocoding providers. Geocoding is the process of converting addresses into geographic coordinates (latitude and longitude), enabling businesses and data analysts to leverage location-based information in their applications and analyses.

The geocoding script is encapsulated in a Docker image, making it easy to deploy and use. The script supports the following geocoding providers:

- Google Maps
- MapBox
- OpenCage
- MapTiler
- Geoapify

## Features

- Geocodes CSV files with contact addresses using the specified geocoding provider
- Retrieves latitude and longitude information for each address
- Adds latitude and longitude to a new column in the CSV file
- Flexible configuration to choose the geocoding provider based on the API key provided
- Useful for businesses and data analysts working with address data


## Usage

You can use the geocoding solution by directly pulling the Docker image from Docker Hub or by building the image from the source code. 

_**Note:** Make sure you have Docker installed and running on your system before executing the docker command._

For detailed instructions on building and running the Docker image, please refer to the project documentation.


### 🐳 Using Docker Hub:

1. Pull the [Docker image from Docker Hub](https://hub.docker.com/r/nicolasverlhiac/geocode-csv):

```bash
docker pull nicolasverlhiac/geocode-csv
```

2. Create a `data` directory and place your input CSV file in the `data` directory.

	* **You need to name the CSV file `input.csv`.**
    * You can use the provided `sample-input.csv` file as a base by duplicating it and renaming the duplicate to `input.csv`. This file already has the required CSV structure and serves as a template for your own data.

3. Set the environment variables: Depending on the geocoding provider you want to use, set the corresponding API key as an environment variable. The supported environment variables are:
   - `GOOGLE_API_KEY` for Google Maps API key
   - `MAPBOX_API_KEY` for MapBox API key
   - `OPENCAGE_API_KEY` for OpenCage API key
   - `MAPTILER_API_KEY` for MapTiler API key
   - `GEOAPIFY_API_KEY` for Geoapify API key

4. Execute the Docker container with the selected environment variable:

```bash
docker run --rm -v "$(pwd)/data:/app/csv" -e GOOGLE_API_KEY=your_key nicolasverlhiac/geocode-csv
```
5. After the execution completes, you will find the geocoded CSV `ouput.csv` file with latitude and longitude information in the csv directory.

### 🔧 Build image

1. Build the Docker image:
```bash
docker build -t nicolasverlhiac/geocode-csv .
```

This command builds the Docker image using the Dockerfile in the current directory. The -t flag allows you to specify a tag or name for the image. In this example, the image is tagged as nicolasverlhiac/geocode-csv.

1. Once the image is built, you can use it in the same way as described in the "Using Docker Hub" section. **Follow steps 2 to 5** mentioned in the "[Using Docker Hub](#-using-docker-hub)" section to geocode your CSV file.

By building the image locally, you have more control over the image and can make modifications if needed. Additionally, building the image locally ensures that you have the latest version of the code and dependencies.

### Required CSV fields (`input.csv` CSV example)

Example of a CSV file to be placed in the `data/input.csv` folder before executing the Docker command.

You can use the provided `sample-input.csv` file located in `/data` as a base by duplicating it and renaming the duplicate to `input.csv`. This file already has the required CSV structure and serves as a template for your own data.

| name                | address                     | postcode | state | city                 | country | latitude | longitude |
|---------------------|-----------------------------|----------|-------|----------------------|---------|----------|-----------|
| CAVE ARDONEO        | 768 Avenue du Président JFK | 40280    |       | SAINT PIERRE DU MONT | France  |          |           |
| LA CAVE             | 87 Route de Montpellier     | 34110    |       | FRONTIGNAN           | France  |          |           |
| ETS BRIAU           | 94 Rue David Johnston       | 33000    |       | BORDEAUX             | France  |          |           |

## Requirements
* Docker
* Geocoding providers API KEY

## Supported Architectures
This geocoding solution supports the following architectures:

- linux/386
- linux/amd64
- linux/arm/v5
- linux/arm/v7
- linux/arm64/v8
- linux/mips64le
- linux/ppc64le
- linux/s390x

Whether you're running on a traditional x86 architecture or ARM-based devices, you can leverage this geocoding solution for your CSV files.

## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the  [MIT License](https://opensource.org/license/mit/) .

## Acknowledgements
This geocoding solution is built upon the geocoding providers API. Special thanks to the contributors of the [Geopy](https://github.com/geopy/geopy) library.

## References
*  [Geopy Documentation](https://geopy.readthedocs.io/en/stable/) 
*  [Geopy](https://github.com/geopy/geopy) 