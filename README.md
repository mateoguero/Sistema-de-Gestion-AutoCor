# Sistema de Gestión para Repuestera y Taller Multimarca "Autocor"

El proyecto de **InnovaCore Tech** consiste en el desarrollo de un Sistema de Gestión para un taller mecánico y comercio de repuestos automotores, denominado **Autocor**. La aplicación permite administrar y organizar de manera centralizada la información relacionada con clientes, vehículos, órdenes de trabajo, servicios realizados, ventas y stock de repuestos.

---

## Estado Actual del Proyecto
- **Arquitectura modular:** Separación limpia de responsabilidades organizadas en paquetes (`gui/`, `database/`, `utils/`).
- **Modelo relacional (3FN):** Implementación de las 4 entidades requeridas (`Cliente`, `Vehiculo`, `Repuesto`, `Orden_de_Trabajo`) y la tabla asociativa (`Orden_Utiliza_Repuesto`).
- **Integridad y Lógica en Motor:** Control de inventario en tiempo real mediante el disparador `trg_control_stock` y restricciones formales de dominio (`CHECK`, `FOREIGN KEY`).
- **Seguridad Informática:** Consultas 100% parametrizadas con marcadores `%s` (prevención de Inyección SQL), principio de menor privilegio con rol `app_autocor` y desacoplamiento de credenciales con variables de entorno (`.env`).
- **Interfaz Gráfica:** Construida en Python con Tkinter / ttk, incorporando Dashboard operativo en tiempo real, tablas interactivas (`Treeview`) y manejo de validaciones mediante cuadros de diálogo (`messagebox`).

---

## Tipo de Proyecto
Proyecto tecnológico y socioeconómico enfocado en desarrollar un sistema de software para mejorar la gestión operativa y comercial de una PyME, agilizando tareas administrativas, evitando faltantes de inventario y optimizando la rentabilidad.

---

## Problemática y Necesidades
Autocor es una PyME de Córdoba Capital dedicada a la reparación y la venta de repuestos automotores. Tradicionalmente, gran parte de su información se administraba de forma manual (turnos por teléfono, registros aislados y control de stock no centralizado). Esta situación provocaba demoras en la atención, errores administrativos, quiebres de inventario y falta de trazabilidad en las reparaciones realizadas.

---

## Roles de Usuario del Sistema
- **Propietario o dueño:** Acceso integral a la información, métricas principales, ventas y stock.
- **Administrativo:** Registro y actualización de datos de clientes, vehículos y órdenes de trabajo.
- **Vendedor:** Consulta de stock disponible, historial de operaciones y registro de ventas de mostrador (asociadas al cliente genérico *Consumidor Final*).
- **Mecánico:** Visualización de órdenes de trabajo y actualización del estado de las reparaciones (responsable asignado a nivel de orden).

---

## Tecnologías Utilizadas
- **Lenguaje:** Python 3.10+
- **Interfaz Gráfica:** Tkinter / ttk
- **Base de Datos:** MySQL / MariaDB (conector oficial `mysql-connector-python`)
- **Gestión de Entorno:** `python-dotenv`
- **Control de Versiones:** Git y GitHub

---

## Instrucciones de Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone [https://github.com/mateoguero/Sistema-de-Gestion-AutoCor.git](https://github.com/mateoguero/Sistema-de-Gestion-AutoCor.git)
cd Sistema-de-Gestion-AutoCor
