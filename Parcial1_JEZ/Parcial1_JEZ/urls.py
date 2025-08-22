from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', include('vuelos.urls')),
    path('registrador/', RedirectView.as_view(url='/registrar/', permanent=False)),
    path('admin/', admin.site.urls),
    path('vuelos/', include('vuelos.urls')),
]
