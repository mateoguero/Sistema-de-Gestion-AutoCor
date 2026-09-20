-- creamos la base (por si no esta)
CREATE DATABASE IF NOT EXISTS SistemaAutocor;
USE SistemaAutocor;


-- arrancamos por las tablas fuertes que no dependen de otras

-- tabla clientes
CREATE TABLE Cliente (
    Documento VARCHAR(20) PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Telefono VARCHAR(20),
    Email VARCHAR(100)
);


CREATE TABLE Mecanico (
    Id_Mecanico INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Especialidad VARCHAR(100),
    Telefono VARCHAR(20)
);


-- catalogo de repuestos para el stock
CREATE TABLE Repuesto (
    Codigo_Repuesto VARCHAR(50) PRIMARY KEY,
    Nombre_Repuesto VARCHAR(100) NOT NULL,
    Precio DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL DEFAULT 0
);



-- tablas "hijo" (las que tienen claves foraneas)

CREATE TABLE Vehiculo (
    Patente VARCHAR(10) PRIMARY KEY,
    Marca VARCHAR(50) NOT NULL,
    Modelo VARCHAR(50) NOT NULL,
    Anio INT,
    
    Documento_Cliente VARCHAR(20), -- fk a cliente
    
    FOREIGN KEY (Documento_Cliente) REFERENCES Cliente(Documento) 
    ON DELETE RESTRICT ON UPDATE CASCADE
);


-- cabecera de la orden
CREATE TABLE Orden_de_Trabajo (
    Id_Orden INT AUTO_INCREMENT PRIMARY KEY,
    Fecha DATE NOT NULL,
    Observacion TEXT,
    Descripcion_Servicio VARCHAR(200) NOT NULL,
    
    Costo_Mano_Obra DECIMAL(10,2) NOT NULL,
    Estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente',
    
    Patente_Vehiculo VARCHAR(10), 
    Id_Mecanico INT,              
    
    -- vinculamos con el auto y quien lo atiende
    FOREIGN KEY (Patente_Vehiculo) REFERENCES Vehiculo(Patente) 
    ON DELETE RESTRICT ON UPDATE CASCADE,
    
    FOREIGN KEY (Id_Mecanico) REFERENCES Mecanico(Id_Mecanico) 
    ON DELETE RESTRICT ON UPDATE CASCADE
);



-- tabla intermedia para la relacion muchos a muchos (orden - repuesto)
-- OJO: le dejamos CASCADE al id_orden para q si se borra una orden no queden repuestos colgados
CREATE TABLE Orden_Utiliza_Repuesto (
    Id_Orden INT,
    Codigo_Repuesto VARCHAR(50),
    Cantidad INT NOT NULL,
    
    -- pk compuesta
    PRIMARY KEY (Id_Orden, Codigo_Repuesto),
    
    FOREIGN KEY (Id_Orden) REFERENCES Orden_de_Trabajo(Id_Orden) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    
    FOREIGN KEY (Codigo_Repuesto) REFERENCES Repuesto(Codigo_Repuesto) 
    ON DELETE RESTRICT ON UPDATE CASCADE
);