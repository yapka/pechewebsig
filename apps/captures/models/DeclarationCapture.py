from django.contrib.gis.db import models
from django.utils import timezone
from .espece_poison_model import EspecePoisson
from apps.accounts.models.pecheur_model import Pecheur
from apps.accounts.models.bateau_model import Bateau
from apps.accounts.models.utilisateur_model import Utilisateur
from apps.zones.models import ZonePeche

class DeclarationCapture(models.Model):

    STATUT = [
        ('brouillon', 'Brouillon'),
        ('soumise',   'Soumise'),
        ('validee',   'Validée'),
        ('rejetee',   'Rejetée'),
    ]

    ENGIN_PECHE = [
        ('filet',      'Filet'),
        ('ligne',      'Ligne'),
        ('chalut',     'Chalut'),
        ('nasse',      'Nasse'),
        ('harpon',     'Harpon'),
        ('autre',      'Autre'),
    ]

    # Relations
    pecheur      = models.ForeignKey(
                       Pecheur,
                       on_delete=models.CASCADE,
                       related_name='captures'
                   )
    bateau       = models.ForeignKey(
                       Bateau,
                       on_delete=models.SET_NULL,
                       null=True, blank=True
                   )
    zone         = models.ForeignKey(
                       ZonePeche,
                       on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='captures'
                   )
    espece       = models.ForeignKey(
                       EspecePoisson,
                       on_delete=models.SET_NULL,
                       null=True
                   )

    # ✅ CHAMP SPATIAL : Point GPS de la capture
    position_gps = models.PointField(srid=4326, null=True, blank=True)

    # Données de capture
    quantite_kg   = models.FloatField()
    engin_peche   = models.CharField(max_length=20, choices=ENGIN_PECHE, blank=True)
    date_capture  = models.DateTimeField()
    observations  = models.TextField(blank=True)

    # Workflow de validation
    statut        = models.CharField(max_length=20, choices=STATUT, default='soumise')
    valide_par    = models.ForeignKey(
                        Utilisateur,
                        on_delete=models.SET_NULL,
                        null=True, blank=True,
                        related_name='captures_validees'
                    )
    date_soumission  = models.DateTimeField(auto_now_add=True)
    date_validation  = models.DateTimeField(null=True, blank=True)
    motif_rejet      = models.TextField(blank=True)

    def valider(self, utilisateur):
        """Méthode pour valider une déclaration"""
        self.statut = 'validee'
        self.valide_par = utilisateur
        self.date_validation = timezone.now()
        self.save()

    def rejeter(self, utilisateur, motif):
        """Méthode pour rejeter une déclaration"""
        self.statut = 'rejetee'
        self.valide_par = utilisateur
        self.motif_rejet = motif
        self.save()

    def __str__(self):
        return f"{self.pecheur} — {self.espece} — {self.quantite_kg}kg ({self.date_capture.date()})"

    class Meta:
        verbose_name = "Déclaration de capture"
        verbose_name_plural = "Déclarations de captures"
        ordering = ['-date_capture']