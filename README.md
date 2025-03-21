# twss-geonode

Repositorio que extiende GeoNode con un módulo personalizado para actualizar dinámicamente shapefiles y reflejarlos en GeoServer.

---

## 📌 Objetivo

Este proyecto tiene como propósito mantener actualizados datasets de puntos en un mapa, generando y publicando shapefiles periódicamente desde una base de datos.

---

## 🧱 Estructura del Proyecto

Dentro de `/geonode/geonode_updater` se encuentra el codigo de la extension del proyecto.

---

## ⚙️ Instalación local


1. (Requisito) milleniumdb tiene que estar corriendo en el puerto 1234.
2. generar archivo .env, a partir de .env.sample o corriendo el script de `create-envfile.py`.
3. correr `docker-compose build --no-cache` para preparar el proyecto.
4. correr `docker-compose up -d` para levantar el proyecto.
4. acceder a `http://localhost/` para ver el proyecto.

### Prerrequisitos

- Docker
- Docker Compose
- Python 3.8
- Base de datos milleniumdb corriendo en el puerto 1234


### Clonar el repositorio

```bash
git clone https://github.com/JulietaRey/twss-geonode.git
cd twss-geonode

```

### Uso / Funcionamiento

1. Acceder a la url `http://localhost/` para ver el portal de geonode.
2. Usuario y contraseña por defecto: `admin` / `admin`
3. Dentro de http://localhost/en-us/admin/django_q/ puedes ver los jobs que se están ejecutando.
4. Dentro de http://localhost/catalogue/#/datasets puede verse el dataset actualizado cada 5 minutos