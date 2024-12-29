
import sqlite3
import os
class SqliteClient:  
        
    def connect(self):
        self.SQLITE_DB="agenda.db"
        inicializar_bd=False
        if not os.path.exists(self.SQLITE_DB):
            inicializar_bd=True
        try:
            self.connection=sqlite3.connect(self.SQLITE_DB, check_same_thread=False)
            #print("Conexión existosa a base de datos sqlite")
            self.cursor=self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys=ON");
            self.connection.commit()
        except Exception as e:
            print(f"currió un error al conectar con sqlite: {e}")
        if inicializar_bd:
            self.create_table_usuario()
            self.create_table_deporte()
            self.create_table_deportes_usuario()
            self.create_table_dia_prohibido()
            self.add_fake_users()
            self.add_fake_deportes()
            self.add_fake_deportes_usuarios()
            #self.add_fake_dias_prohibidos()

    def close(self):
        if self.connection!=None:
            self.connection.close()
    def get_connection(self):
        return self.connection
    def get_cursor(self):
        return self.cursor
    def reset(self):
        self.cursor.execute("DROP TABLE IF EXISTS dia_prohibido")
        self.cursor.execute("DROP TABLE IF EXISTS deportes_usuario")
        self.cursor.execute("DROP TABLE IF EXISTS deporte")
        self.cursor.execute("DROP TABLE IF EXISTS usuario")
       
        self.connection.commit()
        self.create_table_usuario()
        self.create_table_deporte()
        self.create_table_deportes_usuario()
        self.create_table_dia_prohibido()
        self.add_fake_users()
        self.add_fake_deportes()
    
    # USUARIOS
    #######################################################  
    def create_table_usuario(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario varchar(20),
                clave_usuario varchar(255),
                apellidos_usuario varchar(50),
                rol varchar(20) default 'normal'
        );         
        ''')
        self.connection.commit()
    def add_fake_users(self):
        self.cursor.executemany("insert into usuario (`nombre_usuario`, `clave_usuario`, `apellidos_usuario`, `rol`)values (?,?,?,?);",
            [
                ('kike','1234', 'martinez', 'administrador'),
                ('carlos','1234', 'lopez', 'administrador'),
                ('pablo','1234', 'perez', 'normal'),
                ('loreto','1234', 'rodriguez', 'normal'),
                ('teo','1234', 'torres', 'normal'),
                ('sergio','1234', 'lopez', 'normal'),
                ('david','1234', 'rodriguez', 'normal')
            ]
        )  
        self.connection.commit()


    




        
   # deportes
    #######################################################
    def create_table_deporte(self): 
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS deporte (
                id_deporte INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_deporte varchar(30),
                fecha_inicio date,
                fecha_fin date,
                hora_inicio time,
                hora_fin time
        );         
        ''')
        self.connection.commit()


    def add_fake_deportes(self):
        self.cursor.executemany("insert into deporte (`nombre_deporte`, `fecha_inicio`, `fecha_fin`, `hora_inicio`, `hora_fin`) values (?,?,?,?,?);",
            [
                ('futbol', '2024-09-01', '2024-12-30', '10:00', '12:00'),
                ('criquet', '2024-09-15', '2024-12-20', '09:00', '14:00'),
                ('padel', '2024-12-01', '2024-12-03', '16:00', '18:00'),
                ('natacion', '2024-12-21', '2024-12-22', '18:00', '19:00')
            ]
        )
        self.connection.commit()


    # deportes_usuarios
    #######################################################
    # da error con 2 claves primarias
    def create_table_deportes_usuario(self): 
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS deportes_usuario (
                id_deporte int key not null,
                id_usuario int key not null,
                constraint `fk_deportes_usuario_deporte` foreign key (id_deporte) references deporte(id_deporte) ON UPDATE CASCADE ON DELETE CASCADE,
                constraint `fk_deportes_usuario_usuario` foreign key (id_usuario) references usuario(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE

        );         
        ''')
        self.connection.commit()
        """
        self.cursor.execute("ALTER table deportes_usuario 
                            add constraint fk_deportes_usuarios_usuario foreign key (id_usuario)
                            references usuario (id_usuario) on update cascade on delete no action;
                            ")
        self.connection.commit()
        """
    def add_fake_deportes_usuarios(self):
        self.cursor.executemany("insert into deportes_usuario (`id_deporte`, `id_usuario`) values (?,?);",
            [
                (1,3)
            ]
        )
        self.connection.commit()

    def create_table_dia_prohibido(self): 
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS dia_prohibido (
                id_dia_prohibido INTEGER PRIMARY KEY AUTOINCREMENT,
                id_deporte int,
                fecha date,
                constraint `fk_dia_prohibido_deporte` foreign key (id_deporte) references deporte (id_deporte) on update cascade on delete cascade
        );         
        ''')
        self.connection.commit()

    def add_fake_dias_prohibidos(self):
        self.cursor.executemany("insert into dia_prohibido (`id_deporte`, `fecha`) values (?,?);",
            [
                (1,'2024-12-01')
            ]
        )
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
        self.cursor.execute("select * from usuario where nombre_usuario = ?", (nombre_usuario,))
        tuplas=self.cursor.fetchall()
        return tuplas
    def obtener_el_id_usuario_a_partir_del_nombre_usuario(self, nombre_usuario):
        self.cursor.execute("select id_usuario from usuario where nombre_usuario = ?", (nombre_usuario,))
        id_usuario=self.cursor.fetchall()[0][0]
        return id_usuario
    def anadir_un_nuevo_usuario(self, nombre_usuario, clave_usuario, apellidos_usuario):
        self.cursor.execute("insert into usuario (nombre_usuario, clave_usuario, apellidos_usuario, rol) values (?, ?, ?, ?)", (nombre_usuario, clave_usuario, apellidos_usuario, "normal"))
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
        self.cursor.execute("select * from deporte where nombre_deporte like ?", ("%"+nombre_deporte+"%",))
        tuplas=self.cursor.fetchall()
        return tuplas
    def obtener_el_id_deporte_a_partir_del_nombre_deporte(self, nombre_deporte):
        self.cursor.execute("select id_deporte from deporte where nombre_deporte = ?", (nombre_deporte,))
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
        self.cursor.execute(f"insert into deporte (nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin) values (?,?,?,?,?)", (nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin))
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
        self.cursor.execute("select * from deportes_usuario where id_usuario = ?", (id_usuario,))
        tuplas=self.cursor.fetchall()
        return tuplas
  
    def obtener_todos_los_deportes_usuario_por_id_deporte(self, id_deporte):
        self.cursor.execute("select * from deportes_usuario where id_deporte = ?", (id_deporte,))
        tuplas=self.cursor.fetchall()
        return tuplas
    def insertar_nuevo_deporte_usuario(self, id_deporte, id_usuario):
        self.cursor.execute(f"insert into deportes_usuario (id_deporte, id_usuario) values (?,?)", (id_deporte,id_usuario,))
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
        self.cursor.execute("select * from dia_prohibido where id_deporte = ?", (id_deporte,))
        tuplas=self.cursor.fetchall()
        return tuplas
    def obtener_todos_los_dias_prohibido_por_id_deporte_y_fecha(self, id_deporte, fecha):
        self.cursor.execute("select * from dia_prohibido where id_deporte = ? and fecha = ?", (id_deporte,fecha))
        tuplas=self.cursor.fetchall()
        return tuplas
    def insertar_nuevo_dia_prohibido(self, id_deporte, fecha):
        self.cursor.execute(f"insert into dia_prohibido (id_deporte, fecha) values (?,?)", (id_deporte,fecha,))
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