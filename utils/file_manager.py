import csv
import json
import datetime
def leer_archivo_csv(tabla,archivo):
    filas=[]
    len_tabla=0
    if (tabla=="usuario"):
        len_tabla=5
    elif (tabla=="deporte"):
        len_tabla=6
    elif (tabla=="deportes_usuario"):
        len_tabla=2
    elif (tabla=="dia_prohibido"):
        len_tabla=3
    try:
        with open(archivo, encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for linea,fila in enumerate(reader):
                if len(fila) !=len_tabla:
                    input(f"Se ha detectado un problema en el csv en la fila {linea+2}: {fila} y se borrará. ")
                else:
                    filas.append(fila)
        return filas
    except Exception as e:  
        print(e)
        return None
def leer_archivo_csv_final(archivo):
    filas={
        "usuarios":[],
        "deportes":[],
        "deportes_usuarios":[],
        "dias_prohibidos":[]
    }
    fila_tipo=None
    try:
        with open(archivo, "r", encoding='utf-8') as f:
            reader = csv.reader(f)
            for linea,fila in enumerate(reader):   
                if (len(fila)==0 or fila==None):
                    continue         
                if fila[0]=="id_usuario" and fila[1]=="nombre_usuario":   
                    fila_tipo="usuarios"
                    continue
                elif fila[0]=="id_deporte" and fila [1]=="nombre_deporte":
                    fila_tipo="deportes"
                    continue
                elif fila[0]=="id_deporte" and fila[1]=="id_usuario":
                    fila_tipo="deportes_usuarios"
                    continue
                elif fila[0]=="id_dia_prohibido":
                    fila_tipo="dias_prohibidos"
                    continue
                if fila_tipo=="usuarios":
                    if len(fila) ==5: 
                        filas["usuarios"].append(fila)
                elif fila_tipo=="deportes":
                    if len(fila) ==6:  
                        filas["deportes"].append(fila)   
                elif fila_tipo=="deportes_usuarios":
                    if len(fila) ==2:
                        filas["deportes_usuarios"].append(fila)
                elif fila_tipo=="dias_prohibidos":
                    if len(fila) ==3:
                        filas["dias_prohibidos"].append(fila)

        return filas
    except Exception as e:  
        print("hubo un error al leer el archivo: ",e)
        return None
def escribir_archivo_csv(tabla,filas):
    print("estas en la funcion escribir csv")
    ahora = datetime.datetime.now()
    ahora = ahora.strftime("%Y%m%d%H%M%S")
    archivo_csv=str(ahora)+"_"+tabla+".csv"
    try:
        with open(archivo_csv, "w", newline="") as f:
            writer = csv.writer(f)
            if(tabla=="usuario"):
                writer.writerow(["id_usuario", "nombre_usuario", "clave_usuario", "apellidos_usuario", "rol"])
            elif(tabla=="deporte"):
                writer.writerow(["id_deporte", "nombre_deporte", "fecha_inicio", "fecha_fin", "hora_inicio", "hora_fin"])
            elif(tabla=="deportes_usuario"):
                writer.writerow(["id_deporte", "id_usuario"])
            elif(tabla=="dia_prohibido"):
                writer.writerow(["id_dia_prohibido", "id_deporte", "fecha"])
            print("filas --->",filas)
            for fila in filas:
                #print(fila)
                if(tabla=="usuario"):
                    writer.writerow([fila[0], fila[1], fila[2], fila[3], fila[4]])
                elif(tabla=="deporte"):
                    writer.writerow([fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]])
                elif(tabla=="deportes_usuario"):
                    writer.writerow([fila[0], fila[1]])
                elif(tabla=="dia_prohibido"):
                    writer.writerow([fila[0], fila[1], fila[2]])
    except Exception as e:  
        print(e)

                
def escribir_archivo_csv_final(usuarios, deportes, deportes_usuarios, dias_prohibidos):
    ahora = datetime.datetime.now()
    ahora = ahora.strftime("%Y%m%d%H%M%S")
    archivo_csv=str(ahora)+"_backup_agenda.csv"
    try:
        with open(archivo_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id_usuario", "nombre_usuario", "clave_usuario", "apellidos_usuario", "rol"])
            for fila in usuarios:
                writer.writerow([fila[0], fila[1], fila[2], fila[3], fila[4]])
            writer.writerow(["id_deporte", "nombre_deporte", "fecha_inicio", "fecha_fin", "hora_inicio", "hora_fin"])
            for fila in deportes:
                writer.writerow([fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]])
            writer.writerow(["id_deporte", "id_usuario"])
            for fila in deportes_usuarios:
                writer.writerow([fila[0], fila[1]])
            writer.writerow(["id_dia_prohibido", "id_deporte", "fecha"])
            for fila in dias_prohibidos:
                writer.writerow([fila[0], fila[1], fila[2]])
    except Exception as e:  
        print(e)
    
def leer_archivo_json(archivo_json):
    try:
        with open(archivo_json, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:  
        print(e)
        return None

def escribir_archivo_json(filas, archivo_json):
    print("estas en la funcion escribir json")
    try:
        with open(archivo_json, "w") as f:
            json.dump(filas, f)
    except Exception as e:  
        print(e)

def escribir_archivo_json_final(usuarios, deportes, deportes_usuarios, dias_prohibidos):
    ahora = datetime.datetime.now()
    ahora = ahora.strftime("%Y%m%d%H%M%S")
    archivo_json=str(ahora)+"_backup_agenda.json"
    agenda={
        "usuarios":usuarios,
        "deportes":deportes,
        "deportes_usuarios":deportes_usuarios,
        "dias_prohibidos":dias_prohibidos
    }
    try:
        with open(archivo_json, "w") as f:
            json.dump(agenda, f)
    except Exception as e:  
        print(e)