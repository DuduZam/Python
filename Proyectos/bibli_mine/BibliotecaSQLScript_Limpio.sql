USE [master]
GO
/****** Object:  Database [BibliotecaDB]    Script Date: 27/2/2025 02:47:56 ******/
CREATE DATABASE [BibliotecaDB]
 CONTAINMENT = NONE
 ON  PRIMARY
( NAME = N'BibliotecaDB', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\BibliotecaDB.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON
( NAME = N'BibliotecaDB_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\BibliotecaDB_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [BibliotecaDB] SET READ_WRITE
GO
USE [BibliotecaDB]
GO
/****** Object:  Table [dbo].[Historial_Libros]      Script Date: 27/2/2025 02:47:56 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Historial_Libros](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [id_libro] [int] NULL,
        [fecha_cambio] [datetime] NULL,
        [detalle] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED
(
        [id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Historial_Usuarios]        Script Date: 27/2/2025 02:47:56 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Historial_Usuarios](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [id_usuario] [nvarchar](50) NULL,
        [fecha_cambio] [datetime] NULL,
        [detalle] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED
(
        [id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Libros]        Script Date: 27/2/2025 02:47:56 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Libros](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [titulo] [nvarchar](255) NULL,
        [autor] [nvarchar](255) NULL,
        [año_publicacion] [int] NULL,
        [disponible] [bit] CONSTRAINT [DF_Libros_Disponible] DEFAULT ((1)) NULL,
        [eliminado] [bit] DEFAULT ((0)) NULL,
PRIMARY KEY CLUSTERED
(
        [id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Prestamos]      Script Date: 27/2/2025 02:47:56 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
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
/****** Object:  Table [dbo].[Usuarios]        Script Date: 27/2/2025 02:47:56 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Usuarios](
        [id] [nvarchar](50) NOT NULL,
        [nombre] [nvarchar](255) NULL,
        [eliminado] [bit] DEFAULT ((0)) NULL,
PRIMARY KEY CLUSTERED
(
        [id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_Prestamo_Unico]       Script Date: 27/2/2025 02:47:56 ******/
CREATE UNIQUE NONCLUSTERED INDEX [IX_Prestamo_Unico] ON [dbo].[Prestamos]
(
        [id_usuario] ASC,
        [id_libro] ASC
)
WHERE ([fecha_devolucion] IS NULL)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IX_Prestamos_Libro]      Script Date: 27/2/2025 02:47:56 ******/
CREATE NONCLUSTERED INDEX [IX_Prestamos_Libro] ON [dbo].[Prestamos]
(
        [id_libro] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_Prestamos_Usuario]    Script Date: 27/2/2025 02:47:56 ******/
CREATE NONCLUSTERED INDEX [IX_Prestamos_Usuario] ON [dbo].[Prestamos]
(
        [id_usuario] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Historial_Libros] WITH CHECK ADD FOREIGN KEY([id_libro])
REFERENCES [dbo].[Libros] ([id])
GO
ALTER TABLE [dbo].[Historial_Usuarios] WITH CHECK ADD FOREIGN KEY([id_usuario])
REFERENCES [dbo].[Usuarios] ([id])
GO
ALTER TABLE [dbo].[Prestamos] WITH CHECK ADD FOREIGN KEY([id_libro])
REFERENCES [dbo].[Libros] ([id])
GO
ALTER TABLE [dbo].[Prestamos] WITH CHECK ADD FOREIGN KEY([id_usuario])
REFERENCES [dbo].[Usuarios] ([id])
GO