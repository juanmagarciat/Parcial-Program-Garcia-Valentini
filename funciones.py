"""
funciones.py
Trabajo Práctico Integrador - Parcial 2

Este módulo gestiona un sistema jerárquico de países con persistencia en archivos CSV.
Cumple con los puntos del parcial:
- Estructura de 3 niveles (continente / región / subregión)
- Lectura recursiva de carpetas
- CRUD completo (alta, lectura, modificación, eliminación)
- Manejo seguro de archivos CSV con 'with open()'
- Uso de la librería os
- Código legible y con comentarios explicativos
"""

import csv
import os
from typing import List, Dict, Optional

# Carpeta base donde se guarda toda la jerarquía
DATOS_DIR = "datos"


# --------------------------------------------------------------------
# Funciones auxiliares y de validación
# --------------------------------------------------------------------

def _mostrar_pais(pais: Dict) -> None:
    """Muestra los datos de un país en formato ordenado y legible."""
    print("\n------------------------------")
    print(f"Nombre:     {pais.get('nombre')}")
    print(f"Población:  {pais.get('poblacion'):,}")
    print(f"Superficie: {pais.get('superficie'):,} km²")
    print(f"Continente: {pais.get('continente')}")
    print(f"Región:     {pais.get('region')}")
    print(f"Subregión:  {pais.get('subregion')}")
    print("------------------------------")


def crear_ruta_y_archivo(continente: str, region: str, subregion: str) -> str:
    """
    Crea las carpetas necesarias según el continente, región y subregión.
    Devuelve la ruta completa del archivo CSV donde se guardará el país.
    """
    ruta = os.path.join(DATOS_DIR, continente, region, subregion)
    os.makedirs(ruta, exist_ok=True)  # si no existen, las crea
    return os.path.join(ruta, "paises.csv")


def _es_valido_pais(pais: Dict) -> bool:
    """
    Verifica que el país tenga todos los datos correctos antes de guardarlo.
    Retorna True si está todo bien, False si falta algo o hay error.
    """
    try:
        nombre = str(pais.get("nombre", "")).strip()
        if not nombre:
            return False
        poblacion = int(pais.get("poblacion", 0))
        superficie = int(pais.get("superficie", 0))
        if poblacion < 0 or superficie < 0:
            return False
    except (ValueError, TypeError):
        return False
    return True


# --------------------------------------------------------------------
# CRUD: Alta (Create)
# --------------------------------------------------------------------

def alta_pais(pais: Dict) -> bool:
    """
    Da de alta un país nuevo en su carpeta correspondiente.
    Si el archivo no existe, lo crea con encabezado.
    """
    if not _es_valido_pais(pais):
        print("Error: datos del país inválidos o incompletos.")
        return False

    ruta_csv = crear_ruta_y_archivo(pais["continente"], pais["region"], pais["subregion"])
    existe_encabezado = os.path.exists(ruta_csv)

    try:
        with open(ruta_csv, mode="a", newline="", encoding="utf-8") as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente", "region", "subregion"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            if not existe_encabezado:
                escritor.writeheader()
            escritor.writerow({
                "nombre": pais["nombre"].strip(),
                "poblacion": int(pais["poblacion"]),
                "superficie": int(pais["superficie"]),
                "continente": pais["continente"],
                "region": pais["region"],
                "subregion": pais["subregion"]
            })
        return True
    except Exception as e:
        print(f"Error al escribir el archivo CSV: {e}")
        return False


# --------------------------------------------------------------------
# Lectura recursiva (Read)
# --------------------------------------------------------------------

def leer_recursivo(ruta_base: str = DATOS_DIR) -> List[Dict]:
    """
    Función recursiva que recorre todas las carpetas desde 'datos/'
    y lee cada 'paises.csv' encontrado.
    Devuelve una lista única con todos los países del sistema.
    """
    paises = []

    if not os.path.exists(ruta_base):
        return paises

    for entrada in os.scandir(ruta_base):
        if entrada.is_dir():
            # Si es carpeta, llamo de nuevo a la función (recursividad)
            paises.extend(leer_recursivo(entrada.path))
        elif entrada.is_file() and entrada.name.lower().endswith(".csv"):
            try:
                # saco continente, región y subregión desde la ruta
                partes = os.path.normpath(entrada.path).split(os.sep)
                if DATOS_DIR in partes:
                    i = partes.index(DATOS_DIR)
                    continente = partes[i + 1] if len(partes) > i + 1 else ""
                    region = partes[i + 2] if len(partes) > i + 2 else ""
                    subregion = partes[i + 3] if len(partes) > i + 3 else ""
                else:
                    continente = region = subregion = ""

                # leo el CSV y sumo sus países a la lista
                with open(entrada.path, mode="r", newline="", encoding="utf-8") as f:
                    lector = csv.DictReader(f)
                    for fila in lector:
                        fila["poblacion"] = int(fila.get("poblacion") or 0)
                        fila["superficie"] = int(fila.get("superficie") or 0)
                        fila.setdefault("continente", continente)
                        fila.setdefault("region", region)
                        fila.setdefault("subregion", subregion)
                        paises.append(fila)
            except Exception as e:
                print(f"Error al leer {entrada.path}: {e}")

    return paises


# --------------------------------------------------------------------
# Migración desde un CSV original
# --------------------------------------------------------------------

def migrar_datos(archivo_fuente: str = "paises.csv") -> int:
    """
    Migra todos los países desde un CSV plano a la estructura jerárquica.
    Si no hay región/subregión, usa 'SinRegion' y 'SinSubregion'.
    """
    migrados = 0
    if not os.path.exists(archivo_fuente):
        print("No se encontró el archivo de origen.")
        return 0

    with open(archivo_fuente, mode="r", newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            pais = {
                "nombre": fila.get("nombre", "").strip(),
                "poblacion": int(fila.get("poblacion", 0) or 0),
                "superficie": int(fila.get("superficie", 0) or 0),
                "continente": fila.get("continente", "").strip() or "SinContinente",
                "region": fila.get("region", "").strip() or "SinRegion",
                "subregion": fila.get("subregion", "").strip() or "SinSubregion"
            }

            if alta_pais(pais):
                migrados += 1

    print(f"Migración completa: {migrados} países migrados correctamente.")
    return migrados


# --------------------------------------------------------------------
# Funciones de búsqueda y acceso a la lista global
# --------------------------------------------------------------------

def buscar_pais_nombre(lista_paises: Optional[List[Dict]] = None, termino: str = "") -> List[Dict]:
    """Busca un país por nombre (no distingue mayúsculas/minúsculas)."""
    if lista_paises is None:
        lista_paises = leer_recursivo()
    termino = termino.lower().strip()
    return [p for p in lista_paises if termino in p.get("nombre", "").lower()]


def obtener_lista_global() -> List[Dict]:
    """Devuelve la lista completa de países usando la función recursiva."""
    return leer_recursivo()


# --------------------------------------------------------------------
# Modificación (Update) y Eliminación (Delete)
# --------------------------------------------------------------------

def modificar_item(continente: str, region: str, subregion: str, nombre: str, campo: str, nuevo_valor) -> bool:
    """Modifica un país ya existente dentro de su CSV."""
    ruta_csv = os.path.join(DATOS_DIR, continente, region, subregion, "paises.csv")
    if not os.path.exists(ruta_csv):
        print("No se encontró el archivo del país.")
        return False

    try:
        with open(ruta_csv, mode="r", newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return False

    modificado = False
    for fila in filas:
        if fila["nombre"].strip().lower() == nombre.strip().lower():
            if campo in fila:
                fila[campo] = nuevo_valor
                modificado = True
            else:
                print("El campo ingresado no existe.")
                return False

    if not modificado:
        print("No se encontró el país para modificar.")
        return False

    try:
        with open(ruta_csv, mode="w", newline="", encoding="utf-8") as f:
            campos = ["nombre", "poblacion", "superficie", "continente", "region", "subregion"]
            escritor = csv.DictWriter(f, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(filas)
        print("País modificado correctamente.")
        return True
    except Exception as e:
        print(f"Error al guardar los cambios: {e}")
        return False


def eliminar_item(continente: str, region: str, subregion: str, nombre: str) -> bool:
    """Elimina un país del archivo correspondiente."""
    ruta_csv = os.path.join(DATOS_DIR, continente, region, subregion, "paises.csv")
    if not os.path.exists(ruta_csv):
        print("No se encontró el archivo.")
        return False

    try:
        with open(ruta_csv, mode="r", newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return False

    nuevas = [r for r in filas if r["nombre"].strip().lower() != nombre.strip().lower()]
    if len(nuevas) == len(filas):
        print("No se encontró el país a eliminar.")
        return False

    try:
        with open(ruta_csv, mode="w", newline="", encoding="utf-8") as f:
            campos = ["nombre", "poblacion", "superficie", "continente", "region", "subregion"]
            escritor = csv.DictWriter(f, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(nuevas)
        print("País eliminado correctamente.")
        return True
    except Exception as e:
        print(f"Error al sobrescribir el archivo: {e}")
        return False


# --------------------------------------------------------------------
# Ordenamiento y Estadísticas
# --------------------------------------------------------------------

def ordenar_global(criterio: str = "nombre", reverse: bool = False) -> List[Dict]:
    """Ordena la lista global de países según nombre, población o superficie."""
    lista = obtener_lista_global()

    if criterio == "nombre":
        return sorted(lista, key=lambda p: p["nombre"].lower(), reverse=reverse)
    elif criterio == "poblacion":
        return sorted(lista, key=lambda p: int(p["poblacion"]), reverse=reverse)
    elif criterio == "superficie":
        return sorted(lista, key=lambda p: int(p["superficie"]), reverse=reverse)
    else:
        return lista


def estadisticas_globales() -> Dict:
    """
    Calcula estadísticas generales:
    - cantidad total de países
    - promedios de población y superficie
    - cantidad por continente
    """
    lista = obtener_lista_global()
    total = len(lista)
    if total == 0:
        return {"total": 0, "promedio_poblacion": 0, "promedio_superficie": 0, "por_continente": {}}

    suma_pob = sum(int(p["poblacion"]) for p in lista)
    suma_sup = sum(int(p["superficie"]) for p in lista)

    conteo = {}
    for p in lista:
        c = p.get("continente", "SinContinente")
        conteo[c] = conteo.get(c, 0) + 1

    return {
        "total": total,
        "promedio_poblacion": suma_pob / total,
        "promedio_superficie": suma_sup / total,
        "por_continente": conteo
    }

# --------------------------------------------------------------------
# Limpieza de duplicados (utilidad opcional)
# --------------------------------------------------------------------

def limpiar_duplicados(ruta_csv: str) -> None:
    """
    Elimina filas duplicadas dentro de un mismo archivo CSV según el nombre del país.
    Se queda solo con la primera aparición de cada país.
    """
    if not os.path.exists(ruta_csv):
        print("⚠️  No se encontró el archivo especificado.")
        return

    try:
        with open(ruta_csv, "r", newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            vistos = set()
            filas_unicas = []

            for fila in lector:
                nombre = fila.get("nombre", "").strip().lower()
                if nombre and nombre not in vistos:
                    vistos.add(nombre)
                    filas_unicas.append(fila)

        with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=lector.fieldnames)
            escritor.writeheader()
            escritor.writerows(filas_unicas)

        print(f"Duplicados eliminados correctamente en '{ruta_csv}'. "
              f"Total final: {len(filas_unicas)} países.")
    except Exception as e:
        print(f"Error al limpiar duplicados: {e}")
