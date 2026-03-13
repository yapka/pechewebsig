# zones/views.py
# =============================================================================
# VUES DE L'APP ZONES
# Gère : Carte interactive, Liste zones, Créer/Modifier zone, Détail zone
# =============================================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.core.serializers import serialize
import json

from apps.zones.models import ZonePeche
from .forms import ZonePecheForm


# -----------------------------------------------------------------------------
# VUE 1 : Carte interactive Leaflet
# URL : /zones/carte/
# Template : zones/carte.html
# -----------------------------------------------------------------------------
@login_required
def carte(request):
    """
    Affiche la carte Leaflet avec toutes les zones de pêche.
    Toutes les zones sont converties en GeoJSON pour Leaflet.
    """
    zones = ZonePeche.objects.filter(statut='active')

    # Sérialiser les zones en GeoJSON pour Leaflet
    zones_geojson = serialize('geojson', zones,
                               geometry_field='geom',
                               fields=['nom', 'type_zone', 'statut', 'description'])

    contexte = {
        'zones_geojson': zones_geojson,
        'total_zones': zones.count(),
        'zones_interdites': zones.filter(type_zone='interdite').count(),
        'zones_protegees': zones.filter(type_zone='protegee').count(),
    }
    return render(request, 'zones/carte.html', contexte)


# -----------------------------------------------------------------------------
# VUE 2 : API GeoJSON des zones (pour Leaflet AJAX)
# URL : /zones/api/geojson/
# Retourne du JSON (pas un template HTML)
# -----------------------------------------------------------------------------
@login_required
def zones_geojson(request):
    """
    Endpoint API qui retourne les zones en GeoJSON.
    Utilisé par Leaflet pour charger les zones dynamiquement.
    """
    type_filtre = request.GET.get('type', None)
    zones = ZonePeche.objects.filter(statut='active')

    if type_filtre:
        zones = zones.filter(type_zone=type_filtre)

    data = serialize('geojson', zones,
                     geometry_field='geom',
                     fields=['nom', 'type_zone', 'statut',
                             'description', 'superficie_km2'])
    return JsonResponse(json.loads(data), safe=False)


# -----------------------------------------------------------------------------
# VUE 3 : Liste des zones
# URL : /zones/
# Template : zones/liste.html
# -----------------------------------------------------------------------------
@login_required
def liste_zones(request):
    """Liste toutes les zones avec filtres."""
    type_filtre = request.GET.get('type', '')
    statut_filtre = request.GET.get('statut', '')

    zones = ZonePeche.objects.all().order_by('-date_creation')

    if type_filtre:
        zones = zones.filter(type_zone=type_filtre)
    if statut_filtre:
        zones = zones.filter(statut=statut_filtre)

    contexte = {
        'zones': zones,
        'type_filtre': type_filtre,
        'statut_filtre': statut_filtre,
        'total': zones.count(),
    }
    return render(request, 'alertes/liste.html', contexte)


# -----------------------------------------------------------------------------
# VUE 4 : Détail d'une zone
# URL : /zones/<id>/
# Template : zones/detail.html
# -----------------------------------------------------------------------------
@login_required
def detail_zone(request, pk):
    """Affiche le détail d'une zone avec sa carte."""
    zone = get_object_or_404(ZonePeche, pk=pk)
    zone_geojson = serialize('geojson', [zone], geometry_field='geom',
                             fields=['nom', 'type_zone'])
    contexte = {
        'zone': zone,
        'zone_geojson': zone_geojson,
        'nb_captures': zone.captures.count(),
        'nb_alertes': zone.alertes.count(),
    }
    return render(request, 'zones/detail.html', contexte)


# -----------------------------------------------------------------------------
# VUE 5 : Créer une zone (Admin/Expert)
# URL : /zones/creer/
# Template : zones/form.html
# -----------------------------------------------------------------------------
@login_required
def creer_zone(request):
    """Permet à l'admin ou l'expert SIG de créer une zone."""
    if not (request.user.est_admin or request.user.est_expert):
        return HttpResponseForbidden("Accès réservé aux experts et administrateurs.")

    form = ZonePecheForm()

    if request.method == 'POST':
        form = ZonePecheForm(data=request.POST)
        if form.is_valid():
            zone = form.save(commit=False)
            zone.cree_par = request.user
            zone.save()
            messages.success(request, f"Zone '{zone.nom}' créée avec succès !")
            return redirect('zones:detail', pk=zone.pk)

    return render(request, 'zones/form.html', {'form': form, 'action': 'Créer'})


# -----------------------------------------------------------------------------
# VUE 6 : Modifier une zone (Admin/Expert)
# URL : /zones/<id>/modifier/
# Template : zones/form.html
# -----------------------------------------------------------------------------
@login_required
def modifier_zone(request, pk):
    """Modifie une zone existante."""
    if not (request.user.est_admin or request.user.est_expert):
        return HttpResponseForbidden()

    zone = get_object_or_404(ZonePeche, pk=pk)
    form = ZonePecheForm(instance=zone)

    if request.method == 'POST':
        form = ZonePecheForm(data=request.POST, instance=zone)
        if form.is_valid():
            form.save()
            messages.success(request, f"Zone '{zone.nom}' mise à jour !")
            return redirect('zones:detail', pk=zone.pk)

    return render(request, 'zones/form.html', {
        'form': form, 'zone': zone, 'action': 'Modifier'
    })


# -----------------------------------------------------------------------------
# VUE 7 : Supprimer une zone (Admin seulement)
# URL : /zones/<id>/supprimer/
# -----------------------------------------------------------------------------
@login_required
def supprimer_zone(request, pk):
    """Supprime une zone — Admin seulement."""
    if not request.user.est_admin:
        return HttpResponseForbidden()

    zone = get_object_or_404(ZonePeche, pk=pk)
    if request.method == 'POST':
        nom = zone.nom
        zone.delete()
        messages.success(request, f"Zone '{nom}' supprimée.")
        return redirect('zones:liste')

    return render(request, 'zones/confirmer_suppression.html', {'zone': zone})
