# ✈️ Aerowise — Empty Legs Marketplace

**Aerowise** es una plataforma de marketplace de **empty legs** (vuelos de reposicionamiento de aviación privada) que agrega vuelos de múltiples operadores, los muestra al público y permite gestionar consultas desde un panel de administración.

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Arquitectura](#-arquitectura)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación Local](#-instalación-local)
- [Comandos de Seed (Datos de Ejemplo)](#-comandos-de-seed-datos-de-ejemplo)
- [Ejecutar el Proyecto](#-ejecutar-el-proyecto)
- [Estructura de la API](#-estructura-de-la-api)
- [Panel de Administración](#-panel-de-administración)
- [Web Scrapers](#-web-scrapers)
- [Variables de Entorno](#-variables-de-entorno)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Deploy Gratis](#-deploy-gratis---opciones-de-hosting)
- [Contribuir](#-contribuir)

---

## 📝 Descripción

Los **empty legs** son vuelos de reposicionamiento de aeronaves privadas que se ofrecen con descuentos del 50-90% sobre el precio normal. Aerowise:

- **Agrega** empty legs de 9+ operadores de aviación privada (GlobeAir, Avcon Jet, Luxaviation, etc.)
- **Muestra** los vuelos al público en una landing page moderna (sin mostrar precios)
- **Recibe consultas** "Me interesa" de usuarios interesados
- **Panel privado** para el dueño: gestionar consultas, verificar/publicar legs, ver estadísticas
- **Web scraping** automático con Celery para mantener datos frescos
- **Alertas por email** a usuarios suscritos cuando aparecen nuevos legs

---

## 🏗 Arquitectura

```
┌──────────────────────┐    ┌──────────────────────┐
│   Frontend (React)   │    │   Backend (Django)    │
│   Vite + Tailwind    │───▶│   DRF + SQLite/PG    │
│   Puerto 5173        │    │   Puerto 8000         │
└──────────────────────┘    └──────────┬───────────┘
                                       │
                            ┌──────────▼───────────┐
                            │   Celery Workers     │
                            │   + Redis Broker     │
                            │   (Web Scraping)     │
                            └──────────────────────┘
```

| Componente      | Tecnología                        |
|-----------------|-----------------------------------|
| **Frontend**    | React 18, Vite 5, Tailwind CSS 3  |
| **Backend**     | Django 5, Django REST Framework    |
| **Base de Datos** | SQLite (dev) / PostgreSQL (prod)|
| **Task Queue**  | Celery 5 + Redis                  |
| **Scraping**    | BeautifulSoup, Requests, Selenium |

---

## 📦 Requisitos Previos

- **Python** 3.10+
- **Node.js** 18+
- **Redis** (opcional, para Celery — no requerido para dev básico)
- **Git**

---

## 🚀 Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/aerowise.git
cd aerowise
```

### 2. Backend (Django)

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env
# Editar .env si querés cambiar algo (la config por defecto funciona)

# Crear tablas en la base de datos
python manage.py migrate

# Crear superusuario de Django Admin (opcional)
python manage.py createsuperuser
```

### 3. Cargar datos de ejemplo

```bash
# Cargar 85+ aeropuertos internacionales
python manage.py load_airports

# Crear 30 aeronaves (Cessna, Gulfstream, Bombardier, etc.)
python manage.py seed_aircraft

# Crear 11 operadores y sus fuentes de datos
python manage.py seed_sources

# Crear 50 empty legs de demostración
python manage.py seed_demo_legs

# Crear 15 consultas de ejemplo
python manage.py seed_inquiries
```

> **Tip:** Para limpiar y regenerar datos: `python manage.py seed_demo_legs --clear`

### 4. Frontend (React)

```bash
cd ../frontend

# Instalar dependencias
npm install

# (Opcional) Si npm install falla, borrar node_modules y lockfile:
# rm -rf node_modules package-lock.json && npm install
```

---

## ▶️ Ejecutar el Proyecto

Necesitás **dos terminales** abiertas:

### Terminal 1 — Backend

```bash
cd backend
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
python manage.py runserver
```

El backend corre en `http://localhost:8000`

### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

El frontend corre en `http://localhost:5173`

> Vite proxy automáticamente `/api/*` → `http://localhost:8000`

### (Opcional) Terminal 3 — Celery Worker

Solo necesario si querés ejecutar scraping automático:

```bash
cd backend
celery -A config worker -l info
```

### (Opcional) Terminal 4 — Celery Beat

Para tareas programadas (scraping periódico, expiración de legs):

```bash
cd backend
celery -A config beat -l info
```

---

## 🔗 Estructura de la API

### Endpoints Públicos (sin autenticación)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/flights/public/empty-legs/` | Listar empty legs publicados (sin precios) |
| `GET` | `/api/flights/public/empty-legs/?search=miami` | Buscar por ciudad/país |
| `POST` | `/api/flights/public/inquiries/` | Enviar consulta "Me interesa" |
| `POST` | `/api/notifications/subscribe/` | Suscribirse a alertas |
| `POST` | `/api/notifications/unsubscribe/` | Cancelar suscripción |

### Endpoints del Panel (requieren Token)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/flights/panel/login/` | Login → devuelve token |
| `POST` | `/api/flights/panel/logout/` | Cerrar sesión |
| `GET` | `/api/flights/panel/check/` | Verificar token |
| `GET` | `/api/flights/panel/inquiries/` | Listar consultas |
| `PATCH` | `/api/flights/panel/inquiries/:id/` | Actualizar status/notas |
| `PATCH` | `/api/flights/panel/empty-legs/:id/toggle/` | Toggle verificado/publicado |
| `GET` | `/api/flights/dashboard/` | Estadísticas del dashboard |

### Endpoints CRUD (requieren Token)

| Recurso | Endpoint Base | Métodos |
|---------|---------------|---------|
| Operadores | `/api/flights/operators/` | GET, POST, PUT, PATCH, DELETE |
| Aeropuertos | `/api/flights/airports/` | GET, POST, PUT, PATCH, DELETE |
| Fuentes | `/api/flights/sources/` | GET, POST, PUT, PATCH, DELETE |
| Aeronaves | `/api/flights/aircraft/` | GET, POST, PUT, PATCH, DELETE |
| Vuelos | `/api/flights/flights/` | GET, POST, PUT, PATCH, DELETE |
| Empty Legs | `/api/flights/empty-legs/` | GET, POST, PUT, PATCH, DELETE |
| Scraping Manual | `/api/flights/sources/:id/trigger-scrape/` | POST |

### Ejemplo: Enviar una consulta

```bash
curl -X POST http://localhost:8000/api/flights/public/inquiries/ \
  -H "Content-Type: application/json" \
  -d '{
    "empty_leg": 1,
    "name": "Juan Pérez",
    "email": "juan@email.com",
    "phone": "+54 11 1234-5678",
    "passengers": 4,
    "message": "Me interesa este vuelo"
  }'
```

### Ejemplo: Login al Panel

```bash
curl -X POST http://localhost:8000/api/flights/panel/login/ \
  -H "Content-Type: application/json" \
  -d '{"password": "aerowise2026"}'

# Respuesta: {"token": "abc123..."}
```

### Ejemplo: Suscribirse a alertas

```bash
curl -X POST http://localhost:8000/api/notifications/subscribe/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@email.com",
    "name": "María",
    "origin_keywords": "Buenos Aires, Argentina",
    "destination_keywords": "Miami, Punta Cana",
    "max_price_usd": 20000,
    "frequency": "daily"
  }'
```

---

## 🔐 Panel de Administración

### Acceso

- URL: `http://localhost:5173/panel`
- Contraseña por defecto: `aerowise2026` (configurable vía `PANEL_PASSWORD` en `.env`)

### Funcionalidades

| Sección | Descripción |
|---------|-------------|
| **Dashboard** | Estadísticas: total de legs, consultas pendientes, descuento promedio, top rutas, gráfico por fecha |
| **Consultas** | Gestionar consultas: cambiar status (pendiente → contactado → cerrado), agregar notas |
| **Empty Legs** | Tabla con filtros, toggle de verificado/publicado, paginación |
| **Fuentes** | Ver fuentes de datos, última scrapeada, errores, disparar scraping manual |

### Django Admin

También disponible en `http://localhost:8000/admin/` (requiere superusuario).

---

## 🕷 Web Scrapers

Aerowise incluye 9 scrapers para operadores reales de aviación privada:

| Scraper | Operador | País | Estrategia |
|---------|----------|------|------------|
| GlobeAir | globeair.com | Austria | Regex + ICAO codes |
| Avcon Jet | avconjet.at | Austria | mailto: subject parsing |
| ProAir | proair.de | Alemania | HTML table parsing |
| Gestair | grupogestair.es | España | ASP.NET login + CSRF |
| Luxaviation | luxaviation.com | Luxemburgo | Multi-strategy (cards, tables) |
| Vacant Seat | vacantseat.com | UK | Cards/tables + fallback regex |
| Feeling Air | feelingair.com.ar | Argentina | Cards + route extraction |
| Jets Partners | jets.partners | Italia | Cards + aircraft extraction |
| Pacific Ocean | pacific-ocean.com.ar | Argentina | Generic card parsing |

### Ejecutar scraping manualmente

```bash
# Ver fuentes disponibles
python manage.py scrape_flights --list

# Scrapear una fuente específica
python manage.py scrape_flights --source "GlobeAir"

# Scrapear todas las fuentes activas
python manage.py scrape_flights
```

---

## ⚙️ Variables de Entorno

Copiar `backend/.env.example` → `backend/.env`:

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DEBUG` | `True` | Modo debug de Django |
| `SECRET_KEY` | insecure-key | Clave secreta (cambiar en producción) |
| `PANEL_PASSWORD` | `aerowise2026` | Contraseña del panel |
| `ALLOWED_HOSTS` | `*` | Hosts permitidos |
| `DATABASE_URL` | (vacío = SQLite) | URL de PostgreSQL |
| `REDIS_URL` | `redis://localhost:6379/0` | Broker de Celery |
| `EMAIL_HOST` | `localhost` | Servidor SMTP |
| `EMAIL_PORT` | `587` | Puerto SMTP |
| `EMAIL_HOST_USER` | (vacío) | Usuario SMTP |
| `EMAIL_HOST_PASSWORD` | (vacío) | Contraseña SMTP |

---

## 📁 Estructura del Proyecto

```
aerowise/
├── backend/
│   ├── config/              # Configuración Django
│   │   ├── settings.py      # Settings principal
│   │   ├── urls.py          # URLs raíz
│   │   ├── celery.py        # Configuración Celery
│   │   └── wsgi.py / asgi.py
│   ├── flights/             # App principal
│   │   ├── models.py        # Operator, Airport, Aircraft, Flight, EmptyLeg, Inquiry
│   │   ├── views.py         # Endpoints públicos + panel + CRUD ViewSets
│   │   ├── serializers.py   # Serializers DRF
│   │   ├── urls.py          # Rutas de API
│   │   ├── admin.py         # Django Admin
│   │   ├── tasks.py         # Tareas Celery (scraping, expiración)
│   │   ├── management/commands/
│   │   │   ├── load_airports.py    # Cargar 85+ aeropuertos
│   │   │   ├── seed_aircraft.py    # Cargar 30 aeronaves
│   │   │   ├── seed_sources.py     # Cargar 11 operadores/fuentes
│   │   │   ├── seed_demo_legs.py   # Crear 50 empty legs demo
│   │   │   ├── seed_inquiries.py   # Crear consultas demo
│   │   │   └── scrape_flights.py   # CLI para scraping manual
│   │   └── scrapers/        # 9 scrapers para operadores
│   │       ├── base.py      # Clase base con helpers
│   │       ├── registry.py  # Registro nombre→scraper
│   │       └── *.py         # Scrapers individuales
│   ├── notifications/       # Alertas por email
│   │   ├── models.py        # AlertSubscription, NotificationLog
│   │   ├── views.py         # subscribe/unsubscribe
│   │   └── tasks.py         # Envío de emails Celery
│   ├── requirements.txt
│   ├── .env.example
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Rutas principales
│   │   ├── api.js           # Cliente API (axios)
│   │   ├── main.jsx         # Punto de entrada
│   │   ├── index.css        # Tailwind + estilos custom
│   │   ├── components/      # Componentes reutilizables
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── EmptyLegCard.jsx
│   │   │   ├── InquiryModal.jsx
│   │   │   ├── SubscribeForm.jsx
│   │   │   └── PanelLogin.jsx
│   │   ├── pages/           # Páginas
│   │   │   ├── LandingPage.jsx      # Página pública
│   │   │   ├── PanelDashboard.jsx   # Dashboard admin
│   │   │   ├── PanelEmptyLegs.jsx   # Gestión empty legs
│   │   │   ├── PanelInquiries.jsx   # Gestión consultas
│   │   │   └── PanelSources.jsx     # Gestión fuentes
│   │   ├── context/
│   │   │   └── AuthContext.jsx      # Autenticación panel
│   │   └── layouts/
│   │       └── PanelLayout.jsx      # Layout del panel
│   ├── package.json
│   ├── vite.config.js       # Proxy /api → :8000
│   ├── tailwind.config.js
│   └── index.html
└── README.md
```

---

## Modelos de Datos

### Flights App

| Modelo | Campos Principales | Descripción |
|--------|-------------------|-------------|
| **Operator** | name, company_type (operator/broker), country, city, website | Operadores de aviación |
| **Airport** | icao, iata, name, city, country, lat, lng | 85+ aeropuertos precargados |
| **Aircraft** | model, manufacturer, category, max_passengers, range_km | Tipos de aeronaves |
| **FlightSource** | name, source_type, operator, url, scrape_interval, errors | Fuentes de datos/scraping |
| **Flight** | source, origin, destination, departure_time, status | Vuelos trackeados |
| **EmptyLeg** | origin, destination, departure_date, price_usd, discount_%, status, verified, published | Empty legs — modelo principal |
| **Inquiry** | empty_leg, name, email, phone, passengers, status (pending/contacted/closed) | Consultas de usuarios |

### Notifications App

| Modelo | Campos Principales | Descripción |
|--------|-------------------|-------------|
| **AlertSubscription** | email, origin/dest keywords, max_price, frequency | Suscripciones de alerta |
| **NotificationLog** | subscription, empty_leg, sent_at | Registro de notificaciones enviadas |

---

## 🌐 Deploy Gratis — Opciones de Hosting

### Opción 1: Render.com (⭐ Recomendado)

**Backend (Django):**
- Tipo: **Web Service** (free tier)
- Build: `pip install -r requirements.txt && python manage.py migrate && python manage.py load_airports && python manage.py seed_aircraft && python manage.py seed_sources && python manage.py seed_demo_legs`
- Start: `gunicorn config.wsgi:application`
- PostgreSQL gratis incluido
- Variables de entorno en el dashboard

**Frontend (React):**
- Tipo: **Static Site** (free tier)
- Build: `npm run build`
- Publish: `dist`
- Redirect rule: `/* → /index.html` (para SPA)

**Redis:** Usar el Redis gratis de Render o [Upstash](https://upstash.com)

**Pasos:**
1. Crear cuenta en [render.com](https://render.com)
2. Conectar repo de GitHub
3. Crear **PostgreSQL** → copiar Internal Database URL
4. Crear **Web Service** → configurar variables de entorno
5. Crear **Static Site** para React

> Para producción en Render, agregar `gunicorn` al `requirements.txt`:
> ```
> gunicorn>=21.0
> whitenoise>=6.5
> ```
> Y agregar `'whitenoise.middleware.WhiteNoiseMiddleware'` después de `SecurityMiddleware` en `settings.py`.

---

### Opción 2: Railway.app

- PostgreSQL + Redis incluidos en free tier
- Deploy automático desde GitHub
- CLI: `railway up`
- Free tier: 500 horas/mes

**Pasos:**
1. Instalar CLI: `npm install -g @railway/cli`
2. `railway login`
3. `railway init` en cada carpeta (backend/frontend)
4. Agregar PostgreSQL y Redis desde el dashboard
5. Configurar variables de entorno

---

### Opción 3: Vercel (Frontend) + Render (Backend)

**Frontend en Vercel:**
```bash
cd frontend
npx vercel
# Framework: Vite
# Build: npm run build
# Output: dist
```

**Backend en Render:**
- Mismo setup que Opción 1

**Nota:** Cambiar `vite.config.js` para apuntar al backend en producción:
```js
// En producción, usar la URL del backend de Render
proxy: {
  '/api': {
    target: process.env.VITE_API_URL || 'http://localhost:8000',
    changeOrigin: true,
  },
},
```

---

### Opción 4: Fly.io

- Free tier con 3 máquinas compartidas
- PostgreSQL y Redis disponibles
- Deploy con Dockerfile

```bash
# Backend
cd backend
fly launch
fly postgres create
fly deploy

# Frontend (como static site)
cd frontend
npm run build
fly launch  # usar Dockerfile con nginx
```

---

### Opción 5: PythonAnywhere (Solo Backend)

- Free tier con 1 web app
- No necesita Redis (usar SQLite como broker de Celery con `django-celery-results`)
- Ideal para probar solo la API
- No soporta Celery workers en free tier

**Pasos:**
1. Crear cuenta en [pythonanywhere.com](https://www.pythonanywhere.com)
2. Subir código o clonar desde GitHub
3. Crear web app → Manual Config → Python 3.10
4. Configurar WSGI apuntando a `config.wsgi`
5. Configurar virtualenv y variables de entorno

---

### Comparativa Rápida

| Plataforma | Backend | Frontend | DB Gratis | Redis Gratis | Dificultad |
|------------|---------|----------|-----------|--------------|------------|
| **Render** | ✅ | ✅ | ✅ PostgreSQL | ✅ | ⭐ Fácil |
| **Railway** | ✅ | ✅ | ✅ PostgreSQL | ✅ | ⭐ Fácil |
| **Vercel + Render** | ✅ | ✅ | ✅ PostgreSQL | ✅ | ⭐⭐ Media |
| **Fly.io** | ✅ | ✅ | ✅ PostgreSQL | ✅ | ⭐⭐⭐ Avanzada |
| **PythonAnywhere** | ✅ | ❌ | ✅ SQLite | ❌ | ⭐ Fácil |

---

### Preparar para Producción

Antes de hacer deploy, actualizar `backend/.env`:

```env
DEBUG=False
SECRET_KEY=una-clave-secreta-muy-larga-y-segura-aqui
PANEL_PASSWORD=tu-contraseña-segura
ALLOWED_HOSTS=tu-dominio.onrender.com,tu-dominio.com
DATABASE_URL=postgres://user:pass@host:5432/dbname
REDIS_URL=redis://default:pass@host:6379/0
```

Agregar al `requirements.txt` para producción:

```
gunicorn>=21.0
whitenoise>=6.5
```

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crear una rama: `git checkout -b feature/nueva-funcionalidad`
3. Hacer cambios y commit: `git commit -m "Agregar nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear un Pull Request

---

## 📄 Licencia

MIT License — libre para uso personal y comercial.

---

> **Aerowise** — Vuelos privados al alcance de todos. ✈️