# -*- coding: utf-8 -*-
"""
@author: Juan Felipe Ladino
"""

import os
import pickle
import pandas as pd
import numpy as np
import nltk
import unidecode
from collections import Counter
from itertools import permutations
import networkx as nx
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [18.0, 8.0]



os.chdir("C:\\Users\\juanf\\Desktop\\UR 2018 - 2\\MCPP\\Proyecto Final")

with open("speeches.pkl", "rb") as f:  
    speeches = pickle.load(f)


#Nuevo data frame

speeches1 = speeches.loc[:,["no tildes", "tokens", "no stopwords", "nltk_discurso"]]

#Definimos stopwords y otras palabras para quitar de los textos
stopwords_esp = nltk.corpus.stopwords.words('spanish')
stopwords_esp = [unidecode.unidecode(x) for x in stopwords_esp]

stopwords_esp = stopwords_esp + ["aqui", "vamos", "va", "hoy", "ustedes", "anos", "ano",
                                 "importante", "hacer", "ser", "gran", "hace", "mil",
                                 "ahi", "bien", "muchas", "vez", "sido", "cada", "van",
                                 "mejor", "forma", "usted", "dos", "asi", "tan", "toda",
                                 "entonces", "hecho", "--", "dia", "sino", "ver", "'",
                                 "todas", "pues", "solo", "mismo", "decia", "unas", "aun",
                                 "voy", "...", "casa", "carrera", "8", "no726",
                                 "25", "60", "ii", "11","<", ">", "creo" ] 
def no_stopwords(tokens):
    return [w for w in tokens if w not in stopwords_esp]

speeches1["no stop2"] = speeches1["no stopwords"].apply(no_stopwords) 

#Funciones para obtener keywords

def get_keywords(tokens):
    '''
    Obtiene las cinco palabras más repetidas del texto
    '''
    return Counter(tokens).most_common(3)

def set_keywords(tokens):
    '''
    Junta a un data frame las palabras más repetidas de cada texto
    '''
    key = get_keywords(tokens)
    x = []
    for pair in key:
        x += [pair[0]]
    return x

speeches1["keywords"] = speeches1["no stop2"].apply(set_keywords)

#Separamos lista de keywords y creamos función para emparejar


keywords = list(speeches1["keywords"])


def permut(keyword_list):
    orig_dest = []
    for i in range(len(keyword_list)):
        x = list(permutations(keyword_list[i], 2))
        orig_dest += x
    return orig_dest

orig_dest = list(permut(keywords))

#Separar tupla en dos columnas y crear nuevo dataframe

origin, dest = zip(*orig_dest)

nodes = list(origin + dest)
nodes = pd.DataFrame({"node": nodes})
nodes = nodes["node"].unique()
nodes = pd.DataFrame({"node": nodes})
nodes = nodes.reset_index()
nodes.columns = ["index", "node"]
nodes.to_csv("nodes.csv", sep = ",")


edges = pd.DataFrame({"origin": origin, "destiny": dest})

nodes_list = list(nodes["node"])

def source_target(word):
    for i in range(len(nodes_list)):
        if nodes_list[i] == word:
            x = i
    return x
    
edges["Source"] = edges["origin"].apply(source_target)
edges["Target"] = edges["destiny"].apply(source_target)

edges.to_csv("edges.csv", sep = ",")

##Se analiza en gephi y se importa tabla 

gephi = pd.read_csv("info_nodes.csv")

#degree vs betweness
plt.style.use("ggplot")
plt.scatter(gephi["degree"], gephi["betweenesscentrality"], color = "blue")
plt.title("Relación grado y betweness", fontdict={'fontsize': 20})
plt.ylabel("Betweness", fontdict={'fontsize': 14})
plt.xlabel("Grado", fontdict={'fontsize': 14});
plt.savefig("grade_between.png")


#betweenes vs clustering

plt.style.use("ggplot")
plt.scatter(gephi["clustering"], gephi["betweenesscentrality"], color = "blue")
plt.title("Relación clustering y betweness ", fontdict={'fontsize': 20})
plt.ylabel("Betweness", fontdict={'fontsize': 14})
plt.xlabel("Clustering", fontdict={'fontsize': 14});
plt.savefig("cluster_between.png")

#betweenes vs eigencentrality

plt.style.use("ggplot")
plt.scatter(gephi["eigencentrality"], gephi["betweenesscentrality"], color = "blue")
plt.title("Relación eigen centrality y betweness", fontdict={'fontsize': 20})
plt.ylabel("Betweness", fontdict={'fontsize': 14})
plt.xlabel("Eigen Centrality", fontdict={'fontsize': 14});
plt.savefig("eigen_between.png")

#Histograma mayores

gephi_1 = pd.DataFrame({"nodes": gephi["node"][gephi["betweenesscentrality"] > 4500],
                               "between": gephi["betweenesscentrality"][gephi["betweenesscentrality"] > 4500]})

labels = ["colombia", "gobierno", "pais", "paz", "presidente"]
plt.style.use("ggplot")
gephi_1.plot.bar(color = "red")
plt.title("Palabras mayor betweenes", fontdict={'fontsize': 20})
plt.ylabel("Betweenes", fontdict={'fontsize': 14})
plt.xlabel("Palabra", fontdict={'fontsize': 14})
plt.xticks(range(len(labels)), labels, rotation='horizontal')
plt.savefig("bet.png")

##Realizando redes

G = nx.Graph()

#Adding nodes

G.add_nodes_from(list(nodes["node"]))
G.nodes()

#Adding edges

edges["edges"] = pd.DataFrame({"edges": orig_dest})
G.add_edges_from(list(edges["edges"]))
G.edges()

#Eliminando isolates

G.remove_nodes_from(list(nx.isolates(G)))

words = ["paz", "equidad", "educación", "colombia", "colombianos", "pobreza", 
         "terrorismo", "farc", "eln", "gobierno", "fuerzas", "acuerdos", "solidaridad",
         "corrupcion", "constitucional", "tierra", "tierras", "derechos", "seguridad",
         "democracia", "elecciones", "salud", "infraestructura", "desarrollo", "policia",
         "ejercito", "congreso", "america", "energia", "justicia", "ambiente", "cafe",
         "petroleo", "pasado", "reforma", "ministerio", "fiscalia", "gas", "proyectos",
         "campesinos", "transparencia", "politica", "futbol", "empleo", "crecimiento",
         "ambiental"]

G_sub = nx.subgraph(G, words)


labels = {}
labels["paz"]=r'$paz$'

#Dibujando red

nx.draw(G_sub, pos=nx.random_layout(G), with_labels = True, node_size = 400)
plt.title("Red Palabras");
plt.savefig("simple_path.png") # save as png

