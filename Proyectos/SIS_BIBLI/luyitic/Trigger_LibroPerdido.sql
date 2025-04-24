-- =============================================
--		  INICIO INSERT LIBRO PERDIDO		  --
-- =============================================
CREATE TRIGGER trg_InsertLibroPerdido
ON LibroPerdido
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- =============================================
        -- 1. VALIDAR QUE EL LIBRO ESTÉ PRESTADO
        -- =============================================
        IF EXISTS (
            SELECT 1
            FROM inserted i
            INNER JOIN Prestamo p ON i.ID_Prestamo = p.ID_Prestamo
            WHERE p.Estado <> 'PRESTADO'
        )
        BEGIN
            RAISERROR ('No se puede reportar pérdida de un libro no prestado.', 16, 1);
            ROLLBACK;
            RETURN;
        END;

        -- =============================================
        -- 2. ACTUALIZAR ESTADO DEL PRÉSTAMO A 'PERDIDO'
        -- =============================================
        UPDATE p
        SET Estado = 'PERDIDO'
        FROM Prestamo p
        INNER JOIN inserted i ON p.ID_Prestamo = i.ID_Prestamo;

        -- =============================================
        -- 3. ACTUALIZAR PUNTAJE DEL USUARIO A 0
        -- =============================================
        UPDATE u
        SET Puntaje = 0
        FROM Usuario u
        INNER JOIN inserted i ON u.ID_Usuario = i.ID_Usuario;

        -- =============================================
        -- 4. REGISTRAR AUDITORÍAS
        -- =============================================
        -- Auditoría de Usuario
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
            i.ID_Usuario,
            p.ID_Usuario_Cambio,  -- Quien reportó la pérdida
            'PERDIDA DE LIBRO',
            l.Titulo,
            (SELECT Puntaje FROM Usuario WHERE ID_Usuario = i.ID_Usuario),
            0,
            GETDATE()
        FROM inserted i
        INNER JOIN Prestamo p ON i.ID_Prestamo = p.ID_Prestamo
        INNER JOIN Libro l ON p.ID_Libro = l.ID_Libro;

        -- Auditoría de Libro
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
            'PERDIDA DE LIBRO',
            l.Titulo,
            l.Cantidad_Disponible,
            l.Cantidad_Disponible,  -- El stock no cambia con pérdidas
            GETDATE()
        FROM inserted i
        INNER JOIN Prestamo p ON i.ID_Prestamo = p.ID_Prestamo
        INNER JOIN Libro l ON p.ID_Libro = l.ID_Libro;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
-- =============================================
--		    FIN INSERT LIBRO PERDIDO		  --
-- =============================================