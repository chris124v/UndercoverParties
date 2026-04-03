# Workflows

## 1) Create Party

- `GET /crear-fiesta` muestra el formulario.
- `POST /fiestas` crea la fiesta (form submission, no JSON).

## 2) List + Accept Invitations

- `GET /fiestas` lista fiestas con filtros por querystring.
- `GET /invitados?usuario=alice` lista invitaciones.
- `POST /invitaciones/<id>/aceptar` acepta si hay cupo.
