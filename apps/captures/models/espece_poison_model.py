from django.contrib.gis.db import models


class EspecePoisson(models.Model):

    CATEGORIE = [
        ('pelagique',  'Pélagique'),
        ('demersal',   'Démersal'),
        ('crustace',   'Crustacé'),
        ('mollusque',  'Mollusque'),
    ]

    nom_commun    = models.CharField(max_length=100)
    nom_latin     = models.CharField(max_length=150, blank=True)
    categorie     = models.CharField(max_length=20, choices=CATEGORIE)
    taille_min_cm = models.FloatField(
                        null=True, blank=True,
                        help_text="Taille légale minimale de capture en cm"
                    )
    poids_min_kg  = models.FloatField(null=True, blank=True)
    is_protege    = models.BooleanField(default=False)
    description   = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nom_commun} ({self.nom_latin})"

    class Meta:
        verbose_name = "Espèce de poisson"
        verbose_name_plural = "Espèces de poissons"
