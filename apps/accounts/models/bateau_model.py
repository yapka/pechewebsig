from django.contrib.gis.db import models
from .pecheur_model import Pecheur


class Bateau(models.Model):

    TYPE_BATEAU = [
        ('pirogue',    'Pirogue'),
        ('chalutier',  'Chalutier'),
        ('sardinier',  'Sardinier'),
        ('autre',      'Autre'),
    ]

    pecheur           = models.ForeignKey(
                            Pecheur,
                            on_delete=models.CASCADE,
                            related_name='bateaux'
                        )
    nom               = models.CharField(max_length=100)
    immatriculation   = models.CharField(max_length=50, unique=True)
    type_bateau       = models.CharField(max_length=20, choices=TYPE_BATEAU)
    longueur_m        = models.FloatField(null=True, blank=True)
    capacite_tonnes   = models.FloatField(null=True, blank=True)
    annee_fabrication = models.PositiveIntegerField(null=True, blank=True)
    is_actif          = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} ({self.immatriculation})"

    class Meta:
        verbose_name = "Bateau"
        verbose_name_plural = "Bateaux"