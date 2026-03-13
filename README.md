================================================================================
  WebSIG PÊCHE — README TECHNIQUE
  Plateforme de gestion des activités de pêche en Côte d'Ivoire
================================================================================

DESCRIPTION
-----------
Application web géospatiale (WebSIG) permettant la gestion, le suivi et la
cartographie des activités de pêche maritime et continentale en Côte d'Ivoire.

Problèmes adressés :
  - Surexploitation des ressources halieutiques
  - Pêche illégale dans les zones protégées
  - Absence de cartographie dynamique des zones de pêche
  - Manque de données géospatiales pour la prise de décision

INSTALLATION
------------
  1. Cloner le dépôt
     git clone <url-du-depot>
     cd peche_sig

  2. Créer l'environnement virtuel
     python -m venv .venv
     source .venv/bin/activate          # Linux/Mac
     .venv\Scripts\activate             # Windows

  3. Installer les dépendances Python
  pip install -r requirements.txt
    Dans le  settings.py, ajouter les chemins vers les bibliothèques GDAL et GEOS :
     GDAL_LIBRARY_PATH = r'C:/Program Files/QGIS 3.28.0/bin/gdal307.dll'
     GEOS_LIBRARY_PATH = r'C:/Program Files/QGIS 3.28.0/bin/geos_c.dll'

  4. Créer la base de données PostgreSQL
     createdb peche_db
     psql peche_db -c "CREATE EXTENSION postgis;"

  5. Configurer settings.py
     Éditer config/settings.py :
       - DATABASE NAME     : peche_db
       - DATABASE USER     : <votre_user_postgres>
       - DATABASE PASSWORD : <votre_mot_de_passe>
       - DATABASE HOST     : localhost
       - DATABASE PORT     : 5432

  6. Appliquer les migrations
     python manage.py makemigrations
     python manage.py migrate

  7. Créer un superutilisateur
     python manage.py createsuperuser

  8. Lancer le serveur
     python manage.py runserver

  Accès : http://127.0.0.1:8000
  Admin : http://127.0.0.1:8000/admin/



MODÈLES DE DONNÉES
------------------
  accounts.Utilisateur      Modèle utilisateur personnalisé (rôles)
  accounts.Pecheur          Profil pêcheur (licence, commune, type)
  accounts.Bateau           Bateaux enregistrés par pêcheur

  zones.ZonePeche           Zones géospatiales (PolygonField PostGIS)

  captures.EspecePoisson    Référentiel des espèces marines
  captures.DeclarationCapture  Captures déclarées (PointField)

  alertes.Alerte            Signalements géolocalisés (PointField)

  trajets.TrajetPeche       Trajets GPS des bateaux (LineStringField)

  Champs spatiaux (PostGIS) :
    ZonePeche.geom          → PolygonField  (SRID 4326)
    DeclarationCapture.position_gps → PointField (SRID 4326)
    Alerte.position         → PointField    (SRID 4326)
    TrajetPeche.trajet      → LineStringField(SRID 4326)


RÔLES UTILISATEURS
------------------
  pecheur        Déclarer captures, voir zones, signaler alertes
  expert_sig     Analyser données, statistiques, gérer zones
  administrateur Accès complet, valider captures, gérer utilisateurs


URLs PRINCIPALES
----------------
  /                         Redirection vers dashboard
  /accounts/login/          Connexion
  /accounts/inscription/    Inscription
  /accounts/profil/         Profil utilisateur
  /zones/                   Liste des zones
  /zones/carte/             Carte interactive Leaflet
  /zones/api/geojson/       API GeoJSON (Leaflet AJAX)
  /captures/                Liste des captures
  /captures/declarer/       Formulaire de déclaration
  /captures/mes-captures/   Captures du pêcheur connecté
  /captures/valider/        Validation (admin)
  /captures/statistiques/   Statistiques et graphiques
  /alertes/                 Liste des alertes
  /alertes/signaler/        Formulaire de signalement
  /trajets/                 Liste des trajets
  /dashboard/               Tableau de bord (redirige selon rôle)
  /dashboard/pecheur/       Dashboard pêcheur
  /dashboard/expert/        Dashboard expert SIG
  /dashboard/admin/         Dashboard administrateur
  /admin/                   Interface d'administration Django