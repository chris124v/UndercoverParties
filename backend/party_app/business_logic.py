from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from django.utils import timezone

from .models import Invitation
from .repositories import InvitationRepository, PartyRepository


class BusinessRuleError(Exception):
    pass


@dataclass(frozen=True)
class CreatePartyCommand:
    nombre: str
    ubicacion: str
    ubicacion_lat: float
    ubicacion_lng: float
    capacidad: int
    fecha: datetime
    anfitrion: str


class PartyService:
    def __init__(self, *, party_repo: PartyRepository, invitation_repo: InvitationRepository):
        self._party_repo = party_repo
        self._invitation_repo = invitation_repo

    def create_party(self, command: CreatePartyCommand):
        self._validate_create_party(command)
        return self._party_repo.create_party(
            nombre=command.nombre,
            ubicacion=command.ubicacion,
            ubicacion_lat=command.ubicacion_lat,
            ubicacion_lng=command.ubicacion_lng,
            capacidad=command.capacidad,
            fecha=command.fecha,
            anfitrion=command.anfitrion,
        )

    def accept_invitation(self, *, invitation_id: int) -> Invitation:
        invitation = self._invitation_repo.get_invitation(invitation_id)
        if invitation.estado != Invitation.Estado.PENDIENTE:
            raise BusinessRuleError("La invitación ya fue respondida.")

        accepted = self._party_repo.accepted_count(invitation.party_id)
        if accepted >= invitation.party.capacidad:
            raise BusinessRuleError("La fiesta está llena. No se pueden aceptar más invitados.")

        return self._invitation_repo.set_estado(invitation, estado=Invitation.Estado.ACEPTADA)

    def reject_invitation(self, *, invitation_id: int) -> Invitation:
        invitation = self._invitation_repo.get_invitation(invitation_id)
        if invitation.estado != Invitation.Estado.PENDIENTE:
            raise BusinessRuleError("La invitación ya fue respondida.")
        return self._invitation_repo.set_estado(invitation, estado=Invitation.Estado.RECHAZADA)

    def _validate_create_party(self, command: CreatePartyCommand) -> None:
        if not command.nombre.strip():
            raise BusinessRuleError("El nombre es requerido.")
        if not command.ubicacion.strip():
            raise BusinessRuleError("La ubicación es requerida.")
        if command.capacidad <= 0:
            raise BusinessRuleError("La capacidad debe ser mayor a 0.")
        if command.fecha < timezone.now():
            raise BusinessRuleError("La fecha debe ser en el futuro.")
