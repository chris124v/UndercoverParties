from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.utils import timezone

from .models import Invitation, Party


@dataclass(frozen=True)
class PartyFilters:
    ubicacion_contains: Optional[str] = None
    capacidad_min: Optional[int] = None
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None


class PartyRepository:
    def create_party(
        self,
        *,
        nombre: str,
        ubicacion: str,
        ubicacion_lat: float,
        ubicacion_lng: float,
        capacidad: int,
        fecha: datetime,
        anfitrion: str,
    ) -> Party:
        return Party.objects.create(
            nombre=nombre,
            ubicacion=ubicacion,
            ubicacion_lat=ubicacion_lat,
            ubicacion_lng=ubicacion_lng,
            capacidad=capacidad,
            fecha=fecha,
            anfitrion=anfitrion,
        )

    def list_parties(self, *, filters: PartyFilters | None = None):
        queryset = Party.objects.all().order_by("-fecha")
        if not filters:
            return queryset

        if filters.ubicacion_contains:
            queryset = queryset.filter(ubicacion__icontains=filters.ubicacion_contains)
        if filters.capacidad_min is not None:
            queryset = queryset.filter(capacidad__gte=filters.capacidad_min)
        if filters.fecha_desde is not None:
            queryset = queryset.filter(fecha__gte=filters.fecha_desde)
        if filters.fecha_hasta is not None:
            queryset = queryset.filter(fecha__lte=filters.fecha_hasta)
        return queryset

    def get_party(self, *, party_id: int) -> Party:
        return Party.objects.get(id=party_id)

    def accepted_count(self, party_id: int) -> int:
        return Invitation.objects.filter(party_id=party_id, estado=Invitation.Estado.ACEPTADA).count()


class InvitationRepository:
    def list_invitations_for_user(self, *, usuario: str):
        return (
            Invitation.objects.select_related("party")
            .filter(usuario__iexact=usuario)
            .order_by("estado", "party__fecha")
        )

    def list_invitations_for_party(self, *, party_id: int):
        return (
            Invitation.objects.select_related("party")
            .filter(party_id=party_id)
            .order_by("estado", "usuario")
        )

    def get_invitation(self, invitation_id: int) -> Invitation:
        return Invitation.objects.select_related("party").get(id=invitation_id)

    def set_estado(self, invitation: Invitation, *, estado: str) -> Invitation:
        if estado == Invitation.Estado.ACEPTADA:
            invitation.estado = Invitation.Estado.ACEPTADA
            invitation.fecha_aceptacion = timezone.now()
        elif estado == Invitation.Estado.RECHAZADA:
            invitation.estado = Invitation.Estado.RECHAZADA
            invitation.fecha_aceptacion = None
        else:
            invitation.estado = Invitation.Estado.PENDIENTE
            invitation.fecha_aceptacion = None
        invitation.save(update_fields=["estado", "fecha_aceptacion"])
        return invitation
