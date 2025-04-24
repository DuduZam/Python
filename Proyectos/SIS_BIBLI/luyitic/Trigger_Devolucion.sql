-- =============================================
--			INICIO INSERT DEVOLUCION		  --
-- =============================================
CREATE TRIGGER trg_InsertDevolucion
ON Devolucion
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;  -- Evita mensajes de salida innecesarios

    -- =============================================
    -- 1. VALIDAR QUE EL PRÉSTAMO ESTÉ ACTIVO
    -- =============================================
    IF EXISTS (
        SELECT 1 
        FROM inserted i
        INNER JOIN Prestamo p ON i.ID_Prestamo = p.ID_Prestamo
        WHERE p.Estado <> 'PRESTADO'  -- Solo permite devoluciones de préstamos activos
    )
    BEGIN
        RAISERROR ('No se puede devolver un libro no prestado.', 16, 1);
        RETURN;
    END;

    -- =============================================
    -- 2. ACTUALIZAR ESTADO DEL PRÉSTAMO A 'DEVUELTO'
    -- =============================================
    UPDATE p
    SET Estado = 'DEVUELTO'
    FROM Prestamo p
    INNER JOIN inserted i ON p.ID_Prestamo = i.ID_Prestamo;

    -- =============================================
    -- 3. AUMENTAR STOCK DEL LIBRO
    -- =============================================
    UPDATE l
    SET Cantidad_Disponible = Cantidad_Disponible + 1
    FROM Libro l
    INNER JOIN Prestamo p ON l.ID_Libro = p.ID_Libro
    INNER JOIN inserted i ON p.ID_Prestamo = i.ID_Prestamo;

    -- =============================================
    -- 4. CALCULAR CAMBIOS EN EL PUNTAJE DEL USUARIO
    -- =============================================
    ;WITH DevolucionData AS (
        SELECT 
            p.ID_Usuario,
            i.Fecha_Devolucion_Real,
            p.Fecha_Devolucion_Esperada,
            i.Condicion_Libro_Devuelto,
            u.Puntaje AS Puntaje_Actual,
            p.ID_Usuario_Cambio,
            l.Titulo
        FROM inserted i
        INNER JOIN Prestamo p ON i.ID_Prestamo = p.ID_Prestamo
        INNER JOIN Usuario u ON p.ID_Usuario = u.ID_Usuario
        INNER JOIN Libro l ON p.ID_Libro = l.ID_Libro
    )
    UPDATE Usuario
    SET Puntaje = 
        CASE 
            -- Límites: 0 <= Puntaje <= 20
            WHEN (Puntaje + Delta) > 20 THEN 20  
            WHEN (Puntaje + Delta) < 0 THEN 0
            ELSE Puntaje + Delta
        END
    FROM Usuario u
    INNER JOIN (
        SELECT 
            ID_Usuario,
            -- Cálculo del delta: Fecha + Condición
            Delta = 
                CASE 
                    WHEN Fecha_Devolucion_Real <= Fecha_Devolucion_Esperada THEN 1  -- Puntaje +1
                    ELSE -2  -- Puntaje -2 por retraso
                END +
                CASE 
                    WHEN Condicion_Libro_Devuelto = 'Alterado' THEN -3  -- Penalización adicional
                    ELSE 0 
                END
        FROM DevolucionData
    ) AS Calculos ON u.ID_Usuario = Calculos.ID_Usuario;

    -- =============================================
    -- 5. REGISTRAR AUDITORÍAS
    -- =============================================
    -- 5.1 Auditoría de Usuario
    INSERT INTO Usuario_Auditoria (
        ID_Usuario, 
        ID_Usuario_Cambio, 
        Accion, 
        Campo_Modificado, 
        Valor_Anterior, 
        Valor_Nuevo
    )
    SELECT 
        p.ID_Usuario,
        p.ID_Usuario_Cambio,
        'DEVOLUCION',
        l.Titulo,  -- Título del libro como campo modificado
        dd.Puntaje_Actual,
        CASE 
            WHEN (dd.Puntaje_Actual + dd.Delta) > 20 THEN 20
            WHEN (dd.Puntaje_Actual + dd.Delta) < 0 THEN 0
            ELSE dd.Puntaje_Actual + dd.Delta
        END
    FROM (
        SELECT 
            ID_Usuario,
            ID_Usuario_Cambio,
            Titulo,
            Puntaje_Actual,
            Delta = 
                CASE 
                    WHEN Fecha_Devolucion_Real <= Fecha_Devolucion_Esperada THEN 1
                    ELSE -2
                END +
                CASE 
                    WHEN Condicion_Libro_Devuelto = 'Alterado' THEN -3
                    ELSE 0 
                END
        FROM DevolucionData
    ) dd
    INNER JOIN Libro l ON dd.Titulo = l.Titulo;

    -- 5.2 Auditoría de Libro
    INSERT INTO Libro_Auditoria (
        ID_Libro, 
        ID_Usuario_Cambio, 
        Accion, 
        Campo_Modificado, 
        Valor_Anterior, 
        Valor_Nuevo
    )
    SELECT 
        p.ID_Libro,
        p.ID_Usuario_Cambio,
        'DEVOLUCION',
        l.Titulo,  -- Título del libro
        l.Cantidad_Disponible - 1,  -- Stock antes de la devolución
        l.Cantidad_Disponible  -- Stock después de la devolución
    FROM inserted i
    INNER JOIN Prestamo p ON i.ID_Prestamo = p.ID_Prestamo
    INNER JOIN Libro l ON p.ID_Libro = l.ID_Libro;

END;
-- =============================================
--			  FIN INSERT DEVOLUCION			  --
-- =============================================

-- =============================================
--			 INICIO DELETE DEVOLUCION		  --
-- =============================================
CREATE TRIGGER trg_EliminarDevolucion
ON Devolucion
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Verificar si se está realizando una eliminación lógica
    IF UPDATE(Eliminado)
    BEGIN
        BEGIN TRY
            BEGIN TRANSACTION;

            -- Actualizar préstamo a PRESTADO y libro a -1 disponibilidad
            UPDATE p
            SET 
                p.Estado = 'PRESTADO'
            FROM Prestamo p
            INNER JOIN inserted i ON p.ID_Prestamo = i.ID_Prestamo
            WHERE i.Eliminado = 1;

            UPDATE l
            SET 
                l.Cantidad_Disponible = l.Cantidad_Disponible - 1
            FROM Libro l
            INNER JOIN Prestamo p ON l.ID_Libro = p.ID_Libro
            INNER JOIN inserted i ON p.ID_Prestamo = i.ID_Prestamo
            WHERE i.Eliminado = 1;

            -- Registrar auditorías
            INSERT INTO Usuario_Auditoria (
                ID_Usuario,
                ID_Usuario_Cambio,
                Accion,
                Campo_Modificado,
                Valor_Anterior,
                Valor_Nuevo,
                Fecha_Cambio
            )
            SELECT 
                p.ID_Usuario,
                p.ID_Usuario_Cambio,
                'ELIMINACION DE DEVOLUCION',
                l.Titulo,
                'DEVUELTO',
                'PRESTADO',
                GETDATE()
            FROM inserted i
            INNER JOIN Prestamo p ON i.ID_Prestamo = p.ID_Prestamo
            INNER JOIN Libro l ON p.ID_Libro = l.ID_Libro
            WHERE i.Eliminado = 1;

            INSERT INTO Libro_Auditoria (
                ID_Libro,
                ID_Usuario_Cambio,
                Accion,
                Campo_Modificado,
                Valor_Anterior,
                Valor_Nuevo,
                Fecha_Cambio
            )
            SELECT 
                p.ID_Libro,
                p.ID_Usuario_Cambio,
                'ELIMINACION DE DEVOLUCION',
                l.Titulo,
                l.Cantidad_Disponible + 1,  -- Valor antes de la eliminación
                l.Cantidad_Disponible,      -- Valor después de la eliminación
                GETDATE()
            FROM inserted i
            INNER JOIN Prestamo p ON i.ID_Prestamo = p.ID_Prestamo
            INNER JOIN Libro l ON p.ID_Libro = l.ID_Libro
            WHERE i.Eliminado = 1;

            COMMIT TRANSACTION;
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION;
            THROW;
        END CATCH;
    END;
END;
-- =============================================
--			  FIN DELETE DEVOLUCION			  --
-- =============================================