# 👕 Urban Store

Tienda virtual de ropa construida como **monolito Django**: catálogo, carrito, envíos/pagos y cuentas de usuario.

![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-MariaDB-4479A1?logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)

## Módulos (`store_urban/apps`)

`productos` · `carrito` · `envios_y_pagos` · `usuario`

## Variables de entorno

Copia `.env.example` a `.env`. La configuración ya no tiene credenciales en el código.

| Variable | Descripción |
|---|---|
| `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` | Configuración de Django |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Conexión MySQL/MariaDB (**`DB_PASSWORD` es obligatoria**) |

## Cómo correrlo

### Con Docker

```bash
git clone https://github.com/JSRT23/Urban_Store.git
cd Urban_Store
cp .env.example .env
docker compose up --build        # web en http://localhost:8000, MariaDB 11.4 en el servicio db
```

### Sin Docker

Requiere Python 3.12 y un MySQL/MariaDB accesible, más `libmysqlclient-dev` para compilar `mysqlclient`.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd store_urban
export DB_PASSWORD=... DB_HOST=127.0.0.1
python manage.py migrate
python manage.py runserver
```

> 🔐 La contraseña de la base de datos que estaba escrita en `settings.py` fue sacada del código. Como estuvo en un repo público, **cámbiala** en tu servidor.
