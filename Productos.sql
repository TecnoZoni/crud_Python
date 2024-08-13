CREATE DATABASE producto;

USE producto;

CREATE TABLE Productos (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Nombre NVARCHAR(100) NOT NULL,
    Precio DECIMAL(10, 2) NOT NULL,
    CantidadEnStock INT NOT NULL,
    Categoria NVARCHAR(50) NOT NULL
);
