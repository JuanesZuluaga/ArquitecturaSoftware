from django.urls import path
from . import views

app_name = 'vuelos'
urlpatterns = [
    path('', views.HomeView.as_view(), name='inicio'),
    path('registrar/', views.VueloCreateView.as_view(), name='registrar'),
    path('listar/', views.VueloListView.as_view(), name='listar'),
    path('estadisticas/', views.vuelo_stats_view, name='estadisticas'),
]
