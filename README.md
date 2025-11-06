# Proyecto_Paises: El Desafío Jerárquico (Parcial 2)

¡Hola! Este proyecto es la entrega final integradora y representa nuestro paso de gestionar datos en un solo archivo a dominar la **persistencia jerárquica** en el sistema de archivos.

## La Estructura que Elegimos

[cite_start]Decidimos modelar el mundo usando una jerarquía de países, lo cual requería tres niveles de profundidad (como se solicitaba en el parcial [cite: 22, 141]):

`datos/`
└── <Continente> (Nivel 1)
    └── <Región> (Nivel 2)
        └── <Subregión> (Nivel 3)
            └── `paises.csv` (Aquí viven los datos)

Si un país no tiene una región o subregión definida en el CSV inicial, usamos los filtros `SinRegion` o `SinSubregion` para mantener la integridad de la estructura.

## Lo Más Importante: Los Pilares del Proyecto

[cite_start]Estos son los puntos que demuestran que realmente entendimos el núcleo del parcial[cite: 118, 119]:

1.  **La Función Recursiva:** El corazón de la lectura de datos es nuestra función `leer_recursivo()`. Se encarga de entrar en cada carpeta, buscar *todos* los `paises.csv` que existan en cualquier nivel de la jerarquía, y consolidar los datos en una sola lista gigante en Python. [cite_start]¡Adiós a los bucles simples! [cite: 44, 165]
2.  [cite_start]**Sistema de Archivos Dinámico:** Utilizamos la librería **`os`** [cite: 39] para un manejo robusto:
    * [cite_start]Crea automáticamente cualquier carpeta (`Continente`, `Región`, `Subregión`) que no exista al dar de alta un nuevo país[cite: 41, 153].
    * [cite_start]Todo el manejo de I/O se hace con la cláusula **`with open()`** para evitar fugas de recursos[cite: 43, 155].
3.  **Identificación de Ítem:** Para las funciones de `Modificar` y `Eliminar`, un país se identifica por su ubicación completa: `Continente + Región + Subregión + Nombre`.

## Funcionalidades del Menú (CRUD y Más)

El programa se ejecuta desde `main.py` y presenta un menú completo para manipular los datos:

* **Migración Inicial:** La primera vez que ejecutas `main.py`, automáticamente toma los datos de nuestro `paises.csv` plano y los distribuye a la nueva estructura de carpetas jerárquica.
* **CRUD Completo:**
    * **Alta:** Inserta nuevos países en la jerarquía correcta.
    * **Lectura:** Muestra todos los países (resultado de la función recursiva).
    * [cite_start]**Modificación/Eliminación:** Permite actualizar campos o dar de baja países específicos[cite: 76, 89].
* **Consultas:** Puedes buscar cualquier país por nombre.
* [cite_start]**Estadísticas Globales:** Calculamos promedios de población/superficie y el conteo total por continente[cite: 98].
* [cite_start]**Ordenamiento:** Ordenamos la lista global por Nombre, Población o Superficie[cite: 97].

## Notas de Calidad

* [cite_start]**Modularización:** El código está organizado en `funciones.py` (lógica y persistencia) y `main.py` (interfaz y menú)[cite: 37, 181].
* [cite_start]**Estilo:** Usamos indentación de 4 espacios consistentes (PEP8)[cite: 189].
* [cite_start]**Robustez:** Implementamos `try...except` para capturar errores de formato (`ValueError`) y problemas de I/O[cite: 51, 52].
