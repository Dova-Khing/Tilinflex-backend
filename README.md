# Sistema de Gestión de Plataforma de streaming - API REST

Este proyecto implementa un sistema sobre reproducir contenido, recomendar el contenido mas visto y una busqueda por género
utilizando **API REST** con conexión a **PostgreSQL** (Neon Database), containerizado con **Docker**.  
Incluye operaciones CRUD.


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

