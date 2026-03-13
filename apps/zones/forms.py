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
