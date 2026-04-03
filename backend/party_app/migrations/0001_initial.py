# Generated manually for this exercise.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Party",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=200)),
                ("ubicacion", models.CharField(max_length=255)),
                ("ubicacion_lat", models.FloatField()),
                ("ubicacion_lng", models.FloatField()),
                ("capacidad", models.PositiveIntegerField()),
                ("fecha", models.DateTimeField()),
                ("anfitrion", models.CharField(max_length=120)),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Invitation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("usuario", models.CharField(max_length=120)),
                (
                    "estado",
                    models.CharField(
                        choices=[("PENDIENTE", "Pendiente"), ("ACEPTADA", "Aceptada"), ("RECHAZADA", "Rechazada")],
                        default="PENDIENTE",
                        max_length=20,
                    ),
                ),
                ("fecha_aceptacion", models.DateTimeField(blank=True, null=True)),
                (
                    "party",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="invitaciones", to="party_app.party"),
                ),
            ],
        ),
    ]
