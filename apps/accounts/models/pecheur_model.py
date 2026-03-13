from django.contrib.gis.db import models
from .utilisateur_model import Utilisateur




class Pecheur(models.Model):

    TYPE_PECHE = [
        ('artisanale',   'Artisanale'),
        ('industrielle', 'Industrielle'),
        ('continentale', 'Continentale'),
        ('maritime',     'Maritime'),
    ]

    utilisateur      = models.OneToOneField(
                           Utilisateur,
                           on_delete=models.CASCADE,
                           related_name='profil_pecheur'
                       )
    numero_licence   = models.CharField(max_length=50, unique=True)
    date_naissance   = models.DateField(null=True, blank=True)
    commune          = models.CharField(max_length=100)
    type_peche       = models.CharField(max_length=20, choices=TYPE_PECHE)
    experience_annee = models.PositiveIntegerField(default=0)
    is_actif         = models.BooleanField(default=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pêcheur : {self.utilisateur.get_full_name()} [{self.numero_licence}]"

    class Meta:
        verbose_name = "Pêcheur"
        verbose_name_plural = "Pêcheurs"
