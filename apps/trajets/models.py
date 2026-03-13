from django.contrib.gis.db import models
from apps.accounts.models import Bateau
from apps.accounts.models import Pecheur

# Create your models here.
class TrajetPeche(models.Model):

    pecheur     = models.ForeignKey(
                      Pecheur,
                      on_delete=models.CASCADE,
                      related_name='trajets'
                  )
    bateau      = models.ForeignKey(
                      Bateau,
                      on_delete=models.SET_NULL,
                      null=True, blank=True
                  )

    # ✅ CHAMP SPATIAL : Ligne GPS du trajet (suite de points)
    trajet      = models.LineStringField(srid=4326, null=True, blank=True)

    date_depart    = models.DateTimeField()
    date_retour    = models.DateTimeField(null=True, blank=True)
    distance_km    = models.FloatField(null=True, blank=True)
    is_suspect     = models.BooleanField(
                         default=False,
                         help_text="True si le trajet passe par une zone interdite"
                     )
    notes          = models.TextField(blank=True)

    def duree(self):
        """Calcule la durée du trajet"""
        if self.date_retour and self.date_depart:
            return self.date_retour - self.date_depart
        return None

    def __str__(self):
        return f"Trajet de {self.pecheur} — {self.date_depart.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Trajet de pêche"
        verbose_name_plural = "Trajets de pêche"
        ordering = ['-date_depart']