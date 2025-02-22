CREATE DATABASE [BibliotecaDB]
USE [BibliotecaDB]

CREATE TABLE [dbo].[Libros](
    [id] [int] IDENTITY(1,1) NOT NULL,
    [titulo] [nvarchar](255) NULL,
    [autor] [nvarchar](255) NULL,
    [año_publicacion] [int] NULL,
    [disponible] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
    [id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Prestamos]    Script Date: 20/2/2025 02:29:46 ******/
CREATE TABLE [dbo].[Prestamos](
    [id] [int] IDENTITY(1,1) NOT NULL,
    [id_usuario] [nvarchar](50) NULL,
    [id_libro] [int] NULL,
    [fecha_prestamo] [datetime] NULL,
    [fecha_devolucion] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
    [id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Usuarios]    Script Date: 20/2/2025 02:29:46 ******/
CREATE TABLE [dbo].[Usuarios](
    [id] [nvarchar](50) NOT NULL,
    [nombre] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
    [id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
/****** Object:  Index [IX_Prestamo_Unico]    Script Date: 20/2/2025 02:29:46 ******/
CREATE UNIQUE NONCLUSTERED INDEX [IX_Prestamo_Unico] ON [dbo].[Prestamos]
(
    [id_usuario] ASC,
    [id_libro] ASC
)
WHERE ([fecha_devolucion] IS NULL)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]

/****** Object:  Index [IX_Prestamos_Libro]    Script Date: 20/2/2025 02:29:46 ******/
CREATE NONCLUSTERED INDEX [IX_Prestamos_Libro] ON [dbo].[Prestamos]
(
    [id_libro] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]

/****** Object:  Index [IX_Prestamos_Usuario]    Script Date: 20/2/2025 02:29:46 ******/
CREATE NONCLUSTERED INDEX [IX_Prestamos_Usuario] ON [dbo].[Prestamos]
(
    [id_usuario] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Libros] ADD  CONSTRAINT [DF_Libros_Disponible]  DEFAULT ((1)) FOR [disponible]
GO
ALTER TABLE [dbo].[Prestamos]  WITH CHECK ADD FOREIGN KEY([id_libro])
REFERENCES [dbo].[Libros] ([id])
GO
ALTER TABLE [dbo].[Prestamos]  WITH CHECK ADD FOREIGN KEY([id_usuario])
REFERENCES [dbo].[Usuarios] ([id])
GO
USE [master]
GO
ALTER DATABASE [BibliotecaDB] SET  READ_WRITE 
GO


CREATE TABLE Historial_Libros (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_libro INT,
    fecha_cambio DATETIME,
    tipo_cambio NVARCHAR(255), -- Ejemplo: 'Añadido', 'Modificado', 'Eliminado'
    detalle NVARCHAR(255),     -- Detalles sobre el cambio (por ejemplo, si fue un cambio de autor, título, etc.)
    FOREIGN KEY (id_libro) REFERENCES Libros(id)
);

CREATE TABLE Historial_Usuarios (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario NVARCHAR(50),
    fecha_cambio DATETIME,
    tipo_cambio NVARCHAR(255),  -- Ejemplo: 'Añadido', 'Modificado', 'Eliminado'
    detalle NVARCHAR(255),      -- Detalles sobre el cambio (por ejemplo, si fue un cambio de nombre, eliminación, etc.)
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);