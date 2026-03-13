from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from apps.alertes.models import Alerte
from apps.alertes.forms import AlerteForm


@login_required
def liste(request):
    """
    Liste les alertes.
    - Pêcheur : voit les alertes qui le concernent (zone, météo)
    - Expert/Admin : voit toutes les alertes
    """
    if request.user.est_pecheur:
        alertes = Alerte.objects.filter(
            statut__in=['ouverte', 'en_traitement']
        ).order_by('-date_creation')
    else:
        statut = request.GET.get('statut', '')
        alertes = Alerte.objects.all().order_by('-date_creation')
        if statut:
            alertes = alertes.filter(statut=statut)

    return render(request, 'alertes/liste.html', {
        'alertes': alertes,
        'total_ouvertes': Alerte.objects.filter(statut='ouverte').count(),
    })


@login_required
def signaler(request):
    """Le pêcheur signale une activité suspecte."""
    form = AlerteForm()

    if request.method == 'POST':
        form = AlerteForm(data=request.POST)
        if form.is_valid():
            alerte = form.save(commit=False)
            alerte.signale_par = request.user
            alerte.save()
            messages.success(request, "Signalement envoyé !")
            return redirect('alertes:liste')

    return render(request, 'alertes/signaler.html', {'form': form})


@login_required
def detail(request, pk):
    """Détail d'une alerte avec carte de localisation."""
    alerte = get_object_or_404(Alerte, pk=pk)
    return render(request, 'alertes/detail.html', {'alerte': alerte})


@login_required
def traiter(request, pk):
    """Marque une alerte comme résolue — Admin seulement."""
    if not (request.user.est_admin or request.user.est_expert):
        return HttpResponseForbidden()

    alerte = get_object_or_404(Alerte, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'en_traitement':
            alerte.statut = 'en_traitement'
            alerte.traite_par = request.user
            alerte.save()
            messages.info(request, "Alerte prise en charge.")
        elif action == 'resoudre':
            alerte.resoudre(request.user)
            messages.success(request, "Alerte marquée comme résolue ✅")
        return redirect('alertes:liste')

    return render(request, 'alertes/traiter.html', {'alerte': alerte})


# =============================================================================
# alertes/urls.py
# =============================================================================
"""
from django.urls import path
from . import views

app_name = 'alertes'

urlpatterns = [
    path('',               views.liste,    name='liste'),
    path('signaler/',      views.signaler, name='signaler'),
    path('<int:pk>/',      views.detail,   name='detail'),
    path('<int:pk>/traiter/', views.traiter, name='traiter'),
]
"""


# =============================================================================
# trajets/views.py
# =============================================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.serializers import serialize


@login_required
def liste(request):
    """Liste les trajets."""
    from apps.trajets.models import TrajetPeche

    if request.user.est_pecheur:
        trajets = TrajetPeche.objects.filter(
            pecheur=request.user.profil_pecheur
        ).order_by('-date_depart')
    else:
        trajets = TrajetPeche.objects.all().select_related(
            'pecheur__utilisateur', 'bateau'
        ).order_by('-date_depart')

        # Filtre trajets suspects
        suspects = request.GET.get('suspects', '')
        if suspects:
            trajets = trajets.filter(is_suspect=True)

    return render(request, 'alertes/liste.html', {
        'trajets': trajets,
        'nb_suspects': TrajetPeche.objects.filter(is_suspect=True).count(),
    })


@login_required
def detail(request, pk):
    """Affiche le trajet sur une carte Leaflet."""
    from apps.trajets.models import TrajetPeche
    trajet = get_object_or_404(TrajetPeche, pk=pk)

    # Vérifier l'accès : pêcheur voit seulement ses propres trajets
    if request.user.est_pecheur:
        if trajet.pecheur != request.user.profil_pecheur:
            return HttpResponseForbidden()

    # Sérialiser le LineString en GeoJSON pour Leaflet
    trajet_geojson = serialize('geojson', [trajet],
                               geometry_field='trajet',
                               fields=['date_depart', 'date_retour', 'is_suspect'])

    return render(request, 'trajets/detail.html', {
        'trajet': trajet,
        'trajet_geojson': trajet_geojson,
    })


@login_required
def marquer_suspect(request, pk):
    """Marque un trajet comme suspect — Admin."""
    if not request.user.est_admin:
        return HttpResponseForbidden()

    from apps.trajets.models import TrajetPeche
    trajet = get_object_or_404(TrajetPeche, pk=pk)
    trajet.is_suspect = not trajet.is_suspect
    trajet.save()
    messages.warning(request, f"Trajet marqué comme {'suspect' if trajet.is_suspect else 'normal'}.")
    return redirect('trajets:liste')





