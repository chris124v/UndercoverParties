from __future__ import annotations

from django import forms

from .models import Party


class PartyCreateForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = [
            "nombre",
            "ubicacion",
            "ubicacion_lat",
            "ubicacion_lng",
            "capacidad",
            "fecha",
            "anfitrion",
        ]
        widgets = {
            "fecha": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
