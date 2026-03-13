
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.serializers import serialize

from apps.trajets.models import TrajetPeche



@login_required
def liste(request):

    if request.user.est_pecheur:
        try:
            pecheur = request.user.profil_pecheur
        except Exception:
            messages.warning(request, "Complétez d'abord votre profil pêcheur.")
            return redirect('accounts:profil_pecheur')

        trajets = TrajetPeche.objects.filter(
            pecheur=pecheur
        ).order_by('-date_depart')

    else:
        trajets = TrajetPeche.objects.all().select_related(
            'pecheur__utilisateur', 'bateau'
        ).order_by('-date_depart')

        # Filtre suspects uniquement
        if request.GET.get('suspects'):
            trajets = trajets.filter(is_suspect=True)

    contexte = {
        'trajets':     trajets,
        'total':       trajets.count(),
        'nb_suspects': TrajetPeche.objects.filter(is_suspect=True).count(),
    }
    return render(request, 'trajets/liste.html', contexte)



@login_required
def detail(request, pk):

    trajet = get_object_or_404(TrajetPeche, pk=pk)

    # Un pêcheur ne peut voir que ses propres trajets
    if request.user.est_pecheur:
        try:
            if trajet.pecheur != request.user.profil_pecheur:
                return HttpResponseForbidden("Ce trajet ne vous appartient pas.")
        except Exception:
            return HttpResponseForbidden()

    # Sérialiser le LineString en GeoJSON pour Leaflet
    trajet_geojson = None
    if trajet.trajet:
        trajet_geojson = serialize(
            'geojson', [trajet],
            geometry_field='trajet',
            fields=['date_depart', 'date_retour', 'is_suspect', 'notes']
        )

    contexte = {
        'trajet':        trajet,
        'trajet_geojson':trajet_geojson,
        'duree':         trajet.duree(),
    }
    return render(request, 'trajets/detail.html', contexte)


@login_required
def marquer_suspect(request, pk):

    if not request.user.est_admin:
        return HttpResponseForbidden("Réservé aux administrateurs.")

    trajet = get_object_or_404(TrajetPeche, pk=pk)

    if request.method == 'POST':
        trajet.is_suspect = not trajet.is_suspect
        trajet.save()
        statut = "suspect 🚨" if trajet.is_suspect else "normal ✅"
        messages.success(request, f"Trajet marqué comme {statut}")
        return redirect('trajets:liste')

    return render(request, 'trajets/confirmer_suspect.html', {'trajet': trajet})