# -*- coding: utf-8 -*-
"""
@author: Juan Felipe Ladino
"""
import os
import pickle
import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import unidecode
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [18.0, 8.0]
import re
import string


os.chdir("C:\\Users\\juanf\\Desktop\\UR 2018 - 2\\MCPP\\Proyecto Final")

with open("speeches.pkl", "rb") as f:  
    speeches = pickle.load(f)
    
# Limpiar textos de inicio y final de discursos

def clean_speech(text):
    return re.sub('.*?(SIG)|(Presidencia de la República de Colombia).*$|(Casa de Nariño).*$|(Sistema Informativo de Gobierno)|(Horario de atención: .*)', '', text)

speeches["discurso"] = speeches["discurso"].apply(clean_speech)

# Eliminar duplicados

len(speeches)
speeches.drop_duplicates(subset = ("titulo", "fecha"), inplace = True)
speeches.drop_duplicates(subset = ("discurso"), inplace = True)
speeches.drop_duplicates(subset = ("link discurso"), inplace = True)
len(speeches)   

#Ordenar y reindexar

speeches.sort_values("fecha", inplace = True)
speeches.reset_index(inplace = True, drop = True)

#Eliminar puntuacion

string.punctuation
punctuation = string.punctuation + "–¡¿”“•\r"
punctuation

def no_punct(string):
    transtable = string.maketrans('', '', punctuation)
    return string.translate(transtable)

speeches["no puntuacion"] = speeches["discurso"].apply(no_punct)

#Convertir a minúsculas

speeches["no puntuacion"] = speeches["no puntuacion"].apply(str.lower)

#Reemplazar tildes

speeches["no tildes"] = speeches["no puntuacion"].apply(unidecode.unidecode)

#Tokenize

speeches["tokens"] = speeches["no tildes"].apply(word_tokenize)

#Quitar stopwords

stopwords_esp = [unidecode.unidecode(x) for x in stopwords.words("spanish")]
stopwords_esp

def no_stopwords(tokens):
    return [w for w in tokens if w not in stopwords_esp]

speeches["no stopwords"] = speeches["tokens"].apply(no_stopwords)

#Convertir a objeto nltk

speeches["nltk discurso"] = speeches["no stopwords"].apply(nltk.Text)

#Revisar fechas

speeches["dia"].unique()

def fix_day(string):
    if string[0] == "0":
        string = string[1]
    return string

speeches["dia"] = speeches["dia"].apply(fix_day)

speeches["mes"].unique()

def fix_month(string):
    if string[0] == "0":
        string = string[1]
    return string

speeches["mes"] = speeches["mes"].apply(fix_month)

speeches["año"].unique()

#Guardar dataset

with open("speeches.pkl", "wb") as f:
    pickle.dump(speeches, f)