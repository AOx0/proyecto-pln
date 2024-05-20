#import "template.typ": *
#import "@preview/tablex:0.0.8": tablex

#show: project.with(
  title: "Proyecto Final: Procesamiento de lenguaje natural",
  authors: (
    (name: "Osornio López Daniel Alejandro", email: "0244685@up.edu.mx"),
    (name: "Jesús Alejandro Valencia Guzmán", email: "0252011@up.edu.mx"),
  ),
  date: "May 24, 2024",
)

#let TODO(msg) = {[]}

= Introducción

== Objetivo

== Metodología


= Entrega

Le entregamos un repositorio de código _hosteado_ en GitHub con todo el código generado para el proyecto, así como con los recursos resultantes como son imágenes, documentos PDF, embeddings y modelos.

La liga con el código fuente es:

#text(font: "JetBrainsMono NFM", size: 9pt, weight: 900, [#h(1cm) https://github.com/AOx0/proyecto-pln])

La estructura de los archivos de código incluidos es la que se describe en la siguiente tabla:

#tablex(
  columns: (2.6cm, 1fr),
  map-cells: it => {
    if it.x == 0 {
      it.align = right
    }
    it
  },
  stroke: gray + 0pt,
  [*Carpeta*], [*Función*],
  [`cleaner-lib/`], [Incluye la implementación de un _parser_ que puede encontrar bloques de comentarios de una sola línea y multilínea con soporte para _lookahead_ sin límite @lookahead.],
  [`cleaner-cli/`], [Incluye la implementación de una herramienta de la line de comandos para hacer una limpieza anticipada de los datos (ver la #TODO("Agregar sección de limpieza anticipada"))],
  [`cleaner-py/`], [Incluye la implementación de una librería de Python con _bindings_ para usar la librería de limpieza de comentarios.],
  [`embeddings/`], [Contiene _pickles_ con los _embeddings_ generados para el entrenamiento y pruebas.],
  [`notebooks/`], [Contiene todos los _notebooks_ empleados para limpieza, experimentación, y respaldo de información mencionada en el resto del documento.],
  [`reporte/`], [Contiene el código de Typst #TODO("Mencionar Typst") para generar el PDF del reporte final.],
  [`resources/`], [Contiene recursos extras empleados por streamlit #TODO("Verificar si vale la pena moverlo a streamlit")],
  [`scripts/`], [Contiene _scripts_ empleados para la limpieza de los datos de forma anticipada (ver la #TODO("Mencionar seccion de limpieza anticipada")).],
  [`streamlit/`], [Incluye la implementación de la página WEB mostrada en la presentación del proyecto realizada con Streamlit.],
)

= Dataset

== Estructura del Dataset

El dataset obtenido de Kaggle @dataset contiene 86,227 archivos de código dentro de un directorio con 77 lenguajes de programación y un CSV que describe la ubicación, tipo de lenguaje e información extra como tamaño del archivo y líneas de código.

```py
.
├── sources.json    # Contiene las fuentes donde se obtuvieron los archivos.
├── dataset.csv     # Contiene la información de todos los archivos.
└── dataset/        # Un folder con carpetas para cada lenguaje de programación.
	├── AppleScript/  
	├── AsciiDoc/     # Cada carpeta contiene archivos con código correspondiente 
	├── Assembly/     # ... al lenguaje de programación de la carpeta.
	├── ...
	├── XSLT/
	├── Yacc/
	└── YAML/
```

== Campos de `dataset.csv`

En la siguiente tabla se listan los campos que contiene el archivo `dataset.csv`, se incluyen comentarios preliminares sobre la importancia del campo y consideraciones para el resto del escrito.

#table(
  columns: (auto, 1fr),
  stroke: 0pt,
  [*Campo*], [*Descripción*],
  [`id`], [Un identificador único por entrada. No aporta información relevante y por eso lo eliminamos del _dataframe_ en la sección de limpieza #TODO("Agregar referencia").],
  [`file_path`], [La ruta en el directorio `dataset` donde está ubicado el archivo. La ruta en sí no nos es de utilidad, así que se usa para leer los contenidos y después se elimina en el preprocesamiento y limpieza (ver la #TODO("Referencia a eliminación de cosas extra"))],
  [`file_size`], [El tamaño del archivo en bytes. No aporta a la información relevante y por eso lo eliminamos del _dataframe_ en la sección de limpieza #TODO("Agregar referencia").],
  [`line_count`], [El número de líneas de código que contiene el archivo. El número, junto con el tamaño del archivo se vuelven irrelevantes al limpiar los archivos de código en la sección de limpieza #TODO("Agregar referencia")],
  [`extension`], [La extensión del archivo que contiene el código. Como nos basaremos enteramente en el corpus del documento para la predicción, la extensión es irrelevante y la eliminamos en la fase de limpieza de los datos #TODO("Agregar referencia").],
  [`language`], [La etiqueta que indica el lenguaje de programación que se usa en el archivo.],
)

== Preprocesamiento

=== Limpieza

Existen dos estrategias de limpieza utilizadas a lo largo del programa. Una limpieza anticipada de todos los archivos de código, que permite tener código fuente limpio desde el inicio y no tener que repetir el procedimiento en cada modelo (p. ej. en cada notebook) y la funcionalidad necesaria para limpiar entrada de usuario por demanda.

Ambas estrategias realizan las mismas operaciones en tiempos distintos, y con herramientas distintas:
+ Eliminar los comentarios (ver la @eliminar_comentarios para la justificación)
+ Eliminar saltos de línea 

==== Limpieza anticipada

La idea de la limpieza anticipada es procesar el código contenido en los 86 mil archivos de código una sola vez, así evitamos tener que realizar el procedimiento repetidas veces para los distintos ejercicios y experimentos con la base de información durante el proyecto.

La limpieza anticipada se realiza aprovechando ejecutables existentes para la línea de comandos que permiten realizar operaciones individuales sobre el conjunto de archivos.

==== Limpieza por demanda

El objetivo de la limpieza por demanda es de proveer un mecanismo para realizar el mismo proceso de limpieza que se llevó a cabo en la limpieza anticipada para que se pueda emplear en nuevos datos, como es la entrada del usuario. Para este propósito se definen funciones en Python que realizan el mismo procedimiento por medio de librerías con funcionalidad análoga a los ejecutables empleados (p. ej. usar `re` para realizar la limpieza que hace `ruplacer`) o implementando librerías que permitan reusar la implementación de los ejecutables desde Python (p. ej. Python bindings para `cleaner-lib`).


==== Eliminación de comentarios <eliminar_comentarios>




== Embeddings


#show bibliography: set heading(numbering: "1")
#bibliography("bib.yml")

