from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from apps.accounts.models import Utilisateur, Pecheur, Bateau
from .forms import (
    ConnexionForm,
    InscriptionForm,
    ProfilForm,
    PecheurForm,
    BateauForm,
)



def connexion(request):
    """
    Affiche le formulaire de connexion.
    Si l'utilisateur est déjà connecté, redirige vers le dashboard.
    """
    # Si déjà connecté → rediriger
    if request.user.is_authenticated:
        return redirect('dashboard:accueil')

    form = ConnexionForm()

    if request.method == 'POST':
        form = ConnexionForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Django vérifie username + password dans la BDD
            utilisateur = authenticate(request, username=username, password=password)

            if utilisateur is not None:
                login(request, utilisateur)
                messages.success(request, f"Bienvenue {utilisateur.get_full_name()} !")

                # Rediriger selon le rôle
                if utilisateur.est_admin:
                    return redirect('dashboard:admin')
                elif utilisateur.est_expert:
                    return redirect('dashboard:expert')
                else:
                    return redirect('dashboard:pecheur')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'accounts/login.html', {'form': form})



@login_required
def deconnexion(request):
    """Déconnecte l'utilisateur et redirige vers login."""
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('accounts:login')


def inscription(request):
    """
    Formulaire d'inscription pour les nouveaux pêcheurs.
    Seul le rôle 'pecheur' peut s'inscrire librement.
    Les experts et admins sont créés par l'administrateur.
    """
    if request.user.is_authenticated:
        return redirect('dashboard:accueil')

    form = InscriptionForm()

    if request.method == 'POST':
        form = InscriptionForm(data=request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.role = 'pecheur'  # Rôle par défaut
            utilisateur.save()

            messages.success(request, "Compte créé avec succès ! Vous pouvez vous connecter.")
            return redirect('accounts:login')

    return render(request, 'accounts/inscription.html', {'form': form})


@login_required
def profil(request):
    """
    Affiche et permet de modifier le profil de l'utilisateur connecté.
    Si c'est un pêcheur, affiche aussi son profil pêcheur et ses bateaux.
    """
    utilisateur = request.user
    profil_pecheur = None
    bateaux = []

    # Récupérer le profil pêcheur si applicable
    if utilisateur.est_pecheur:
        try:
            profil_pecheur = utilisateur.profil_pecheur
            bateaux = profil_pecheur.bateaux.all()
        except Pecheur.DoesNotExist:
            pass

    form = ProfilForm(instance=utilisateur)

    if request.method == 'POST':
        form = ProfilForm(data=request.POST, files=request.FILES, instance=utilisateur)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect('accounts:profil')

    contexte = {
        'form': form,
        'profil_pecheur': profil_pecheur,
        'bateaux': bateaux,
    }
    return render(request, 'accounts/profil.html', contexte)



@login_required
def profil_pecheur(request):
    """
    Permet au pêcheur de compléter son profil spécifique
    (numéro de licence, commune, type de pêche...).
    """
    if not request.user.est_pecheur:
        return HttpResponseForbidden("Accès réservé aux pêcheurs.")

    # Récupérer ou créer le profil pêcheur
    pecheur, created = Pecheur.objects.get_or_create(
        utilisateur=request.user
    )

    form = PecheurForm(instance=pecheur)

    if request.method == 'POST':
        form = PecheurForm(data=request.POST, instance=pecheur)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil pêcheur enregistré !")
            return redirect('accounts:profil')

    return render(request, 'accounts/profil_pecheur.html', {'form': form})



@login_required
def ajouter_bateau(request):
    """Permet à un pêcheur d'ajouter un bateau."""
    if not request.user.est_pecheur:
        return HttpResponseForbidden("Accès réservé aux pêcheurs.")

    try:
        pecheur = request.user.profil_pecheur
    except Pecheur.DoesNotExist:
        messages.warning(request, "Complétez d'abord votre profil pêcheur.")
        return redirect('accounts:profil_pecheur')

    form = BateauForm()

    if request.method == 'POST':
        form = BateauForm(data=request.POST)
        if form.is_valid():
            bateau = form.save(commit=False)
            bateau.pecheur = pecheur
            bateau.save()
            messages.success(request, f"Bateau '{bateau.nom}' ajouté !")
            return redirect('accounts:profil')

    return render(request, 'accounts/bateau_form.html', {'form': form})


@login_required(login_url='login')
def bateau_list(request):
    bateaux = Bateau.objects.all()
    return render(request, 'accounts/bateau_list.html', {'bateaux': bateaux})


@login_required
def liste_utilisateurs(request):
    """
    Liste tous les utilisateurs — réservé à l'administrateur.
    Permet de filtrer par rôle.
    """
    if not request.user.est_admin:
        return HttpResponseForbidden("Accès réservé aux administrateurs.")

    role_filtre = request.GET.get('role', '')
    utilisateurs = Utilisateur.objects.all().order_by('-date_joined')

    if role_filtre:
        utilisateurs = utilisateurs.filter(role=role_filtre)

    contexte = {
        'utilisateurs': utilisateurs,
        'role_filtre': role_filtre,
        'total': utilisateurs.count(),
    }
    return render(request, 'accounts/liste_utilisateurs.html', contexte)



@login_required
def toggle_utilisateur(request, pk):
    """Active ou désactive un compte utilisateur."""
    if not request.user.est_admin:
        return HttpResponseForbidden()

    utilisateur = get_object_or_404(Utilisateur, pk=pk)
    utilisateur.is_active = not utilisateur.is_active
    utilisateur.save()

    action = "activé" if utilisateur.is_active else "désactivé"
    messages.success(request, f"Compte {utilisateur.username} {action}.")
    return redirect('accounts:liste_utilisateurs')
