from flask import render_template,request,redirect,flash, url_for, session, jsonify
from mainFlask import MainFlask
from data.database import Database
from routesManager import *
#https://docs.python.org/es/3/library/calendar.html
import calendar
import datetime
from utils.utils import *
#pip install -U flask-cors: https://flask-cors.readthedocs.io/en/latest/
from flask_cors import CORS, cross_origin
ruta_base = "https://agenda-ai2z.onrender.com"
# La app y la base de datos está inicializada en una clase de tipo 
# singleton para poder usarlas en otros archivos
app = MainFlask.getFlask()
CORS(app)
#cors = CORS(app, resources={r"/api/*": {"origins": "https://agenda-ai2z.onrender.com/"}})
database:Database= MainFlask.get_database()

# Puedes utilizar la base de datos de tipo mysql con la siguiente instrucción
#database.set_database_engine_name_current(database.database_engine_mysql)

@app.before_request
def before_request_func():
    database.connect()
        
@app.after_request
def after_request_func(response):
    #database.close()
    return response

#####################################################################
#####################################################################
#####################################################################
# #          Rutas: index, about, contact y search
#####################################################################
#####################################################################
#####################################################################
@app.route("/")
@app.route("/index/<int:anio_actual>/<int:mes_actual>")
def index(anio_actual=-1, mes_actual=-1):
    """
    Se fecine la ruta de la página principal

    Args:
        Año y mes, por defecto será -1
    Return:
        La vista index.html

    """
    if (anio_actual==-1):
        anio_actual=datetime.datetime.now().year
    if (mes_actual==-1):
        mes_actual=datetime.datetime.now().month
    if (mes_actual>12):
        mes_actual=1
        anio_actual=anio_actual+1
    elif (mes_actual==0):
        mes_actual=12
        anio_actual=anio_actual-1
    # Creamos nuestro diccionario de tipo calendario[anio][mes][dia]["actividad"][]
    # en el que guardaremos nuestros actividades deportivas que es una lista de string
    anios = [2024, 2025]
    diccionario_calendario = generar_diccionario_calendario(anios)
    #Obetenemos todos las actividades deportivas y las guardamos en el diccionario_calendario
    acitividades_deportivas=database.obtener_todos_los_deportes()
    for anio in anios:
        for mes, dias in diccionario_calendario[anio].items():
            for dia, info in dias.items():
                #print("dia",dia)
                #print("-------"*20)
                for deporte in acitividades_deportivas:
                    fecha_inicio=datetime.datetime.strptime(str(deporte[2]), "%Y-%m-%d").date()
                    fecha_fin=datetime.datetime.strptime(str(deporte[3]), "%Y-%m-%d").date()
                    fecha=datetime.date(anio,mes,dia)
                    dias_prohibidos=database.obtener_todos_los_dias_prohibidos_por_id_deporte(deporte[0])
                    if fecha >= fecha_inicio and fecha <= fecha_fin:
                        #print("dia prohibido de la fecha", fecha, " son ", dias_prohibidos)
                        dia_prohibido_encontrado=False
                        for dia_prohibido in dias_prohibidos:
                            fecha_dia_prohibido=datetime.datetime.strptime(str(dia_prohibido[2]), "%Y-%m-%d").date()
                            if fecha_dia_prohibido == fecha:
                                dia_prohibido_encontrado=True
                        if not dia_prohibido_encontrado:
                            agregar_actividad(diccionario_calendario, anio, mes, dia, deporte[1]+" "+str(deporte[4])+" - "+str(deporte[5]))
                    

    # Obtenemos un calndario ya configurado que hay dentro de la clase Calendar en python, 
    # se lo pasamos a la vista para dibujar mejor
    monthcalendar=calendar.monthcalendar(anio_actual, mes_actual)
    return render_template("index.html", monthcalendar=monthcalendar,calendario=diccionario_calendario, mes_actual=mes_actual, anio_actual=anio_actual, deportes=acitividades_deportivas)


@app.route("/about")
def about():
    """
    Se define la ruta de la página donde se describe el funcionamiento de la web

    Return
        La vista about.html

    """
    return render_template("about.html")

@app.route("/contact")
def contact():
    """
    Se define la ruta de la página donde se describe donde se dan los enlaces para comunicarse con nostros

    Return:
        la vista contact.html

    """
    return render_template("contact.html")

@app.route("/search", methods = ["POST"])
def search():
    """
    Página donde se muestra un formulario para buscar actividades deportivas
    
    Args:
        POST['search']
    
    Return:
        La vista search

    """
    if request.method == "POST":
        text_search = request.form.get("search")
        deportes=database.obtener_todos_los_deportes_por_nombre_deporte(text_search)
    return render_template("search.html", deportes=deportes)












#####################################################################
#####################################################################
#####################################################################
#                          Rutas auth
#####################################################################
#####################################################################
#####################################################################
@app.route("/form-login")
def form_login():
    """
    Muestra un formaulario de login
    """
    return render_template("auth/form-login.html")

@app.route("/login", methods = ["POST"])
def login():
    """
    Contiene la logica de login
    """
    nombre = request.form.get("nombre_usuario")
    clave = request.form.get("clave")
    nombre=nombre.lower()
    if check_empty(nombre) or check_empty(clave):
        flash("No puede haber campos vacios")
        return redirect(url_for("form_login"))
    lista_tuplas=database.obtener_todos_los_usuarios_por_nombre_usuario(nombre)
    if (len(lista_tuplas)==0):
        print("El usuario no existe")
        flash("El usuario no existe")
        return redirect(url_for("form_login"))
    usuario=lista_tuplas[0]
    print (usuario)
    print("la clave es", clave)
    print("alacenada: ",usuario[2])
    if clave != usuario[2]:
        print("La clave no es correcta")
        flash("La clave es incorrecta ")
        return redirect(url_for("form_login"))
    else:
        print("La clave es correcta ", nombre)
        session["nombre"] = nombre
        session["rol"] = usuario[4]
        print("rol", usuario[4])
        if usuario[4] == "administrador":
            return redirect(url_for("menu_admin"))
        elif usuario[4] == "normal":
            return redirect(url_for("menu_usuario"))
        else:
            return redirect("/")

@app.route("/form-register")
def form_register():
    """
    Contiene la logica de logout para registrar un nuevo usuario
    """
    return render_template("auth/form-register.html")

@app.route("/register", methods = ["POST"])
def register():
    """
    Contiene la logica de logout para registrar un nuevo usuario
    """
    nombre_usuario = request.form.get("nombre_usuario")
    nombre_usuario=nombre_usuario.lower()
    apellidos_usuario = request.form.get("apellidos_usuario")
    clave_usuario = request.form.get("clave_usuario")
    clave_usuario_repeat = request.form.get("clave_usuario")

    lista_tuplas=database.obtener_todos_los_usuarios_por_nombre_usuario(nombre_usuario)
    if (len(lista_tuplas)>0):
        flash("El usuario ya existe")
        return redirect(url_for("form_register"))

    if check_empty(nombre_usuario) or check_empty(clave_usuario) or check_empty(apellidos_usuario):
        flash("No puede haber campos vacios")
        return redirect(url_for("form_register"))

    if len(clave_usuario)<4: 
        flash("Las clave tiene que ser mayor de 3 caracteres")
        return redirect(url_for("form_register"))

    if clave_usuario != clave_usuario_repeat:
        flash("Las claves no son iguales")
        return redirect(url_for("form_register"))
    database.anadir_un_nuevo_usuario(nombre_usuario,  clave_usuario, apellidos_usuario)
    
    flash("Usuario registrado con exito")
    return redirect(url_for("form_login"))
    
@app.route("/logout")
def form_logout():
    """
    Contiene la logica de logout para cerrar la sesión
    """
    # Clear the session
    session.clear()
    return redirect("/")










#####################################################################
#####################################################################
#####################################################################
#                     Rutas usuarios
#####################################################################
#####################################################################
#####################################################################
@app.route("/menu_usuario")
@app.route("/menu_usuario/<int:anio_actual>/<int:mes_actual>")
#@cross_origin()
def menu_usuario(anio_actual=-1, mes_actual=-1):
#def menu_usuario():
    if "nombre" not in session:
        return redirect(url_for("form_login"))
    else:
        print("hemos entradao en menu_usuario")
        todos_los_deportes=database.obtener_todos_los_deportes()
        nombre_usuario=session["nombre"]
        if (anio_actual==-1):
            anio_actual=datetime.datetime.now().year
        if (mes_actual==-1):
            mes_actual=datetime.datetime.now().month
        if (mes_actual>12):
            mes_actual=1
            anio_actual=anio_actual+1
        elif (mes_actual==0):
            mes_actual=12
            anio_actual=anio_actual-1
        anios = [2024, 2025]
        diccionario_calendario = generar_diccionario_calendario(anios)
        # Comprobamos que los horarios de los deportes no coincidan
        actividades_deportivas=database.obtener_todos_los_deportes_por_nombre_de_usuario2(nombre_usuario)
        print("los deportes del usuario ",nombre_usuario, " son ", actividades_deportivas)
        # L lista de horarios seá una lista de tuplas con (fecha, deporte_name,  fecha_inicio, fecha_fin, horario_inicio,horario_fin)
        lista_horarios_acitvidades_deportivas=[]
        for anio in anios:
            for mes, dias in diccionario_calendario[anio].items():
                for dia, info in dias.items():
                    for deporte in actividades_deportivas:
                        fecha=datetime.date(anio,mes,dia)
                        fecha_inicio=datetime.datetime.strptime(str(deporte[2]), "%Y-%m-%d").date()
                        fecha_fin=datetime.datetime.strptime(str(deporte[3]), "%Y-%m-%d").date()
                        dias_prohibidos=database.obtener_todos_los_dias_prohibidos_por_id_deporte(deporte[0])
                        if fecha >= fecha_inicio and fecha <= fecha_fin:
                            #print("dia prohibido de la fecha", fecha, " son ", dias_prohibidos)
                            dia_prohibido_encontrado=False
                            for dia_prohibido in dias_prohibidos:
                                fecha_dia_prohibido=datetime.datetime.strptime(str(dia_prohibido[2]), "%Y-%m-%d").date()
                                if fecha_dia_prohibido == fecha:
                                    dia_prohibido_encontrado=True
                            if not dia_prohibido_encontrado:
                                if (database.get_database_engine_name_current()==Database.database_engine_mysql):
                                    h_inicio=str(deporte[4])
                                    h_fin=str(deporte[5])
                                else:
                                    h_inicio=str(deporte[4])+":00"
                                    h_fin=str(deporte[5])+":00"
                                    
                                horario_inicio=datetime.datetime.strptime(h_inicio, "%H:%M:%S").time()
                                horario_fin=datetime.datetime.strptime(h_fin, "%H:%M:%S").time()
                                lista_horarios_acitvidades_deportivas.append((fecha,deporte[1],fecha_inicio,fecha_fin,horario_inicio,horario_fin))
                                agregar_actividad(diccionario_calendario, anio, mes, dia, deporte[1]+" "+str(deporte[4])+" - "+str(deporte[5]))
        mensajes_solapamiento=verificar_solapamientos_rangos(lista_horarios_acitvidades_deportivas)            
        monthcalendar=calendar.monthcalendar(anio_actual, mes_actual)
        return render_template("users/menu_usuario.html",mensajes_solapamiento=mensajes_solapamiento,todos_los_deportes=todos_los_deportes, nombre_usuario=nombre_usuario,monthcalendar=monthcalendar,calendario=diccionario_calendario, mes_actual=mes_actual, anio_actual=anio_actual, deportes=actividades_deportivas)




















#####################################################################
#####################################################################
#####################################################################
#                          Rutas API
#####################################################################
#####################################################################
#####################################################################
@app.route("/api/obtener_todos")
#@cross_origin()
def api_mostrar_todos():
    tuplas=database.obtener_todos_los_deportes()
    deportes=[]
    for deporte in tuplas:
        print(deporte)
        deportes.append(deporte[1])
    response=jsonify(deportes)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/api/add_deporte_usuario", methods = ["POST", "GET"])
#@cross_origin()
def add_deporte_usuario():

    if request.method == "POST":
        request_data = request.get_json()
        nombre_usuario = request_data['nombre_usuario']
        nombre_deporte = request_data['nombre_deporte']
    elif request.method == "GET":
        request_data = request.args
        nombre_usuario = request_data['nombre_usuario']
        nombre_deporte = request_data['nombre_deporte']

    id_usuario=database.obtener_el_id_usuario_a_partir_del_nombre_usuario(nombre_usuario)
    id_deporte=database.obtener_el_id_deporte_a_partir_del_nombre_deporte(nombre_deporte)
    database.insertar_nuevo_deporte_usuario(id_deporte, id_usuario)
    deportes_usuario=database.obtener_deportes_usuario_por_id_usuario(id_usuario)

    #print("El deportes_usuario es: ", deportes_usuario)
    response=jsonify(deportes_usuario)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/api/delete_deporte_usuario", methods = ["POST", "GET"])
#@cross_origin()
def delete_deporte_usuario():

    if request.method == "POST":
        request_data = request.get_json()
        nombre_usuario = request_data['nombre_usuario']
        nombre_deporte = request_data['nombre_deporte']
    elif request.method == "GET":
        request_data = request.args
        nombre_usuario = request_data['nombre_usuario']
        nombre_deporte = request_data['nombre_deporte']

    id_usuario=database.obtener_el_id_usuario_a_partir_del_nombre_usuario(nombre_usuario)
    id_deporte=database.obtener_el_id_deporte_a_partir_del_nombre_deporte(nombre_deporte)
    database.eliminar_deporte_usuario_por_id_deporte_y_id_usuario(id_deporte, id_usuario)
    deportes_usuario= database.obtener_deportes_usuario_por_id_usuario(id_usuario)

    response=jsonify(deportes_usuario)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/api/obtener_deportes_usuario", methods = ["POST", "GET"])
#@cross_origin()
def obtener_deportes_usuario():
    request_data = request.get_json()
    if request.method == "POST":
        request_data = request.get_json()
    elif request.method == "GET":
        request_data = request.args
    nombre_usuario = request_data['nombre_usuario']

    deportes_usuario=database.obtener_todos_los_deportes_por_nombre_de_usuario(nombre_usuario)

    response=jsonify(deportes_usuario)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response























#####################################################################
# MAIN
#####################################################################
# Start the Server
if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=3000, debug=True)
    app.run(host="0.0.0.0", port=3000, debug=False)
    #app.run(debug=True)






















