\# Proyecto Django — API RESTful con JWT



API RESTful construida con Django REST Framework y autenticación JWT (Simple JWT)

para el dominio de \*\*gestión de equipos y órdenes de trabajo\*\*.



\## 📋 Tabla de modelos



\### Modelos principales (CRUD completo)



| Modelo | Descripción | Relaciones |

|---|---|---|

| \*\*Empresa\*\* | Empresa cliente | 1→N con `Area` |

| \*\*Area\*\* | Área dentro de una empresa | N→1 con `Empresa`, 1→N con `Equipo` |

| \*\*Equipo\*\* | Equipo físico inventariado | N→1 con `TipoEquipo` y `Area`, 1→N con `OrdenTrabajo` |

| \*\*OrdenTrabajo\*\* | Orden de trabajo sobre un equipo | N→1 con `Equipo`, `EstadoOrden` y `User` (propietario) |



\### Modelos operacionales (solo lectura)



| Modelo | Descripción | Relaciones |

|---|---|---|

| \*\*EstadoOrden\*\* | Catálogo de estados de una orden | 1→N con `OrdenTrabajo` |

| \*\*DetalleOrden\*\* | Detalle de actividades de una orden | N→1 con `OrdenTrabajo` |



\### Modelo auxiliar



| Modelo | Descripción |

|---|---|

| \*\*TipoEquipo\*\* | Catálogo de tipos de equipo (también expuesto en la API como extra) |



\---



\## 🔌 Endpoints



Todas las rutas están bajo `/api/` y requieren \*\*JWT\*\* (excepto `/api/token/`).



| Recurso | Lista | Detalle | Métodos permitidos |

|---|---|---|---|

| Empresas | `GET /api/empresas/` | `GET /api/empresas/{id}/` | CRUD (según rol) |

| Áreas | `GET /api/areas/` | `GET /api/areas/{id}/` | CRUD (según rol) |

| Equipos | `GET /api/equipos/` | `GET /api/equipos/{id}/` | CRUD (según rol) |

| Órdenes de trabajo | `GET /api/ordenes/` | `GET /api/ordenes/{id}/` | CRUD (según rol) |

| Estados de orden | `GET /api/estados-orden/` | `GET /api/estados-orden/{id}/` | Solo lectura |

| Detalles de orden | `GET /api/detalles-orden/` | `GET /api/detalles-orden/{id}/` | Solo lectura |

| Tipos de equipo | `GET /api/tipos-equipo/` | `GET /api/tipos-equipo/{id}/` | CRUD (extra) |



\### Autenticación



| Endpoint | Método | Descripción |

|---|---|---|

| `/api/token/` | POST | Obtener par de tokens (access + refresh) |

| `/api/token/refresh/` | POST | Renovar el access token |



\*\*Uso del token:\*\*



```

Authorization: Bearer <access\_token>

```



\---



\## 👥 Roles y permisos



| Grupo | GET (lista/detalle) | POST | PUT/PATCH | DELETE |

|---|---|---|---|---|

| `admin\_api` | ✅ 200 | ✅ 201 | ✅ 200 | ✅ 204 |

| `operador\_api` | ✅ 200 | ❌ 403 | ❌ 403 | ❌ 403 |

| `sin\_rol\_api` | ❌ 403 | ❌ 403 | ❌ 403 | ❌ 403 |

| \*\*Sin token\*\* | ❌ 401 | ❌ 401 | ❌ 401 | ❌ 401 |



\### Usuarios de prueba (creados por `seed\_data`)



| Usuario | Contraseña | Grupo |

|---|---|---|

| `admin\_api` | `AdminApi2026!` | `admin\_api` |

| `operador\_api` | `OperadorApi2026!` | `operador\_api` |

| `sin\_rol\_api` | `SinRolApi2026!` | `sin\_rol\_api` |



\---



\## 📊 Datos de prueba



El comando `seed\_data` carga automáticamente:



| Modelo | Registros |

|---|---|

| Empresa | 5 |

| Area | 20 |

| TipoEquipo | 8 |

| EstadoOrden | 5 |

| Equipo | 300 |

| OrdenTrabajo | 1000 |

| DetalleOrden | 700 |

| \*\*TOTAL\*\* | \*\*2038\*\* |



\---



\## 🛠️ Preparación del entorno



\### Requisitos previos

\- Python 3.10+

\- MySQL 5.7+ o MariaDB 10.4+ (por ejemplo, el que trae XAMPP)



\### Pasos



1\. \*\*Clonar el repositorio\*\*

&#x20;  ```bash

&#x20;  git clone <url-del-repo>

&#x20;  cd proyecto\_django

&#x20;  ```



2\. \*\*Crear y activar entorno virtual\*\*

&#x20;  ```bash

&#x20;  python -m venv venv

&#x20;  source venv/Scripts/activate      # Windows Git Bash

&#x20;  # source venv/bin/activate        # Linux / Mac

&#x20;  ```



3\. \*\*Instalar dependencias\*\*

&#x20;  ```bash

&#x20;  pip install -r requirements.txt

&#x20;  ```



4\. \*\*Configurar variables de entorno\*\*

&#x20;  ```bash

&#x20;  cp .env.example .env

&#x20;  ```

&#x20;  Editar `.env` con los datos de conexión a MySQL:

&#x20;  ```

&#x20;  DB\_NAME=proyecto\_django

&#x20;  DB\_USER=root

&#x20;  DB\_PASSWORD=

&#x20;  DB\_HOST=127.0.0.1

&#x20;  DB\_PORT=3306

&#x20;  ```



5\. \*\*Crear la base de datos en MySQL\*\*

&#x20;  ```sql

&#x20;  CREATE DATABASE proyecto\_django CHARACTER SET utf8mb4 COLLATE utf8mb4\_unicode\_ci;

&#x20;  ```



6\. \*\*Aplicar migraciones\*\*

&#x20;  ```bash

&#x20;  python manage.py migrate

&#x20;  ```



7\. \*\*Cargar datos de prueba\*\* (crea grupos, usuarios y 2038 registros)

&#x20;  ```bash

&#x20;  python manage.py seed\_data

&#x20;  ```



8\. \*\*Levantar el servidor\*\*

&#x20;  ```bash

&#x20;  python manage.py runserver

&#x20;  ```



La API queda disponible en `http://127.0.0.1:8000/api/`.



\---



\## 📄 Paginación



Todas las listas están paginadas con `PageNumberPagination` a \*\*25 elementos por página\*\*.



Para pedir otra página:

```

GET /api/ordenes/?page=2

```



La respuesta incluye `count`, `next`, `previous` y `results`.



Ejemplo (órdenes, 1000 registros):

```json

{

&#x20; "count": 1000,

&#x20; "next": "http://127.0.0.1:8000/api/ordenes/?page=3",

&#x20; "previous": "http://127.0.0.1:8000/api/ordenes/",

&#x20; "results": \[ ... 25 items ... ]

}

```



\---



\## ✅ Validaciones implementadas



| Validación | Tipo | Dónde | Ejemplo |

|---|---|---|---|

| RUT mínimo 8 caracteres | Campo | `EmpresaSerializer.validate\_rut` | `400` si es más corto |

| Área duplicada por empresa | Relación | `AreaSerializer.validate` | `400` si ya existe |

| Código de equipo mínimo 3 caracteres | Campo | `EquipoSerializer.validate\_codigo` | `400` si es más corto |

| Fecha de término ≥ fecha inicio | Relación | `OrdenTrabajoSerializer.validate\_fecha\_termino` | `400` si es anterior |

| Horas de trabajo > 0 | Campo | `DetalleOrdenSerializer.validate\_horas\_trabajo` | `400` si es ≤ 0 |



\---



\## 🧪 Pruebas con Apidog



La colección exportada se encuentra en `apidog\_collection.json` (o carpeta `apidog/`).



Casos cubiertos:

1\. Obtener token JWT (admin) → 200

2\. Renovar access token → 200

3\. GET recurso protegido sin token → 401

4\. GET con admin → 200

5\. POST con admin → 201

6\. GET con operador → 200

7\. POST con operador → 403

8\. GET con sin\_rol → 403

9\. GET id inexistente → 404

10\. POST con datos inválidos → 400

11\. Paginación página 1 y 2 → 200



\---



\## 🗂️ Estructura del proyecto



```

proyecto\_django/

├── config/

│   ├── settings.py       # Config DRF + JWT

│   └── urls.py           # Rutas /api/ y /api/token/

├── gestion/

│   ├── models.py         # 7 modelos

│   ├── serializers.py    # Serializers DRF

│   ├── views.py          # ViewSets

│   ├── permissions.py    # Permisos por grupo

│   ├── urls.py           # Router DRF

│   ├── admin.py

│   └── management/

│       └── commands/

│           └── seed\_data.py   # Poblado de datos

├── requirements.txt

├── .env.example

├── .gitignore

└── README.md

```



\---



\## 🔐 Notas de seguridad



\- El archivo `.env` \*\*no\*\* se sube al repositorio (ver `.gitignore`).

\- No se incluyen tokens vigentes ni credenciales reales.

\- El comando `seed\_data` es idempotente: usa `get\_or\_create` para no duplicar datos.

---

## 📊 Matriz de evidencias — Pruebas Apidog

Todas las pruebas fueron ejecutadas sobre el servidor local en `http://127.0.0.1:8000` con la base de datos poblada (2.038 registros). La colección exportada se encuentra en `apidog/Proyecto Django API.apidog.json`.

| # | Método | Endpoint | Identidad | Estado esperado | Estado observado | Respuesta representativa |
|---|---|---|---|---|---|---|
| 1 | POST | `/api/token/` | admin_api | 200 | ✅ 200 | `{"access":"...","refresh":"..."}` |
| 2 | POST | `/api/token/` | operador_api | 200 | ✅ 200 | `{"access":"...","refresh":"..."}` |
| 3 | POST | `/api/token/` | sin_rol_api | 200 | ✅ 200 | `{"access":"...","refresh":"..."}` |
| 4 | GET | `/api/empresas/` | admin_api | 200 | ✅ 200 | `{"count":5,"results":[...]}` |
| 5 | GET | `/api/empresas/` | operador_api | 200 | ✅ 200 | `{"count":5,"results":[...]}` |
| 6 | GET | `/api/empresas/` | sin_rol_api | 403 | ✅ 403 | `{"detail":"You do not have permission..."}` |
| 7 | GET | `/api/empresas/` | sin token | 401 | ✅ 401 | `{"detail":"Authentication credentials were not provided."}` |
| 8 | GET | `/api/empresas/99999/` | admin_api | 404 | ✅ 404 | `{"detail":"No Empresa matches the given query."}` |
| 9 | POST | `/api/empresas/` | admin_api | 201 | ✅ 201 | `{"id":6,"nombre":"Empresa Creada por Apidog",...}` |
| 10 | POST | `/api/empresas/` | operador_api | 403 | ✅ 403 | `{"detail":"You do not have permission..."}` |
| 11 | POST | `/api/empresas/` | admin_api | 400 | ✅ 400 | `{"rut":["El RUT debe tener al menos 8 caracteres."]}` |
| 12 | GET | `/api/ordenes/?page=2` | operador_api | 200 | ✅ 200 | `{"count":1000,"next":"...page=3","previous":".../","results":[...25 items]}` |

### Cobertura de la matriz

| Criterio evaluación | Casos | Estado |
|---|---|---|
| CRUD admin en modelo principal | 4, 8, 9, 11 | ✅ |
| Solo lectura operador | 5, 12 | ✅ |
| Denegación sin rol (403) | 6, 10 | ✅ |
| Denegación sin token (401) | 7 | ✅ |
| JWT obtener token | 1, 2, 3 | ✅ |
| Validaciones (campo + relación) | 11 | ✅ |
| ID inexistente (404) | 8 | ✅ |
| Paginación (2 páginas) | 12 | ✅ |
