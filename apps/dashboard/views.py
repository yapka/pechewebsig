from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone

from apps.captures.models import DeclarationCapture
from apps.zones.models import ZonePeche
from apps.alertes.models import Alerte
from apps.trajets.models import TrajetPeche


@login_required
def accueil(request):
    """Redirige vers le bon dashboard selon le rôle."""
    if request.user.est_admin:
        return redirect('dashboard:admin')
    elif request.user.est_expert:
        return redirect('dashboard:expert')
    else:
        return redirect('dashboard:pecheur')



@login_required
def dashboard_pecheur(request):
    """
    Tableau de bord du pêcheur.
    Affiche : ses captures récentes, ses bateaux, les alertes actives, les zones.
    """
    try:
        pecheur = request.user.profil_pecheur
    except Exception:
        return redirect('accounts:profil_pecheur')

    # Ses captures récentes
    captures_recentes = DeclarationCapture.objects.filter(
        pecheur=pecheur
    ).order_by('-date_capture')[:5]

    # Statistiques personnelles
    stats = DeclarationCapture.objects.filter(pecheur=pecheur).aggregate(
        total_kg=Sum('quantite_kg'),
        nb_total=Count('id'),
        nb_validees=Count('id', filter=__import__('django.db.models', fromlist=['Q']).Q(statut='validee')),
    )

    # Alertes actives (important pour le pêcheur)
    alertes_actives = Alerte.objects.filter(
        statut='ouverte',
        niveau__in=['warning', 'danger']
    ).order_by('-date_creation')[:3]

    # Zones interdites (le pêcheur doit les connaître)
    zones_interdites = ZonePeche.objects.filter(
        type_zone='interdite', statut='active'
    )[:5]

    contexte = {
        'pecheur': pecheur,
        'captures_recentes': captures_recentes,
        'stats': stats,
        'alertes_actives': alertes_actives,
        'zones_interdites': zones_interdites,
        'nb_bateaux': pecheur.bateaux.filter(is_actif=True).count(),
    }
    return render(request, 'dashboard/pecheur.html', contexte)


@login_required
def dashboard_expert(request):
    """
    Tableau de bord de l'expert SIG.
    Affiche : statistiques captures, zones, analyses.
    """
    if not (request.user.est_expert or request.user.est_admin):
        return redirect('dashboard:pecheur')

    annee = timezone.now().year

    # Statistiques globales captures
    stats_captures = DeclarationCapture.objects.aggregate(
        total_kg=Sum('quantite_kg'),
        nb_total=Count('id'),
        nb_validees=Count('id', filter=__import__('django.db.models', fromlist=['Q']).Q(statut='validee')),
        nb_en_attente=Count('id', filter=__import__('django.db.models', fromlist=['Q']).Q(statut='soumise')),
    )

    # Top 5 espèces capturées
    top_especes = (
        DeclarationCapture.objects
        .filter(statut='validee')
        .values('espece__nom_commun')
        .annotate(total=Sum('quantite_kg'))
        .order_by('-total')[:5]
    )

    # Captures par mois (année en cours)
    par_mois = (
        DeclarationCapture.objects
        .filter(statut='validee', date_capture__year=annee)
        .values('date_capture__month')
        .annotate(total=Sum('quantite_kg'))
        .order_by('date_capture__month')
    )

    # Zones
    stats_zones = {
        'total': ZonePeche.objects.count(),
        'interdites': ZonePeche.objects.filter(type_zone='interdite').count(),
        'protegees': ZonePeche.objects.filter(type_zone='protegee').count(),
    }

    # Alertes récentes
    alertes_recentes = Alerte.objects.order_by('-date_creation')[:5]

    contexte = {
        'stats_captures': stats_captures,
        'top_especes': list(top_especes),
        'par_mois': list(par_mois),
        'stats_zones': stats_zones,
        'alertes_recentes': alertes_recentes,
        'annee': annee,
        # Pour graphique Chart.js
        'mois_labels': [str(m['date_capture__month']) for m in par_mois],
        'mois_data':   [float(m['total'] or 0) for m in par_mois],
    }
    return render(request, 'dashboard/expert.html', contexte)



@login_required
def dashboard_admin(request):
    """
    Tableau de bord global de l'administrateur.
    Affiche : toutes les métriques, utilisateurs, validation en attente.
    """
    if not request.user.est_admin:
        return redirect('dashboard:accueil')

    from    apps.accounts.models import Utilisateur

    # Métriques globales
    metriques = {
        'nb_utilisateurs': Utilisateur.objects.filter(is_active=True).count(),
        'nb_pecheurs': Utilisateur.objects.filter(role='pecheur', is_active=True).count(),
        'nb_zones': ZonePeche.objects.filter(statut='active').count(),
        'nb_captures': DeclarationCapture.objects.count(),
        'captures_en_attente': DeclarationCapture.objects.filter(statut='soumise').count(),
        'alertes_ouvertes': Alerte.objects.filter(statut='ouverte').count(),
        'trajets_suspects': TrajetPeche.objects.filter(is_suspect=True).count(),
        'total_kg': DeclarationCapture.objects.filter(
            statut='validee'
        ).aggregate(t=Sum('quantite_kg'))['t'] or 0,
    }

    # Dernières inscriptions
    derniers_users = Utilisateur.objects.order_by('-date_joined')[:5]

    # Captures à valider en urgence
    captures_urgentes = DeclarationCapture.objects.filter(
        statut='soumise'
    ).select_related('pecheur__utilisateur', 'espece').order_by('-date_soumission')[:5]

    # Alertes non traitées
    alertes_urgentes = Alerte.objects.filter(
        statut='ouverte', niveau='danger'
    ).order_by('-date_creation')[:5]

    contexte = {
        'metriques': metriques,
        'derniers_users': derniers_users,
        'captures_urgentes': captures_urgentes,
        'alertes_urgentes': alertes_urgentes,
    }
    return render(request, 'dashboard/admin.html', contexte)
