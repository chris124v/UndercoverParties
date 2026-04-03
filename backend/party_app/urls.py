from django.urls import path

from . import views


urlpatterns = [
    path("", views.home),
    path("crear-fiesta", views.crear_fiesta_form),
    path("fiestas", views.fiestas),
    path("fiestas/<int:party_id>/invitados", views.lista_invitados_fiesta),
    path("invitaciones/<int:invitation_id>/aceptar", views.aceptar_invitacion),
    path("invitaciones/<int:invitation_id>/rechazar", views.rechazar_invitacion),
    path("invitados", views.invitados_frontend),
    path("localizacion", views.localizacion_frontend),
]
