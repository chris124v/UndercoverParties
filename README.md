# UndercoverParties
The project consists of a Django monolith for managing underground parties, where users can publish parties at houses or farms, accept guests, and consult locations through a server-side rendered application with logical component separation. This are undercover parties wherever you are whenever you want.

It will execute entirely locally with SQLite and independent executable bundles.

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

