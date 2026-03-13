from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Utilisateur, Pecheur, Bateau



class ConnexionForm(AuthenticationForm):

    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 '
                     'focus:outline-none focus:ring-2 focus:ring-cyan-500 '
                     'bg-white/80 text-slate-800 placeholder-slate-400',
            'placeholder': "Votre nom d'utilisateur",
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 '
                     'focus:outline-none focus:ring-2 focus:ring-cyan-500 '
                     'bg-white/80 text-slate-800 placeholder-slate-400',
            'placeholder': "Votre mot de passe",
        })
    )


class InscriptionForm(UserCreationForm):
    """Formulaire d'inscription pour les nouveaux pêcheurs."""

    CSS = ('w-full px-4 py-3 rounded-xl border border-slate-300 '
           'focus:outline-none focus:ring-2 focus:ring-cyan-500 '
           'bg-white/80 text-slate-800 placeholder-slate-400')

    first_name = forms.CharField(
        label="Prénom",
        widget=forms.TextInput(attrs={'class': CSS, 'placeholder': 'Votre prénom'})
    )
    last_name = forms.CharField(
        label="Nom",
        widget=forms.TextInput(attrs={'class': CSS, 'placeholder': 'Votre nom'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': CSS, 'placeholder': 'votre@email.com'})
    )
    telephone = forms.CharField(
        label="Téléphone",
        required=False,
        widget=forms.TextInput(attrs={'class': CSS, 'placeholder': '+225 XX XX XX XX'})
    )

    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email',
                  'telephone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CSS = ('w-full px-4 py-3 rounded-xl border border-slate-300 '
               'focus:outline-none focus:ring-2 focus:ring-cyan-500 '
               'bg-white/80 text-slate-800 placeholder-slate-400')
        for field in self.fields.values():
            field.widget.attrs['class'] = CSS


class ProfilForm(forms.ModelForm):

    CSS = ('w-full px-4 py-3 rounded-xl border border-slate-300 '
           'focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white/80')

    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email', 'telephone', 'photo']
        widgets = {
            'first_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':   forms.TextInput(attrs={'class': 'form-control'}),
            'email':       forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone':   forms.TextInput(attrs={'class': 'form-control'}),
        }



class PecheurForm(forms.ModelForm):

    CSS = ('w-full px-4 py-3 rounded-xl border border-slate-300 '
           'focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white/80')

    class Meta:
        model = Pecheur
        fields = ['numero_licence', 'date_naissance', 'commune',
                  'type_peche', 'experience_annee']
        widgets = {
            'numero_licence':   forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance':   forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            'commune':          forms.TextInput(attrs={'class': 'form-control'}),
            'type_peche':       forms.Select(attrs={'class': 'form-control'}),
            'experience_annee': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class BateauForm(forms.ModelForm):

    CSS = ('w-full px-4 py-3 rounded-xl border border-slate-300 '
           'focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white/80')

    class Meta:
        model = Bateau
        fields = ['nom', 'immatriculation', 'type_bateau',
                  'longueur_m', 'capacite_tonnes', 'annee_fabrication']
        widgets = {
            'nom':              forms.TextInput(attrs={'class': 'form-control'}),
            'immatriculation':  forms.TextInput(attrs={'class': 'form-control'}),
            'type_bateau':      forms.Select(attrs={'class': 'form-control'}),
            'longueur_m':       forms.NumberInput(attrs={'class': 'form-control'}),
            'capacite_tonnes':  forms.NumberInput(attrs={'class': 'form-control'}),
            'annee_fabrication':forms.NumberInput(attrs={'class': 'form-control'}),
        }
