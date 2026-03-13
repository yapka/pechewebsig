from django.urls import path
from . import views

app_name = 'zones'

urlpatterns = [
    path('',                    views.liste_zones,    name='liste'),
    path('carte/',              views.carte,          name='carte'),
    path('api/geojson/',        views.zones_geojson,  name='geojson'),
    path('creer/',              views.creer_zone,     name='creer'),
    path('<int:pk>/',           views.detail_zone,    name='detail'),
    path('<int:pk>/modifier/',  views.modifier_zone,  name='modifier'),
    path('<int:pk>/supprimer/', views.supprimer_zone, name='supprimer'),
]