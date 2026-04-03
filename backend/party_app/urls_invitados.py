from django.urls import path

from . import views


urlpatterns = [
    path("", views.invitados_frontend),
    path("invitados", views.invitados_frontend),
    path("invitaciones/<int:invitation_id>/aceptar", views.aceptar_invitacion),
    path("invitaciones/<int:invitation_id>/rechazar", views.rechazar_invitacion),
]
