import mysql.connector
from mysql.connector import Error
# Si al conectar te dá el error de autentificación, debes cambiar el plugin de autentificación a mysql_native_password
# escribiendo en el workbench ALTER USER 'tu_usario'@'localhost' IDENTIFIED WITH mysql_native_password BY 'tu_contraseña';
def create_connection(host_name, user_name, user_password, db_name):
       connection = None
       try:
           connection = mysql.connector.connect(
               host=host_name,
               user=user_name,
               password=user_password,
               database=db_name,
               auth_plugin='mysql_native_password'
           )
           print("Conexión exitosa a la base de datos")
       except Error as e:
           print(f"Error '{e}' ocurrió")

       return connection

   # Reemplaza con tus credenciales


# cursor = connection.cursor()