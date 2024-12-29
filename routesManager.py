
from mainFlask import MainFlask
from flask import render_template,request,redirect,flash, url_for, session, jsonify
from utils.utils import *
import utils.file_manager as file_manager
from data.database import Database
from mysql.connector import Error

app = MainFlask.getFlask()
database:Database= MainFlask.get_database()



#####################################################################
#####################################################################
#####################################################################
#                           ADMIN
#####################################################################
#####################################################################
#####################################################################
@app.route("/menu_admin")
def menu_admin():
    """
    Se define la ruta para mostrar el menú del administrador
    """
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    return render_template("adm/menu_admin.html")
@app.route("/adm/settings")
def menu_settings():
    """
    Se define la ruta para mostrar el menú de configuración
    """
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    return render_template("adm/settings.html")

@app.route("/adm/csv_crear_backup")
def adm_csv_crear_backup():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    usuarios=database.obtener_todos_los_usuarios()
    deportes=database.obtener_todos_los_deportes()
    deportes_usuarios=database.obtener_todos_los_deportes_usuario()
    dias_prohibidos=database.obtener_todos_los_dias_prohibidos()

    file_manager.escribir_archivo_csv_final(usuarios, deportes, deportes_usuarios, dias_prohibidos)
    flash("Archivo usuario.csv creado con exito")
    return redirect(url_for("menu_admin"))

@app.route("/adm/csv_leer", methods=["POST"])
def adm_csv_leer():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    file=request.files["file_csv"] 
    file_name=file.filename
    file.save(file_name) 
    if (file_name.split(".")[-1] != "csv"):
        flash("El archivo debe ser de tipo csv")
        return redirect(url_for("menu_admin"))
    if (file==None):
        flash("LEl archivo no puede estar vacío")
        return redirect(url_for("menu_admin"))
    #obtenemos un diccionario con los usuarios, deportes, deportes_usuarios y días_prohibidos
    datos=file_manager.leer_archivo_csv_final(file_name)    
    usuarios=datos["usuarios"]
    if(len(usuarios)!=0):
        database.borrar_todos_los_usuarios()
        for usuario in usuarios:
            database.anadir_un_nuevo_usuario(usuario[1],usuario[2],usuario[3])
    deportes=datos["deportes"]
    if (len(deportes)!=0):
        database.borrar_todos_los_deportes()
    for deporte in deportes:
        database.anadir_un_nuevo_deporte(deporte[1], deporte[2], deporte[3], deporte[4], deporte[5])  
    deportes_usuarios=datos["deportes_usuarios"]
    if( deportes_usuarios!=0):
        database.borrar_todos_los_deportes_usuario()
        for deporte_usuario in deportes_usuarios:
            database.insertar_nuevo_deporte_usuario(deporte_usuario[0], deporte_usuario[1])
    dias_prohibidos=datos["dias_prohibidos"]
    if (len(dias_prohibidos)!=0):
        database.borrar_todos_los_dias_prohibidos()
        for dia_prohibido in dias_prohibidos:
            database.insertar_nuevo_dia_prohibido(dia_prohibido[1],dia_prohibido[2])
    
    flash("Archivo usuario.csv leido con exito")
    return redirect(url_for("menu_admin"))



@app.route("/adm/json_crear_backup")
def adm_json_crear_backup_user():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    usuarios=database.obtener_todos_los_usuarios()
    deportes=database.obtener_todos_los_deportes()
    deportes_usuarios=database.obtener_todos_los_deportes_usuario()
    dias_prohibidos=database.obtener_todos_los_dias_prohibidos()
    file_manager.escribir_archivo_json_final(usuarios,deportes,deportes_usuarios,dias_prohibidos)
    flash("Archivo usuario.json creado con exito")
    return redirect(url_for("menu_admin"))

@app.route("/adm/json_leer", methods=["POST"])
def adm_json_leer_user():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    
    file=request.files["file_json"] 
    file_name=file.filename
    if (file_name.split(".")[-1] != "json"):
        flash("El archivo debe ser de tipo json")
        return redirect(url_for("menu_admin"))
    file.save(file_name) 

    if (file==None):
        flash("LEl archivo no puede estar vacío")
        return redirect(url_for("menu_admin"))
    #obtenemos un diccionario con los usuarios, deportes, deportes_usuarios y días_prohibidos
    agenda=file_manager.leer_archivo_json(file_name)
  
    database.borrar_todos_los_usuarios()
    database.borrar_todos_los_deportes()
    database.borrar_todos_los_deportes_usuario()
    database.borrar_todos_los_dias_prohibidos()
    usuarios=agenda["usuarios"]
    for usuario in usuarios:
        database.anadir_un_nuevo_usuario(usuario[1],usuario[2],usuario[3])
    deportes=agenda["deportes"]
    for deporte in deportes:
        database.anadir_un_nuevo_deporte(deporte[1], deporte[2], deporte[3], deporte[4], deporte[5])  
    deportes_usuarios=agenda["deportes_usuarios"]
    for deporte_usuario in deportes_usuarios:
        database.insertar_nuevo_deporte_usuario(deporte_usuario[0], deporte_usuario[1])
    dias_prohibidos=agenda["dias_prohibidos"]
    for dia_prohibido in dias_prohibidos:
        database.insertar_nuevo_dia_prohibido(dia_prohibido[1],dia_prohibido[2])
    flash("Archivo usuario.json leido con exito")
    return redirect(url_for("menu_admin"))


@app.route("/adm/database_reset")
def adm_database_reset():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    database.database_reset()
    flash("Base de datos reseteada con exito")
    return redirect(url_for("menu_admin"))





    
#                          USER
#####################################################################    
@app.route("/adm/users/showAll")
def show_all_user_admin():
    """
    Se define la ruta para mostrar los usuarios que verá el administrador
    Return
        la vista donde se
    """
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")

    usuarios=database.obtener_todos_los_usuarios()
 
    return render_template("adm/users/showAll.html",usuarios=usuarios)
@app.route("/adm/users/form-create")
def adm_form_create_user():
    """
    Se define la ruta para la creación de un usuario

    Return 
        la vista del formulario de creación
    """
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    return render_template("adm/users/form-create.html")
@app.route("/adm/users/create", methods=["POST"])
def adm_create_user():
    """
    Se define ala lógica para insertar en la base de datos un nuevo usuario

    Args:
        POST[usuario]
    
        Return:
            redirecciona a otra web

    """
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    nombre = request.form.get("nombre_usuario")
    apellido = request.form.get("apellido_usuario")
    clave = request.form.get("clave_usuario")
    clave_repeat = request.form.get("clave_usuario_repeat")
    if clave != clave_repeat:
        flash("Las claves no son iguales")
        return redirect(url_for("adm_form_create_user"))
    if check_empty(nombre) or check_empty(apellido) or check_empty(clave):
        flash("No puede haber campos vacios")
        return redirect(url_for("adm_form_create_user"))
    database.anadir_un_nuevo_usuario(nombre,apellido,clave)
    return redirect(url_for("show_all_user_admin"))
@app.route("/adm/users/form-update", methods=["POST", "GET"])
def adm_form_update_user():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    if (request.method == "GET"):
        id= request.args.get("id_usuario")
    elif (request.method == "POST"):
        id =request.form.get("id_usuario")
    print("El id es ",id)

    usuarios=database.obtenr_todos_los_usuarios_por_id_usuario(id)
    usuario=usuarios[0]
    print(usuario)
    return render_template("adm/users/form-update.html",usuario=usuario)
@app.route("/adm/users/update", methods=["POST"])
def adm_update_user():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    id = request.form.get("id_usuario")
    nombre = request.form.get("nombre_usuario")
    apellido = request.form.get("apellido_usuario")
    clave = request.form.get("clave_usuario")
    clave_repeat = request.form.get("clave_usuario_repeat")
    #usuario=[id,nombre,clave,apellido]
    if clave != clave_repeat:
        flash("Las claves no son iguales")
        return redirect(url_for("adm_form_update_user", id_usuario=id))
    if check_empty(nombre) or check_empty(apellido) or check_empty(clave):
        flash("No puede haber campos vacios")
        return redirect(url_for("adm_form_update_user", id_usuario=id))

    database.actualizar_un_usuario(id,nombre,apellido,clave)
    return redirect(url_for("show_all_user_admin"))
@app.route("/adm/users/delete", methods=["post"])
def adm_delete_user():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    id= request.form.get("id_usuario")
    print("El id a borrar es ",id)
    try:
        database.borrar_un_usuario(id)
    except Error as e:
        print("No es posible borrar al usuario si está referenciado en otra tabla: ",e)
        flash("No es posible borrar al usuario si está referenciado en otra tabla")
    return redirect(url_for("show_all_user_admin"))








#                           Sports
#####################################################################
@app.route("/adm/sports/showAll")
def show_all_sports_admin():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")

    deportes=database.obtener_todos_los_deportes()
    return render_template("adm/sports/showAll.html",deportes=deportes)
@app.route("/adm/sports/form-create")
def adm_form_create_sport():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    return render_template("adm/sports/form-create.html")
@app.route("/adm/sports/create", methods=["POST"])
def adm_create_sport():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    nombre_deporte = request.form.get("nombre_deporte")
    fecha_inicio = request.form.get("fecha_inicio")
    fecha_fin = request.form.get("fecha_fin")
    hora_inicio = request.form.get("hora_inicio")
    hora_fin = request.form.get("hora_fin")
    if check_empty(nombre_deporte) or check_empty(fecha_inicio) or check_empty(fecha_fin) or check_empty(hora_inicio) or check_empty(hora_fin):
        flash("No puede haber campos vacios")
        return redirect(url_for("adm_form_create_sport"))

    database.anadir_un_nuevo_deporte(nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin)
    return redirect(url_for("show_all_sports_admin"))
@app.route("/adm/sports/form-update", methods=["POST", "GET"])
def adm_form_update_sport():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    if (request.method == "GET"):
        id_deporte= request.args.get("id_deporte")
    elif (request.method == "POST"):
        id_deporte =request.form.get("id_deporte")
    print("El id es ",id)

    deportes = database.obtener_todos_los_deportes_por_id_deporte(id_deporte)
    deporte=deportes[0]
    #Formateamos la hora de inicio y la hora final para que salga en el input time
    str_horario_inicio=str(deporte[4])
    str_horario_fin=str(deporte[5])
    if len(str_horario_inicio)==7:
        str_horario_inicio="0"+str_horario_inicio
    if len(str_horario_fin)==7:
        str_horario_fin="0"+str_horario_fin
    deporte_formateado=[deporte[0],deporte[1],deporte[2],deporte[3],str_horario_inicio,str_horario_fin]

    return render_template("adm/sports/form-update.html",deporte=deporte_formateado)
@app.route("/adm/sports/update", methods=["POST"])
def adm_update_sport():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    id_deporte = request.form.get("id_deporte")
    nombre_deporte = request.form.get("nombre_deporte")
    fecha_inicio = request.form.get("fecha_inicio")
    fecha_fin = request.form.get("fecha_fin")
    hora_inicio = request.form.get("hora_inicio")
    hora_fin = request.form.get("hora_fin")
    #print(id_deporte, " ", nombre_deporte, " ", fecha_inicio, " ", fecha_fin, " ", hora_inicio, " ", hora_fin)
    if check_empty(nombre_deporte) or check_empty(fecha_inicio) or check_empty(fecha_fin) or check_empty(hora_inicio) or check_empty(hora_fin):
        flash("No puede haber campos vacios")
        return redirect(url_for("adm_form_update_sport", id_deporte=id_deporte))

    database.actualizar_deporte(id_deporte,nombre_deporte,fecha_inicio,fecha_fin,hora_inicio,hora_fin)
    return redirect(url_for("show_all_sports_admin"))
@app.route("/adm/sports/delete", methods=["post"])
def adm_delete_sport():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    id_deporte= request.form.get("id_deporte")
    print("El id a borrar es ",id_deporte)
    try:
        database.borrar_un_deporte(id_deporte)
    except Error as e:
        print("No es posible borrar la atividad deportiva si está referenciada en otra tabla: ",e)
        flash("No es posible borrar la atividad deportiva si está referenciada en otra tabla")
    return redirect(url_for("show_all_sports_admin"))











#                           User-sports
#####################################################################
@app.route("/adm/user_sports/showAll")
def show_all_user_sports_admin():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")

    deportes_usuario=database.obtener_todos_los_deportes_usuario()
    return render_template("adm/user_sports/showAll.html",deportes_usuario=deportes_usuario)
@app.route("/adm/user_sports/form-create")
def adm_form_create_user_sport():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")

    deportes=database.obtener_todos_los_deportes()
    usuarios=database.obtener_todos_los_usuarios()
    return render_template("adm/user_sports/form-create.html", deportes=deportes, usuarios=usuarios)
@app.route("/adm/user_sports/create", methods=["POST"])
def adm_create_user_sport():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    id_deporte = request.form.get("id_deporte")
    id_usuario = request.form.get("id_usuario")
    if id_deporte==0 or id_usuario==0:
        flash("No puede haber campos vacios")
        return redirect(url_for("adm_form_create_user_sport"))
    try:
        database.insertar_nuevo_deporte_usuario(id_deporte,id_usuario)
    except Error as e:
        flash("Ese usuario ya estaba matriculado para ese deporte")
        return redirect(url_for("adm_form_create_user_sport"))


    return redirect(url_for("show_all_user_sports_admin"))
@app.route("/adm/user_sports/form-update", methods=["POST", "GET"])
def adm_form_update_user_sport():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    if (request.method == "GET"):
        id_deporte= request.args.get("id_deporte")
        id_usuario= request.args.get("id_usuario")
    elif (request.method == "POST"):
        id_deporte =request.form.get("id_deporte")
        id_usuario =request.form.get("id_usuario")
    print("el id_deporte es ", id_deporte, " EL id usuario es: ", id_usuario)

    deportes=database.obtener_todos_los_deportes()
    usuarios=database.obtener_todos_los_usuarios()

    deporte=database.obtener_todos_los_deportes_por_id_deporte(id_deporte)[0]
    usuario=database.obtenr_todos_los_usuarios_por_id_usuario(id_usuario)[0]
    
    return render_template("adm/user_sports/form-update.html", deportes=deportes, usuarios=usuarios, deporte=deporte, usuario=usuario)
@app.route("/adm/user_sports/update", methods=["POST"])
def adm_update_user_sport():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    id_deporte_nuevo = request.form.get("id_deporte_nuevo")
    id_usuario_nuevo = request.form.get("id_usuario_nuevo")
    id_deporte_viejo = request.form.get("id_deporte_viejo")
    id_usuario_viejo = request.form.get("id_usuario_viejo")
    if id_deporte_nuevo==0 or id_usuario_nuevo==0:
        flash("No puede haber campos vacios")
        return redirect(url_for("adm_form_update_user_sport", id_deporte=id_deporte_viejo, id_usuario=id_usuario_viejo))
    try:
        database.actualizar_deportes_usuario(id_deporte_nuevo,id_usuario_nuevo,id_deporte_viejo,id_usuario_viejo)
    except Error as e:
        flash("El usuario ya tenía esta actividad deportiva asignada y no puede estar duplicada")
        return redirect(url_for("adm_form_update_user_sport", id_deporte=id_deporte_viejo, id_usuario=id_usuario_viejo))
    return redirect(url_for("show_all_user_sports_admin"))
@app.route("/adm/user_sports/delete", methods=["post"])
def adm_delete_user_sport():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    id_deporte= request.form.get("id_deporte")
    id_usuario= request.form.get("id_usuario")
    print("El id_deporte a borrar es ",id_deporte," el id_usuario es ",id_usuario)

    database.elimnar_deportes_usuario(id_deporte, id_usuario)
    return redirect(url_for("show_all_user_sports_admin"))












#                   forbidden days
#####################################################################
@app.route("/adm/forbidden_days/showAll")
def show_all_forbidden_days_admin():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    dias_prohibidos=database.obtener_todos_los_dias_prohibidos()
    return render_template("adm/forbidden_days/showAll.html",dias_prohibidos=dias_prohibidos)

@app.route("/adm/forbidden_days/form-create")
def adm_form_create_forbidden_days():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")

    deportes=database.obtener_todos_los_deportes()
    return render_template("adm/forbidden_days/form-create.html", deportes=deportes)
@app.route("/adm/forbidden_days/create", methods=["POST"])
def adm_create_forbidden_days():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    id_deporte = request.form.get("id_deporte")
    fecha = request.form.get("fecha")
    if id_deporte==0 or fecha==0:
        flash("No puede haber campos vacios")
        return redirect(url_for("adm_form_create_forbidden_days"))
    existe_ya_en_la_tabla=database.obtener_todos_los_dias_prohibidos_por_id_deporte_y_fecha(id_deporte,fecha)
    if(len(existe_ya_en_la_tabla)>0):
        flash("Ya está creado ese día prohibido para el deporte")
        return redirect(url_for("adm_form_create_forbidden_days"))
    
    database.insertar_nuevo_dia_prohibido(id_deporte,fecha)
    return redirect(url_for("show_all_forbidden_days_admin"))
@app.route("/adm/forbidden_days/form-update", methods=["POST", "GET"])
def adm_form_update_forbidden_days():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    if (request.method == "GET"):
        id_dia_prohibido= request.args.get("id_dia_prohibido")
    elif (request.method == "POST"):
        id_dia_prohibido =request.form.get("id_dia_prohibido")
    #print("El id es ",id_dia_prohibido)
    dias_prohibidos = database.obtener_todos_los_dias_prohibidos_por_id(id_dia_prohibido)
    #print("El dia prohibido es ",dias_prohibidos)
    deportes=database.obtener_todos_los_deportes()
     
    dia_prohibido=dias_prohibidos[0]
    return render_template("adm/forbidden_days/form-update.html",dia_prohibido=dia_prohibido, deportes=deportes)
    
@app.route("/adm/forbidden_days/update", methods=["POST"])
def adm_update_forbidden_days():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    id_dia_prohibido = request.form.get("id_dia_prohibido")
    id_deporte = request.form.get("id_deporte")
    fecha = request.form.get("fecha")
    if id_deporte==0 or fecha==0:
        flash("No puede haber campos vacios")
        return redirect(url_for("adm_form_update_forbidden_days", id_dia_prohibido=id_dia_prohibido))

    database.actualizar_dia_prohibido(id_dia_prohibido,id_deporte,fecha)
    return redirect(url_for("show_all_forbidden_days_admin"))
@app.route("/adm/forbidden_days/delete", methods=["post"])
def adm_delete_forbidden_days():
    if 'nombre' not in session:
        if session["rol"] != "administrador":
            return redirect("/login")
    id_dia_prohibido= request.form.get("id_dia_prohibido")
    print("El id a borrar es ",id_dia_prohibido)

    database.elimnar_dia_prohibido(id_dia_prohibido)
    return redirect(url_for("show_all_forbidden_days_admin"))