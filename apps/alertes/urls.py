from django.urls import path
from . import views

app_name = 'alertes'

urlpatterns = [
    path('',                  views.liste,    name='liste'),
    path('signaler/',         views.signaler, name='signaler'),
    path('<int:pk>/',         views.detail,   name='detail'),
    path('<int:pk>/traiter/', views.traiter,  name='traiter'),
]