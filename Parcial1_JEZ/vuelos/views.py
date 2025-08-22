from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from django.urls import reverse_lazy
from django.db.models import Avg, Count
from django.db import OperationalError
from django.contrib import messages
from .models import Vuelo
from .forms import VueloForm, check_vuelo_table_exists

# Zona de inicio
class HomeView(TemplateView):
    template_name = 'vuelos/home.html'

# Registrar vuelos
class VueloCreateView(CreateView):
    model = Vuelo
    form_class = VueloForm
    template_name = 'vuelos/flight_form.html'
    success_url = reverse_lazy('vuelos:listar')

    def dispatch(self, request, *args, **kwargs):
        if not check_vuelo_table_exists():
            messages.error(request, "La tabla de vuelos no existe. Ejecuta: python manage.py makemigrations && python manage.py migrate")
            return redirect('vuelos:inicio')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except OperationalError:
            # Evita el crash y muestra instrucción clara al usuario
            messages.error(self.request, "Error de base de datos: falta la tabla 'vuelos_vuelo'. Ejecuta: python manage.py makemigrations && python manage.py migrate")
            return redirect('vuelos:inicio')  # ajusta la ruta de redirección según tu app

# Listar vuelos
class VueloListView(ListView):
    model = Vuelo
    template_name = 'vuelos/flight_list.html'
    context_object_name = 'vuelos'

    def dispatch(self, request, *args, **kwargs):
        # evita ejecutar la vista si la tabla no existe
        if not check_vuelo_table_exists():
            messages.error(request, "La tabla de vuelos no existe. Ejecuta: python manage.py makemigrations && python manage.py migrate")
            return redirect('vuelos:inicio')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Vuelo.objects.order_by('precio')

# Estadísticas
def vuelo_stats_view(request):
    # chequeo rápido antes de realizar consultas
    if not check_vuelo_table_exists():
        messages.error(request, "No se pueden calcular estadísticas porque falta la tabla de vuelos. Ejecuta las migraciones.")
        return redirect('vuelos:inicio')

    try:
        # contar por tipo
        counts = Vuelo.objects.values('flight_type').annotate(total=Count('id'))
        # preparar defaults
        nacionales = 0
        internacionales = 0
        for c in counts:
            if c['flight_type'] == 'N':
                nacionales = c['total']
            elif c['flight_type'] == 'I':
                internacionales = c['total']

        # promedio del precio de vuelos nacionales (puede ser None)
        avg_nacionales = Vuelo.objects.filter(flight_type='N').aggregate(avg=Avg('precio'))['avg']
        if avg_nacionales is None:
            avg_nacionales_display = 0
        else:
            # precio ya es entero; aseguramos entero para mostrar
            avg_nacionales_display = int(avg_nacionales)

        # nuevo: promedio de vuelos internacionales
        avg_internacionales = Vuelo.objects.filter(flight_type='I').aggregate(avg=Avg('precio'))['avg']
        if avg_internacionales is None:
            avg_internacionales_display = 0
        else:
            avg_internacionales_display = int(avg_internacionales)

        context = {
            'nacionales': nacionales,
            'internacionales': internacionales,
            'avg_nacionales': avg_nacionales_display,
            'avg_internacionales': avg_internacionales_display,
        }
        return render(request, 'vuelos/estadisticas.html', context)
    except OperationalError:
        messages.error(request, "Error de base de datos al obtener estadísticas. Ejecuta: python manage.py makemigrations && python.manage.py migrate")
        return redirect('vuelos:inicio')
