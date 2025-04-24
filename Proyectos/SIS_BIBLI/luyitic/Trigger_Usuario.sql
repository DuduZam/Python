-- TRIGGER: Audita la creación de un usuario
CREATE TRIGGER trg_Insert_Usuario
ON Usuario
AFTER INSERT
AS
BEGIN
    -- Inserta un registro en la tabla de auditoría indicando la creación de la cuenta.
    INSERT INTO Usuario_Auditoria (ID_Usuario, ID_Usuario_Cambio, Accion, Campo_Modificado, Fecha_Cambio, Valor_Anterior, Valor_Nuevo)
    SELECT 
        i.ID_Usuario,                 -- ID del usuario recién creado.
        i.ID_Usuario,                 -- Se asume que el usuario se crea a sí mismo.
        'CREACION DE CUENTA',         -- Acción de auditoría.
        'NUEVO USUARIO',              -- Campo modificado (es un usuario nuevo).
        GETDATE(),                     -- Fecha y hora de creación.
        NULL,                          -- No hay valor anterior porque es un nuevo registro.
        CONCAT(i.Nombre, ' ', i.Apellido, ' - ', i.Correo ' - ', i.Contraseña ' - ', i.Telefono ' - ', i.Direccion ' - ', i.Puntaje ' - ', i.Rol ' - ', i.Eliminado) -- Nombre completo del nuevo usuario.
    FROM inserted i;
END;

-- TRIGGER: Audita cambios en datos personales de un usuario
CREATE TRIGGER trg_Update_Usuario
ON Usuario
AFTER UPDATE
AS
BEGIN
    -- Registra cambios en Nombre
    INSERT INTO Usuario_Auditoria (ID_Usuario, ID_Usuario_Cambio, Accion, Campo_Modificado, Fecha_Cambio, Valor_Anterior, Valor_Nuevo)
    SELECT 
        i.ID_Usuario, 
        i.ID_Usuario, 
        'MODIFICACION DATOS DE CUENTA', 
        'Nombre', 
        GETDATE(), 
        d.Nombre, 
        i.Nombre
    FROM inserted i
    JOIN deleted d ON i.ID_Usuario = d.ID_Usuario
    WHERE i.Nombre <> d.Nombre;

    -- Registra cambios en Apellido
    INSERT INTO Usuario_Auditoria (ID_Usuario, ID_Usuario_Cambio, Accion, Campo_Modificado, Fecha_Cambio, Valor_Anterior, Valor_Nuevo)
    SELECT 
        i.ID_Usuario, 
        i.ID_Usuario, 
        'MODIFICACION DATOS DE CUENTA', 
        'Apellido', 
        GETDATE(), 
        d.Apellido, 
        i.Apellido
    FROM inserted i
    JOIN deleted d ON i.ID_Usuario = d.ID_Usuario
    WHERE i.Apellido <> d.Apellido;

    -- Registra cambios en Contraseña
    INSERT INTO Usuario_Auditoria (ID_Usuario, ID_Usuario_Cambio, Accion, Campo_Modificado, Fecha_Cambio, Valor_Anterior, Valor_Nuevo)
    SELECT 
        i.ID_Usuario, 
        i.ID_Usuario, 
        'MODIFICACION DATOS DE CUENTA', 
        'Contraseña', 
        GETDATE(), 
        d.Contraseña,
        i.Contraseña
    FROM inserted i
    JOIN deleted d ON i.ID_Usuario = d.ID_Usuario
    WHERE i.Contraseña <> d.Contraseña;

    -- Registra cambios en Telefono
    INSERT INTO Usuario_Auditoria (ID_Usuario, ID_Usuario_Cambio, Accion, Campo_Modificado, Fecha_Cambio, Valor_Anterior, Valor_Nuevo)
    SELECT 
        i.ID_Usuario, 
        i.ID_Usuario, 
        'MODIFICACION DATOS DE CUENTA', 
        'Telefono', 
        GETDATE(), 
        d.Telefono, 
        i.Telefono
    FROM inserted i
    JOIN deleted d ON i.ID_Usuario = d.ID_Usuario
    WHERE i.Telefono <> d.Telefono;
END;

-- TRIGGER: Audita la eliminación lógica de un usuario
CREATE TRIGGER trg_Update_Usuario
ON Usuario
AFTER UPDATE
AS
BEGIN
    -- Registra eliminación lógica del usuario
    INSERT INTO Usuario_Auditoria (ID_Usuario, ID_Usuario_Cambio, Accion, Campo_Modificado, Fecha_Cambio, Valor_Anterior, Valor_Nuevo)
    SELECT 
        i.ID_Usuario, 
        i.ID_Usuario, 
        'ELIMINACION DE CUENTA', 
        'Eliminado', 
        GETDATE(), 
        '0', 
        '1'
    FROM inserted i
    JOIN deleted d ON i.ID_Usuario = d.ID_Usuario
    WHERE i.Eliminado = 1 AND d.Eliminado = 0;
END;
