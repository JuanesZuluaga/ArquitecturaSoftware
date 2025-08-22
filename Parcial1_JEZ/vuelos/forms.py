from django import forms
from .models import Vuelo

class VueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = ['origen', 'flight_type','destino', 'fecha', 'asientos',  'precio']  # incluir flight_type
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'flight_type': forms.Select(),  # selector para Nacional/Internacional
        }

def check_vuelo_table_exists():
    try:
        from django.db import connection
        tables = connection.introspection.table_names()
        if 'vuelos_vuelo' not in tables:
            import sys
            print("ERROR: no se completaron las migraciones", file=sys.stderr)
            return False
        return True
    except Exception:
        import sys
        print("AVISO: no fue posible comprobar tablas de la BD.", file=sys.stderr)
        return False
