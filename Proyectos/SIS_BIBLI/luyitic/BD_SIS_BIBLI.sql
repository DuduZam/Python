-- Crear y usar la base de datos Biblioteca
CREATE DATABASE Biblioteca;
USE Biblioteca;

DROP DATABASE Biblioteca;

-- Tabla Usuario
-- Almacena información sobre los usuarios de la biblioteca.
CREATE TABLE Usuario (
    ID_Usuario INT PRIMARY KEY IDENTITY(1,1), -- Identificador único del usuario (clave primaria).	
    Nombre NVARCHAR(50) NOT NULL,              -- Nombre del usuario.
    Apellido NVARCHAR(50) NOT NULL,            -- Apellido del usuario.
    Correo NVARCHAR(100) UNIQUE NOT NULL,      -- Correo electrónico del usuario (único).
	Contraseña NVARCHAR(255) NOT NULL,         -- Contraseña del usuario (debe ser hasheada en la aplicación).
    Telefono NVARCHAR(20) NOT NULL,      -- Número de teléfono del usuario.
    Direccion NVARCHAR(200),                   -- Dirección del usuario.
	Puntaje INT DEFAULT 20 CHECK (PUNTAJE BETWEEN 0 AND 20),			-- Puntaje del usuario para si
    Rol NVARCHAR(13) NOT NULL CHECK (Rol IN ('Bibliotecario', 'Usuario')),				   -- Roles: Bibliotecario y Usuario
    Eliminado BIT DEFAULT 0                    -- Indica si el usuario ha sido eliminado (soft delete).
);

-- Tabla Libro
-- Almacena información sobre los libros disponibles en la biblioteca.
CREATE TABLE Libro (
	ID_Libro INT PRIMARY KEY IDENTITY(1,1),
    ISBN VARCHAR(20) UNIQUE NOT NULL,             -- Identificador único del libro (clave primaria).
    Titulo VARCHAR(200) NOT NULL,             -- Título del libro.
    Autor VARCHAR(100) NOT NULL,              -- Autor del libro.
    Editorial VARCHAR(100),                   -- Editorial del libro.
    Año_Publicacion INT CHECK (Año_Publicacion >= 1500 AND Año_Publicacion <= YEAR(GETDATE())), -- Año de publicación (entre 1500 y el año actual).
    Genero VARCHAR(50),                       -- Género del libro.
    Numero_Paginas INT CHECK (Numero_Paginas > 0), -- Número de páginas (debe ser mayor que 0).
	Cantidad_Total INT NOT NULL CHECK (Cantidad_Total >= 0),				--Stock Total de cuantos libros llego a la biblioteca
    Cantidad_Disponible INT NOT NULL CHECK (Cantidad_Disponible >= 0) AND CHECK (Cantidad_Disponible <= Cantidad_Total),				--Stock del Libros disponibles a prestamo siempre mayor o igual a 0
    Eliminado BIT DEFAULT 0,                   -- Indica si el libro ha sido eliminado (soft delete).
);


-- Tabla Prestamo
-- Registra los préstamos de libros realizados por los usuarios.
CREATE TABLE Prestamo (
    ID_Prestamo INT PRIMARY KEY IDENTITY(1,1), -- Identificador único del préstamo (clave primaria).
    ID_Usuario INT FOREIGN KEY REFERENCES Usuario(ID_Usuario), -- Usuario afectado que tiene préstamo.
	ID_Usuario_Cambio INT NOT NULL DEFAULT 0;			--Usuario que gestiona el prestamo.
    ID_Libro INT FOREIGN KEY REFERENCES Libro(ID_Libro), -- Libro prestado.
    Fecha_Prestamo DATE NOT NULL DEFAULT GETDATE(),              -- Fecha en que se realiza el préstamo.
    Fecha_Devolucion_Esperada DATE NOT NULL DEFAULT DATEADD(DAY, 14, GETDATE()),   -- Fecha esperada de devolución.
	Estado NVARCHAR(20) CHECK (Estado IN ('PRESTADO', 'DEVUELTO', 'PERDIDO')) NOT NULL DEFAULT 'PRESTADO', -- Estado por defecto 'Prestado' Estado del libro prestado
	Eliminado BIT DEFAULT 0                   -- Indica si el prestamo ha sido eliminado (soft delete).
);

-- Tabla Devolucion
-- Registra las devoluciones de libros realizadas por los usuarios.
CREATE TABLE Devolucion (
    ID_Devolucion INT PRIMARY KEY IDENTITY(1,1), -- Identificador único de la devolución (clave primaria).
    ID_Prestamo INT FOREIGN KEY REFERENCES Prestamo(ID_Prestamo), -- Préstamo asociado a la devolución.
    Fecha_Devolucion_Real DATE NOT NULL DEFAULT GETDATE(),        -- Fecha en que se realiza la devolución.
    Condicion_Libro_Devuelto VARCHAR(200) CHECK (Estado IN ('INTACTO', 'ALTERADO')),       -- Condición del libro devuelto (opcional).
	Eliminado BIT DEFAULT 0
);

-- Tabla LibrosPerdidos
-- Registra libros perdidos por los usuarios.
CREATE TABLE LibroPerdido (
    ID_Perdido INT PRIMARY KEY IDENTITY(1,1),				-- Identificador único de la perdida (clave primaria).
	ID_Usuario INT FOREIGN KEY REFERENCES Usuario(ID_Usuario), -- Usuario que realizo la perdida.
    ID_Libro INT FOREIGN KEY REFERENCES Libro(ID_Libro),			-- Libro perdido.
    FechaPerdida DATETIME DEFAULT GETDATE()
);

-- Tabla Usuarios_Auditoria
-- Registra todo lo que puede hacer un rol usuario
CREATE TABLE Usuario_Auditoria (
    ID INT IDENTITY(1,1) PRIMARY KEY,				-- Identificador único del cambio (clave primaria).
    ID_Usuario INT FOREIGN KEY REFERENCES Usuario(ID_Usuario),      -- Usuario asociado al cambio.
	ID_Usuario_Cambio INT FOREIGN KEY REFERENCES Usuario(ID_Usuario),			-- ID del Usuario que hizo la accion, o si el mismo usuario o un bibliotecario con permisos
    Accion NVARCHAR(50) CHECK (Accion IN ('CREACION DE CUENTA', 'MODIFICACION DATOS DE CUENTA', 'ELIMINACION DE CUENTA', 'PRESTAMO', 'DEVOLUCION','PERDIDA DE LIBRO')),							-- Tipo de Accion CREACION DE CUENTA,MODIFICACION DE DATOS USUARIO,ELIMINACION LOGICA DE CUENTA,PRESTAMO LIBRO, DEVOLUCION LIBRO, PERDIDA DE LIBRO	
	Campo_Modificado NVARCHAR(100) NOT NULL,  -- Especifica qué campo cambió.
    Fecha_Cambio DATETIME NOT NULL DEFAULT GETDATE(), -- Fecha y hora del cambio.
    Valor_Anterior NVARCHAR(MAX),                    -- Valor anterior del campo.
    Valor_Nuevo NVARCHAR(MAX)							-- Valor nuevo del campo.
);


-- Tabla Historial_Libro
-- Registra los cambios realizados en la tabla Libro.
CREATE TABLE Libro_Auditoria (
    ID INT IDENTITY(1,1) PRIMARY KEY,						-- Identificador único del cambio (clave primaria).
    ID_Libro INT FOREIGN KEY REFERENCES Libro(ID_Libro),		-- Tipo de Accion CREACION,MODIFICACION,ELIMINACION,PRESTAMO,DEVOLUCION
	ID_Usuario_Cambio INT NOT NULL,				-- ID del Usuario que hizo la accion, o si el mismo usuario o un bibliotecario con permisos
    Accion NVARCHAR(50) CHECK (Accion IN ('CREACION DE LIBRO', 'MODIFICACION DATOS DE LIBRO', 'ELIMINACION DE LIBRO', 'PRESTAMO', 'DEVOLUCION','PERDIDA DE LIBRO')),							-- Tipo de Accion CREACION DE LIBRO,MODIFICACION DE DATOS LIBRO,ELIMINACION LOGICA DE LIBRO,PRESTAMO LIBRO, DEVOLUCION LIBRO, PERDIDA DE LIBRO
	Campo_Modificado NVARCHAR(100) NOT NULL,  -- Especifica qué campo cambió.
    Fecha_Cambio DATETIME NOT NULL DEFAULT GETDATE(), -- Fecha y hora del cambio.
    Valor_Anterior NVARCHAR(MAX),                    -- Valor anterior del campo.
    Valor_Nuevo NVARCHAR(MAX)                        -- Valor nuevo del campo.
);

-- Índices en las columnas más consultadas
CREATE INDEX idx_Usuario_Correo ON Usuario(Correo); -- Para búsquedas por correo
CREATE INDEX idx_Prestamo_Usuario ON Prestamo(ID_Usuario); -- Para consultas de préstamos por usuario
CREATE INDEX idx_Prestamo_Libro ON Prestamo(ID_Libro); -- Para consultas de préstamos por libro
CREATE INDEX idx_Devolucion_Prestamo ON Devolucion(ID_Prestamo); -- Para búsquedas rápidas de devoluciones
CREATE INDEX idx_Libro_Titulo ON Libro(Titulo); -- Para búsquedas rápidas por título de libro