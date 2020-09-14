# -*- coding: utf-8 -*-
"""
@author: Juan Felipe Ladino
"""

###############################################################################
#
#Procesar missing values de lugar - 2
#
#Las funciones siguientes permiten obtener los lugares faltantes para Batch 3.
#No permiten obtener la totalidad, sin embargo los faltantes pueden
#revisarse de manera manual
#
###############################################################################

import os
import nltk
import unidecode
import pickle

os.chdir("C:\\Users\\juanf\\Desktop\\UR 2018 - 2\\MCPP\\Proyecto Final")
    
def clean(depto):
    '''
    Cambiar forma de nombre de departamentos
    '''
    for i in range(len(depto)):
        if depto[i] == "bogota d.c.":
            depto[i] = "bogota"
        elif depto[i] == "archipielago de san andres, providencia y santa catalina":
            depto[i] = "andres"
        elif depto[i] == "valle del cauca":
            depto[i] = "valle"
        elif depto[i] == "la guajira":
            depto[i] = "guajira"
    return depto

    
def tokenize3(list_places):
    '''
    Convierte en lista de tokens
    columna de lugares de dataframe
    '''
    for i in range(len(list_places)):
        list_places[i] = nltk.word_tokenize(list_places[i])
    return list_places

def getting_missing_depts3(list_places, list_deptos, empty_depto_list):
        for i in range(len(list_places)):
            for w in range(len(list_places[i])):
                for depto in list_deptos:
                    if depto == list_places[i][w]:
                        empty_depto_list[i] = list_places[i][w]
        return empty_depto_list

def not_matched3(miss_sp, empty_depto):
    '''
    De los municipios que no se juntaron
    establecemos por qué valores equivalen
    '''
    for i in range(len(miss_sp)):
        for w in range(len(miss_sp[i])):
            if miss_sp[i][w] == "tolemaida":
                empty_depto[i] = "tolima"
            elif miss_sp[i][w] == "santa":
                empty_depto[i] = "magdalena"
            elif miss_sp[i][w] == "tumaco":
                empty_depto[i] = "narino"
            elif miss_sp[i][w] == "mompox":
                empty_depto[i] = "bolivar"
            elif miss_sp[i][w] == "perdida":
                empty_depto[i] = "magdalena"
            elif miss_sp[i][w] == "chiribiquete":
                empty_depto[i] = "guaviare"
            elif miss_sp[i][w] == "codazzi":
                empty_depto[i] = "cesar"
            elif miss_sp[i][w] == "cristales":
                empty_depto[i] = "meta"
            elif miss_sp[i][w] == "malaga":
                empty_depto[i] = "valle"
            elif miss_sp[i][w] == "espinal":
                empty_depto[i] = "tolima"
            elif miss_sp[i][w] == "peregrino":
                empty_depto[i] = "caldas"
            elif miss_sp[i][w] == "nabusimake":
                empty_depto[i] = "cesar"
            elif miss_sp[i][w] == "chibolo":
                empty_depto[i] = "magdalena"
            elif miss_sp[i][w] == "maria":
                empty_depto[i] = "sucre"
            elif miss_sp[i][w] == "hormiga":
                empty_depto[i] = "putumayo"
            elif miss_sp[i][w] == "barranquill":
                empty_depto[i] = "atlantico"
            elif miss_sp[i][w] == "rioblanco":
                empty_depto[i] = "tolima"
    return empty_depto

def reverse_clean(depto):
    '''
    Devuelve nombre de departamento a versión original
    (Menos bogota)
    '''
    for i in range(len(depto)):
        if depto[i] == "andres":
            depto[i] = "archipielago de san andres, providencia y santa catalina"
        elif depto[i] == "valle":
            depto[i] = "valle del cauca"
        elif depto[i] == "guajira":
            depto[i] = "la guajira"
        elif depto[i] == "bogota":
            depto[i] = "bogota d.c."
    return depto

def missing_places3(df, depto_list):
    '''
    Procesa lugares faltantes para el dataframe
    '''
    empty_depto = list(df.department)
    miss_sp = list(df.ubicacion)
    miss_sp = [unidecode.unidecode(x) for x in miss_sp]
    miss_sp = [x.lower() for x in miss_sp]
    miss_sp = [x.strip() for x in miss_sp]
    miss_sp = tokenize3(miss_sp)
    empty_depto = getting_missing_depts3(miss_sp, depto_list, empty_depto)
    empty_depto = not_matched3(miss_sp, empty_depto)
    empty_depto = reverse_clean(empty_depto)
    df["department"] = empty_depto
    return df 

#Tratamiento de missings restantes 
with open("missing.pkl", "rb") as f:  
    missing_2015_2018, missing_2010_2014, missing_add = pickle.load(f) 

with open("depto_muni.pkl", "rb") as f:  
    depto_muni = pickle.load(f)     

#Departamentos para definicion de lugares
depto = list(depto_muni["DEPARTAMENTO"].unique())
depto = clean(depto)

###Batch 3

missing_2015_2018 = missing_places3(missing_2015_2018, depto)

#Juntar con dataset de speeches

with open("speeches.pkl", "rb") as f:  
    speeches = pickle.load(f)

speeches = speeches.append(missing_2015_2018, sort = False)

with open("speeches.pkl", "wb") as f:
    pickle.dump(speeches, f)
    
'''
#Guardar bases usadas para missings (por si acaso)

with open("missings_b3.pkl", "wb") as f:
    pickle.dump(missing_2015_2018, f)
'''



