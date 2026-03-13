# apps/alertes/forms.py

from django import forms
from apps.alertes.models import Alerte

CSS = ('w-full px-4 py-3 rounded-xl border border-slate-300 '
       'focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white')


class AlerteForm(forms.ModelForm):

    class Meta:
        model  = Alerte
        fields = ['type_alerte', 'niveau', 'titre', 'description', 'zone']
        widgets = {
            'type_alerte': forms.Select(attrs={
                'class': CSS
            }),
            'niveau': forms.Select(attrs={
                'class': CSS
            }),
            'titre': forms.TextInput(attrs={
                'class': CSS,
                'placeholder': 'Ex: Bateau suspect dans la zone nord'
            }),
            'description': forms.Textarea(attrs={
                'class': CSS,
                'rows': 4,
                'placeholder': 'Décrivez ce que vous avez observé...'
            }),
            'zone': forms.Select(attrs={
                'class': CSS
            }),
        }