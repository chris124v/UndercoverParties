from django.contrib import admin

from .models import Invitation, Party


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "anfitrion", "capacidad", "fecha", "ubicacion")
    search_fields = ("nombre", "anfitrion", "ubicacion")


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("id", "party", "usuario", "estado", "fecha_aceptacion")
    list_filter = ("estado",)
    search_fields = ("usuario", "party__nombre")
