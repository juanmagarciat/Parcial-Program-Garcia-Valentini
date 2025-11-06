"""
main.py - Programa principal que utiliza funciones.py

Uso rápido:
- Ejecutar: python main.py
- Al primer run se intentará migrar los datos desde 'paises.csv' hacia la jerarquía en 'datos/'.
- Luego usar el menú para Alta/Lectura/Modificación/Eliminación/Estadísticas.
"""

import sys
from funciones import (
    migrar_datos, obtener_lista_global, buscar_pais_nombre, alta_pais,
    ordenar_global, estadisticas_globales, modificar_item, eliminar_item
)

def mostrar_menu():
    print("\n--- Menú Principal ---")
    print("1. Migrar datos desde paises.csv (si no se hizo)")
    print("2. Mostrar todos los países (lectura recursiva)")
    print("3. Buscar país por nombre (global)")
    print("4. Alta de país (jerárquico)")
    print("5. Modificar país")
    print("6. Eliminar país")
    print("7. Ordenar (global)")
    print("8. Estadísticas globales")
    print("9. Eliminar duplicados en un archivo CSV")
    print("0. Salir")

def solicitar_pais_interactivo() -> dict:
    print("\nAlta de país: completa los datos solicitados.")
    nombre = input("Nombre: ").strip()
    try:
        poblacion = int(input("Población (número): ").strip())
    except ValueError:
        print("Población inválida.")
        return {}
    try:
        superficie = int(input("Superficie (km2) (número): ").strip())
    except ValueError:
        print("Superficie inválida.")
        return {}
    continente = input("Continente: ").strip() or 'SinContinente'
    region = input("Región: ").strip() or 'SinRegion'
    subregion = input("Subregión: ").strip() or 'SinSubregion'
    return {
        'nombre': nombre,
        'poblacion': poblacion,
        'superficie': superficie,
        'continente': continente,
        'region': region,
        'subregion': subregion
    }

def main():
    # Intentar migración inicial automática (silenciosa)
    migrar_datos('paises.csv')
    while True:
        mostrar_menu()
        opcion = input("\nIngrese opción: ").strip()
        if opcion == '1':
            migrar_datos('paises.csv')
        elif opcion == '2':
            lista = obtener_lista_global()
            if not lista:
                print("No hay registros.")
            else:
                for p in lista:
                    print(f"{p.get('nombre')} - {p.get('continente')} / {p.get('region')} / {p.get('subregion')}")
        elif opcion == '3':
            termino = input("Término a buscar: ").strip()
            res = buscar_pais_nombre(None, termino)
            if not res:
                print("No se encontraron resultados.")
            else:
                for p in res:
                    print(p)
        elif opcion == '4':
            pais = solicitar_pais_interactivo()
            if pais:
                ok = alta_pais(pais)
                print("Alta exitosa." if ok else "Alta fallida.")
        elif opcion == '5':
            continente = input("Continente donde está el país: ").strip()
            region = input("Región: ").strip()
            subregion = input("Subregión: ").strip()
            nombre = input("Nombre del país a modificar: ").strip()
            campo = input("Campo a modificar (nombre/poblacion/superficie/continente/region/subregion): ").strip()
            nuevo = input("Nuevo valor: ").strip()
            # intentar convertir numeros si corresponde
            if campo in ('poblacion','superficie'):
                try:
                    nuevo = int(nuevo)
                except ValueError:
                    print("Valor numérico inválido.")
                    continue
            OK = modificar_item(continente, region, subregion, nombre, campo, nuevo)
            print("Modificado." if OK else "No modificado.")
        elif opcion == '6':
            continente = input("Continente donde está el país: ").strip()
            region = input("Región: ").strip()
            subregion = input("Subregión: ").strip()
            nombre = input("Nombre del país a eliminar: ").strip()
            OK = eliminar_item(continente, region, subregion, nombre)
            print("Eliminado." if OK else "No eliminado.")
        elif opcion == '7':
            criterio = input("Criterio (nombre/poblacion/superficie): ").strip()
            orden = input("Orden (asc/desc): ").strip().lower()
            rev = (orden == 'desc')
            ordenados = ordenar_global(criterio, reverse=rev)
            for p in ordenados:
                print(f"{p.get('nombre')} - {p.get('poblacion'):,} - {p.get('superficie'):,}")
        elif opcion == '8':
            est = estadisticas_globales()
            print(est)
        elif opcion == "9":
            print("\n--- Limpieza de duplicados ---")
            ruta = input("Ingrese la ruta completa del archivo CSV a limpiar (por ejemplo: datos/America/SinRegion/SinSubregion/paises.csv): ").strip()
            from funciones import limpiar_duplicados
            limpiar_duplicados(ruta)
        elif opcion == '0':
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")


if __name__ == '__main__':
    main()
