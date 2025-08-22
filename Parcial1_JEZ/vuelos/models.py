from django.db import models

class Flight(models.Model):
    class Type(models.TextChoices):
        Nacional = 'N', 'Nacional'
        Internacional = 'I', 'Internacional'

    name = models.CharField(max_length=120)
    flight_type = models.CharField(max_length=1, choices=Type.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.get_flight_type_display()} (${self.price})'

class Vuelo(models.Model):
    Type = Flight.Type  # reutiliza las mismas opciones

    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha = models.DateField()
    asientos = models.PositiveIntegerField(default=0)
    flight_type = models.CharField(max_length=1, choices=Type.choices, default=Type.Nacional)
    precio = models.IntegerField(default=0)  # ahora entero

    def __str__(self):
        return f"{self.origen} → {self.destino} ({self.fecha}) - {self.get_flight_type_display()} ${self.precio}"
