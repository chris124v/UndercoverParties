# Architecture

- Django monolith con server-side rendering (templates HTML).
- Repositorio en capas dentro de `party_app`:
  - `models.py`: entidades (Party, Invitation)
  - `repositories.py`: acceso a datos (ORM encapsulado)
  - `business_logic.py`: reglas (validación, capacidad)
  - `views.py`: manejo HTTP + render de templates
- Tres "bundles" ejecutables (tres instancias Django) con settings distintos:
  - `config.settings` (server principal)
  - `config.settings_invitados` (frontend invitados)
  - `config.settings_localizacion` (frontend localización)
