import funciones as fn

def mostrar_menu():
    """Imprime el menú de opciones en pantalla."""
    print("\n--- 🗂️ Sistema de Gestión Jerárquica (Países) ---")
    print("Operaciones de Base de Datos:")
    print(" 1. Importar datos iniciales (desde paises.csv)")
    print(" 2. Alta de nuevo país (Crear)")
    print("\nOperaciones de Consulta (Usan Lectura Recursiva):")
    print(" 3. Mostrar todos los países (Lectura Global)")
    print(" 4. Filtrar países (Por Continente o Región)")
    print(" 5. Modificar país (Actualizar)")
    print(" 6. Eliminar país (Borrar)")
    print(" 7. Ordenar países (Por Nombre o Población)")
    print(" 8. Ver Estadísticas Globales")
    print("\n 0. Salir")
    print("-------------------------------------------------")

def main():
    """Función principal que maneja el bucle del menú."""
    
    lista_global_memoria = None
    datos_necesitan_recarga = True 

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        # (Cumple Fase 3 - Carga centralizada recursiva)
        if opcion in ['3', '4', '5', '6', '7', '8'] and datos_necesitan_recarga:
            print("\nCargando datos desde la estructura de carpetas (recursivo)...")
            lista_global_memoria = fn.obtener_todos_los_datos()
            datos_necesitan_recarga = False
            if not lista_global_memoria and opcion != '3':
                print("No se encontraron datos. Intente 'Importar' o 'Dar de Alta' primero.")


        if opcion == '1':
            fn.importar_datos_iniciales('paises.csv')
            datos_necesitan_recarga = True 
        
        elif opcion == '2':
            # (Cumple Fase 3 - Alta)
            print("\n--- Alta de Nuevo País ---")
            continente = fn.validar_no_vacio("Ingrese Continente (Nivel 1): ")
            region = fn.validar_no_vacio("Ingrese Región (Nivel 2): ")
            pais = fn.validar_no_vacio("Ingrese Nombre del País: ")
            poblacion = fn.validar_numero_positivo("Ingrese Población (numérico): ")
            superficie = fn.validar_numero_positivo("Ingrese Superficie (numérico): ")
            
            fn.alta_item(continente, region, pais, poblacion, superficie)
            datos_necesitan_recarga = True

        elif opcion == '3':
            # (Cumple Fase 3 - Mostrar)
            fn.mostrar_items(lista_global_memoria)

        elif opcion == '4':
            # (Cumple Fase 3 - Filtrado)
            fn.filtrar_items(lista_global_memoria)

        elif opcion == '5':
            # (Cumple Fase 3 - Modificar)
            lista_global_memoria = fn.modificar_item(lista_global_memoria)
            
        elif opcion == '6':
            # (Cumple Fase 3 - Eliminar)
            lista_global_memoria = fn.eliminar_item(lista_global_memoria)

        elif opcion == '7':
            # (Cumple Fase 3 - Adicionales)
            fn.ordenar_items(lista_global_memoria)

        elif opcion == '8':
            # (Cumple Fase 3 - Adicionales)
            fn.calcular_estadisticas(lista_global_memoria)

        elif opcion == '0':
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

        if opcion != '0':
            input("\nPresione Enter para continuar...")

# --- Punto de entrada estándar de Python ---
if __name__ == "__main__":
    main()