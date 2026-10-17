# Sistema de Gestión para Repuestera y Taller Multimarca "Autocor"

El proyecto de **InnovaCore Tech** consiste en el desarrollo de un Sistema de Gestión para un taller mecánico y comercio de repuestos automotores, denominado **Autocor**.
La aplicación permite administrar y organizar de manera centralizada la información relacionada con clientes, vehículos, órdenes de trabajo, servicios realizados, ventas y stock de repuestos.

## Estado Actual del Proyecto

* **Arquitectura modular:** Separación de responsabilidades organizada en paquetes (`gui/`, `database/`, `utils/`).
* **Modelo relacional:** Implementación de las 4 entidades requeridas (`Cliente`, `Vehiculo`, `Repuesto`, `Orden_de_Trabajo`) y la tabla asociativa (`Orden_Utiliza_Repuesto`).
* **Motor de base de datos:** Conexión exclusiva a **MySQL** mediante sentencias parametrizadas.
* **Interfaz Gráfica:** Construida en Python con **Tkinter**, incorporando Dashboard con indicadores operativos, gestión de entidades y registro de órdenes de trabajo.


## Tipo de Proyecto

Proyecto tecnológico y socioeconómico enfocado en desarrollar un sistema de software para mejorar la gestión de una PyME. Su finalidad es centralizar la administración de clientes, vehículos, órdenes de trabajo, servicios realizados, ventas y stock de repuestos para reducir errores, agilizar tareas y optimizar la rentabilidad.

## Problemática y Necesidades

Autocor es una PyME de Córdoba Capital dedicada a la reparación y a la venta de repuestos automotores. Actualmente, gran parte de su información se administra de forma manual (turnos por teléfono, control de stock no centralizado). Esta situación provoca demoras en la atención, errores administrativos, faltantes de repuestos y dificulta conocer con precisión los ingresos y costos del negocio.

## Roles de Usuario del Sistema

* **Propietario o dueño:** Acceso integral a la información, métricas principales, ventas y stock.
* **Administrativo:** Registro y actualización de datos de clientes, vehículos y órdenes de trabajo.
* **Vendedor:** Consulta de stock disponible, historial de operaciones y registro de ventas de mostrador.
* **Mecánico:** Visualización de órdenes de trabajo y actualización del estado de las reparaciones (asociado a nivel de orden sin entidad independiente).

## Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Interfaz Gráfica:** Tkinter / ttk
* **Base de Datos:** MySQL
* **Control de Versiones:** Git & GitHub

## Instrucciones de Ejecución

1. Clonar el repositorio:
git clone https://github.com/mateoguero/Sistema-de-Gestion-AutoCor.git
cd Sistema-de-Gestion-AutoCor

2. Configurar la base de datos:
* Contar con una instancia de MySQL en ejecución en el puerto configurado (puerto 3307 por defecto).
* Verificar los parámetros de acceso en `database/connection.py`.

3. Iniciar la aplicación:
python main.py

## Modelo Prototipo y Estado de Desarrollo

* **Etapa actual:** El sistema se encuentra en fase de desarrollo activo bajo un modelo prototipo.
* **Ciclo de actualizaciones:** Se realizan iteraciones y actualizaciones constantes sobre el código base con el objetivo de alcanzar los requerimientos de la entrega final.
* **Empaquetado y Distribución:** El script de automatización o empaquetado (`empaquetado.py`) será liberado e integrado al repositorio una vez que el software supere de manera exitosa todas las pruebas de chequeo y validación correspondientes.

## Integrantes del Equipo (InnovaCore Tech)

* Aguero, Mateo Gabriel
* Balderrama, Juan Manuel
* Barrionuevo, Julian
* Carbajal, Naara
* Colombano, Lucila Gabriela
