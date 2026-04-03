from __future__ import annotations

import os
import sys
import argparse
import random
from datetime import timedelta
from pathlib import Path

import django
from django.utils import timezone


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete previously seeded records before seeding (keeps non-seed data).",
    )
    args = parser.parse_args()

    backend_dir = Path(__file__).resolve().parent.parent / "backend"
    sys.path.insert(0, str(backend_dir))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    from party_app.models import Invitation, Party

    now = timezone.now()

    if args.reset:
        Invitation.objects.all().delete()
        Party.objects.all().delete()

    rng = random.Random(2026)

    hosts = ["Isaac", "Christopher", "Sofía", "Valeria", "Daniel"]
    party_names = [
        "After Office Secreto",
        "Noche en la Finca",
        "Casa Abierta (Solo Invitados)",
        "Vinilos & Luces Neón",
        "Café de Medianoche",
        "Silent Party",
        "Rooftop Clandestino",
        "Electro en la Bodega",
        "Salsa en la Sala",
        "Fiesta Retro 2000s",
        "Noche de Máscaras",
        "Garden Session",
        "Karaoke Prohibido",
        "Techno en la Quinta",
        "Fuego & Parrilla",
        "Cumbia en la Cocina",
        "Noche de Juegos",
        "Rumba Bajo las Estrellas",
        "House Session",
        "Fiesta Temática: Negro",
        "Meet & Dance",
        "La Reunión",
        "Chill & Beats",
        "Fiesta de Aniversario",
        "Desvelo Tropical",
        "La Noche del DJ",
        "Jam Session",
        "Fiesta de Disfraces",
        "Baila en Silencio",
        "Brindis a Medianoche",
    ]
    locations = [
        ("Casa en San Pedro", 9.9360, -84.0530),
        ("Finca cerca de Santa Ana", 9.9300, -84.1800),
        ("Apartamento en Escazú", 9.9196, -84.1380),
        ("Casa en Heredia centro", 9.9970, -84.1160),
        ("Bodega en Alajuela", 10.0160, -84.2140),
        ("Finca en Cartago", 9.8640, -83.9190),
        ("Casa en Guadalupe", 9.9570, -84.0610),
        ("Quinta en Grecia", 10.0720, -84.3130),
        ("Finca en Orotina", 9.9120, -84.5230),
        ("Casa en Tres Ríos", 9.9090, -83.9880),
        ("Rancho en Jacó", 9.6160, -84.6290),
        ("Casa en Liberia", 10.6350, -85.4400),
        ("Cabina en Monteverde", 10.3000, -84.8160),
        ("Casa en Pérez Zeledón", 9.3720, -83.7030),
        ("Finca en San Carlos", 10.3330, -84.4270),
    ]

    parties = []
    rng.shuffle(party_names)
    for idx in range(1, 26):
        ubicacion, lat, lng = locations[(idx - 1) % len(locations)]
        anfitrion = hosts[(idx - 1) % len(hosts)]
        capacidad = 4 + (idx % 10)  # 4..13
        fecha = now + timedelta(days=idx, hours=((idx + 1) % 6) * 2)
        nombre = party_names[idx - 1]

        party, _ = Party.objects.update_or_create(
            nombre=nombre,
            defaults={
                "ubicacion": ubicacion,
                "ubicacion_lat": float(lat) + (idx * 0.0007),
                "ubicacion_lng": float(lng) - (idx * 0.0006),
                "capacidad": capacidad,
                "fecha": fecha,
                "anfitrion": anfitrion,
            },
        )
        parties.append(party)

    # Create 50 unique guests and invite them across parties.
    # Requirement: >= 3 invitados por fiesta.
    # All invitations start as PENDIENTE so the user can accept them in the UI.
    first_names = [
        "Ana",
        "Luis",
        "María José",
        "Carlos",
        "Valentina",
        "Diego",
        "Camila",
        "Santiago",
        "Lucía",
        "Andrés",
        "Paula",
        "Javier",
        "Gabriela",
        "Sebastián",
        "Daniela",
        "Mateo",
        "Fernanda",
        "Emiliano",
        "Isabella",
        "Martín",
    ]
    last_names = [
        "Morales",
        "Fernández",
        "Pérez",
        "Vargas",
        "Soto",
        "Ramírez",
        "Rojas",
        "Herrera",
        "Jiménez",
        "Navarro",
        "Chaves",
        "Mena",
        "Salas",
        "Aguilar",
        "Quesada",
        "Solano",
        "Cordero",
        "Madrigal",
        "Araya",
        "Campos",
    ]

    guest_names: list[str] = []
    for fn in first_names:
        for ln in last_names:
            guest_names.append(f"{fn} {ln}")
    rng.shuffle(guest_names)
    guest_names = guest_names[:50]

    invitations_created = 0
    for party in parties:
        for usuario in rng.sample(guest_names, 3):
            Invitation.objects.update_or_create(
                party=party,
                usuario=usuario,
                defaults={
                    "estado": Invitation.Estado.PENDIENTE,
                    "fecha_aceptacion": None,
                },
            )
            invitations_created += 1

    print(
        "Seed complete: "
        f"parties={Party.objects.count()} "
        f"guests={len(guest_names)} "
        f"invitations={Invitation.objects.count()} (min 3 per party)"
    )


if __name__ == "__main__":
    main()
