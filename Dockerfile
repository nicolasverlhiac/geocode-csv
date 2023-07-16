# Utiliser une image de base contenant Python
FROM --platform=$BUILDPLATFORM python:slim-bookworm 

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requis dans le conteneur
COPY ./src /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exécuter le script Python lors du lancement du conteneur
CMD ["python", "geocode.py"]