use agenda;

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario varchar(20),
    clave_usuario varchar(255),
    apellidos_usuario varchar(50),
    rol varchar(20) default 'normal'
);   
INSERT INTO `usuario` 
	(`nombre_usuario`, `clave_usuario`, `apellidos_usuario`, `rol`)
VALUES 
    ('kike','1234', 'martinez', 'administrador'),
    ('carlos','1234', 'lopez', 'administrador'),
    ('pablo','1234', 'perez', 'normal'),
    ('loreto','1234', 'rodriguez', 'normal'),
    ('teo','1234', 'torres', 'normal'),
    ('sergio','1234', 'lopez', 'normal'),
    ('david','1234', 'rodriguez', 'normal');

CREATE TABLE IF NOT EXISTS deporte (
        id_deporte INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_deporte varchar(30),
        fecha_inicio date,
        fecha_fin date,
        hora_inicio time,
        hora_fin time
);       
INSERT INTO `agenda`.`deporte` 
    (`nombre_deporte`, `fecha_inicio`, `fecha_fin`, `hora_inicio`, `hora_fin`) 
VALUES 
    ('futbol', '2024-09-01', '2024-12-30', '10:00', '12:00'),
    ('criquet', '2024-09-15', '2024-10-04', '09:00', '14:00'),
    ('padel', '2024-10-10', '2024-10-21', '16:00', '18:00'),
    ('natacion', '2024-11-21', '2024-12-15', '18:00', '19:00'),
    ('esgrima', '2024-12-01', '2024-12-31', '14:30', '21:30'),
    ('judo', '2024-10-20', '2024-11-20', '07:00', '10:00'),
    ('baloncesto', '2024-09-01', '2024-12-30', '10:00', '12:00'),
    ('beisbol', '2024-09-15', '2024-10-04', '09:00', '14:00'),
    ('tenis', '2024-10-10', '2024-10-21', '16:00', '18:00'),
    ('atletismo', '2024-11-21', '2024-12-15', '18:00', '19:00'),
    ('voleibol', '2024-12-01', '2024-12-31', '14:30', '21:30');
CREATE TABLE IF NOT EXISTS deportes_usuario (
    id_deporte int key not null,
    id_usuario int key not null,
    constraint `fk_deportes_usuario_deporte` foreign key (id_deporte) references deporte(id_deporte) ON UPDATE CASCADE ON DELETE CASCADE,
    constraint `fk_deportes_usuario_usuario` foreign key (id_usuario) references usuario(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE
); 
INSERT INTO `agenda`.`deportes_usuario` 
	(`id_deporte`, `id_usuario`)
VALUES 
    (1,2),
    (2,2);
CREATE TABLE IF NOT EXISTS dia_prohibido (
    id_dia_prohibido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_deporte int,
    fecha date,
    constraint `fk_dia_prohibido_deporte` foreign key (id_deporte) references deporte (id_deporte) on update cascade on delete cascade
); 