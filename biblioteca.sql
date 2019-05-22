CREATE DATABASE biblioteca;

USE biblioteca;

CREATE TABLE usuario(
    id_usuario INT UNSIGNED PRIMARY KEY NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    tipo TINYINT UNSIGNED NOT NULL,
    email VARCHAR(254) NOT NULL, 
    telefono VARCHAR(15) NOT NULL,
    pass VARCHAR(50) NOT NULL,
    estado BOOLEAN DEFAULT 1,
    fechaRegistro DATE NOT NULL,
    penalizaciones TINYINT UNSIGNED NOT NULL DEFAULT 0,
    area VARCHAR(30) NOT NULL
);

CREATE TABLE prestamo(
    folio INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    id_user INT UNSIGNED,
    FOREIGN KEY(id_user)
    REFERENCES usuario(id_usuario),
    fecha DATE NOT NULL

);

CREATE TABLE libro(
    id_libro INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    autor VARCHAR(50) NOT NULL,
    genero VARCHAR(50) NOT NULL,
    edicion INT NOT NULL, 
    editorial VARCHAR(50) NOT NULL,
    idioma VARCHAR(50) NOT NULL,
    isbn VARCHAR(15) NOT NULl,
    descripcion TEXT, 
    existencia INT NOT NULL DEFAULT 1,
    unicos INT UNSIGNED  NOT NULL DEFAULT 1,
    disponibles INT UNSIGNED NOT NULL
);

CREATE TABLE material(
    id_material INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    tipo INT NOT NULL,
    marca VARCHAR(50) NOT NULL,
    descripcion TEXT,
    numSerie VARCHAR(50) NOT NULL
);

CREATE TABLE libroUsuarios(
    id_user INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_user)
    REFERENCES usuario(id_usuario),
    contLibros TINYINT NOT NULL
);

CREATE TABLE materialesUsuarios(
    id_user INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_user)
    REFERENCES usuario(id_usuario),
    contMateriales TINYINT UNSIGNED NOT NULL
);

CREATE TABLE prestamoLibro(
    folio INT UNSIGNED NOT NULL,
    FOREIGN KEY (folio)
    REFERENCES prestamo(folio),
    id_libro INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_libro)
    REFERENCES libro(id_libro),
    fechaDevolucion DATE NOT NULL,
    extension BOOLEAN DEFAULT 0
);

CREATE TABLE prestamoMaterial(
    folio INT UNSIGNED NOT NULL,
    FOREIGN KEY (folio)
    REFERENCES prestamo(folio),
    id_material INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_material)
    REFERENCES material(id_material),
    fechaDevolucion DATE NOT NULL
);

CREATE TABLE dinero(
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fecha DATE,
    monto DECIMAL(6,2) UNSIGNED NOT NULL,
    id_prestamo INT  UNSIGNED NOT NULL,
    FOREIGN KEY (id_prestamo)
    REFERENCES prestamo(folio)
);

CREATE TABLE monto(
    fecha DATE PRIMARY KEY NOT NULL,
    montoActual DECIMAL(6,2) UNSIGNED NOT NULL
);