from __future__ import annotations

from datetime import datetime

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_GET, require_http_methods

from .business_logic import BusinessRuleError, CreatePartyCommand, PartyService
from .forms import PartyCreateForm
from .repositories import InvitationRepository, PartyFilters, PartyRepository


def _service() -> PartyService:
    return PartyService(party_repo=PartyRepository(), invitation_repo=InvitationRepository())


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    return redirect("/fiestas")


@require_http_methods(["GET"])
def crear_fiesta_form(request: HttpRequest) -> HttpResponse:
    form = PartyCreateForm()
    return render(request, "parties/create_party.html", {"form": form})


@require_http_methods(["GET", "POST"])
def fiestas(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PartyCreateForm(request.POST)
        if not form.is_valid():
            return render(request, "parties/create_party.html", {"form": form}, status=400)

        cleaned = form.cleaned_data
        fecha: datetime = cleaned["fecha"]
        cmd = CreatePartyCommand(
            nombre=cleaned["nombre"],
            ubicacion=cleaned["ubicacion"],
            ubicacion_lat=float(cleaned["ubicacion_lat"]),
            ubicacion_lng=float(cleaned["ubicacion_lng"]),
            capacidad=int(cleaned["capacidad"]),
            fecha=fecha,
            anfitrion=cleaned["anfitrion"],
        )
        try:
            _service().create_party(cmd)
        except BusinessRuleError as exc:
            form.add_error(None, str(exc))
            return render(request, "parties/create_party.html", {"form": form}, status=400)
        messages.success(request, "Fiesta creada correctamente.")
        return redirect("/fiestas")

    filters = PartyFilters(
        ubicacion_contains=request.GET.get("ubicacion") or None,
        capacidad_min=int(request.GET["capacidad_min"]) if request.GET.get("capacidad_min") else None,
        fecha_desde=parse_datetime(request.GET.get("fecha_desde") or "") or None,
        fecha_hasta=parse_datetime(request.GET.get("fecha_hasta") or "") or None,
    )
    parties = PartyRepository().list_parties(filters=filters)
    return render(request, "parties/list_parties.html", {"parties": parties, "filters": filters})


@require_http_methods(["POST"])
def aceptar_invitacion(request: HttpRequest, invitation_id: int) -> HttpResponse:
    try:
        _service().accept_invitation(invitation_id=invitation_id)
        messages.success(request, "Invitación aceptada.")
    except BusinessRuleError as exc:
        messages.error(request, str(exc))
    return redirect(request.META.get("HTTP_REFERER", "/invitados"))


@require_http_methods(["POST"])
def rechazar_invitacion(request: HttpRequest, invitation_id: int) -> HttpResponse:
    try:
        _service().reject_invitation(invitation_id=invitation_id)
        messages.success(request, "Invitación rechazada.")
    except BusinessRuleError as exc:
        messages.error(request, str(exc))
    return redirect(request.META.get("HTTP_REFERER", "/invitados"))


@require_GET
def invitados_frontend(request: HttpRequest) -> HttpResponse:
    usuario = (request.GET.get("usuario") or "").strip() or "alice"
    invitations = InvitationRepository().list_invitations_for_user(usuario=usuario)
    return render(request, "invitados/invitados.html", {"usuario": usuario, "invitations": invitations})


@require_GET
def localizacion_frontend(request: HttpRequest) -> HttpResponse:
    parties = PartyRepository().list_parties(filters=None)

    parties_data = [
        {
            "id": party.id,
            "nombre": party.nombre,
            "ubicacion": party.ubicacion,
            "lat": party.ubicacion_lat,
            "lng": party.ubicacion_lng,
            "capacidad": party.capacidad,
            "fecha": party.fecha.isoformat(),
        }
        for party in parties
    ]

    return render(
        request,
        "localizacion/localizacion.html",
        {"parties": parties, "parties_data": parties_data},
    )


@require_GET
def lista_invitados_fiesta(request: HttpRequest, party_id: int) -> HttpResponse:
    party = PartyRepository().get_party(party_id=party_id)
    invitations = InvitationRepository().list_invitations_for_party(party_id=party_id)
    return render(request, "parties/party_guests.html", {"party": party, "invitations": invitations})
