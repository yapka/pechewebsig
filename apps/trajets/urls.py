from django.urls import path
from apps.trajets import views

app_name = 'trajets'

urlpatterns = [
    path('',views.liste,name='liste'),
    path('<int:pk>/',      views.detail,          name='detail'),
    path('<int:pk>/suspect/', views.marquer_suspect, name='suspect'),
]