-- =============================================
--			INICIO	INSERT	PRESTAMO		  --
-- =============================================
-- Creación del trigger para gestionar préstamos
-- =============================================
-- TRIGGER: Controla la inserción de préstamos
-- Nombre: trg_InsertPrestamo
-- Descripción: Valida reglas de negocio antes de registrar un préstamo.
-- =============================================
CREATE TRIGGER trg_InsertPrestamo
ON Prestamo
INSTEAD OF INSERT
AS
BEGIN
    -- =============================================
    -- 1. DECLARACIÓN DE VARIABLES
    -- =============================================
    DECLARE @ID_Usuario INT, 
            @ID_Libro INT, 
            @ID_Prestamo INT, 
            @Rol_Cambio NVARCHAR(13),
            @ID_Usuario_Cambio INT,
            @TituloLibro NVARCHAR(200);  -- Nueva variable para el título

    -- =============================================
    -- 2. CAPTURAR DATOS DEL PRÉSTAMO
    -- =============================================
    SELECT 
        @ID_Usuario = i.ID_Usuario,
        @ID_Libro = i.ID_Libro,
        @ID_Usuario_Cambio = i.ID_Usuario_Cambio
    FROM inserted i;

    -- =============================================
    -- 3. OBTENER TÍTULO DEL LIBRO
    -- =============================================
    SELECT @TituloLibro = Titulo 
    FROM Libro 
    WHERE ID_Libro = @ID_Libro;

    -- =============================================
    -- 4. VALIDACIONES
    -- =============================================
    -- 4.1 Verificar rol del usuario que realiza el préstamo
    SET @Rol_Cambio = (SELECT Rol FROM Usuario WHERE ID_Usuario = @ID_Usuario_Cambio);

    -- 4.2 Validar que el usuario receptor no esté eliminado
    IF (SELECT Eliminado FROM Usuario WHERE ID_Usuario = @ID_Usuario) = 1
    BEGIN
        RAISERROR ('RECHAZADO. El usuario no puede realizar préstamos porque está eliminado.', 16, 1);
        RETURN;
    END

    -- 4.3 Validar puntaje del usuario receptor
    IF (SELECT Puntaje FROM Usuario WHERE ID_Usuario = @ID_Usuario) <= 0
    BEGIN
        RAISERROR ('RECHAZADO. Por favor habla con administración.', 16, 1);
        RETURN;
    END
    
    -- 4.4 Verificar disponibilidad del libro
    IF (SELECT Cantidad_Disponible FROM Libro WHERE ID_Libro = @ID_Libro) <= 0
    BEGIN
        RAISERROR ('Todos los ejemplares de este libro no están disponibles.', 16, 1);
        RETURN;
    END
    
    -- 4.5 Validar límite de préstamos activos
    IF (SELECT COUNT(*) FROM Prestamo WHERE ID_Usuario = @ID_Usuario AND Estado = 'PRESTADO') >= 3
    BEGIN
        RAISERROR ('No puedes tener más de 3 préstamos activos.', 16, 1);
        RETURN;
    END
    
    -- =============================================
    -- 5. INSERTAR PRÉSTAMO
    -- =============================================
    INSERT INTO Prestamo (
        ID_Usuario, 
        ID_Libro, 
        ID_Usuario_Cambio, 
        Fecha_Prestamo, 
        Fecha_Devolucion_Esperada, 
        Estado
    )
    SELECT 
        ID_Usuario, 
        ID_Libro, 
        ID_Usuario_Cambio, 
        GETDATE(), 
        DATEADD(DAY, 14, GETDATE()), 
        'PRESTADO'
    FROM inserted;

    -- =============================================
    -- 6. ACTUALIZAR STOCK DEL LIBRO
    -- =============================================
    UPDATE Libro
    SET Cantidad_Disponible = Cantidad_Disponible - 1
    WHERE ID_Libro = @ID_Libro;

    -- =============================================
    -- 7. REGISTRAR AUDITORÍAS
    -- =============================================
    -- 7.1 Auditoría de Usuario
    INSERT INTO Usuario_Auditoria (
        ID_Usuario, 
        ID_Usuario_Cambio, 
        Accion, 
        Campo_Modificado, 
        Valor_Nuevo
    )
    VALUES (
        @ID_Usuario,
        @ID_Usuario_Cambio,
        'PRESTAMO',
        @TituloLibro,  -- Modificado: Ahora usa el título del libro
        CAST(SCOPE_IDENTITY() AS NVARCHAR)
    );

    -- 7.2 Auditoría de Libro
    INSERT INTO Libro_Auditoria (
        ID_Libro, 
        ID_Usuario_Cambio, 
        Accion, 
        Campo_Modificado, 
        Valor_Anterior, 
        Valor_Nuevo
    )
    VALUES (
        @ID_Libro,
        @ID_Usuario_Cambio,
        'PRESTAMO',
        @TituloLibro,  -- Modificado: Ahora usa el título del libro
        (SELECT Cantidad_Disponible + 1 FROM Libro WHERE ID_Libro = @ID_Libro),
        (SELECT Cantidad_Disponible FROM Libro WHERE ID_Libro = @ID_Libro)
    );
END;

-- =============================================
--				FIN	INSERT PRESTAMO			  --
-- =============================================

-- =============================================
--			  INICIO UPDATE PRESTAMO		  --
-- =============================================
-- =============================================
-- TRIGGER: Controla la actualización de préstamos
-- Nombre: trg_UpdatePrestamo
-- Descripción: Valida reglas de negocio antes de actualizar un préstamo.
-- =============================================
CREATE TRIGGER trg_UpdatePrestamo
ON Prestamo
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Solo procesar si hay cambios en Libro/Usuario
    IF NOT (UPDATE(ID_Usuario) OR UPDATE(ID_Libro))
        RETURN;

    -- =============================================
    -- A. DECLARAR VARIABLES (DATOS ANTIGUOS/NUEVOS)
    -- =============================================
    DECLARE @ID_Prestamo INT,
            @Old_ID_Usuario INT,
            @New_ID_Usuario INT,
            @Old_ID_Libro INT,
            @New_ID_Libro INT,
            @ID_Usuario_Cambio INT,
            @Old_Titulo NVARCHAR(200),
            @New_Titulo NVARCHAR(200);

    -- =============================================
    -- B. CAPTURAR DATOS DEL UPDATE
    -- =============================================
    SELECT 
        @ID_Prestamo = i.ID_Prestamo,
        @Old_ID_Usuario = d.ID_Usuario,
        @New_ID_Usuario = i.ID_Usuario,
        @Old_ID_Libro = d.ID_Libro,
        @New_ID_Libro = i.ID_Libro,
        @ID_Usuario_Cambio = i.ID_Usuario_Cambio,
        @Old_Titulo = dl.Titulo,
        @New_Titulo = il.Titulo
    FROM inserted i
    INNER JOIN deleted d ON i.ID_Prestamo = d.ID_Prestamo
    INNER JOIN Libro dl ON d.ID_Libro = dl.ID_Libro  -- Libro antiguo
    INNER JOIN Libro il ON i.ID_Libro = il.ID_Libro; -- Libro nuevo

    -- =============================================
    -- C. VALIDAR QUE EL NUEVO USUARIO NO ESTÉ ELIMINADO
    -- =============================================
    IF (SELECT Eliminado FROM Usuario WHERE ID_Usuario = @New_ID_Usuario) = 1
    BEGIN
        RAISERROR ('RECHAZADO. No se puede actualizar el préstamo porque el usuario está eliminado.', 16, 1);
        ROLLBACK;
        RETURN;
    END;

    -- =============================================
    -- D. VALIDAR DISPONIBILIDAD DEL NUEVO LIBRO
    -- =============================================
    IF (SELECT Cantidad_Disponible FROM Libro WHERE ID_Libro = @New_ID_Libro) <= 0
    BEGIN
        RAISERROR ('El libro nuevo no está disponible.', 16, 1);
        ROLLBACK;
        RETURN;
    END;

    -- =============================================
    -- E. AJUSTAR STOCK DE LIBROS
    -- =============================================
    BEGIN TRANSACTION;
    -- Devolver libro antiguo
    UPDATE Libro SET Cantidad_Disponible += 1 WHERE ID_Libro = @Old_ID_Libro;
    -- Prestar libro nuevo
    UPDATE Libro SET Cantidad_Disponible -= 1 WHERE ID_Libro = @New_ID_Libro;
    COMMIT;

    -- =============================================
    -- F. REGISTRAR AUDITORÍAS
    -- =============================================
    -- Auditoría para libro/usuario antiguo (devolución)
    INSERT INTO Usuario_Auditoria (
        ID_Usuario, 
        ID_Usuario_Cambio, 
        Accion, 
        Campo_Modificado, 
        Valor_Anterior, 
        Valor_Nuevo
    )
    VALUES (
        @Old_ID_Usuario,
        @ID_Usuario_Cambio,
        'MODIFICACION DE PRESTAMO',
        @Old_Titulo,
        'PRESTADO',
        'DEVUELTO'
    );

    INSERT INTO Libro_Auditoria (
        ID_Libro, 
        ID_Usuario_Cambio, 
        Accion, 
        Campo_Modificado, 
        Valor_Anterior, 
        Valor_Nuevo
    )
    VALUES (
        @Old_ID_Libro,
        @ID_Usuario_Cambio,
        'DEVOLUCION',
        @Old_Titulo,
        (SELECT Cantidad_Disponible - 1 FROM Libro WHERE ID_Libro = @Old_ID_Libro),
        (SELECT Cantidad_Disponible FROM Libro WHERE ID_Libro = @Old_ID_Libro)
    );

    -- Auditoría para libro/usuario nuevo (préstamo)
    INSERT INTO Usuario_Auditoria (
        ID_Usuario, 
        ID_Usuario_Cambio, 
        Accion, 
        Campo_Modificado, 
        Valor_Anterior, 
        Valor_Nuevo
    )
    VALUES (
        @New_ID_Usuario,
        @ID_Usuario_Cambio,
        'MODIFICACION DE PRESTAMO',
        @New_Titulo,
        'DEVUELTO',
        'PRESTADO'
    );

    INSERT INTO Libro_Auditoria (
        ID_Libro, 
        ID_Usuario_Cambio, 
        Accion, 
        Campo_Modificado, 
        Valor_Anterior, 
        Valor_Nuevo
    )
    VALUES (
        @New_ID_Libro,
        @ID_Usuario_Cambio,
        'PRESTAMO',
        @New_Titulo,
        (SELECT Cantidad_Disponible + 1 FROM Libro WHERE ID_Libro = @New_ID_Libro),
        (SELECT Cantidad_Disponible FROM Libro WHERE ID_Libro = @New_ID_Libro)
    );
END;
-- =============================================
--				FIN UPDATE PRESTAMO		   	  --
-- =============================================

-- =============================================
--			INICIO DELETE PRESTAMO		   	  --
-- =============================================
CREATE TRIGGER trg_DeletePrestamo
ON Prestamo
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Solo procesar si Eliminado cambió de 0 → 1
    IF NOT (UPDATE(Eliminado)) 
        RETURN;

    -- =============================================
    -- A. DECLARAR VARIABLES
    -- =============================================
    DECLARE @ID_Prestamo INT,
            @ID_Usuario INT,
            @ID_Libro INT,
            @ID_Usuario_Cambio INT,
            @TituloLibro NVARCHAR(200);

    -- =============================================
    -- B. CAPTURAR DATOS DEL PRÉSTAMO ELIMINADO
    -- =============================================
    SELECT 
        @ID_Prestamo = i.ID_Prestamo,
        @ID_Usuario = i.ID_Usuario,
        @ID_Libro = i.ID_Libro,
        @ID_Usuario_Cambio = i.ID_Usuario_Cambio,
        @TituloLibro = l.Titulo
    FROM inserted i
    INNER JOIN Libro l ON i.ID_Libro = l.ID_Libro
    WHERE i.Eliminado = 1;

    -- =============================================
    -- C. REVERTIR PRÉSTAMO (AUMENTAR STOCK)
    -- =============================================
    UPDATE Libro
    SET Cantidad_Disponible += 1
    WHERE ID_Libro = @ID_Libro;

    -- =============================================
    -- D. REGISTRAR AUDITORÍAS
    -- =============================================
    INSERT INTO Usuario_Auditoria (
        ID_Usuario, 
        ID_Usuario_Cambio, 
        Accion, 
        Campo_Modificado, 
        Valor_Anterior, 
        Valor_Nuevo
    )
    VALUES (
        @ID_Usuario,
        @ID_Usuario_Cambio,
        'ELIMINACION DE PRESTAMO',
        @TituloLibro,
        'PRESTADO',
        'DEVUELTO'
    );

    INSERT INTO Libro_Auditoria (
        ID_Libro, 
        ID_Usuario_Cambio, 
        Accion, 
        Campo_Modificado, 
        Valor_Anterior, 
        Valor_Nuevo
    )
    VALUES (
        @ID_Libro,
        @ID_Usuario_Cambio,
        'ELIMINACION DE PRESTAMO',
        @TituloLibro,
        (SELECT Cantidad_Disponible - 1 FROM Libro WHERE ID_Libro = @ID_Libro),
        (SELECT Cantidad_Disponible FROM Libro WHERE ID_Libro = @ID_Libro)
    );
END;
-- =============================================
--			  FIN DELETE PRESTAMO		   	  --
-- =============================================