# -*- coding: utf-8 -*-
"""
@author: Juan Felipe Ladino
"""
import os
import pickle
import pandas as pd
import numpy as np
import datetime
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import unidecode
import string
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [18.0, 8.0]


os.chdir("C:\\Users\\juanf\\Desktop\\UR 2018 - 2\\MCPP\\Proyecto Final")

with open("speeches.pkl", "rb") as f:  
    speeches = pickle.load(f)

##Número de discursos

len(speeches)

##Número de días en los que por lo menos un discurso fue dado

len(speeches.fecha.unique())

##Máximo número de discursos en un día

speeches["fecha"].value_counts()

list(speeches[speeches["fecha"] == "2013-11-21"]["titulo"]) #se repite uno

##Histograma: Número de discursos por día

by_date = speeches["fecha"].value_counts()
plt.style.use('ggplot')
by_date.plot.hist(bins=range(1,9), align='left', color = "red")
plt.xticks(range(1,7))
plt.xlim(0.5, 6.5)
plt.title("Número de Discursos por día ", fontdict={'fontsize': 20})
plt.ylabel("Frecuencia", fontdict={'fontsize': 14})
plt.xlabel("Discursos por día", fontdict={'fontsize': 14});
plt.savefig("hist_daily.png")

##Histograma por día de la semana

# Obtener día de la semana

speeches["Dia de la semana"] = speeches["fecha"].dt.dayofweek

# Diccionario para definir día de la semana

days = {0:'Monday',1:'Tuesday',2:'Wedsnesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}

# For each value in 'Weekday', apply function that labels with corresponding name of the weekday

speeches["Dia de la semana"] = speeches['Dia de la semana'].apply(lambda x: days[x])

#Categorizar

speeches["Dia de la semana"] = pd.Categorical(speeches["Dia de la semana"], \
                   ['Monday','Tuesday','Wedsnesday','Thursday',\
                    'Friday','Saturday','Sunday'])

#Conteo por día de la semana

by_weekday = speeches["Dia de la semana"].value_counts().sortlevel()
by_weekday


plt.style.use("ggplot")
by_weekday.plot.bar(color = "red")
plt.title("Número de discursos por día de la semana", fontdict={'fontsize': 20})
plt.ylabel("Número de discursos", fontdict={'fontsize': 14})
plt.xlabel("Día de la semana", fontdict={'fontsize': 14});
plt.savefig("bar_weekday.png")

##Histograma por mes

speeches["mes"] = pd.to_numeric(speeches["mes"])

by_month = speeches["mes"].value_counts().sort_index()
by_month

plt.style.use("ggplot")
by_month.plot.bar(color = "red")
plt.title("Número de discursos por mes", fontdict={'fontsize': 20})
plt.ylabel("Número de discursos", fontdict={'fontsize': 14})
plt.xlabel("Mes", fontdict={'fontsize': 14})
labels = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto"\
          , "Septiembre", "Octubre", "Noviembre", "Diciembre"]
plt.xticks(range(12), labels, rotation = "horizontal");
plt.savefig("bar_month.png")

##Histograma por año

by_year = speeches["año"].value_counts().sort_index()
by_year

plt.style.use("ggplot")
by_year.plot.bar(color = "red")
plt.title("Número de discursos por año", fontdict={'fontsize': 20})
plt.ylabel("Número de discursos", fontdict={'fontsize': 14})
plt.xlabel("Año", fontdict={'fontsize': 14})
plt.xticks(range(9), rotation = "horizontal");
plt.savefig("bar_year.png")

##Evolución discursos

by_year_month = speeches.groupby(by = [speeches["año"], speeches["mes"]])

by_month = by_year_month["mes"].agg("count")

months = list(speeches["mes"].unique())
year = list(speeches["año"].unique())

def month_labels(list_year, list_month):
    '''
    Combinación de meses y años
    '''
    labels = []
    for year in list_year:
        for month in list_month:
            x = [year + "/" + str(month)]
            labels += x
    return labels

labels = month_labels(year, months)
labels = [datetime.datetime.strptime(x, "%Y/%m") for x in labels]
labels = [datetime.datetime.strftime(x, "%Y/%m") for x in labels]
labels.sort()
labels = labels[7:104]

by_month.plot()
plt.title("Número de discursos por mes (Agosto-2010 a Julio-2018)", fontdict={'fontsize': 20,\
                                                                                'verticalalignment': 'bottom'})
plt.ylabel("Número de discursos", fontdict={'fontsize': 14})
plt.xlabel("Mes", fontdict={'fontsize': 14})
labels = labels
plt.xticks(range(len(labels)), labels, rotation='vertical')
plt.axvline(x=39, linewidth=1, color='b')
plt.axvline(x= 25, linewidth=1, color='g')
plt.axvline(x= 73, linewidth=1, color='g');
plt.savefig("line_month.png")

##Uso de las palabras "paz", "equidad", "educacion"

speeches["FreqDist"] = speeches["nltk discurso"].apply(nltk.FreqDist)

def count_words(word):
    '''
    Toma el número de veces que se repite la palabra por discurso
    '''
    x = [speeches["FreqDist"][i][word] for i in range(len(speeches["FreqDist"]))]
    y = pd.DataFrame({word: x})
    return y
    
speeches["paz"] = count_words("paz")
speeches["equidad"] = count_words("equidad")
speeches["educacion"] = count_words("educacion")

paz_by_month = by_year_month["paz"].agg('sum').sort_index()
educ_by_month = by_year_month["educacion"].agg('sum')
equi_by_month = by_year_month["equidad"].agg('sum')

paz_by_month.plot()
equi_by_month.plot()
educ_by_month.plot()
plt.title("Uso de palabras Paz, Equidad y Educación (Agosto-2010 a Julio-2018)", fontdict={'fontsize': 20,\
                                                                                'verticalalignment': 'bottom'})
plt.ylabel("Frecuencia palabra", fontdict={'fontsize': 14})
plt.xlabel("Mes", fontdict={'fontsize': 14})
labels = labels
plt.xticks(range(len(labels)), labels, rotation='vertical')
plt.axvline(x=48, linewidth=2, color='g')
plt.axvline(x= 25, linewidth=2, color='g')
plt.axvline(x= 73, linewidth=2, color='g')
plt.legend(["paz", "equidad", "educacion"], loc = "upper left");
plt.savefig("paz_equid_educ.png")

##Uso de palabras pobreza, terrorismo, infraestructura

speeches["terrorismo"] = count_words("terrorismo")
speeches["pobreza"] = count_words("pobreza")
speeches["infraestructura"] = count_words("infraestructura")

terrorismo_by_month = by_year_month["terrorismo"].agg('sum').sort_index()
pobreza_by_month = by_year_month["pobreza"].agg('sum')
infraes_by_month = by_year_month["infraestructura"].agg('sum')

terrorismo_by_month.plot()
pobreza_by_month.plot()
infraes_by_month.plot()
plt.title("Uso de palabras Terrorismo, Pobreza e Infraestructura (Agosto-2010 a Julio-2018)", fontdict={'fontsize': 20,\
                                                                                'verticalalignment': 'bottom'})
plt.ylabel("Frecuencia palabra", fontdict={'fontsize': 14})
plt.xlabel("Mes", fontdict={'fontsize': 14})
labels = labels
plt.xticks(range(len(labels)), labels, rotation='vertical')
plt.axvline(x=48, linewidth=2, color='g')
plt.axvline(x= 25, linewidth=2, color='g')
plt.axvline(x= 73, linewidth=2, color='g')
plt.legend(["terrorismo", "pobreza", "infraestructura"], loc = "upper left");
plt.savefig("terr_pob_inf.png")


##Uso de palabras petroleo, comercio, impuestos

speeches["petroleo"] = count_words("petroleo")
speeches["comercio"] = count_words("comercio")
speeches["impuestos"] = count_words("impuestos")

pet_by_month = by_year_month["petroleo"].agg('sum').sort_index()
com_by_month = by_year_month["comercio"].agg('sum')
imp_by_month = by_year_month["impuestos"].agg('sum')

pet_by_month.plot()
com_by_month.plot()
infraes_by_month.plot()
plt.title("Uso de palabras Petroleo, Comercio e Impuestos (Agosto-2010 a Julio-2018)", fontdict={'fontsize': 20,\
                                                                                'verticalalignment': 'bottom'})
plt.ylabel("Frecuencia palabra", fontdict={'fontsize': 14})
plt.xlabel("Mes", fontdict={'fontsize': 14})
labels = labels
plt.xticks(range(len(labels)), labels, rotation='vertical')
plt.axvline(x=48, linewidth=2, color='g')
plt.axvline(x= 25, linewidth=2, color='g')
plt.axvline(x= 73, linewidth=2, color='g')
plt.legend(["petroleo", "comercio", "impuestos"], loc = "upper left");
plt.savefig("pet_com_imp.png")

##Uso de palabras Paz, Pobreza, Comercio

paz_by_month.plot()
com_by_month.plot()
pobreza_by_month.plot()
plt.title("Uso de palabras Paz, Comercio y Pobreza (Agosto-2010 a Julio-2018)", fontdict={'fontsize': 20,\
                                                                                'verticalalignment': 'bottom'})
plt.ylabel("Frecuencia palabra", fontdict={'fontsize': 14})
plt.xlabel("Mes", fontdict={'fontsize': 14})
labels = labels
plt.xticks(range(len(labels)), labels, rotation='vertical')
plt.axvline(x=48, linewidth=2, color='g')
plt.axvline(x= 25, linewidth=2, color='g')
plt.axvline(x= 73, linewidth=2, color='g')
plt.legend(["paz", "comercio", "pobreza"], loc = "upper left");
plt.savefig("paz_com_pob.png")

##Convertir discursos en un solo texto 

all_speeches = speeches["no tildes"].str.cat(sep=',')
len(all_speeches)

#El texto ya está en minúsculas y sin tildes, de manera que falta quitar puntuación adicional

punctuation = string.punctuation + '–¡¿”“•\r´'
punctuation

def no_punct(string):
    transtable = string.maketrans('', '', punctuation)
    return string.translate(transtable)

all_speeches = no_punct(all_speeches)

#Tokenize

all_tokens = word_tokenize(all_speeches)

#Eliminar stopwords

stopwords_esp = stopwords.words('spanish')
stopwords_esp = [unidecode.unidecode(x) for x in stopwords_esp]

def no_stopwords(tokens):
    return [w for w in tokens if w not in stopwords_esp]

all_tokens = no_stopwords(all_tokens)
len(all_tokens)

#Distribución de frecuencia de los tokens

nltk.FreqDist(all_tokens).most_common()
nltk.FreqDist(all_tokens).most_common()[0:10]

#Collocations

all_speeches_text = nltk.Text(all_tokens)
all_speeches_text.collocations(num = 30)

all_speeches_text.dispersion_plot(['uribe', 'lleras', 'angelino', 'chavez', 'maduro', 'correa',\
                                   'paz', 'seguridad', 'oposicion', 'farc', 'paramilitares', 'terroristas'])
    
all_speeches_text.dispersion_plot(['petroleo', 'pib', 'fiscal', 'inflacion', 'tributaria', 'devaluacion',\
                                  'empleo', 'paro', 'tlc', 'mar', 'elecciones'])

all_speeches_text.dispersion_plot(['paz', 'equidad', 'educacion', 'desempleo', 'seguridad', 'economia',\
                                  'crisis', 'farc', 'eln', 'bacrim'])
plt.savefig("displot3.png");
