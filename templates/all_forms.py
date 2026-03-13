# =============================================================================
# apps/zones/forms.py
# =============================================================================
from django import forms
from .models import ZonePeche

CSS = ('w-full px-4 py-3 rounded-xl border border-slate-300 '
       'focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white')

class ZonePecheForm(forms.ModelForm):
    class Meta:
        model  = ZonePeche
        fields = ['nom', 'code', 'type_zone', 'statut',
                  'description', 'profondeur_min', 'profondeur_max']
        widgets = {
            'nom':           forms.TextInput(attrs={'class': CSS}),
            'code':          forms.TextInput(attrs={'class': CSS}),
            'type_zone':     forms.Select(attrs={'class': CSS}),
            'statut':        forms.Select(attrs={'class': CSS}),
            'description':   forms.Textarea(attrs={'class': CSS, 'rows': 3}),
            'profondeur_min':forms.NumberInput(attrs={'class': CSS}),
            'profondeur_max':forms.NumberInput(attrs={'class': CSS}),
        }
    # Le champ geom (polygone) est dessiné sur la carte Leaflet
    # et soumis via un champ caché dans le template zones/form.html


# =============================================================================
# apps/captures/forms.py
# =============================================================================
from django import forms
from .models import DeclarationCapture, EspecePoisson
from zones.models import ZonePeche
from accounts.models import Bateau   # on importe Bateau depuis accounts

CSS = ('w-full px-4 py-3 rounded-xl border border-slate-300 '
       'focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white')

class DeclarationCaptureForm(forms.ModelForm):

    def __init__(self, *args, pecheur=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les bateaux : afficher seulement les bateaux du pêcheur connecté
        if pecheur:
            self.fields['bateau'].queryset = pecheur.bateaux.filter(is_actif=True)

    class Meta:
        model  = DeclarationCapture
        fields = ['espece', 'zone', 'bateau', 'quantite_kg',
                  'engin_peche', 'date_capture', 'observations']
        widgets = {
            'espece':       forms.Select(attrs={'class': CSS}),
            'zone':         forms.Select(attrs={'class': CSS}),
            'bateau':       forms.Select(attrs={'class': CSS}),
            'quantite_kg':  forms.NumberInput(attrs={
                                'class': CSS, 'step': '0.1', 'min': '0'
                            }),
            'engin_peche':  forms.Select(attrs={'class': CSS}),
            'date_capture': forms.DateTimeInput(attrs={
                                'class': CSS, 'type': 'datetime-local'
                            }),
            'observations': forms.Textarea(attrs={'class': CSS, 'rows': 3}),
        }


# =============================================================================
# apps/alertes/forms.py
# =============================================================================
from django import forms
from .models import Alerte

CSS = ('w-full px-4 py-3 rounded-xl border border-slate-300 '
       'focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white')

class AlerteForm(forms.ModelForm):
    class Meta:
        model  = Alerte
        fields = ['type_alerte', 'niveau', 'titre', 'description', 'zone']
        widgets = {
            'type_alerte': forms.Select(attrs={'class': CSS}),
            'niveau':      forms.Select(attrs={'class': CSS}),
            'titre':       forms.TextInput(attrs={
                               'class': CSS,
                               'placeholder': 'Ex: Bateau suspect zone nord'
                           }),
            'description': forms.Textarea(attrs={
                               'class': CSS, 'rows': 4,
                               'placeholder': 'Décrivez ce que vous avez observé...'
                           }),
            'zone':        forms.Select(attrs={'class': CSS}),
        }


# =============================================================================
# apps/trajets/forms.py
# =============================================================================
from django import forms
from .models import TrajetPeche

CSS = ('w-full px-4 py-3 rounded-xl border border-slate-300 '
       'focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white')

class TrajetPecheForm(forms.ModelForm):
    class Meta:
        model  = TrajetPeche
        fields = ['bateau', 'date_depart', 'date_retour', 'notes']
        widgets = {
            'bateau':      forms.Select(attrs={'class': CSS}),
            'date_depart': forms.DateTimeInput(attrs={
                               'class': CSS, 'type': 'datetime-local'
                           }),
            'date_retour': forms.DateTimeInput(attrs={
                               'class': CSS, 'type': 'datetime-local'
                           }),
            'notes':       forms.Textarea(attrs={'class': CSS, 'rows': 3}),
        }
