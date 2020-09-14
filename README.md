
# Análisis de Discursos del Ex- Presidente Santos

A través de los discursos que se dan frente a la población pueden mostrarse la forma en la que un gobierno prioriza o toca temas coyunturales de política pública. El presente  proyecto tiene como fin analizar los discursos del ex - presidente de Colombia Juan Manuel Santos, quién fue lider de Estado entre el 2010 y 2018. Durante sus dos periodos (fue reelegido en el 2014) un aspecto fundamental de su agenda de política fue la paz con el grupo al margen de la ley de las FARC. El acuerdo de paz fue anunciado en el 2012 y firmado en el 2016. Durante su presidencia también sucedieron temas como la caida internacional de los precios petroleros o la firma del TLC con Estados Unidos.  Este tipo de temáticas debería verse reflejadas en qué tanto se repiten ciertos conceptos.

Además, el análisis de discurso permite no sólo ver si la agenda de política pública reaccionó a ciertos sucesos, sino que también permite obtener descriptivamente la forma en la que se comportaron ciertos temas de política pública, y la prioridad qeu se les dió en la discursiva presidencial. Por último, es importante revisar qué tan importante pueden llegar a ser ciertas palabras en los discursos del presidente, con el fin de entender qué conceptos fueron los que marcaron su liderazgo como jefe de Estado.

## Instrucciones 

En la carpeta Code se encuentran los códigos usados para procesar y analizar los datos.
La extracción de los discursos requería la extracción de datos de tres sitios web distintos

#### Batch 1. 
Discursos desde agosto del 2010 a agosto del 2014
http://wsp.presidencia.gov.co/Discursos
#### Batch 2.
Discursos desde agosto del 2014 hasta diciembre del 2015
http://wp.presidencia.gov.co/Discursos
#### Batch 3.
Discursos desde septiembre del 2015 hasta agosto del 2018
http://es.presidencia.gov.co/discursos

### Archivos Scrapping

Para la extracción inicial de los datos se usaron los códigos:
- Scrapping Batch 1
-  Scrapping Batch 2
- Scrapping Batch 3
Cada uno de los cuales corresponde a un sitio web (Batch 1, Batch 2, Batch 3 respectivamente). De estas páginas se extrajo información de fecha, título, ubicación y discurso.

### Extracción Ubicación

El conocimiento de la información sobre la ubicación de los archivos era imperfecta, de manera que se proceso de la siguiente manera:

- Primero se proceso de manera general las ubicaciones que habían sido extraidas de manera correcta con el código presente en
    - Prococessing Places

- Luego, para tratar los missing values se utilizaron en orden
    - Processing Places - Missings 1
    - Processing Places - Missings 2 - Batch 1 & 2
    - Processing Places - Missings 2 - Batch 3
    - Processing Places - Missings 3
    
### Limpieza de Datos

Tras la extracción de la ubicación se consolidad la base de datos y se empieza a limpiar el texto de los discursos para su posterior análisis. El archivo correspondiente a la limpieza de la base es
- Cleaning Data

### Análisis de datos

El análisis de hizo en tres formas

1. El análisis inicial corresponde a un análisis temporal, de cómo evolucionó la forma en la que se repetían ciertas palabras, así como ciertos datos adicionales de cómo y cuando se estaban dando estos discursos. El archivo correspondiente a esta sección es
    - Speeches Analysis
    
    
2. La segunda parte correspondió a procesar ciertos datos de palabras a nivel geográfico para luego usar la herramienta ArcGis para visualizar de manera georeferenciada. El archivo correspondiente a esta sección es
    - Speeches Analysis 2
    
    
3. Finalmente, con el fin de entender qué tan importante eran ciertas palabras en la forma en la que se constituyeron los discursos, se realizó un análisis de redes. Se obtuvo información de las 3 principales palabras por discurso, luego a partir de estas se generó una lista de nodos y de aristas. Las aristas fueron construidas de manera que hubiera una conexión entre las palabras principales del discurso (Ej: Si se tiene paz, equidad, educación, las aristas serán todas las posibles permutaciones de estas tres palabras). Estos datos fueron exportados a Gephi, donde se graficó y se extrajo información de medidas de centralidad para los nodos. Esta información fue nuevamente puesta en python para completar el análisis de las medidas
    - Speeches Analysis 3

## Requerimientos

- Tener instalado Python 3.*
- Tener instalado ArcGis para la lectura de las capas (archivos.mxd) de la carpeta Images
- Tener instalado Gephi

##### Paquetes de Python

- pandas
- numpy
- matplotlib
- unideco
- string
- re
- nltk
- permutations (from itertools)
- reduce (from functools)
- BeautifulSoup (from bs4)
- pickle
- os
- networkx
- webdriver (from selenium)
- datetime
- Counter (from collections)
- time

## Adicionales

En la carpeta de Datasets se encuentran las bases de datos usadas para el análisis.
En la carpeta de Images se encuentran las imágenes y capas que resultaron del análisis de los datos.
