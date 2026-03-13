from django.contrib.gis.db import models
from apps.accounts.models.utilisateur_model import Utilisateur

class ZonePeche(models.Model):

    TYPE_ZONE = [
        ('autorisee',    'Zone Autorisée'),
        ('interdite',    'Zone Interdite'),
        ('protegee',     'Aire Protégée'),
        ('surveillance', 'Zone de Surveillance'),
    ]

    STATUT_ZONE = [
        ('active',     'Active'),
        ('inactive',   'Inactive'),
        ('en_revision','En révision'),
    ]

    nom            = models.CharField(max_length=200)
    code           = models.CharField(max_length=50, unique=True)
    type_zone      = models.CharField(max_length=20, choices=TYPE_ZONE)
    statut         = models.CharField(max_length=20, choices=STATUT_ZONE, default='active')
    description    = models.TextField(blank=True)

    # ✅ CHAMP SPATIAL : Polygone stocké dans PostGIS
    # srid=4326 = système de coordonnées GPS standard (WGS84)
    geom           = models.PolygonField(srid=4326)

    superficie_km2 = models.FloatField(null=True, blank=True)
    profondeur_min = models.FloatField(null=True, blank=True, help_text="En mètres")
    profondeur_max = models.FloatField(null=True, blank=True, help_text="En mètres")

    cree_par       = models.ForeignKey(
                         Utilisateur,
                         on_delete=models.SET_NULL,
                         null=True,
                         related_name='zones_creees'
                     )
    valide_par     = models.ForeignKey(
                         Utilisateur,
                         on_delete=models.SET_NULL,
                         null=True, blank=True,
                         related_name='zones_validees'
                     )
    date_creation  = models.DateTimeField(auto_now_add=True)
    date_maj       = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calcul automatique de la superficie en km²
        if self.geom:
            self.superficie_km2 = round(self.geom.area * 12365.1613, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} [{self.get_type_zone_display()}]"

    class Meta:
        verbose_name = "Zone de pêche"
        verbose_name_plural = "Zones de pêche"
        ordering = ['-date_creation']
