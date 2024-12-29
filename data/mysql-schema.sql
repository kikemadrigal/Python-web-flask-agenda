CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(20) DEFAULT NULL,
  `clave_usuario` varchar(255) DEFAULT NULL,
  `apellidos_usuario` varchar(50) DEFAULT NULL,
  `rol` enum('normal','administrador') DEFAULT 'normal',
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `agenda`.`usuario` 
	(`nombre_usuario`, `clave_usuario`, `apellidos_usuario`, `rol`)
VALUES 
    ('kike','1234', 'martinez', 'administrador'),
    ('carlos','1234', 'lopez', 'administrador'),
    ('pablo','1234', 'perez', 'normal'),
    ('loreto','1234', 'rodriguez', 'normal'),
    ('teo','1234', 'torres', 'normal'),
    ('sergio','1234', 'lopez', 'normal'),
    ('david','1234', 'rodriguez', 'normal');



DROP TABLE IF EXISTS `deporte`;

CREATE TABLE `deporte` (
  `id_deporte` int NOT NULL AUTO_INCREMENT,
  `nombre_deporte` varchar(30) DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `hora_inicio` time DEFAULT NULL,
  `hora_fin` time DEFAULT NULL,
  PRIMARY KEY (`id_deporte`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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




DROP TABLE IF EXISTS `deportes_usuario`;
CREATE TABLE `deportes_usuario` (
  `id_deporte` int NOT NULL,
  `id_usuario` int NOT NULL,
  PRIMARY KEY (`id_deporte`,`id_usuario`),
  KEY `fk_deportes_usuario_usuario` (`id_usuario`),
  CONSTRAINT `fk_deportes_usuario_deporte` FOREIGN KEY (`id_deporte`) REFERENCES `deporte` (`id_deporte`) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT `fk_deportes_usuario_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/* Otra manera de hacerlo sin poner el key 'fk_deportes_usuario_usurio y el key fk_deporte_usuario_usuario' y los constrainst es escribiendo después:
alter table deportes_usuario add constraint fk_deportes_usuario_usuario foreign key (id_usuario) references usuario (id_usuario) on update cascade on delete no action;
alter table deportes_usuario add constraint fk_deportes_usuario_deporte foreign key (id_deporte) references deporte (id_deporte) on update cascade on delete no action;*/
INSERT INTO `agenda`.`deportes_usuario` 
	(`id_deporte`, `id_usuario`)
VALUES 
    (1,2),
    (2,2);


DROP TABLE IF EXISTS `dia_prohibido`;
   
CREATE TABLE IF NOT EXISTS dia_prohibido (
        id_dia_prohibido int NOT NULL AUTO_INCREMENT,
        id_deporte int,
        fecha date,
        PRIMARY KEY (`id_dia_prohibido`),
        KEY `fk_dia_prohibido_deporte` (`id_deporte`),
        CONSTRAINT `fk_dia_prohibido_deporte` FOREIGN KEY (`id_deporte`) REFERENCES `deporte` (`id_deporte`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;         
/*otra forma de crear el foregn key es crear la tabla sin él y escribir:
alter table dia_prohibido add constraint fk_dia_prohibido_deporte foreign key (id_deporte) references deporte (id_deporte) on update cascade on delete no action;
*/
