# Sistema de Gestión de Plataforma de streaming - API REST

Este proyecto implementa un sistema sobre reproducir contenido, recomendar el contenido mas visto y una busqueda por género
utilizando **API REST** con conexión a **PostgreSQL** (Neon Database), containerizado con **Docker**.  
Incluye operaciones CRUD.


## Autenticación JWT

La API usa **JSON Web Tokens (JWT)** con el algoritmo **HS256** para proteger rutas que requieren sesión activa.

### Flujo de autenticación

```
1. POST /auth/login  →  { email, contrasena }
2. Respuesta         →  { access_token, token_type: "bearer" }
3. Rutas protegidas  →  Header: Authorization: Bearer <access_token>
```

### Estructura del token

El token contiene los siguientes claims:

| Campo | Descripción |
|---|---|
| `sub` | UUID del usuario |
| `nombre_usuario` | Nombre de usuario |
| `rol` | Rol del usuario en el sistema |
| `iat` | Timestamp de emisión |
| `exp` | Timestamp de expiración |

### Variables de entorno requeridas

Agregar al archivo `.env`:

```env
JWT_SECRET_KEY=<cadena-larga-y-aleatoria>      # Obligatorio en producción
JWT_ALGORITHM=HS256                             # Opcional, por defecto HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60                  # Opcional, por defecto 60 min (rango: 5–1440)
```

> **Buenas prácticas:** Generar la clave con `openssl rand -hex 32`. Nunca usar la clave por defecto en producción.

### Validación en rutas protegidas

Cada solicitud a una ruta protegida verifica que:
1. El header `Authorization: Bearer <token>` esté presente.
2. El token sea válido y no haya expirado.
3. El usuario exista y esté activo en la base de datos.

Si falla alguna de estas comprobaciones, la API responde con `401 Unauthorized` o `403 Forbidden`.

---

## Política CORS

La API configura **CORS (Cross-Origin Resource Sharing)** para permitir el consumo desde frontends específicos.

### Orígenes permitidos por defecto (desarrollo)

```
http://localhost:3000
http://localhost:5173
http://127.0.0.1:3000
http://127.0.0.1:5173
```

### Configuración en producción

Definir los orígenes del frontend en el `.env` (separados por coma):

```env
CORS_ORIGINS=https://mi-frontend.com,https://www.mi-frontend.com
```

> **Importante:** No se permite `*` como origen cuando `allow_credentials=True`. Siempre se deben listar los orígenes explícitamente en producción.

### Métodos y cabeceras habilitadas

| Tipo | Valores permitidos |
|---|---|
| Métodos | `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS` |
| Cabeceras | `Authorization`, `Content-Type`, `Accept` |
| Credenciales | Habilitadas (`allow_credentials: true`) |

---

## Recursos Adicionales

### Documentación Oficial
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Neon Documentation](https://neon.tech/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Python Documentation](https://docs.python.org/3/)

## Instalación

Para iniciar el proyecto debes:

1. **Requisitos previos:**
   Asegúrate de tener instalado en tu máquina:
   - [Docker](https://www.docker.com/)
   - [Python](https://www.python.org/)

2. **Configurar variables de entorno:**
   Crear un archivo `.env` en la carpeta **API** del proyecto:
```env
   DATABASE_URL=postgresql://usuario:contraseña@host:puerto/database
```

3. **Levantar el contenedor Docker:**
   Abre la aplicación Docker. Luego ejecuta:
```bash
   docker compose up -d
```
   Esto construirá la imagen y levantará los servicios (FastAPI + Uvicorn).

4. **Iniciar el servidor (dentro del contenedor):**
   El punto de entrada principal es `main.py`. Docker lo ejecuta automáticamente al levantar el contenedor. Si necesitas correrlo manualmente dentro del contenedor:
```bash
   docker exec -it  python main.py
```

El servidor se ejecutará en `http://localhost:8000`

## Documentación de la API

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## CI/CD Pipeline

El proyecto cuenta con un pipeline de integración continua configurado con **GitHub Actions** (`.github/workflows/ci.yml`), que se ejecuta automáticamente en cada `push` o `pull request`.

### Jobs

**1. Lint y formato de código**
Verifica la calidad y consistencia del código usando **Ruff**:
- Detecta errores de linting
- Verifica que el formato sea correcto

**2. Verificación de esquema de base de datos**
Levanta un contenedor temporal de **PostgreSQL 16** y valida que el esquema de la base de datos sea correcto ejecutando `scripts/verify_db.py`.

**3. Build de imagen Docker**
Construye la imagen Docker desde `docker/Dockerfile` para verificar que el build no tenga errores. El contenedor se destruye automáticamente al finalizar el job.

## Endpoints Principales

### Autenticación (`/auth`)
- `POST /auth/login` - Iniciar sesión
- `POST /auth/crear-admin` - Crear usuario administrador
- `GET /auth/verificar/{usuario_id}` - Verificar usuario
- `GET /auth/estado` - Estado del sistema

### Usuarios (`/usuarios`)
- `GET /usuarios/` - Listar usuarios
- `GET /usuarios/{usuario_id}` - Obtener usuario por ID
- `GET /usuarios/email/{email}` - Obtener usuario por email
- `GET /usuarios/username/{nombre_usuario}` - Obtener usuario por nombre de usuario
- `POST /usuarios/` - Crear usuario
- `PUT /usuarios/{usuario_id}` - Actualizar usuario
- `DELETE /usuarios/{usuario_id}` - Eliminar usuario
- `PATCH /usuarios/{usuario_id}/desactivar` - Desactivar usuario
- `POST /usuarios/{usuario_id}/cambiar-contraseña` - Cambiar contraseña
- `GET /usuarios/admin/lista` - Listar administradores
- `GET /usuarios/{usuario_id}/es-admin` - Verificar si es admin

### Categorias (`/categorias`)
- `GET /categorias/` - Listar categoria
- `GET /categorias/{categoria_id}` - Obtener categoria por ID
- `GET /categorias/{categoria_nombre}` - Obtener categoria por nombre

### Géneros (`/generos`)
- `GET /generos/` - Listar género
- `GET /generos/{genero_id}` - Obtener género por ID
- `GET /generos/{genero_nombre}` - Obtener género por nombre

### Obras (`/obras`)
- `GET /obras/` - Listar obras
- `GET /obras/{obra_id}` - Obtener obra por ID
- `GET /obras/{obra_nombre}` - Obtener obra por nombre
- `POST /obras/` - Crear una obra
- `PUT /obras/{obra_id}` - Actualizar una obra
- `DELETE /obras/{obra_id}` - Eliminar una obra

### Historial de Reproducción (`/historial-reproduccion`)
- `GET /historial-reproduccion/` - Listar historial de reproduccion
- `GET /historial-reproduccion/{historial_id}` - Obtener registro por ID
- `GET /historial-reproduccion/{perfil_id}` - Obtener registro por Perfil ID
- `GET /historial-reproduccion/{obra_id}` - Obtener registro por Obra ID
- `POST /historial-reproduccion/` - Crear un registro de reproduccion
- `PUT /historial-reproduccion/{historial_id}` - Actualizar un registro

### Pefiles (`/perfiles`)
- `GET /perfiles/` - Listar perfiles
- `GET /perfiles/{perfil_id}` - Obtener perfil por ID
- `GET /perfiles/{perfil_nombre}` - Obtener perfil por nombre
- `POST /perfiles/` - Crear un perfil
- `PUT /perfiles/{perfil_id}` - Actualizar un perfil
- `DELETE /perfiles/{perfil_id}` - Eliminar un perfil

### Suscripciones (`/suscripciones`)
- `GET /suscripciones/` - Listar suscripciones
- `GET /suscripciones/{suscripcion_id}` - Obtener suscripción por ID
- `POST /suscripciones/` - Crear una suscripción
- `PUT /suscripciones/{suscripcion_id}` - Actualizar una suscripción

### Detalles-Suscripcion (`/detalles-suscripcion`)
- `GET /detalles-suscripcion/` - Listar detalles de las suscripciones
- `GET /detalles-suscripcion/{detalle_id}` - Obtener detalle por ID
- `GET /detalles-suscripcion/{suscripcion_id}` - Obtener detalle por Suscripcion ID
- `POST /detalles-suscripcion/` - Crear un detalle

