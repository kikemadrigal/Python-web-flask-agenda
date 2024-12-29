import calendar
import datetime
import re
def generar_diccionario_calendario(anios):
    calendario = {}
    anios = [2024, 2025]
    for anio in anios:  # Iterar sobre los años proporcionados
        calendario[anio] = {}  # Crear clave para el año

        for mes_num in range(1, 13):  # Iterar sobre los meses (1 a 12)
            #nombre_mes = calendar.month_name[mes_num]  # Nombre del mes
            calendario[anio][mes_num] = {}  # Crear clave para el mes
            # Obtener número de días del mes
            dias_mes = calendar.monthrange(anio, mes_num)[1]
            # Generar estructura para los días
            for dia in range(1, dias_mes + 1):
                #calendario[anio][nombre_mes][dia] = {
                calendario[anio][mes_num][dia] = {
                    "actividad": [],
                    "evento": []  # Lista de eventos para cada día
                }
    return calendario
# Función para mostrar un calendario
def mostrar_actividades_calendario(calendario, anio):
    print(f"Calendario del año {anio}:\n")
    for mes, dias in calendario[anio].items():
        print(f"{mes}:")
        for dia, info in dias.items():
            actividades = ", ".join(info["actividad"]) if info["actividad"] else "Sin actividades"
            print(f"  Día {dia}: {actividades}")
        print("-" * 40)
def agregar_actividad(calendario, anio, mes, dia,  actividad):
    try:
        calendario[anio][mes][dia]["actividad"].append(actividad)
    except KeyError:
        print("La fecha especificada no existe en el calendario.")
def agregar_actividades(calendario, anio, mes, dia,  actividades):
    for anio in anios:
        for mes, dias in calendario[anio].items():
            for dia, info in dias.items():
                for deporte in deportes:
                    fecha_inicio=datetime.datetime.strptime(str(deporte[2]), "%Y-%m-%d").date()
                    fecha_fin=datetime.datetime.strptime(str(deporte[3]), "%Y-%m-%d").date()
                    fecha=datetime.date(anio,mes,dia)
                    if fecha >= fecha_inicio and fecha <= fecha_fin:
                        #agregar_evento(calendario, anio, mes, dia, deporte[1]+" "+str(deporte[4])+" - "+str(deporte[5]))
                        agregar_actividad(calendario, anio, mes, dia, deporte[1]+" "+str(deporte[4])+" - "+str(deporte[5]))
# Función para agregar eventos a una fecha específica
def agregar_evento(calendario, anio, mes, dia,  evento):
    try:
        calendario[anio][mes][dia]["evento"].append(evento)
    except KeyError:
        print("La fecha especificada no existe en el calendario.")

def comprobar_si_rangos_horarios_coinciden(inicio1, fin1, inicio2, fin2):
    """
    Verifica si dos rangos horarios coinciden o se solapan.

    Parámetros:
        inicio1 (str): Hora de inicio del primer rango (formato: 'HH:MM').
        fin1 (str): Hora de fin del primer rango (formato: 'HH:MM').
        inicio2 (str): Hora de inicio del segundo rango (formato: 'HH:MM').
        fin2 (str): Hora de fin del segundo rango (formato: 'HH:MM').

    Retorna:
        bool: True si los rangos se solapan, False si no se solapan.
    """
    # Convertir las horas de texto a objetos time
    formato = "%H:%M"
    inicio1 = datetime.strptime(inicio1, formato).time()
    fin1 = datetime.strptime(fin1, formato).time()
    inicio2 = datetime.strptime(inicio2, formato).time()
    fin2 = datetime.strptime(fin2, formato).time()

    # Verificar si los rangos horarios se solapan
    return inicio1 <= fin2 and inicio2 <= fin1


def verificar_solapamientos_rangos(lista_rangos):
    """
    Verifica si hay solapamientos en una lista de rangos horarios.

    Parámetros:
        lista_rangos (list): Lista de tuplas con horas de inicio y fin en formato 'HH:MM'.
                             Ejemplo: [('08:00', '10:00'), ('09:30', '11:00'), ...]

    Retorna:
        bool: True si algún rango horario se solapa, False si no hay solapamientos.
    """
    mensajes=[]
    # Ordenar los rangos por la hora de inicio
    #lista_rangos.sort()
    # Comparar cada rango con el siguiente para detectar solapamientos
    for i in range(len(lista_rangos) - 1):
        fecha_actual,deporte_name_actual, fecha_inicio_actual, fecha_fin_actual, inicio_actual, fin_actual = lista_rangos[i]
        fecha_siguiente,deporte_name_siguiente, fecha_inicio_siguiente, fecha_fin_siguiente, inicio_siguiente, fin_siguiente = lista_rangos[i + 1]
        
        #Verificamos solo el mismo día
        if fecha_actual == fecha_siguiente:
            # Si el rango actual se solapa con el siguiente, retornamos True
            if fin_actual >= inicio_siguiente:
                mensajes.append("En el día "+formatear_fecha(fecha_actual)+" hay solapamiento: "+" "+str(inicio_actual)+"-"+str(fin_actual)+" y "+str(inicio_siguiente)+"-"+str(fin_siguiente))

    # Si no se encuentran solapamientos
    return mensajes


def formatear_fecha(cadena:datetime)->str:
    """
    Pone un fecha en este formato: dd/mm/aaaa

    Argumentos:
        cadena (string)

    """
    cadena=cadena.strftime("%d/%m/%Y")
    return cadena







def formatear_cadena(cadena:str)->str:
    """
    Recorta un string a 10 caracters y si es menor lo rellena con espacios

    Argumentos:
        cadena (string)

    """
    #print("La longitud inicial de la cadena es: "+str(len(cadena)))
    cadena=cadena.strip()
    if len(cadena)>10:
        return cadena[:10]
    elif len(cadena)<10:
        return cadena+" "*(10-len(cadena))
    return cadena
def formatear_float(flotante:float)->str:
    """
    Pone 4 espacios a la derecha de un float o menos si el float tiene menos de 4 dígitos

    Argumentos:
        flotante (float)
    """
    texto_formateado =str(flotante)
    for i in range(4-len(texto_formateado)):
        texto_formateado = " "+texto_formateado
    return texto_formateado
def formatear_entero(entero:int)->str:
    """
    Pone 4 espacios a la izquierda de un entero o menos si el entero tiene menos de 4 dígitos

    Argumentos:
        entero (int)
    """
    texto_formateado =str(entero)
    for i in range(4-len(texto_formateado)):
        texto_formateado = texto_formateado+" "
    return texto_formateado
def check_empty(cadena):
    """
    Comprueba si una cadena esta vacia

    Argumentos:
        cadena (string)

    """
    cadena=cadena.strip()
    if len(cadena)==0 or not cadena:
        return True
    return False
    #raise ValueError("No puede estar vacio")
def is_greater_cero(number:int):
    """
    Coprueba si el número de páginas es mayor que 0

    Argumentos:
        number (entero)
    """
    if number>0: 
        return True
    return False
        #raise ValueError("El número de páginas no puede ser 0 o negativo")
def is_integer(numero:str):
    """
    Comprueba si el número es entero

    Argumentos:
        numero (string)
    """
    if not numero.isdigit():
        return False
    return True
def check_dni(dni):
    """
    Comprueba que el dni tiene el formato correcto y lo chequea con la letra correspondiente
    Args:
        dni (str): dni a comprobar

    Returns:
        bool: True si el dni es correcto, False en caso contrario
    """
    esCorrecto=False
    if(len(dni)!=9):
        return False
    letra= dni[8]
    letra=letra.upper()
    numeros_dni_string= dni[0:8]
    #print(numeros_dni)
    if (not numeros_dni_string.isdigit()):
        return False
    resto= int(numeros_dni_string)%23
    letras=["T","R","W","A","G","M","Y","F","P","D","X","B","N","J","Z","S","Q","V","H","L","C","K","E"]
    if letras[resto] == dni[8].upper():
        return True
    else:
        return False
def check_fecha(fecha):
    """
    Comprueba que la fecha tiene el formato correcto
    Args:
        fecha (str): fecha a comprobar

    Returns:
        bool: True si la fecha es correcta, False en caso contrario
    """
 
    formato = "%d-%m-%Y"  # Formato esperado: dd-mm-aaaa
    try:
        datetime.datetime.strptime(fecha, formato)
        return True  # Si no hay error, la fecha es válida
    except ValueError:
        return False  # Si hay un error, la fecha no es válida
def check_email(correo):
    """
    Comprueba que el correo tiene el formato correcto
    Args:
        correo (str): correo a comprobar

    Returns:
        bool: True si el correo es correcto, False en caso contrario
    """
    if "@" in correo and "." in correo:
        return True
    return False
def is_float(n):
    if isinstance(n, float):
        return True
    return False
def es_moneda_euros(cadena):
    """
    Comprueba si un string tiene el formato de una moneda de euros.

    Formatos válidos:
    - Cantidades con coma como separador decimal (opcionalmente con separador de miles).
    - El símbolo € puede ir al final (con o sin espacio) o al principio.
    - Ejemplos válidos: '123,45 €', '1.234,56 €', '€ 10', '0,99 €'.

    Args:
        cadena (str): El string a comprobar.

    Returns:
        bool: True si el string tiene el formato de moneda de euros, False en caso contrario.
    """
    # Expresión regular para validar monedas en euros
    patron = r"^\s?(\d{1,3}(\.\d{3})*|\d+)(,\d{2})?\s?$"
    
    # Comprobar si la cadena cumple el patrón
    resultado=bool(re.match(patron, cadena))
    return resultado
def float_moneda_a_str(float):
    """
    Convierte un float con formato de moneda en euros a un número float.

    Args:
        cadena (str): El string que representa la moneda (por ejemplo, '1.234,56').

    Returns:
        float: El valor numérico de la moneda como float.
        None: Si el formato no es válido.
    """
    try:
        cadena = str(float)
    except ValueError:
        return None
    #cadena_limpia = cadena.replace("€", "").replace(" ", "")
    cadena = cadena.replace(".", ",")
    # Convertir a float
    return cadena
def generar_letrar_dni(dni_sin_letra):
    letras=["T","R","W","A","G","M","Y","F","P","D","X","B","N","J","Z","S","Q","V","H","L","C","K","E"]
    letra_posición=int(dni_sin_letra)%23
    letra=letras[letra_posición]
    return letra