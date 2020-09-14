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
from functools import reduce

os.chdir("C:\\Users\\juanf\\Desktop\\UR 2018 - 2\\MCPP\\Proyecto Final")

with open("speeches.pkl", "rb") as f:  
    speeches = pickle.load(f)
    
##Abrir y arreglar base de datos con códigos de departamento
    
depto_muni = pd.read_csv("depto_muni.csv")
 
def cleaning_places(df, column_name):
    '''
    Limpia lugares (quita tildes, convierte a minúscula
    y quita espacios extra)
    '''
    column = df[column_name]
    #Reemplaza letras con tilde por letras sin tilde
    column = [unidecode.unidecode(x) for x in column]
    #Convierte a minúsculas
    column = [x.lower() for x in column]
    #Quita espacios extra al final y al principio del string
    column = [x.strip() for x in column]
    df[column_name] = column
    return df
    
depto_muni = cleaning_places(depto_muni, "DEPARTAMENTO")
x = [1]*1123
depto_muni["x"] = pd.DataFrame({"x": x})

depto_code = depto_muni.groupby(by = [depto_muni["CÓDIGO DANE DEL DEPARTAMENTO"], \
                                      depto_muni["DEPARTAMENTO"]])
##Obtenemos Data Frame con valores únicos de epartamento con su respectivo código DANE
by_dept = depto_code["x"].agg("sum")
by_dept = by_dept.reset_index()

##Arreglamos códigos DANE
by_dept["CÓDIGO DANE DEL DEPARTAMENTO"] = by_dept["CÓDIGO DANE DEL DEPARTAMENTO"].astype(str)

def fix_code(code):
    comp_code = "0"
    if len(code) == 1:
        comp_code += code
    else:
        comp_code = code
    return comp_code

by_dept["CÓDIGO DANE DEL DEPARTAMENTO"] = by_dept["CÓDIGO DANE DEL DEPARTAMENTO"].apply(fix_code)

##Merge con base de discursos

by_dept = pd.DataFrame({"department": by_dept["DEPARTAMENTO"], 
                           "codigo":by_dept["CÓDIGO DANE DEL DEPARTAMENTO"]})
    
speeches_map = speeches.merge(by_dept, on = "department", how = "left")

##Verificar que merge se haya hecho de manera correcta

speeches_map["codigo"].isna().sum()
speeches_map[speeches_map["department"] == "internacional"].count()
speeches_map[speeches_map["department"] == "No identificado"].count()

##Organizar datasets por código para mapas

by_code = speeches_map.groupby(by = speeches_map["codigo"])


speeches_map["FreqDist"] = speeches_map["nltk discurso"].apply(nltk.FreqDist)

def count_words(word):
    '''
    Toma el número de veces que se repite la palabra por discurso
    '''
    x = [speeches_map["FreqDist"][i][word] for i in range(len(speeches["FreqDist"]))]
    y = pd.DataFrame({word: x})
    return y
    
speeches_map["paz"] = count_words("paz")
speeches_map["equidad"] = count_words("equidad")
speeches_map["educacion"] = count_words("educacion")
speeches_map["pobreza"] = count_words("pobreza")
speeches_map["desigualdad"] = count_words("desigualdad")
speeches_map["conflicto"] = count_words("conflicto")


paz = by_code["paz"].agg(sum).reset_index()
equidad = by_code["equidad"].agg(sum).reset_index()
educacion = by_code["educacion"].agg(sum).reset_index()
pobreza = by_code["pobreza"].agg(sum).reset_index()
desigualdad = by_code["desigualdad"].agg(sum).reset_index()
conflicto = by_code["conflicto"].agg(sum).reset_index()

#Unimos data frames y exportamos en formato xls

topics_list = [paz, equidad, educacion, pobreza, desigualdad, conflicto]

maps = reduce(lambda  left,right: pd.merge(left,right,on= "codigo"), topics_list)

maps.to_excel("maps.xls")

##Total discursos

speeches_map["disc"] = pd.DataFrame({"x" :[1]*len(speeches)})

discurso_depto = by_code["disc"].agg(sum)

discurso_depto.to_excel("discurso_depto.xls")

