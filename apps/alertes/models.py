from django.contrib.gis.db import models
from apps.zones.models import ZonePeche
from apps.accounts.models import Utilisateur
from  django.utils import timezone


class Alerte(models.Model):

    TYPE_ALERTE = [
        ('zone_interdite',  'Entrée en zone interdite'),
        ('peche_illegale',  'Pêche illégale signalée'),
        ('surexploitation', 'Surexploitation détectée'),
        ('meteo',           'Alerte météo'),
        ('autre',           'Autre'),
    ]

    NIVEAU = [
        ('info',    'Information'),
        ('warning', 'Avertissement'),
        ('danger',  'Danger'),
    ]

    STATUT_ALERTE = [
        ('ouverte',       'Ouverte'),
        ('en_traitement', 'En traitement'),
        ('resolue',       'Résolue'),
    ]

    type_alerte  = models.CharField(max_length=25, choices=TYPE_ALERTE)
    niveau       = models.CharField(max_length=10, choices=NIVEAU, default='warning')
    statut       = models.CharField(max_length=20, choices=STATUT_ALERTE, default='ouverte')
    titre        = models.CharField(max_length=200)
    description  = models.TextField()

    # ✅ CHAMP SPATIAL : Point GPS de l'alerte
    position     = models.PointField(srid=4326, null=True, blank=True)

    # Qui a signalé / qui traite
    signale_par  = models.ForeignKey(
                       Utilisateur,
                       on_delete=models.SET_NULL,
                       null=True,
                       related_name='alertes_signalees'
                   )
    traite_par   = models.ForeignKey(
                       Utilisateur,
                       on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='alertes_traitees'
                   )

    # Lien optionnel vers une zone concernée
    zone         = models.ForeignKey(
                       ZonePeche,
                       on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='alertes'
                   )

    date_creation   = models.DateTimeField(auto_now_add=True)
    date_resolution = models.DateTimeField(null=True, blank=True)

    def resoudre(self, utilisateur):
        """Méthode pour marquer une alerte comme résolue"""
        self.statut = 'resolue'
        self.traite_par = utilisateur
        self.date_resolution = timezone.now()
        self.save()

    def __str__(self):
        return f"[{self.get_niveau_display()}] {self.titre}"

    class Meta:
        verbose_name = "Alerte"
        verbose_name_plural = "Alertes"
        ordering = ['-date_creation']

