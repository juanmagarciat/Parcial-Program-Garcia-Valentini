import os
import csv
import shutil


BASE_DIR = "DB"  # Directorio raíz para la base de datos jerárquica
HEADERS = ['Pais', 'Poblacion', 'Superficie'] # Cabeceras para los CSV internos



def validar_no_vacio(texto):
    """Valida que la entrada no esté vacía después de quitar espacios."""
    while True:
        entrada = input(texto).strip()
        if entrada:
            return entrada
        else:
            print("Error: El campo no puede estar vacío.")

def validar_numero_positivo(texto):
    """Valida que la entrada sea un número (entero) y sea positivo."""
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



def obtener_ruta_csv(continente, region):
    
    
    ruta_directorio = os.path.join(BASE_DIR, continente, region)
    
    
    ruta_csv = os.path.join(ruta_directorio, "Datos.csv")
    
    return ruta_directorio, ruta_csv

def alta_item(continente, region, pais, poblacion, superficie):
    try:
        ruta_directorio, ruta_csv = obtener_ruta_csv(continente, region)
        
        os.makedirs(ruta_directorio, exist_ok=True)

        nuevo_item = {
            'Pais': pais,
            'Poblacion': poblacion,
            'Superficie': superficie
        }
        
        escribir_cabeceras = not os.path.exists(ruta_csv)

        with open(ruta_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            
            if escribir_cabeceras:
                writer.writeheader()
                
            writer.writerow(nuevo_item)
            
        print(f"Éxito: País '{pais}' agregado en {ruta_csv}")

    except OSError as e: 
        print(f"Error de sistema al crear directorios o escribir archivo: {e}")
    except Exception as e:
        print(f"Error inesperado en alta_item: {e}")


def leer_datos_recursivo(ruta_actual):
    items_consolidados = [] 
    
    try:
        for nombre_entrada in os.listdir(ruta_actual):
            ruta_completa = os.path.join(ruta_actual, nombre_entrada)
            
            if os.path.isdir(ruta_completa):
                # Si es un directorio, volvemos a llamar a la función
                items_consolidados.extend(leer_datos_recursivo(ruta_completa))
                
            elif os.path.isfile(ruta_completa) and nombre_entrada.endswith('.csv'):
                
                
                
                # Obtenemos la jerarquía (Continente, Region) desde la ruta
                partes_ruta = ruta_actual.split(os.sep)
                continente = partes_ruta[1] if len(partes_ruta) > 1 else "N/A"
                region = partes_ruta[2] if len(partes_ruta) > 2 else "N/A"

                
                with open(ruta_completa, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for fila in reader:
                        
                        fila['Continente'] = continente
                        fila['Region'] = region
                        items_consolidados.append(fila)

    except FileNotFoundError: 
        print(f"Error: El directorio base '{BASE_DIR}' no existe.")
    except OSError as e: 
        print(f"Error de sistema al leer el directorio {ruta_actual}: {e}")
        
    return items_consolidados

def obtener_todos_los_datos():
    if not os.path.exists(BASE_DIR):
        print(f"Directorio '{BASE_DIR}' no encontrado. Creando...")
        try:
            os.makedirs(BASE_DIR)
        except OSError as e:
            print(f"No se pudo crear el directorio base: {e}")
            return []
    
    return leer_datos_recursivo(BASE_DIR)

# Funciones de Importación

def importar_datos_iniciales(archivo_origen):
    print(f"\nLimpiando base de datos anterior en '{BASE_DIR}'...")
    try:
        if os.path.exists(BASE_DIR):
            shutil.rmtree(BASE_DIR) # Borra la carpeta y todo su contenido
        
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
        with open(archivo_origen, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            contador = 0
            for fila in reader:
                try:
                    alta_item(
                        fila['Continente'],
                        fila['Region'],
                        fila['Pais'],
                        int(fila['Poblacion']),
                        int(fila['Superficie'])
                    )
                    contador += 1
                except (ValueError, KeyError) as e:
                    print(f"Error en formato de fila: {fila}. Detalle: {e}")
                
            print(f"\nImportación completada. {contador} países migrados a la estructura de carpetas.")
            
    except FileNotFoundError:
        print(f"Error: Archivo '{archivo_origen}' no encontrado.")
    except Exception as e:
        print(f"Error inesperado durante la importación: {e}")

# Funcionalidades Adicionales

def mostrar_items(lista_items):
    """(Cumple Fase 3 - Mostrar) Muestra la lista global de ítems."""
    if not lista_items:
        print("No hay ítems para mostrar.")
        return

    print("\n--- Listado Global de Países (Lectura Recursiva) ---")
    print(f"{'País':<20} {'Población':<15} {'Superficie':<15} {'Continente':<15} {'Región':<15}")
    print("-" * 80)
    
    for item in lista_items:
        try:
            poblacion = f"{int(item['Poblacion']):,}"
            superficie = f"{int(item['Superficie']):,}"
        except (ValueError, TypeError):
            poblacion = item.get('Poblacion', 'N/A')
            superficie = item.get('Superficie', 'N/A')

        
        print(f"{item['Pais']:<20} {poblacion:<15} {superficie:<15} {item['Continente']:<15} {item['Region']:<15}")
    print("-" * 80)
    print(f"Total de ítems: {len(lista_items)}")

def filtrar_items(lista_global):
    """(Cumple Fase 3 - Filtrado) Filtra la lista global."""
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
        if item.get(clave_filtro, '').lower() == termino_busqueda:
            resultados.append(item)

    if not resultados:
        print(f"No se encontraron ítems para '{termino_busqueda}'.")
    else:
        print(f"\n--- Resultados del Filtro ({len(resultados)} encontrados) ---")
        mostrar_items(resultados)


def reescribir_archivo_csv_especifico(continente, region, items_del_archivo):
    """
    (Usado por Modificar y Eliminar - Fase 3)
    Sobrescribe (modo 'w') un único archivo CSV.
    """
    try:
        _, ruta_csv = obtener_ruta_csv(continente, region)
        
        with open(ruta_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            
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
    """(Cumple Fase 3 - Modificación/Update)"""
    if not lista_global:
        print("La lista está vacía. No se puede modificar.")
        return lista_global
        
    pais_a_modificar = input("Ingrese el nombre exacto del país a modificar: ").strip()
    
    item_encontrado = None
    for item in lista_global:
        if item['Pais'].lower() == pais_a_modificar.lower():
            item_encontrado = item
            break
            
    if not item_encontrado:
        print(f"Error: País '{pais_a_modificar}' no encontrado.")
        return lista_global

    print(f"Modificando '{item_encontrado['Pais']}'. Deje en blanco para no cambiar.")
    
    nuevo_pais = input(f"Nuevo nombre ({item_encontrado['Pais']}): ").strip()
    nueva_poblacion_str = input(f"Nueva población ({item_encontrado['Poblacion']}): ").strip()
    nueva_superficie_str = input(f"Nueva superficie ({item_encontrado['Superficie']}): ").strip()

    
    if nuevo_pais:
        item_encontrado['Pais'] = nuevo_pais
    if nueva_poblacion_str:
    
        item_encontrado['Poblacion'] = validar_numero_positivo(f"Confirme nueva población ({nueva_poblacion_str}): ")
    if nueva_superficie_str:
        
        item_encontrado['Superficie'] = validar_numero_positivo(f"Confirme nueva superficie ({nueva_superficie_str}): ")
        

    continente_afectado = item_encontrado['Continente']
    region_afectada = item_encontrado['Region']
    
    items_para_el_archivo = [
        i for i in lista_global 
        if i['Continente'] == continente_afectado and i['Region'] == region_afectada
    ]
    
    reescribir_archivo_csv_especifico(continente_afectado, region_afectada, items_para_el_archivo)
    
    print(f"Éxito: País '{item_encontrado['Pais']}' modificado.")
    return lista_global

def eliminar_item(lista_global):
    """(Cumple Fase 3 - Eliminación/Delete)"""
    if not lista_global:
        print("La lista está vacía. No se puede eliminar.")
        return lista_global

    pais_a_eliminar = input("Ingrese el nombre exacto del país a eliminar: ").strip()
    
    item_encontrado = None
    for item in lista_global:
        if item['Pais'].lower() == pais_a_eliminar.lower():
            item_encontrado = item
            break
            
    if not item_encontrado: 
        print(f"Error: País '{pais_a_eliminar}' no encontrado.")
        return lista_global


    lista_global.remove(item_encontrado)
    

    continente_afectado = item_encontrado['Continente']
    region_afectada = item_encontrado['Region']
    
    items_para_el_archivo = [
        i for i in lista_global 
        if i['Continente'] == continente_afectado and i['Region'] == region_afectada
    ]
    
    reescribir_archivo_csv_especifico(continente_afectado, region_afectada, items_para_el_archivo)
    
    print(f"Éxito: País '{item_encontrado['Pais']}' eliminado.")
    return lista_global # Devuelve la lista actualizada

def calcular_estadisticas(lista_global):
    """Calcula y muestra estadísticas sobre la lista global."""
    if not lista_global:
        print("No hay datos para calcular estadísticas.")
        return

    total_items = len(lista_global)
    suma_poblacion = 0
    conteo_por_continente = {}

    for item in lista_global:
        try:
            suma_poblacion += int(item['Poblacion'])
        except (ValueError, TypeError):
            pass 
            
        continente = item['Continente']
        conteo_por_continente[continente] = conteo_por_continente.get(continente, 0) + 1

    promedio_poblacion = (suma_poblacion / total_items) if total_items > 0 else 0

    print("\n--- Estadísticas Globales ---")
    print(f"Cantidad total de países: {total_items}")
    print(f"Población total mundial (sumada): {suma_poblacion:,}")
    print(f"Población promedio por país: {promedio_poblacion:,.2f}")
    
    print("\nConteo de países por Continente (Nivel 1):")
    for continente, conteo in conteo_por_continente.items():
        print(f"- {continente}: {conteo} país(es)")
    print("-" * 30)

def ordenar_items(lista_global):
    """Ordena la lista global por dos criterios."""
    if not lista_global:
        print("No hay datos para ordenar.")
        return

    print("Seleccione criterio de ordenamiento:")
    print("1. Por País (A-Z)")
    print("2. Por Población (Mayor a Menor)")
    opcion = input("Opción: ").strip()

    lista_ordenada = []
    
    if opcion == '1':
        lista_ordenada = sorted(lista_global, key=lambda item: item['Pais'])
        print("\n--- Países ordenados por Nombre (A-Z) ---")
    elif opcion == '2':
        lista_ordenada = sorted(
            lista_global, 
            key=lambda item: int(item.get('Poblacion', 0) or 0), 
            reverse=True
        )
        print("\n--- Países ordenados por Población (Mayor a Menor) ---")
    else:
        print("Opción no válida.")
        return

    mostrar_items(lista_ordenada)