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

= Introduction

== Objective

== Methodology


= Entrega

All the code, and its results are hosted on GitHub, this includes embeddings, images, models and test/research Jupyter Notebooks and Python scripts.

The repository with the source code can be founda at the URL:

#text(font: "JetBrainsMono NFM", size: 9pt, weight: 900, [#h(1cm) https://github.com/AOx0/proyecto-pln])

The file structure the repository has is:

#tablex(
  columns: (2.6cm, 1fr),
  map-cells: it => {
    if it.x == 0 {
      it.align = right
    }
    it
  },
  stroke: gray + 0pt,
  [*Folder*], [*Description*],
  [`cleaner-lib/`], [Includes a parser implementation with arbitrary _lookahead_ @lookahead that can identify multi and single line comment blocks, this is useful to give the comments in the source code a special treatment/processing],
  [`cleaner-cli/`], [Implementation of a basic CLI tool to clean all comments from the dataset ahead-of-time (see #TODO("Agregar sección de limpieza anticipada"))],
  [`cleaner-py/`], [Python binds for the `cleaner-lib` implementation, allowing us to clean user-input from the Python runtime],
  [`embeddings/`], [Folder with all _pickle_ files with embeddings used to train models],
  [`notebooks/`], [Folder with all Jupyter Notebooks for model training, embedding generation and research],
  [`reporte/`], [The Typst #TODO("Mencionar Typst") source code for the project's report (this document)],
  [`resources/`], [Contains _streamlit_ assests like charts and images #TODO("Verificar si vale la pena moverlo a streamlit")],
  [`scripts/`], [Various scripts for embedding generation, data cleanup and alike. (ver la #TODO("Mencionar seccion de limpieza anticipada"))],
  [`streamlit/`], [Source code for the streamlit WEB page displayed at the project's presentation],
)

= Dataset

== The dataset's structure

The dataset from Kaggle @dataset contains 86,227 source code files inside a directory with 77 programming languages and a CSV file that describes location, programming language and metadata like number of lines of code, or file size.

```py
.
├── sources.json    # Contains the sources with a JSON format where source code was gathered
├── dataset.csv     # Contains information for all source code files in a CSV format
└── dataset/        # Top-folder with subdirectories for each programming language
	├── AppleScript/  
	├── AsciiDoc/     # Each directory contains source code that corresponds to the name 
	├── Assembly/     # ... of the folder.
	├── ...
	├── XSLT/
	├── Yacc/
	└── YAML/
```

== `dataset.csv` fields

The following table contains the fields of the CSV file `dataset.csv`, each field has a description and prelimnary comments about its usefulness and future considerations.

#table(
  columns: (auto, 1fr),
  stroke: 0pt,
  [*Field*], [*Description*],
  [`id`], [A unique identifier per entry, this information does not provide any value to the training process, hence we delete it in the cleanup phase @cleanup],
  [`file_path`], [The path where the source code can be found for the CSV entry, during the preprocessing phase we read the contents from the path and eliminate the path since itself does not provide value to the training of the models @cleanup],
  [`file_size`], [The source file size in bytes. The size of the file does not matter but the contents, hence we delete this information on the cleanup phase @cleanup],
  [`line_count`], [The number of lines of source code the file contains. During cleanup @cleanup we modify the number of lines, this field becomes irrelevant],
  [`extension`], [The file extension the path has, this is redundant since the `language` field can be used as a label for the language type. We delete this field in the cleanup phase @cleanup],
  [`language`], [The name of the programming language the entry refers to, this is the field we use as `label` for training],
)

== Preprocessing

=== Cleanup <cleanup>

There are two times when the source code is cleaned up, one ahead-of-time to clean all training source code files once before training and then each time we have new user input to classify. The same process is applied to the two cleanup stages #TODO("Stages??").

- Clean all multi-line and single-line comments from the source code.
- Eliminate unnecessary spaces and tabulations.

==== #TODO("Title?")

The main idea to pre-process all files once saves us from repeating the process for each trained model for the project, and skip to the embedding generation strategy, allowing us to iterate much faster #TODO("Jusitufy much faster") when doing experiments.

The once ahead-of-time cleanup uses a CLI tool that has the capacity to look for multi/single line comments and eliminate them from the source code with no pre-defined lookahead.

==== On-demmand cleanup #TODO("Title??")

We implement Python functions to perform the same cleanup stages the ahead-of-time does #TODO("Reference ahead-of-time"). This allows us to clean user input consistently with the pre-processing stage cleanup.

== Embeddings

=== BoW

=== TF-IDF

=== CodeBERT

=== spaCy

== Models

=== SVM



=== FNN

=== RNN

#show bibliography: set heading(numbering: "1")
#bibliography("bib.yml")

