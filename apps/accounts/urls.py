
from django.urls import path
from . import views

app_name = 'accounts'  # Namespace pour les templates : {% url 'accounts:login' %}

urlpatterns = [
    # Authentification
    path('login/',       views.connexion,          name='login'),
    path('logout/',      views.deconnexion,         name='logout'),
    path('inscription/', views.inscription,         name='inscription'),

    # Profil
    path('profil/',            views.profil,          name='profil'),
    path('profil/pecheur/',    views.profil_pecheur,  name='profil_pecheur'),
    path('bateau/ajouter/',    views.ajouter_bateau,  name='ajouter_bateau'),
    path('bateau/',views.bateau_list,name='bateau-list'),
    # Administration
    path('utilisateurs/',              views.liste_utilisateurs, name='liste_utilisateurs'),
    path('utilisateurs/<int:pk>/toggle/', views.toggle_utilisateur, name='toggle_utilisateur'),
]
