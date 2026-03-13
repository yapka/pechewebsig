from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Sum, Count
from django.utils import timezone

from apps.captures.models import DeclarationCapture, EspecePoisson
from apps.captures.forms import DeclarationCaptureForm
from apps.zones.models import ZonePeche


# -----------------------------------------------------------------------------
# VUE 1 : liste  ← nom exact utilisé dans urls.py
# URL : /captures/
# Accès : Expert + Admin
# -----------------------------------------------------------------------------
@login_required
def liste(request):
    """Liste toutes les captures — Expert et Admin."""

    if request.user.est_pecheur:
        # Le pêcheur est redirigé vers ses propres captures
        return redirect('captures:mes_captures')

    # Filtres GET
    statut    = request.GET.get('statut', '')
    espece_id = request.GET.get('espece', '')
    zone_id   = request.GET.get('zone', '')

    captures = DeclarationCapture.objects.all().select_related(
        'pecheur__utilisateur', 'espece', 'zone'
    ).order_by('-date_capture')

    if statut:
        captures = captures.filter(statut=statut)
    if espece_id:
        captures = captures.filter(espece_id=espece_id)
    if zone_id:
        captures = captures.filter(zone_id=zone_id)

    contexte = {
        'captures':     captures,
        'especes':      EspecePoisson.objects.all(),
        'zones':        ZonePeche.objects.filter(statut='active'),
        'statut_filtre':statut,
        'total':        captures.count(),
        'total_kg':     captures.aggregate(t=Sum('quantite_kg'))['t'] or 0,
    }
    return render(request, 'captures/liste.html', contexte)


# -----------------------------------------------------------------------------
# VUE 2 : declarer  ← nom exact utilisé dans urls.py
# URL : /captures/declarer/
# Accès : Pêcheur seulement
# -----------------------------------------------------------------------------
@login_required
def declarer(request):
    """Formulaire de déclaration de capture pour le pêcheur."""

    if not request.user.est_pecheur:
        return HttpResponseForbidden("Réservé aux pêcheurs.")

    try:
        pecheur = request.user.profil_pecheur
    except Exception:
        messages.warning(request, "Complétez d'abord votre profil pêcheur.")
        return redirect('accounts:profil_pecheur')

    form = DeclarationCaptureForm(pecheur=pecheur)

    if request.method == 'POST':
        form = DeclarationCaptureForm(data=request.POST, pecheur=pecheur)
        if form.is_valid():
            capture = form.save(commit=False)
            capture.pecheur = pecheur
            capture.statut  = 'soumise'
            capture.save()
            messages.success(request, "✅ Capture déclarée avec succès !")
            return redirect('captures:mes_captures')

    return render(request, 'captures/declarer.html', {'form': form})


# -----------------------------------------------------------------------------
# VUE 3 : mes_captures  ← nom exact utilisé dans urls.py
# URL : /captures/mes-captures/
# Accès : Pêcheur seulement
# -----------------------------------------------------------------------------
@login_required
def mes_captures(request):
    """Liste les captures du pêcheur connecté."""

    if not request.user.est_pecheur:
        return redirect('captures:liste')

    try:
        pecheur = request.user.profil_pecheur
    except Exception:
        messages.warning(request, "Complétez d'abord votre profil pêcheur.")
        return redirect('accounts:profil_pecheur')

    captures = DeclarationCapture.objects.filter(
        pecheur=pecheur
    ).order_by('-date_capture')

    # Filtre par statut
    statut = request.GET.get('statut', '')
    if statut:
        captures = captures.filter(statut=statut)

    # Statistiques personnelles
    stats = {
        'total_kg':       captures.aggregate(total=Sum('quantite_kg'))['total'] or 0,
        'nb_declarations':captures.count(),
        'validees':       captures.filter(statut='validee').count(),
        'en_attente':     captures.filter(statut='soumise').count(),
        'rejetees':       captures.filter(statut='rejetee').count(),
    }

    return render(request, 'captures/mes_captures.html', {
        'captures':      captures,
        'stats':         stats,
        'statut_filtre': statut,
    })



@login_required
def valider(request, pk=None):
    """
    Deux modes :
    - Sans pk  → affiche la liste des captures en attente
    - Avec pk  → valide ou rejette une capture spécifique
    """

    if not request.user.est_admin:
        return HttpResponseForbidden("Réservé aux administrateurs.")

    # MODE AVEC pk : traiter une capture précise
    if pk:
        capture = get_object_or_404(DeclarationCapture, pk=pk)

        if request.method == 'POST':
            action = request.POST.get('action')

            if action == 'valider':
                capture.valider(request.user)
                messages.success(request, f"✅ Capture de {capture.pecheur} validée !")

            elif action == 'rejeter':
                motif = request.POST.get('motif', 'Aucun motif fourni')
                capture.rejeter(request.user, motif)
                messages.warning(request, f"❌ Capture rejetée.")

            return redirect('captures:valider')

        return render(request, 'captures/valider_detail.html', {'capture': capture})

    # MODE SANS pk : liste des captures en attente
    captures = DeclarationCapture.objects.filter(
        statut='soumise'
    ).select_related(
        'pecheur__utilisateur', 'espece', 'zone'
    ).order_by('-date_soumission')

    return render(request, 'captures/valider.html', {
        'captures': captures,
        'total':    captures.count(),
    })


@login_required
def statistiques(request):
    """Statistiques et analyses des captures."""

    if not (request.user.est_expert or request.user.est_admin):
        return HttpResponseForbidden("Réservé aux experts et administrateurs.")

    annee = timezone.now().year

    # Top 10 espèces par volume
    par_espece = list(
        DeclarationCapture.objects
        .filter(statut='validee')
        .values('espece__nom_commun')
        .annotate(total_kg=Sum('quantite_kg'), nb=Count('id'))
        .order_by('-total_kg')[:10]
    )

    # Top 10 zones par volume
    par_zone = list(
        DeclarationCapture.objects
        .filter(statut='validee', zone__isnull=False)
        .values('zone__nom')
        .annotate(total_kg=Sum('quantite_kg'), nb=Count('id'))
        .order_by('-total_kg')[:10]
    )

    # Captures par mois (année en cours)
    par_mois = list(
        DeclarationCapture.objects
        .filter(statut='validee', date_capture__year=annee)
        .values('date_capture__month')
        .annotate(total_kg=Sum('quantite_kg'), nb=Count('id'))
        .order_by('date_capture__month')
    )

    # Totaux globaux
    totaux = DeclarationCapture.objects.filter(statut='validee').aggregate(
        total_kg=Sum('quantite_kg'),
        nb_captures=Count('id'),
    )

    contexte = {
        'par_espece':     par_espece,
        'par_zone':       par_zone,
        'par_mois':       par_mois,
        'totaux':         totaux,
        'annee':          annee,
        # Données JSON pour graphiques Chart.js
        'labels_espece':  [e['espece__nom_commun'] or 'Inconnu' for e in par_espece],
        'data_espece':    [float(e['total_kg'] or 0) for e in par_espece],
        'labels_zone':    [z['zone__nom'] for z in par_zone],
        'data_zone':      [float(z['total_kg'] or 0) for z in par_zone],
        'labels_mois':    [str(m['date_capture__month']) for m in par_mois],
        'data_mois':      [float(m['total_kg'] or 0) for m in par_mois],
    }
    return render(request, 'captures/statistiques.html', contexte)