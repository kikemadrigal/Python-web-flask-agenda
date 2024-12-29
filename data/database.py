from data.mysqlClient import MysqlClient
from data.sqliteClient import SqliteClient

class Database:
    database_engine_mysql="mysql"
    database_engine_sqlite="sqlite"

    def __init__(self):
        #self.mysqlClient =  MysqlClient()
        self.mysqlClient =  None
        self.sqliteClient = SqliteClient()
        self.database_engine_name_current="sqlite"
    def connect(self):
        """
        Se conecta a la base de datos
        """
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.connect()
        else:
            self.sqliteClient.connect()

    def get_database_engine_name_current(self):
        """
        Se devuelve el nombre de la bse de datos actual
        """
        return self.database_engine_name_current
    def set_database_engine_name_current(self,database_engine_name_current):
        """
        Se establece el nombre de la base de datos actual

        Args:
            nombre de la base de datos
        """
        self.database_engine_name_current=database_engine_name_current
    def close(self):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.close()
            #print("Cerrando base de datos mysql")
        else:
            self.sqliteClient.close()
            #print("Cerrando base de datos sqlite")
    def database_reset(self):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.reset()
        else:
            self.sqliteClient.reset()



    # Usuarios
    ####################################################################################
    def obtener_todos_los_usuarios(self):
        """
        Hace una consulta la base de datos para pedir los usuarios

        Return
            Devuelve una tupla con los usuarios
        """
        if self.database_engine_name_current==Database.database_engine_mysql:
            usuarios=self.mysqlClient.obtener_todos_los_usuarios()
        else:
            usuarios=self.sqliteClient.obtener_todos_los_usuarios()
        return usuarios
    def obtener_todos_los_usuarios_por_nombre_usuario(self, nombre):
        """
        Hace una consulta para obtener los usuarios por nombre_usuario

        Args:
            nombre_usuario
        
        """
        if self.database_engine_name_current==Database.database_engine_mysql:
            lista_tuplas=self.mysqlClient.obtener_todos_los_usuarios_por_nombre_usuario(nombre)
        else:
            lista_tuplas=self.sqliteClient.obtener_todos_los_usuarios_por_nombre_usuario(nombre)
        return lista_tuplas
    def obtenr_todos_los_usuarios_por_id_usuario(self,id):
        if self.database_engine_name_current==Database.database_engine_mysql:
            usuarios=self.mysqlClient.obtenr_todos_los_usuarios_por_id_usuario(id)
        else:
            usuarios=self.sqliteClient.obtenr_todos_los_usuarios_por_id_usuario(id)
        return usuarios
    def anadir_un_nuevo_usuario(self,nombre_usuario, clave_usuario, apellidos_usuario):
        if self.database_engine_name_current==self.database_engine_mysql:
            self.mysqlClient.anadir_un_nuevo_usuario(nombre_usuario, clave_usuario, apellidos_usuario)
        else:
            self.sqliteClient.anadir_un_nuevo_usuario(nombre_usuario, clave_usuario, apellidos_usuario)
    def actualizar_un_usuario(self,id,nombre,apellido,clave):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.actualizar_un_usuario(id,nombre,apellido,clave)
        else:
            self.sqliteClient.actualizar_un_usuario(id,nombre,apellido,clave)
    def borrar_un_usuario(self,id):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.borrar_un_usuario(id)
        else:
            self.sqliteClient.borrar_un_usuario(id)
    def borrar_todos_los_usuarios(self):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.borrar_todos_los_usuarios()
        else:
            self.sqliteClient.borrar_todos_los_usuarios()






    # deportes
    ####################################################################################
    def obtener_todos_los_deportes(self):
        if self.database_engine_name_current==Database.database_engine_mysql:
            deportes=self.mysqlClient.obtener_todos_los_deportes()
        else:
            deportes=self.sqliteClient.obtener_todos_los_deportes()
        return deportes

    def obtener_todos_los_deportes_por_nombre_deporte(self, text_search):
        if self.database_engine_name_current==Database.database_engine_mysql:
            deportes=self.mysqlClient.obtener_todos_los_deportes_por_nombe_deporte(text_search)
        else:
            deportes=self.sqliteClient.obtener_todos_los_deportes_por_nombe_deporte(text_search)
        return deportes
    def obtener_todos_los_deportes_por_nombre_de_usuario2(self,nombre_usuario):
        if self.database_engine_name_current==Database.database_engine_mysql:
            deportes=self.mysqlClient.obtener_todos_los_deportes_por_nombre_de_usuario2(nombre_usuario)
        else:
            deportes=self.sqliteClient.obtener_todos_los_deportes_por_nombre_de_usuario2(nombre_usuario)
        return deportes
    def obtener_el_id_usuario_a_partir_del_nombre_usuario(self,nombre_usuario):
        if self.database_engine_name_current==Database.database_engine_mysql:
            id_usuario=self.mysqlClient.obtener_el_id_usuario_a_partir_del_nombre_usuario(nombre_usuario)
        else:
            id_usuario=self.sqliteClient.obtener_el_id_usuario_a_partir_del_nombre_usuario(nombre_usuario)
        return id_usuario
    def obtener_el_id_deporte_a_partir_del_nombre_deporte(self,nombre_deporte):
        if self.database_engine_name_current==Database.database_engine_mysql:
            id_deporte=self.mysqlClient.obtener_el_id_deporte_a_partir_del_nombre_deporte(nombre_deporte)
        else:
            id_deporte=self.sqliteClient.obtener_el_id_deporte_a_partir_del_nombre_deporte(nombre_deporte)
        return id_deporte
    def insertar_nuevo_deporte_usuario(self,id_deporte, id_usuario):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.insertar_nuevo_deporte_usuario(id_deporte, id_usuario)
        else:
            self.sqliteClient.insertar_nuevo_deporte_usuario(id_deporte, id_usuario)

    def obtener_deportes_usuario_por_id_usuario(self,id_usuario):
        if self.database_engine_name_current==Database.database_engine_mysql:
            deportes_usuario=self.mysqlClient.obtener_deportes_usuario_por_id_usuario(id_usuario)
        else:
            deportes_usuario=self.sqliteClient.obtener_deportes_usuario_por_id_usuario(id_usuario)
        return deportes_usuario
    def obtener_todos_los_deportes_por_nombre_de_usuario(self,nombre_usuario):
        if self.database_engine_name_current==Database.database_engine_mysql:
            deportes_usuario=self.mysqlClient.obtener_todos_los_deportes_por_nombre_de_usuario(nombre_usuario)
        else:
            deportes_usuario=self.sqliteClient.obtener_todos_los_deportes_por_nombre_de_usuario(nombre_usuario)
        return deportes_usuario
    def obtener_todos_los_deportes_por_id_deporte(self,id_deporte):
        if self.database_engine_name_current==Database.database_engine_mysql:
            deportes = self.mysqlClient.obtener_todos_los_deportes_por_id_deporte(id_deporte)
        else:
            deportes = self.sqliteClient.obtener_todos_los_deportes_por_id_deporte(id_deporte)
        return deportes
    def anadir_un_nuevo_deporte(self,nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.anadir_un_nuevo_deporte(nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin)
        else:
            self.sqliteClient.anadir_un_nuevo_deporte(nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin)
    def actualizar_deporte(self,id_deporte,nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.actualizar_deporte(id_deporte,nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin)
        else:
            self.sqliteClient.actualizar_deporte(id_deporte,nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin)
    def borrar_un_deporte(self,id_deporte):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.borrar_un_deporte(id_deporte)
        else:
            self.sqliteClient.borrar_un_deporte(id_deporte)
    def borrar_todos_los_deportes(self):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.borrar_todos_los_deportes()
        else:
            self.sqliteClient.borrar_todos_los_deportes()




    # deportes_usuario
    ##########################################################################

    def obtener_todos_los_deportes_usuario(self):
        if self.database_engine_name_current==Database.database_engine_mysql:
            deportes_usuario=self.mysqlClient.obtener_todos_los_deportes_usuario()
        else:
            deportes_usuario=self.sqliteClient.obtener_todos_los_deportes_usuario()
        return deportes_usuario
    def obtener_todos_los_deportes_usuario_por_id_deporte_y_id_usuario(self,id_deporte, id_usuario):
        if self.database_engine_name_current==Database.database_engine_mysql:
            deportes_usuario = self.mysqlClient.obtener_todos_los_deportes_usuario_por_id_deporte_y_id_usuario(id_deporte, id_usuario)
        else:
            deportes_usuario = self.sqliteClient.obtener_todos_los_deportes_usuario_por_id_deporte_y_id_usuario(id_deporte, id_usuario)
        return deportes_usuario
        
    """
    def obtener_todos_los_deportes_usuario_por_id_deporte(self,id_deporte):
        if self.database_engine_name_current==Database.database_engine_mysql:
            deportes_usuario = self.mysqlClient.obtener_todos_los_deportes_usuario_por_id(id_deporte)
        else:
            deportes_usuario = self.sqliteClient.obtener_todos_los_deportes_usuario_por_id_deporte(id_deporte)
        return deportes_usuario
    """
    
    def insertar_nuevo_deporte_usuario(self,id_deporte,id_usuario):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.insertar_nuevo_deporte_usuario(id_deporte,id_usuario)
        else:
            self.sqliteClient.insertar_nuevo_deporte_usuario(id_deporte,id_usuario)

    def actualizar_deportes_usuario(self,id_deporte_nuevo,id_usuario_nuevo,id_deporte_viejo,id_usuario_viejo):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.actualizar_deportes_usuario(id_deporte_nuevo,id_usuario_nuevo,id_deporte_viejo,id_usuario_viejo)
        else:
            self.sqliteClient.actualizar_deportes_usuario(id_deporte_nuevo,id_usuario_nuevo,id_deporte_viejo,id_usuario_viejo)
    def eliminar_deporte_usuario_por_id_deporte_y_id_usuario(self, id_deporte, id_usuario):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.eliminar_deporte_usuario_por_id_deporte_y_id_usuario(id_deporte, id_usuario)
        else:
            self.sqliteClient.eliminar_deporte_usuario_por_id_deporte_y_id_usuario(id_deporte, id_usuario)
    
    
    def elimnar_deportes_usuario(self,id_deporte, id_usuario):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.elimnar_deportes_usuario(id_deporte, id_usuario)
        else:
            self.sqliteClient.elimnar_deportes_usuario(id_deporte, id_usuario)
    def borrar_todos_los_deportes_usuario(self):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.borrar_todos_los_deportes_usuario()
        else:
            self.sqliteClient.borrar_todos_los_deportes_usuario()



    # dia prohibido
    ##########################################################################

    def obtener_todos_los_dias_prohibidos(self):
        if self.database_engine_name_current==Database.database_engine_mysql:
            dias_prohibidos=self.mysqlClient.obtener_todos_los_dias_prohibidos()
        else:
            dias_prohibidos=self.sqliteClient.obtener_todos_los_dias_prohibidos()
        return dias_prohibidos
    def obtener_todos_los_dias_prohibidos_por_id(self,id_dia_prohibido):
        if self.database_engine_name_current==Database.database_engine_mysql:
            dia_prohibido = self.mysqlClient.obtener_todos_los_dias_prohibidos_por_id(id_dia_prohibido)
        else:
            dia_prohibido = self.sqliteClient.obtener_todos_los_dias_prohibidos_por_id(id_dia_prohibido)
        return dia_prohibido
    def obtener_todos_los_dias_prohibidos_por_id_deporte(self,id_deporte):
        if self.database_engine_name_current==Database.database_engine_mysql:
            dias_prohibidos = self.mysqlClient.obtener_dias_prohibido_por_id_deporte(id_deporte)
        else:
            dias_prohibidos = self.sqliteClient.obtener_dias_prohibido_por_id_deporte(id_deporte)
        return dias_prohibidos
    def obtener_todos_los_dias_prohibidos_por_id_deporte_y_fecha(self,id_deporte, fecha):
        if self.database_engine_name_current==Database.database_engine_mysql:
            dias_prohibidos = self.mysqlClient.obtener_todos_los_dias_prohibidos_por_id_deporte_y_fecha(id_deporte, fecha)
        else:
            dias_prohibidos = self.sqliteClient.obtener_todos_los_dias_prohibido_por_id_deporte_y_fecha(id_deporte, fecha)
        return dias_prohibidos
    def insertar_nuevo_dia_prohibido(self,id_deporte,fecha):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.insertar_nuevo_dia_prohibido(id_deporte,fecha)
        else:
            self.sqliteClient.insertar_nuevo_dia_prohibido(id_deporte,fecha)

    def actualizar_dia_prohibido(self,id_dia_prohibido,id_deporte,fecha):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.actualizar_dia_prohibido(id_dia_prohibido,id_deporte,fecha)
        else:
            self.sqliteClient.actualizar_dia_prohibido(id_dia_prohibido,id_deporte,fecha)

    def elimnar_dia_prohibido(self,id_dia_prohibido):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.elimnar_dia_prohibido(id_dia_prohibido)
        else:
            self.sqliteClient.elimnar_dia_prohibido(id_dia_prohibido)
    def borrar_todos_los_dias_prohibidos(self):
        if self.database_engine_name_current==Database.database_engine_mysql:
            self.mysqlClient.borrar_todos_los_dias_prohibidos()
        else:
            self.sqliteClient.borrar_todos_los_dias_prohibidos()