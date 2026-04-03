from django.db import models


class Party(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=255)
    ubicacion_lat = models.FloatField()
    ubicacion_lng = models.FloatField()
    capacidad = models.PositiveIntegerField()
    fecha = models.DateTimeField()
    anfitrion = models.CharField(max_length=120)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.nombre} ({self.anfitrion})"


class Invitation(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ACEPTADA = "ACEPTADA", "Aceptada"
        RECHAZADA = "RECHAZADA", "Rechazada"

    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="invitaciones")
    usuario = models.CharField(max_length=120)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_aceptacion = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Inv({self.usuario} -> {self.party_id}) {self.estado}"
