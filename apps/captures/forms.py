# apps/captures/forms.py
from django import forms
from apps.captures.models import DeclarationCapture

CSS = 'w-full px-4 py-3 rounded-xl border border-slate-300 bg-white'

class DeclarationCaptureForm(forms.ModelForm):
    def __init__(self, *args, pecheur=None, **kwargs):
        super().__init__(*args, **kwargs)
        if pecheur:
            self.fields['bateau'].queryset = pecheur.bateaux.filter(is_actif=True)

    class Meta:
        model = DeclarationCapture
        fields = ['espece','zone','bateau','quantite_kg',
                  'engin_peche','date_capture','observations']
        widgets = {
            'espece':       forms.Select(attrs={'class': CSS}),
            'zone':         forms.Select(attrs={'class': CSS}),
            'bateau':       forms.Select(attrs={'class': CSS}),
            'quantite_kg':  forms.NumberInput(attrs={'class': CSS}),
            'engin_peche':  forms.Select(attrs={'class': CSS}),
            'date_capture': forms.DateTimeInput(attrs={'class': CSS, 'type': 'datetime-local'}),
            'observations': forms.Textarea(attrs={'class': CSS, 'rows': 3}),
        }