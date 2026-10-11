<h1 align="center">UndercoverParties</h1>

<p align="center">
  The project consists of a Django monolith for managing underground parties, where users can publish parties at houses or farms, accept guests, and consult locations through a server-side rendered application with logical component separation. This are undercover parties wherever you are whenever you want.
</p>

<p align="center">
  It will execute entirely locally with SQLite and independent executable bundles.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/PYTHON-3-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/DJANGO-5-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django 5">
  <img src="https://img.shields.io/badge/SQLITE-LOCAL-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/LEAFLET-1.9.4-199900?style=for-the-badge&logo=leaflet&logoColor=white" alt="Leaflet 1.9.4">
  <img src="https://img.shields.io/badge/OPENSTREETMAP-MAPS-7EBC6F?style=for-the-badge&logo=openstreetmap&logoColor=white" alt="OpenStreetMap">
</p>

## Authors
 * Isaac Villalobos Bonilla, 2024124285
 * Christopher Daniel Vargas Villalta, 2024108443
   
---
## Architecture
* Django monolith with server-side rendering
* Monorepo with backend and multiple frontends
* Layered architecture: business logic, repositories, model
* Two independent frontend interfaces with separate entry points
* Local execution with independent scripts for each component in bundles

---
## Database Architecture
* SQLite will be the database engine of choice for the project
* It will contain a small seeded dataset loaded automatically
* Structure: Party (id, nombre, ubicación_lat, ubicación_lng, capacidad, fecha, anfitrión, fecha_creación) and Invitation (id, party_id, usuario, estado, fecha_aceptación)

--- 

## AI 

* We use GPT-5.2 for the coding implementation.

### Prompt: 
**Role**: Create an implementation for the README of UndercoverParties repository.

**Instructions**: Create a functional implementation of the undercoverparties repository, using the detailed README and the project folder structuture presented.

**Context**: README and Monolito Django para gestión de fiestas clandestinas. Construyan una aplicación donde se publiquen fiestas en casas o fincas, se acepten invitados y se puedan consultar ubicaciones, todo dentro de un monolito con renderizado en servidor pero con separación lógica de componentes. Ejercicio en parejas. 


Arquitectura: Django monolith con server side rendering
Monorepo con backend y múltiples frontends
Capas: business logic, repositories, model
Frontend 1: interfaz para aceptar invitados
Frontend 2: interfaz para localizar fiestas
Operación de escritura: POST /fiestas para crear una fiesta con ubicación y capacidad
Operación de lectura: GET /fiestas para listar fiestas disponibles
Capacidad de ejecutar bundles por separado (server, frontend invitados, frontend localización)
Uso de SQLite local con pocos datos
Scripts para correr servidor y cada frontend de forma independiente
Todo funcionando localmente

**Output**: Functional implementation of the undercoverparties repository running locally. 

---
## Layered Design
* The Django monolith is based on a layered architecture
* **Business Logic layer**: Takes care of data type validations, capacity checks, and party management rules
* **Repositories layer**: Takes care of communication between the application and SQLite
* **Model layer**: Defines the structure of Party and Invitation entities
* Clear separation between Django views (presentation) and core logic layers

---

## Scripts
* `scripts/run_server.ps1` / `scripts/run_server.sh`: Starts main Django server on port 8000 (shared backend)
* `scripts/run_frontend_invitados.ps1` / `scripts/run_frontend_invitados.sh`: Starts invitation management interface on port 8001
* `scripts/run_frontend_localizacion.ps1` / `scripts/run_frontend_localizacion.sh`: Starts party discovery interface on port 8002
* `scripts/setup_db.ps1` / `scripts/setup_db.sh`: Initializes SQLite database and runs seed
* `scripts/seed_data.py`: Populates database with sample party and invitation data
* Each bundle runs independently with its own Django instance

---

## Quickstart (Local)

### 1) Python env + install dependencies

From the repo root `UndercoverParties/`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

### 2) Setup SQLite + seed sample data

```powershell
./scripts/setup_db.ps1
```

Note: the seed runs with `--reset` (it deletes all existing `Party` and `Invitation` rows).

### 3) Run bundles (3 independent servers)

```powershell
./scripts/run_server.ps1               # http://127.0.0.1:8000
./scripts/run_frontend_invitados.ps1   # http://127.0.0.1:8001
./scripts/run_frontend_localizacion.ps1# http://127.0.0.1:8002
```

Main URLs:
- `GET /crear-fiesta` (form)
- `POST /fiestas` (create)
- `GET /fiestas` (list)
- `GET /invitados?usuario=alice` (invitation UI)
- `POST /invitaciones/<id>/aceptar` (accept)
- `GET /localizacion` (map)

---
## Paradigm
* **Imperative**: Explicit step-by-step execution
* Request flow: receive form submission → validate data → query/insert to database → render response
* Clear separation between HTTP handling, business rules, and persistence
* Side effects (SQLite read/write) isolated in repositories layer
* Models define entity structure and validation constraints