from django.urls import path

from . import views


urlpatterns = [
    path("", views.localizacion_frontend),
    path("localizacion", views.localizacion_frontend),
    path("fiestas", views.fiestas),
]
