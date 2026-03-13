from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',         views.accueil,           name='accueil'),
    path('pecheur/', views.dashboard_pecheur, name='pecheur'),
    path('expert/',  views.dashboard_expert,  name='expert'),
    path('admin/',   views.dashboard_admin,   name='admin'),
]
