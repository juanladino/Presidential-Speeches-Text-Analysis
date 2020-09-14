# -*- coding: utf-8 -*-
"""
@author: Juan Felipe Ladino
"""
###############################################################################
#
#Procesar lugares para análisis geográfico
#
###############################################################################

import os
import pandas as pd
import unidecode
import pickle


os.chdir("C:\\Users\\juanf\\Desktop\\UR 2018 - 2\\MCPP\\Proyecto Final")

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

def add_cleaning(df, column_name):
    '''
    Convierte bogota d.c. en bogota y casa de nariño en bogota.
    Se encuentra que esto se repite en la base
    '''
    column = df[column_name]
    column = pd.Series(column).str.replace("bogota d.c.", "bogota")
    column = pd.Series(column).str.replace("casa de narino", "bogota")
    df[column_name] = column
    return df

def split_nan(df, column_name):
    '''
    Separa los datasets entre los que tienen asignado departamento
    y los que no 
    '''
    df_1 = df[df[column_name].notnull()]
    df_2 = df[~df[column_name].notnull()]
    return df_1, df_2


#Data frames para cada Batch
    
with open("data_frame_2015_2018.pkl", "rb") as f:  
    data_frame_2015_2018 = pickle.load(f)
with open("data_frame_2010_2014.pkl", "rb") as f:  
    data_frame_2010_2014 = pickle.load(f)
with open("data_frame_add.pkl", "rb") as f:
    data_frame_add = pickle.load(f)


#Base para limpiar lugares de discursos
    
depto_muni = pd.read_csv("depto_muni.csv")

#Limpieza discursos

data_frame_2015_2018 = cleaning_places(data_frame_2015_2018, "ubicacion")
data_frame_2010_2014 = cleaning_places(data_frame_2010_2014, "ubicacion")
data_frame_add = cleaning_places(data_frame_add, "ubicacion")    
    
#Limpieza base de comparación

depto_muni = cleaning_places(depto_muni, "DEPARTAMENTO")
depto_muni = cleaning_places(depto_muni, "MUNICIPIO")

data_frame_2015_2018 = add_cleaning(data_frame_2015_2018, "ubicacion")
data_frame_2010_2014 = add_cleaning(data_frame_2010_2014, "ubicacion")
data_frame_add = add_cleaning(data_frame_add, "ubicacion")    
depto_muni = add_cleaning(depto_muni, "MUNICIPIO")

#Merge por municipio para localizar por departamento

depto_muni_1 = pd.DataFrame({"ubicacion":depto_muni.MUNICIPIO, 
                           "department":depto_muni.DEPARTAMENTO})

data_frame_2015_2018 = data_frame_2015_2018.merge(depto_muni_1.drop_duplicates(subset = ["ubicacion"]), 
                                                  on = "ubicacion", how = "left")
data_frame_2010_2014 = data_frame_2010_2014.merge(depto_muni_1.drop_duplicates(subset = ["ubicacion"]), 
                                                  on = "ubicacion", how = "left")
data_frame_add = data_frame_add.merge(depto_muni_1.drop_duplicates(subset = ["ubicacion"]), 
                                                  on = "ubicacion", how = "left")

#La base data_frame_add contiene mayor información para diciembre del 2015
#Eliminamos de data_frame_2015_2018 las observaciones para 2015 para evitar duplicidad

data_frame_2015_2018 = data_frame_2015_2018[~(data_frame_2015_2018["año"] == "2015")]

#Dividir los datasets para evaluar los missing para cada batch

data_frame_2015_2018, missing_2015_2018 = split_nan(data_frame_2015_2018, "department")
data_frame_2010_2014, missing_2010_2014 = split_nan(data_frame_2010_2014, "department")
data_frame_add, missing_add = split_nan(data_frame_add, "department")

#Append datasets con valores completos

speeches = data_frame_2015_2018.append(data_frame_2010_2014)
speeches = speeches.append(data_frame_add)

with open("depto_muni.pkl", "wb") as f:
    pickle.dump(depto_muni, f)
    
with open("missing.pkl", "wb") as f:
    pickle.dump([missing_2015_2018, missing_2010_2014, missing_add], f)

with open("speeches.pkl", "wb") as f:
    pickle.dump(speeches, f)
