"""Configuración central de AUTOCOR.

Corrección de seguridad: desacoplamiento de credenciales sensibles.
Las credenciales de la base de datos ya no están hardcodeadas en el código
(se eliminó el uso de usuario/contraseña 'root'/'root'). Se leen en tiempo de
ejecución desde variables de entorno cargadas con python-dotenv a partir del
archivo .env local, que está excluido del repositorio mediante .gitignore.

Para configurar un entorno nuevo, copiar .env.example como .env y completar
DB_HOST, DB_PORT, DB_NAME, DB_USER y DB_PASSWORD. Si faltan DB_USER o
DB_PASSWORD, la aplicación se detiene con un mensaje explicativo en lugar de
recurrir a valores por defecto inseguros.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Cargar variables desde el archivo .env ubicado junto a este módulo,
# independientemente del directorio desde el que se ejecute la aplicación.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Variables obligatorias: no se usan valores por defecto para credenciales.
_REQUERIDAS = ("DB_USER", "DB_PASSWORD")
_faltantes = [var for var in _REQUERIDAS if not os.getenv(var)]
if _faltantes:
    raise RuntimeError(
        "Faltan variables de entorno obligatorias: "
        + ", ".join(_faltantes)
        + ". Copie .env.example como .env y complete los datos de conexión."
    )

# Configuración de la Base de Datos MySQL
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'SistemaAutocor'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': int(os.getenv('DB_PORT', '3306'))
}

# Constantes de configuración de la interfaz
APP_TITLE = "AUTOCOR - Sistema de Gestión de Taller y Repuestera"
APP_GEOMETRY = "1100x650"