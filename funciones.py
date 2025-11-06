import os
import csv
import shutil


BASE_DIR = "DB"  # Directorio raíz para la base de datos jerárquica: Continente/Región/Datos.csv
HEADERS = ['Pais', 'Poblacion', 'Superficie'] # Cabeceras para los CSV internos


# Funciones de Validación de Entrada de Usuario

def validar_no_vacio(texto):
    """
    Valida que la entrada del usuario no esté vacía después de quitar espacios.
    Mantiene el bucle hasta recibir una cadena válida (un valor).
    """
    while True:
        entrada = input(texto).strip()
        if entrada:
            return entrada
        else:
            print("Error: El campo no puede estar vacío.")

def validar_numero_positivo(texto):
    """
    Valida que la entrada sea un número entero, positivo y mayor que cero.
    Reitera la solicitud hasta obtener un valor numérico válido.
    """
    while True:
        entrada = input(texto).strip()
        if entrada.isdigit():
            numero = int(entrada)
            if numero > 0:
                return numero
            else:
                print("Error: El número debe ser positivo y mayor a cero.")
        else:
            print("Error: Debe ingresar un valor numérico entero.")


#  Funciones de Gestión de Archivos y Directorios

def obtener_ruta_csv(continente, region):
    """
    Construye la ruta completa del directorio y del archivo CSV.
    Utiliza la jerarquía BASE_DIR/continente/region/Datos.csv.
    """
    # Genera la ruta del directorio basada en la jerarquía Continente/Región
    ruta_directorio = os.path.join(BASE_DIR, continente, region)
    
    # Define el nombre del archivo de datos dentro de ese directorio
    ruta_csv = os.path.join(ruta_directorio, "Datos.csv")
    
    return ruta_directorio, ruta_csv

def alta_item(continente, region, pais, poblacion, superficie):
    """
    Registra un nuevo ítem (país) en el archivo CSV correspondiente.
    Crea la estructura de directorios (Continente/Región) si no existe.
    """
    try:
        ruta_directorio, ruta_csv = obtener_ruta_csv(continente, region)
        
        # Crea recursivamente los directorios si no existen
        os.makedirs(ruta_directorio, exist_ok=True)

        nuevo_item = {
            'Pais': pais,
            'Poblacion': poblacion,
            'Superficie': superficie
        }
        
        # Determina si se deben escribir las cabeceras (si el archivo es nuevo)
        escribir_cabeceras = not os.path.exists(ruta_csv)

        # Abre el archivo en modo 'a' (append/añadir)
        with open(ruta_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            
            if escribir_cabeceras:
                writer.writeheader() # Escribe las cabeceras si es el primer registro
                
            writer.writerow(nuevo_item) # Escribe la nueva fila de datos
            
        print(f"Éxito: País '{pais}' agregado en {ruta_csv}")

    except OSError as e: 
        print(f"Error de sistema al crear directorios o escribir archivo: {e}")
    except Exception as e:
        print(f"Error inesperado en alta_item: {e}")


# Funciones de Lectura y Consolidación de Datos

def leer_datos_recursivo(ruta_actual):
    """
    Recorre de forma recursiva la estructura de carpetas (DB/Continente/Región).
    Lee todos los archivos 'Datos.csv' encontrados y consolida los ítems.
    """
    items_consolidados = [] # Lista para almacenar todos los países encontrados
    
    try:
        # Itera sobre el contenido del directorio actual
        for nombre_entrada in os.listdir(ruta_actual):
            ruta_completa = os.path.join(ruta_actual, nombre_entrada)
            
            if os.path.isdir(ruta_completa):
                # Si es un directorio, realiza la llamada recursiva
                items_consolidados.extend(leer_datos_recursivo(ruta_completa))
                
            # Verifica si es un archivo y termina en '.csv'
            elif os.path.isfile(ruta_completa) and nombre_entrada.endswith('.csv'):
                
                # Extrae los niveles de la jerarquía (Continente y Región) desde la ruta
                partes_ruta = ruta_actual.split(os.sep)
                # partes_ruta[1] es Continente, partes_ruta[2] es Región
                continente = partes_ruta[1] if len(partes_ruta) > 1 else "N/A"
                region = partes_ruta[2] if len(partes_ruta) > 2 else "N/A"

                
                # Abre y lee el archivo CSV encontrado
                with open(ruta_completa, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for fila in reader:
                        
                        # Agrega la información de contexto (Continente/Región) a cada ítem
                        fila['Continente'] = continente
                        fila['Region'] = region
                        items_consolidados.append(fila)

    except FileNotFoundError: 
        print(f"Error: El directorio base '{BASE_DIR}' no existe.")
    except OSError as e: 
        print(f"Error de sistema al leer el directorio {ruta_actual}: {e}")
        
    return items_consolidados

def obtener_todos_los_datos():
    """
    Función principal para iniciar la lectura recursiva desde el directorio base.
    Asegura la existencia del directorio 'BASE_DIR'.
    """
    if not os.path.exists(BASE_DIR):
        print(f"Directorio '{BASE_DIR}' no encontrado. Creando...")
        try:
            os.makedirs(BASE_DIR) # Crea el directorio base si no existe
        except OSError as e:
            print(f"No se pudo crear el directorio base: {e}")
            return []
    
    # Inicia la lectura recursiva de todos los datos
    return leer_datos_recursivo(BASE_DIR)

# Funciones de Importación Masiva

def importar_datos_iniciales(archivo_origen):
    """
    Procesa un archivo CSV y lo migra a la estructura jerárquica de carpetas.
    Borra y recrea la estructura base antes de la importación para asegurar limpieza.
    """
    print(f"\nLimpiando base de datos anterior en '{BASE_DIR}'...")
    try:
        if os.path.exists(BASE_DIR):
            shutil.rmtree(BASE_DIR) # Borra la carpeta base y todo su contenido
        
        # 2. Recrear el directorio base vacío
        os.makedirs(BASE_DIR)
        print("Directorio limpiado. Comenzando nueva importación...")
        
    except OSError as e:
        print(f"Error al limpiar el directorio '{BASE_DIR}': {e}")
        print("La importación no puede continuar. Revise los permisos.")
        return

    if not os.path.exists(archivo_origen):
        print(f"Error: El archivo '{archivo_origen}' no se encuentra.")
        return

    try:
        # Lee el archivo CSV de origen
        with open(archivo_origen, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            contador = 0
            for fila in reader:
                try:
                    # Llama a alta_item para grabar cada fila en la jerarquía
                    alta_item(
                        fila['Continente'],
                        fila['Region'],
                        fila['Pais'],
                        int(fila['Poblacion']),
                        int(fila['Superficie'])
                    )
                    contador += 1
                except (ValueError, KeyError) as e:
                    # Captura errores de formato o campos faltantes
                    print(f"Error en formato de fila: {fila}. Detalle: {e}")
                
            print(f"\nImportación completada. {contador} países migrados a la estructura de carpetas.")
            
    except FileNotFoundError:
        print(f"Error: Archivo '{archivo_origen}' no encontrado.")
    except Exception as e:
        print(f"Error inesperado durante la importación: {e}")

# Funcionalidades Adicionales 

def mostrar_items(lista_items):
    """
    Muestra la lista de ítems de forma clara y formateada.
    Formatea los números de Población y Superficie.
    """
    if not lista_items:
        print("No hay ítems para mostrar.")
        return

    print("\n--- Listado Global de Países (Lectura Recursiva) ---")
    # Imprime las cabeceras de la tabla
    print(f"{'País':<20} {'Población':<15} {'Superficie':<15} {'Continente':<15} {'Región':<15}")
    print("-" * 80)
    
    for item in lista_items:
        try:
            # Formatea los números con separadores de miles
            poblacion = f"{int(item['Poblacion']):,}"
            superficie = f"{int(item['Superficie']):,}"
        except (ValueError, TypeError):
            # En caso de error, muestra 'N/A' o el valor original
            poblacion = item.get('Poblacion', 'N/A')
            superficie = item.get('Superficie', 'N/A')

        
        # Imprime la fila de datos con alineación
        print(f"{item['Pais']:<20} {poblacion:<15} {superficie:<15} {item['Continente']:<15} {item['Region']:<15}")
    print("-" * 80)
    print(f"Total de ítems: {len(lista_items)}")

def filtrar_items(lista_global):
    """
    Permite filtrar la lista de países por 'Continente' o por 'Región'.
    Realiza la búsqueda con coincidencia exacta e insensible a mayúsculas/minúsculas.
    """
    if not lista_global:
        print("No hay datos para filtrar.")
        return

    print("Filtrar por: 1. Continente 2. Región")
    op_filtro = input("Opción: ").strip()
    termino_busqueda = input("Ingrese el término a buscar: ").strip().lower()
    
    resultados = []
    if op_filtro == '1':
        clave_filtro = 'Continente'
    elif op_filtro == '2':
        clave_filtro = 'Region'
    else:
        print("Opción no válida.")
        return
        
    for item in lista_global:
        # Aplica el filtro (coincidencia de cadena completa en minúsculas)
        if item.get(clave_filtro, '').lower() == termino_busqueda:
            resultados.append(item)

    if not resultados:
        print(f"No se encontraron ítems para '{termino_busqueda}'.")
    else:
        print(f"\n--- Resultados del Filtro ({len(resultados)} encontrados) ---")
        mostrar_items(resultados)


def reescribir_archivo_csv_especifico(continente, region, items_del_archivo):
    """
    Sobrescribe un archivo CSV individual (modo 'w') con una nueva lista de ítems.
    Función auxiliar para la modificación y eliminación de datos.
    """
    try:
        _, ruta_csv = obtener_ruta_csv(continente, region)
        
        # Abre el archivo en modo 'w' (write/sobrescribir)
        with open(ruta_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader() # Escribe siempre las cabeceras
            
            # Itera y escribe los ítems (solo los campos de HEADERS)
            for item in items_del_archivo:
                item_a_escribir = {
                    'Pais': item['Pais'],
                    'Poblacion': item['Poblacion'],
                    'Superficie': item['Superficie']
                }
                writer.writerow(item_a_escribir)
                
    except OSError as e: 
        print(f"Error al reescribir el archivo {ruta_csv}: {e}")

def modificar_item(lista_global):
    """
    Busca un país por nombre, solicita nuevos valores y actualiza el ítem.
    Finalmente, reescribe el archivo CSV afectado con los datos actualizados.
    """
    if not lista_global:
        print("La lista está vacía. No se puede modificar.")
        return lista_global
        
    pais_a_modificar = input("Ingrese el nombre exacto del país a modificar: ").strip()
    
    item_encontrado = None
    # Busca el ítem por nombre (comparación insensible a mayúsculas)
    for item in lista_global:
        if item['Pais'].lower() == pais_a_modificar.lower():
            item_encontrado = item
            break
            
    if not item_encontrado:
        print(f"Error: País '{pais_a_modificar}' no encontrado.")
        return lista_global

    print(f"Modificando '{item_encontrado['Pais']}'. Deje en blanco para no cambiar.")
    
    # Solicita nuevos valores, permitiendo dejar en blanco para no cambiar
    nuevo_pais = input(f"Nuevo nombre ({item_encontrado['Pais']}): ").strip()
    nueva_poblacion_str = input(f"Nueva población ({item_encontrado['Poblacion']}): ").strip()
    nueva_superficie_str = input(f"Nueva superficie ({item_encontrado['Superficie']}): ").strip()

    
    if nuevo_pais:
        item_encontrado['Pais'] = nuevo_pais
    if nueva_poblacion_str:
        # Valida y asigna la nueva población si se ingresó un valor
        item_encontrado['Poblacion'] = validar_numero_positivo(f"Confirme nueva población ({nueva_poblacion_str}): ")
    if nueva_superficie_str:
        # Valida y asigna la nueva superficie si se ingresó un valor
        item_encontrado['Superficie'] = validar_numero_positivo(f"Confirme nueva superficie ({nueva_superficie_str}): ")
        

    continente_afectado = item_encontrado['Continente']
    region_afectada = item_encontrado['Region']
    
    # Filtra todos los ítems que pertenecen al mismo CSV (Continente y Región)
    items_para_el_archivo = [
        i for i in lista_global 
        if i['Continente'] == continente_afectado and i['Region'] == region_afectada
    ]
    
    # Sobrescribe el archivo CSV específico con los datos actualizados
    reescribir_archivo_csv_especifico(continente_afectado, region_afectada, items_para_el_archivo)
    
    print(f"Éxito: País '{item_encontrado['Pais']}' modificado.")
    return lista_global

def eliminar_item(lista_global):
    """
    Busca un país por nombre y lo elimina de la lista global.
    Luego, reescribe el archivo CSV afectado para reflejar la eliminación.
    """
    if not lista_global:
        print("La lista está vacía. No se puede eliminar.")
        return lista_global

    pais_a_eliminar = input("Ingrese el nombre exacto del país a eliminar: ").strip()
    
    item_encontrado = None
    # Busca el ítem a eliminar
    for item in lista_global:
        if item['Pais'].lower() == pais_a_eliminar.lower():
            item_encontrado = item
            break
            
    if not item_encontrado: 
        print(f"Error: País '{pais_a_eliminar}' no encontrado.")
        return lista_global


    lista_global.remove(item_encontrado) # Elimina el ítem de la lista en memoria
    

    continente_afectado = item_encontrado['Continente']
    region_afectada = item_encontrado['Region']
    
    # Filtra todos los ítems restantes del mismo CSV
    items_para_el_archivo = [
        i for i in lista_global 
        if i['Continente'] == continente_afectado and i['Region'] == region_afectada
    ]
    
    # Sobrescribe el archivo CSV afectado sin el ítem eliminado
    reescribir_archivo_csv_especifico(continente_afectado, region_afectada, items_para_el_archivo)
    
    print(f"Éxito: País '{item_encontrado['Pais']}' eliminado.")
    return lista_global # Devuelve la lista actualizada

def calcular_estadisticas(lista_global):
    """
    Calcula y muestra estadísticas básicas de la lista global:
    Conteo total, suma de población, promedio de población y conteo por continente.
    """
    if not lista_global:
        print("No hay datos para calcular estadísticas.")
        return

    total_items = len(lista_global)
    suma_poblacion = 0
    conteo_por_continente = {}

    for item in lista_global:
        try:
            # Suma la población (convirtiendo a entero)
            suma_poblacion += int(item['Poblacion'])
        except (ValueError, TypeError):
            # Ignora filas con valores de población no válidos
            pass 
            
        continente = item['Continente']
        # Conteo de países por cada continente
        conteo_por_continente[continente] = conteo_por_continente.get(continente, 0) + 1

    # Calcula el promedio solo si hay ítems
    promedio_poblacion = (suma_poblacion / total_items) if total_items > 0 else 0

    print("\n--- Estadísticas Globales ---")
    print(f"Cantidad total de países: {total_items}")
    # Formatea los números con separadores de miles
    print(f"Población total mundial (sumada): {suma_poblacion:,}")
    print(f"Población promedio por país: {promedio_poblacion:,.2f}")
    
    print("\nConteo de países por Continente (Nivel 1):")
    for continente, conteo in conteo_por_continente.items():
        print(f"- {continente}: {conteo} país(es)")
    print("-" * 30)

def ordenar_items(lista_global):
    """
    Ordena la lista de países según el criterio seleccionado por el usuario:
    1. Por País (alfabético)
    2. Por Población (descendente)
    """
    if not lista_global:
        print("No hay datos para ordenar.")
        return

    print("Seleccione criterio de ordenamiento:")
    print("1. Por País (A-Z)")
    print("2. Por Población (Mayor a Menor)")
    opcion = input("Opción: ").strip()

    lista_ordenada = []
    
    if opcion == '1':
        # Ordena alfabéticamente por el campo 'Pais'
        lista_ordenada = sorted(lista_global, key=lambda item: item['Pais'])
        print("\n--- Países ordenados por Nombre (A-Z) ---")
    elif opcion == '2':
        # Ordena por 'Poblacion' (convirtiendo a int para un orden numérico) de forma descendente
        lista_ordenada = sorted(
            lista_global, 
            key=lambda item: int(item.get('Poblacion', 0) or 0), 
            reverse=True
        )
        print("\n--- Países ordenados por Población (Mayor a Menor) ---")
    else:
        print("Opción no válida.")
        return

    # Muestra el resultado del ordenamiento
    mostrar_items(lista_ordenada)