# Parcial 2 - Gestión Jerárquica de Datos (El Desafío Jerárquico)

Este proyecto es la implementación del Parcial 2 de Programación 1, que consiste en un sistema de gestión de datos (CRUD) que utiliza una estructura de persistencia basada en el sistema de archivos, abandonando el modelo de un CSV único.

El objetivo principal es aplicar conocimientos de manipulación de archivos (`os`), recursividad y buenas prácticas de modularización.

---

## 1. Diseño y Estructura de Datos (Fase 1)

Se cumple con el requisito de definir un dominio y una jerarquía de 3 niveles.

* **Dominio Elegido:** Organización Geográfica de Países.
* **Ítems Individuales:** Cada país se representa internamente como un **diccionario** de Python  (ej. `{'Pais': 'Argentina', 'Poblacion': 45000000, ...}`).

### Lógica de Almacenamiento Jerárquico

La estructura de 3 niveles definida se mapea directamente a la estructura de carpetas de la siguiente manera:

1.  **Nivel 1 (Carpeta):** `Continente` (Ej: `DB/America/`)
2.  **Nivel 2 (Carpeta):** `Región` (Ej: `DB/America/Sur/`)
3.  **Nivel 3 (Archivo):** `Datos.csv` (Ej: `DB/America/Sur/Datos.csv`)

Este archivo final (`Datos.csv`) es el que almacena los ítems (países) que pertenecen a esa ruta jerárquica específica.

La función de **Alta** (`funciones.py -> alta_item`) implementa esta lógica:
1.  Recibe los 3 niveles (Continente, Región, y los datos del país).
2.  Utiliza `os.makedirs(..., exist_ok=True)` para crear dinámicamente la estructura de carpetas (Nivel 1 y 2) si esta no existe.
3.  Añade (modo `'a'`) el nuevo ítem (país) al archivo `Datos.csv` (Nivel 3) dentro de la ruta correspondiente.

---

## 2. Implementación Técnica (Fase 2)

El proyecto se divide en `main.py` (menú y control) y `funciones.py` (lógica) para cumplir con la **modularización**.

### Lectura Recursiva (Requisito Obligatorio)

Para cumplir con la consigna de leer todos los datos de la jerarquía, se implementó la función `leer_datos_recursivo(ruta_actual)`:

* **Paso Recursivo:** Si la función encuentra un directorio, se llama a sí misma (`.extend(leer_datos_recursivo(ruta_completa))`) para explorar ese subdirectorio.
* **Caso Base:** Si la función encuentra un archivo que termina en `.csv`, lo lee usando `csv.DictReader` y añade los diccionarios a la lista.

Esta función consolida todos los ítems de todos los archivos `Datos.csv` dispersos en una **única lista de diccionarios** , que luego es utilizada por el `main.py` para las operaciones de consulta, modificación, estadísticas y ordenamiento.

### Manejo de Archivos y Excepciones

* Toda la lectura y escritura de archivos se realiza de forma segura usando la cláusula `with open(...)`.
* Se utiliza `try...except` para capturar `OSError` (errores al crear carpetas o escribir) y `FileNotFoundError`, como en la importación o al leer el directorio base.

---

## 3. Instrucciones de Uso

Siga estos pasos para ejecutar el programa:

1.  Asegúrese de tener los 4 archivos en la misma carpeta:
    * `main.py`
    * `funciones.py`
    * `paises.csv` (Este es el archivo de origen para la importación)
    * `README.md`
2.  Abra una terminal en esa carpeta.
3.  Ejecute el programa principal:
    ```bash
    python main.py
    ```
4.  **¡IMPORTANTE!** La primera vez que ejecute el programa, debe seleccionar la **Opción 1: Importar datos iniciales**.
    * Esta opción leerá el `paises.csv`, borrará cualquier base de datos `DB/` antigua para evitar duplicados, y creará la estructura jerárquica de carpetas y archivos `Datos.csv` con los datos iniciales.
5.  Una vez importados los datos, puede explorar el resto de las opciones del menú (CRUD, filtrado, estadísticas, etc.).