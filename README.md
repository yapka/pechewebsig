# WebSIG Pêche – Côte d’Ivoire

## Description
WebSIG Pêche CI est une plateforme de gestion, de suivi et de cartographie des activités de pêche maritime et continentale en Côte d’Ivoire.

L’objectif de l’application est de centraliser les données halieutiques afin de faciliter la gestion durable des ressources et de lutter contre la surexploitation et la pêche illégale.

L’application repose sur des technologies SIG modernes permettant de collecter, analyser et visualiser les données géographiques liées aux activités de pêche.

Technologies principales utilisées :

- Django / GeoDjango
- PostgreSQL + PostGIS
- Leaflet
- Python
- JavaScript

---

# Fonctionnalités principales

## Suivi des zones de pêche
Gestion et visualisation des zones de pêche sous forme de polygones stockés dans une base PostGIS.

## Déclaration géolocalisée des captures
Les pêcheurs peuvent enregistrer leurs captures avec leurs coordonnées GPS.

## Suivi des trajets des bateaux
Les déplacements des embarcations sont enregistrés sous forme de trajectoires (LineString).

## Système d’alertes
Détection automatique des infractions lorsque des activités sont signalées dans des zones protégées.

## Tableaux de bord statistiques
Analyse et visualisation des données halieutiques pour le suivi des ressources.

---

# Architecture du projet

Le système repose sur une architecture WebSIG classique.

Client Web  
Interface utilisateur HTML / CSS / JavaScript avec Leaflet

Serveur Web  
Django / GeoDjango pour le traitement et la gestion des données

Base de données spatiale  
PostgreSQL avec extension PostGIS

---

# Installation du projet

## 1. Cloner le dépôt

```bash
git clone git@github.com:yapka/pechewebsig.git
cd peche_sig
```

## 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

### Activation sous Linux / Mac

```bash
source .venv/bin/activate
```

### Activation sous Windows

```bash
.venv\Scripts\activate
```

---

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# Configuration SIG (Windows)

Si vous utilisez Windows, il est nécessaire de préciser les chemins des bibliothèques GDAL et GEOS dans le fichier `settings.py`.

Exemple :

```python
GDAL_LIBRARY_PATH = r'C:/Chemin/Vers/gdal.dll'
GEOS_LIBRARY_PATH = r'C:/Chemin/Vers/geos_c.dll'
```

---

# Configuration de la base de données

L'application utilise PostgreSQL avec l’extension PostGIS.

## 1. Créer la base de données

```bash
createdb peche_db
```

Activer PostGIS :

```bash
psql peche_db -c "CREATE EXTENSION postgis;"
```

---

## 2. Configuration Django

Modifier les paramètres dans :

```
config/settings.py
```

Exemple de configuration :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'peche_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 3. Initialisation du projet

Créer les migrations :

```bash
python manage.py makemigrations
```

Appliquer les migrations :

```bash
python manage.py migrate
```

Créer un compte administrateur :

```bash
python manage.py createsuperuser
```

---

# Lancer le serveur

```bash
python manage.py runserver
```

Accéder ensuite à l'application via :

```
http://127.0.0.1:8000
```

Interface d'administration :

```
http://127.0.0.1:8000/admin
```

---

# Modèles de données géospatiaux

| Modèle | Type géométrique | Description |
|------|------|------|
| ZonePeche | PolygonField (SRID 4326) | Délimitation des zones de pêche |
| DeclarationCapture | PointField (SRID 4326) | Localisation des captures |
| Alerte | PointField (SRID 4326) | Signalement d’incidents |
| TrajetPeche | LineStringField (SRID 4326) | Trajectoires GPS des bateaux |

---

# Rôles utilisateurs

PECHEUR  
Saisie des captures et consultation des zones autorisées.

EXPERT SIG  
Analyse spatiale, production cartographique et exploitation des données.

ADMINISTRATEUR  
Gestion des utilisateurs, validation des données et maintenance du système.

---

# Structure des URLs

| URL | Description |
|-----|-------------|
| /zones/carte/ | Visualisation cartographique des zones |
| /captures/declarer/ | Interface de déclaration des captures |
| /captures/statistiques/ | Analyse statistique |
| /admin/ | Interface d'administration Django |

---

# Structure simplifiée du projet

```
peche_sig/
│
├── config/
│   └── settings.py
│
├── zones/
│   └── models.py
│
├── captures/
│   └── models.py
│
├── trajets/
│   └── models.py
│
├── templates/
│
├── static/
│
├── manage.py
│
└── requirements.txt
```

---

# Perspectives d'amélioration

- Intégration d'un système de suivi GPS en temps réel des bateaux
- Ajout d'analyses spatiales avancées
- Développement d'une application mobile pour les pêcheurs
- Intégration d'images satellitaires pour la surveillance maritime
- Automatisation de la détection de pêche illégale
q
