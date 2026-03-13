from django.urls import path
from apps.captures import views

app_name = 'captures'

urlpatterns = [
    path('',views.liste,name='liste'),
    path('declarer/',views.declarer,name='declarer'),
    path('mes-captures/',views.mes_captures,name='mes_captures'),
    path('valider/',views.valider,name='valider'),
    path('<int:pk>/valider/',views.valider,name='valider_detail'),
    path('statistiques/',views.statistiques,name='statistiques'),
]
