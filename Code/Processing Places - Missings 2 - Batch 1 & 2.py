# -*- coding: utf-8 -*-
"""
@author: Juan Felipe Ladino
"""
###############################################################################
#
#Procesar missing values de lugar - 2
#
#Las funciones siguientes permiten obtener los lugares faltantes para Batch 1
#y Batch 2. No permiten obtener la totalidad, sin embargo los faltantes pueden
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
      
def first_words(list_speeches):
    '''
    Permite tomar los primeros caracteres
    del discurso
    '''
    for i in range(len(list_speeches)):
        list_speeches[i] = list_speeches[i][0:300]
    return list_speeches

def tokenize(list_speeches):
    '''
    Convierte en lista de tokens
    lista de discursos
    '''
    for i in range(len(list_speeches)):
        list_speeches[i] = nltk.word_tokenize(list_speeches[i])
    return list_speeches

def getting_missing_depts(list_speeches, list_deptos, empty_depto_list):
        for i in range(len(list_speeches)):
            for w in range(len(list_speeches[i])):
                for depto in list_deptos:
                    if depto == list_speeches[i][w]:
                        empty_depto_list[i] = list_speeches[i][w]
        return empty_depto_list

def not_matched(miss_sp, empty_depto):
    '''
    De los municipios que no se juntaron
    establecemos por qué valores equivalen
    '''
    for i in range(len(miss_sp)):
        for w in range(len(miss_sp[i])):
            if miss_sp[i][w] == "tolemaida":
                empty_depto[i] = "tolima"
            elif miss_sp[i][w] == "boqueron":
                empty_depto[i] = "tolima"
            elif miss_sp[i][w] == "cartagena":
                empty_depto[i] = "bolivar"
            elif miss_sp[i][w] == "buga":
                empty_depto[i] = "valle"
            elif miss_sp[i][w] == "cali":
                empty_depto[i] = "valle"
            elif miss_sp[i][w] == "esquinas":
                empty_depto[i] = "caqueta"
            elif miss_sp[i][w] == "tumaco":
                empty_depto[i] = "narino"
            elif miss_sp[i][w] == "barranquilla":
                empty_depto[i] = "atlantico"
            elif miss_sp[i][w] == "palanquero":
                empty_depto[i] = "caldas"
            elif miss_sp[i][w] == "catam":
                empty_depto[i] = "bogota"
            elif miss_sp[i][w] == "buenaventura":
                empty_depto[i] = "valle"
            elif miss_sp[i][w] == "malaga":
                empty_depto[i] = "valle"
            elif miss_sp[i][w] == "mompox":
                empty_depto[i] = "bolivar"
            elif miss_sp[i][w] == "neiva":
                empty_depto[i] = "huila"
            elif miss_sp[i][w] == "villavicencio":
                empty_depto[i] = "meta"
            elif miss_sp[i][w] == "armero":
                empty_depto[i] = "tolima"
            elif miss_sp[i][w] == "uribia":
                empty_depto[i] = "guajira"
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

def missing_places(df, depto_list):
    '''
    Procesa lugares faltantes para el dataframe
    '''
    empty_depto = list(df.department)
    miss_sp = list(df.discurso)
    miss_sp = first_words(miss_sp)
    miss_sp = [unidecode.unidecode(x) for x in miss_sp]
    miss_sp = [x.lower() for x in miss_sp]
    miss_sp = [x.strip() for x in miss_sp]
    miss_sp = tokenize(miss_sp)
    empty_depto = getting_missing_depts(miss_sp, depto_list, empty_depto)
    empty_depto = not_matched(miss_sp, empty_depto)
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

###Batch 1

missing_2010_2014 = missing_places(missing_2010_2014, depto)

###Batch 2

missing_add = missing_places(missing_add, depto)

#Juntar con dataset de speeches

with open("speeches.pkl", "rb") as f:  
    speeches = pickle.load(f)

speeches = speeches.append(missing_2010_2014, sort = False)
speeches = speeches.append(missing_add, sort = False)

#Este método no asigna de manera correcta a puerto bolivar (la guajira) y a isla bolivar (san andres)  

speeches.department[speeches.ubicacion == "puerto bolivar"] = "la guajira"
speeches.department[speeches.ubicacion == "isla bolivar"] = "archipielago de san andres, providencia y santa catalina"


with open("speeches.pkl", "wb") as f:
    pickle.dump(speeches, f)
    
'''
#Guardar bases usadas para missings (por si acaso)

with open("missings_b1_b2.pkl", "wb") as f:
    pickle.dump([missing_2010_2014, missing_add], f)
'''

