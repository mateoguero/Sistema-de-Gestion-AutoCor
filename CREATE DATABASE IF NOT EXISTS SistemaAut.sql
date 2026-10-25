CREATE DATABASE IF NOT EXISTS SistemaAutocor;
USE SistemaAutocor;

CREATE TABLE Cliente (
    Documento VARCHAR(20) PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Telefono VARCHAR(20),
    Email VARCHAR(100)
);

CREATE TABLE Repuesto (
    Codigo_Repuesto VARCHAR(50) PRIMARY KEY,
    Nombre_Repuesto VARCHAR(100) NOT NULL,
    Precio DECIMAL(10,2) NOT NULL CHECK (Precio >= 0),
    Stock INT NOT NULL DEFAULT 0 CHECK (Stock >= 0)
);

CREATE TABLE Vehiculo (
    Patente VARCHAR(10) PRIMARY KEY,
    Marca VARCHAR(50) NOT NULL,
    Modelo VARCHAR(50) NOT NULL,
    Anio INT,
    Documento_Cliente VARCHAR(20),
    FOREIGN KEY (Documento_Cliente) REFERENCES Cliente (Documento) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Orden_de_Trabajo (
    Id_Orden INT AUTO_INCREMENT PRIMARY KEY,
    Fecha DATE NOT NULL,
    Observacion TEXT,
    Descripcion_Servicio VARCHAR(200) NOT NULL,
    Costo_Mano_Obra DECIMAL(10,2) NOT NULL CHECK (Costo_Mano_Obra >= 0),
    Estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente',
    Patente_Vehiculo VARCHAR(10),
    Nombre_Mecanico VARCHAR(100), 
    FOREIGN KEY (Patente_Vehiculo) REFERENCES Vehiculo (Patente) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Orden_Utiliza_Repuesto (
    Id_Orden INT,
    Codigo_Repuesto VARCHAR(50),
    Cantidad INT NOT NULL CHECK (Cantidad > 0),
    PRIMARY KEY (Id_Orden, Codigo_Repuesto),
    FOREIGN KEY (Id_Orden) REFERENCES Orden_de_Trabajo(Id_Orden) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Codigo_Repuesto) REFERENCES Repuesto (Codigo_Repuesto) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Creación de roles de seguridad y asignación de permisos
CREATE ROLE 'admin_autocor';
GRANT ALL PRIVILEGES ON SistemaAutocor.* TO 'admin_autocor';

CREATE ROLE 'vendedor_autocor';
GRANT SELECT ON SistemaAutocor.Repuesto TO 'vendedor_autocor';
GRANT SELECT, INSERT, UPDATE ON SistemaAutocor.Orden_de_Trabajo TO 'vendedor_autocor';
GRANT SELECT, INSERT, UPDATE ON SistemaAutocor.Orden_Utiliza_Repuesto TO 'vendedor_autocor';

-- =====================================================================
-- CORRECCIÓN DE SEGURIDAD: PRINCIPIO DE MENOR PRIVILEGIO
-- ---------------------------------------------------------------------
-- La aplicación Python ya NO se conecta como 'root'. Utiliza el usuario
-- dedicado 'autocor_app', al que se le asigna el rol 'app_autocor'.
--
-- El rol 'app_autocor' posee únicamente permisos DML sobre SistemaAutocor:
--   SELECT, INSERT, UPDATE, DELETE
-- No se otorgan privilegios DDL (DROP, ALTER, CREATE, TRUNCATE, etc.),
-- de modo que un fallo o uso indebido de la aplicación no pueda
-- eliminar ni modificar la estructura de la base de datos.
--
-- Las credenciales reales se resguardan en el archivo .env local
-- (no versionado), leído por config.py mediante python-dotenv.
-- =====================================================================

-- Rol de aplicación con principio de menor privilegio:
-- solo operaciones DML, sin permisos DDL (DROP, ALTER, CREATE, etc.).
CREATE ROLE IF NOT EXISTS 'app_autocor';
GRANT SELECT, INSERT, UPDATE, DELETE ON SistemaAutocor.* TO 'app_autocor';

-- Usuario de aplicación (reemplaza el uso de root desde Python).
-- IMPORTANTE: reemplazar 'CAMBIAR_POR_PASSWORD_SEGURO' antes de ejecutar.
-- Esta clave debe coincidir con DB_PASSWORD definida en el archivo .env local.
-- No versionar la contraseña real en este script.
CREATE USER IF NOT EXISTS 'autocor_app'@'localhost' IDENTIFIED BY 'CAMBIAR_POR_PASSWORD_SEGURO';
GRANT 'app_autocor' TO 'autocor_app'@'localhost';
SET DEFAULT ROLE 'app_autocor' TO 'autocor_app'@'localhost';
FLUSH PRIVILEGES;

