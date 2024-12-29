import mysql.connector
from mysql.connector import Error

class MysqlClient():
        
    def connect(self, inicialicer_bd=False):
        self.schema_file="mysql-schema.sql"

        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="agenda",
                auth_plugin='mysql_native_password'
            )
            #print("Conexión exitosa a la base de datos mysql")
            self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Error '{e}' ocurrió")
            #si no existe la base de datos la creamos y la rellenamos
            #self.crear_base_de_datos()


    def close(self):
        if self.connection!=None:
            self.connection.close()
    def reset(self):
        if (self.connection!=None):
            self.connection.close()
        self.crear_base_de_datos()
        
    def crear_base_de_datos(self):
        print("Vamos a crear la base de datos agenda")
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("DROP DATABASE IF EXISTS agenda;")
        self.cursor.execute("CREATE DATABASE agenda")
        self.cursor.execute("USE agenda;")
        self.connection.commit()
        self.crear_tabla_usuario()
        self.crear_tabla_deporte()
        self.crear_tabla_deportes_usuario()
        self.crear_tabla_dia_prohibido()
        self.fake_inserts_usuarios()
        self.fake_inserts_deportes()
        self.close()
    """
    def crear_tablas_base_de_datos_desde_archivo(self, nombre_archivo):
        print("hemos entrado en crear tablas desde el archivo")
        lines=[]
        sql=""
        self.connection.commit()
        with open(nombre_archivo, "r", encoding="utf-8") as file:
            lines +=file.readlines()
            for line in lines:
                sql+=line
        self.cursor.execute(sql)
        self.connection.commit()
    """
    def crear_tabla_usuario(self):
        self.cursor.execute("DROP TABLE IF EXISTS usuario;")
        self.connection.commit()
        self.cursor.execute("""
        CREATE TABLE `usuario` (
            `id_usuario` int NOT NULL AUTO_INCREMENT,
            `nombre_usuario` varchar(20) DEFAULT NULL,
            `clave_usuario` varchar(255) DEFAULT NULL,
            `apellidos_usuario` varchar(50) DEFAULT NULL,
            `rol` enum('normal','administrador') DEFAULT 'normal',
            PRIMARY KEY (`id_usuario`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)
        self.connection.commit()
    def crear_tabla_deporte(self):
        self.cursor.execute("DROP TABLE IF EXISTS deporte;")
        self.connection.commit()
        self.cursor.execute("""
            CREATE TABLE `deporte` (
            `id_deporte` int NOT NULL AUTO_INCREMENT,
            `nombre_deporte` varchar(30) DEFAULT NULL,
            `fecha_inicio` date DEFAULT NULL,
            `fecha_fin` date DEFAULT NULL,
            `hora_inicio` time DEFAULT NULL,
            `hora_fin` time DEFAULT NULL,
            PRIMARY KEY (`id_deporte`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)
        self.connection.commit()
    def crear_tabla_deportes_usuario(self):
        self.cursor.execute("DROP TABLE IF EXISTS deportes_usuario;")
        self.connection.commit()
        self.cursor.execute("""
        CREATE TABLE `deportes_usuario` (
            `id_deporte` int NOT NULL,
            `id_usuario` int NOT NULL,
            PRIMARY KEY (`id_deporte`,`id_usuario`),
            KEY `fk_deportes_usuario_usuario` (`id_usuario`),
            CONSTRAINT `fk_deportes_usuario_deporte` FOREIGN KEY (`id_deporte`) REFERENCES `deporte` (`id_deporte`) ON UPDATE CASCADE ON DELETE CASCADE,
            CONSTRAINT `fk_deportes_usuario_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON UPDATE CASCADE ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)
        self.connection.commit()
    def crear_tabla_dia_prohibido(self):
        self.cursor.execute("DROP TABLE IF EXISTS dia_prohibido;")
        self.connection.commit()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dia_prohibido (
                    id_dia_prohibido int NOT NULL AUTO_INCREMENT,
                    id_deporte int,
                    fecha date,
                    PRIMARY KEY (`id_dia_prohibido`),
                    KEY `fk_dia_prohibido_deporte` (`id_deporte`),
                    CONSTRAINT `fk_dia_prohibido_deporte` FOREIGN KEY (`id_deporte`) REFERENCES `deporte` (`id_deporte`) ON UPDATE CASCADE ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;    
        """)
        self.connection.commit()
    def fake_inserts_usuarios(self):
        self.cursor.execute("""
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
        """)
        self.connection.commit()
    def fake_inserts_deportes(self):    
        self.cursor.execute("""
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
        """)
        self.connection.commit()
               




    # Usuarios
    ########################################################
    def obtener_todos_los_usuarios(self):
        self.cursor.execute("SELECT * FROM usuario")
        tuplas=self.cursor.fetchall()
        return tuplas
    def obtenr_todos_los_usuarios_por_id_usuario(self, id_usuario):
        self.cursor.execute(f"select * from usuario where id_usuario = '{id_usuario}'")
        tuplas = self.cursor.fetchall() 
        return tuplas
    def obtener_todos_los_usuarios_por_nombre_usuario(self, nombre_usuario):
        self.cursor.execute("select * from usuario where nombre_usuario = %s", (nombre_usuario,))
        tuplas=self.cursor.fetchall()
        return tuplas
    def obtener_el_id_usuario_a_partir_del_nombre_usuario(self, nombre_usuario):
        self.cursor.execute("select id_usuario from usuario where nombre_usuario = %s", (nombre_usuario,))
        id_usuario=self.cursor.fetchall()[0][0]
        return id_usuario
    def anadir_un_nuevo_usuario(self, nombre_usuario, clave_usuario, apellidos_usuario):
        self.cursor.execute("insert into usuario (nombre_usuario, clave_usuario, apellidos_usuario, rol) values (%s, %s, %s, %s)", (nombre_usuario, clave_usuario, apellidos_usuario, "normal"))
        self.connection.commit()
    def actualizar_un_usuario(self, id, nombre, apellido, clave):
        self.cursor.execute(f"update usuario set nombre_usuario='{nombre}',apellidos_usuario ='{apellido}', clave_usuario='{clave}'  where id_usuario = '{id}'")
        self.connection.commit()
    def borrar_un_usuario(self, id):
        self.cursor.execute(f"delete from usuario where id_usuario = '{id}'")
        self.connection.commit()
    def borrar_todos_los_usuarios(self):
        self.cursor.execute(f"delete from usuario")
        self.connection.commit()




    # Deportes
    ########################################################
    def obtener_todos_los_deportes(self):
        self.cursor.execute("select * from deporte")
        tuplas=self.cursor.fetchall()
        return tuplas
    def obtener_todos_los_deportes_por_id_deporte(self, id_deporte):
        self.cursor.execute(f"select * from deporte where id_deporte = '{id_deporte}'")
        tuplas = self.cursor.fetchall() 
        return tuplas
    def obtener_todos_los_deportes_por_nombe_deporte(self, nombre_deporte):
        self.cursor.execute("select * from deporte where nombre_deporte like %s", ("%"+nombre_deporte+"%",))
        tuplas=self.cursor.fetchall()
        return tuplas
    def obtener_el_id_deporte_a_partir_del_nombre_deporte(self, nombre_deporte):
        self.cursor.execute("select id_deporte from deporte where nombre_deporte = %s", (nombre_deporte,))
        id_deporte=self.cursor.fetchall()[0][0]
        return id_deporte
    def obtener_todos_los_deportes_por_nombre_de_usuario(self, nombre_usuario):
        self.cursor.execute(f"""select d.nombre_deporte
                        from deporte d
                        inner join deportes_usuario du on d.id_deporte = du.id_deporte
                        where du.id_usuario = (select id_usuario from usuario where nombre_usuario ='{nombre_usuario}')
                    """)
        tuplas=self.cursor.fetchall()
        return tuplas
    def obtener_todos_los_deportes_por_nombre_de_usuario2(self, nombre_usuario):
        self.cursor.execute(f"""select d.id_deporte, d.nombre_deporte, d.fecha_inicio, d.fecha_fin, d.hora_inicio, d.hora_fin
                            from deporte d
                            inner join deportes_usuario du on d.id_deporte = du.id_deporte
                            where du.id_usuario = (select id_usuario from usuario where nombre_usuario ='{nombre_usuario}')
                        """)
        tuplas=self.cursor.fetchall()
        return tuplas
    def anadir_un_nuevo_deporte(self, nombre_deporte, fecha_inicio, fecha_fin, hora_inicio, hora_fin):
        self.cursor.execute(f"insert into deporte (nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin) values (%s,%s,%s,%s,%s)", (nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin))
        self.connection.commit()
    def actualizar_deporte(self, id_deporte, nombre_deporte, fecha_inicio, fecha_fin, hora_inicio, hora_fin):
        self.cursor.execute(f"update deporte set nombre_deporte='{nombre_deporte}',fecha_inicio ='{fecha_inicio}',fecha_fin='{fecha_fin}',hora_inicio='{hora_inicio}',hora_fin='{hora_fin}' where id_deporte = '{id_deporte}'")
        self.connection.commit()
    def borrar_un_deporte(self, id_deporte):
        self.cursor.execute(f"delete from deporte where id_deporte = '{id_deporte}'")
        self.connection.commit()
    def borrar_todos_los_deportes(self):
        self.cursor.execute(f"delete from deporte")
        self.connection.commit()

    






    #deportes_usuario
    ########################################################
    def obtener_todos_los_deportes_usuario(self):
        self.cursor.execute("SELECT * FROM deportes_usuario")
        tuplas=self.cursor.fetchall()
        return tuplas
    def obtener_todos_los_deportes_usuario_por_id_deporte_y_id_usuario(self, id_deporte, id_usuario):
        self.cursor.execute(f"select * from deportes_usuario where id_deporte = '{id_deporte}' and id_usuario='{id_usuario}'")
        tuplas = self.cursor.fetchall() 
        return tuplas
    def obtener_deportes_usuario_por_id_usuario(self, id_usuario):
        self.cursor.execute("select * from deportes_usuario where id_usuario = %s", (id_usuario,))
        tuplas=self.cursor.fetchall()
        return tuplas
    def insertar_nuevo_deporte_usuario(self, id_deporte, id_usuario):
        self.cursor.execute(f"insert into deportes_usuario (id_deporte, id_usuario) values (%s,%s)", (id_deporte,id_usuario,))
        self.connection.commit()
    def actualizar_deportes_usuario(self, id_deporte_nuevo, id_usuario_nuevo, id_deporte_viejo, id_usuario_viejo):
        self.cursor.execute(f"update deportes_usuario set id_deporte='{id_deporte_nuevo}',id_usuario ='{id_usuario_nuevo}' where id_deporte = '{id_deporte_viejo}' and id_usuario='{id_usuario_viejo}'")
        self.connection.commit()
    def eliminar_deporte_usuario_por_id_deporte_y_id_usuario(self, id_deporte, id_usuario):
        self.cursor.execute(f"delete from deportes_usuario where id_deporte = '{id_deporte}' and id_usuario ='{id_usuario}'")
        self.connection.commit()
    def elimnar_deportes_usuario(self, id_deporte, id_usuario):
        self.cursor.execute(f"delete from deportes_usuario where id_deporte = '{id_deporte}' and id_usuario='{id_usuario}'")
        self.connection.commit()
    def borrar_todos_los_deportes_usuario(self):
        self.cursor.execute(f"delete from deportes_usuario")
        self.connection.commit()




    #dias prohibidos
    ########################################################
    def obtener_todos_los_dias_prohibidos(self):
        self.cursor.execute("SELECT * FROM dia_prohibido")
        tuplas=self.cursor.fetchall()
        return tuplas
    def obtener_todos_los_dias_prohibidos_por_id(self, id_dia_prohibido):
        self.cursor.execute(f"select * from dia_prohibido where id_dia_prohibido = '{id_dia_prohibido}'")
        tuplas = self.cursor.fetchall() 
        return tuplas
    def obtener_dias_prohibido_por_id_deporte(self, id_deporte):
        self.cursor.execute("select * from dia_prohibido where id_deporte = %s", (id_deporte,))
        tuplas=self.cursor.fetchall()
        return tuplas

    def obtener_todos_los_dias_prohibidos_por_id_deporte_y_fecha(self, id_deporte, fecha):
        self.cursor.execute("select * from dia_prohibido where id_deporte = %s and fecha = %s", (id_deporte,fecha))
        tuplas=self.cursor.fetchall()
        return tuplas
    def insertar_nuevo_dia_prohibido(self, id_deporte, fecha):
        self.cursor.execute(f"insert into dia_prohibido (id_deporte, fecha) values (%s,%s)", (id_deporte,fecha,))
        self.connection.commit()
    def actualizar_dia_prohibido(self, id_dia_prohibido, id_deporte, fecha):
        self.cursor.execute(f"update dia_prohibido set id_deporte='{id_deporte}',fecha ='{fecha}' where id_dia_prohibido = '{id_dia_prohibido}'")
        self.connection.commit()
    def elimnar_dia_prohibido(self, id_dia_prohibido):
        self.cursor.execute(f"delete from dia_prohibido where id_dia_prohibido = '{id_dia_prohibido}'")
        self.connection.commit()
    def borrar_todos_los_dias_prohibidos(self):
        self.cursor.execute(f"delete from dia_prohibido")
        self.connection.commit()