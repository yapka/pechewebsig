from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models


class Utilisateur(AbstractUser):

    ROLES = [
        ('pecheur',        'Pêcheur'),
        ('expert_sig',     'Expert SIG'),
        ('administrateur', 'Administrateur'),
    ]

    role         = models.CharField(max_length=20, choices=ROLES, default='pecheur')
    telephone    = models.CharField(max_length=20, blank=True, null=True)
    organisation = models.CharField(max_length=200, blank=True, null=True)
    photo        = models.ImageField(upload_to='photos/', blank=True, null=True)
    is_verified  = models.BooleanField(default=False)
    date_maj     = models.DateTimeField(auto_now=True)

    # Propriétés utiles dans les templates pour vérifier le rôle
    @property
    def est_pecheur(self):
        return self.role == 'pecheur'

    @property
    def est_expert(self):
        return self.role == 'expert_sig'

    @property
    def est_admin(self):
        return self.role == 'administrateur'

    def __str__(self):
        return f"{self.username} — {self.get_role_display()}"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

