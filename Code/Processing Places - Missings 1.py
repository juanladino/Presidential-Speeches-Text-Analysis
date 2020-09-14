# -*- coding: utf-8 -*-
"""
@author: Juan Felipe Ladino
"""
import os
import pickle

os.chdir("C:\\Users\\juanf\\Desktop\\UR 2018 - 2\\MCPP\\Proyecto Final")

###############################################################################
#
#Procesar missing values de lugar - 1
#
#Para lugares internacionales identificados
#
############################################################################### 

with open("missing.pkl", "rb") as f:  
    missing_2015_2018, missing_2010_2014, missing_add = pickle.load(f)       
            
unique_2015_2018 = list(missing_2015_2018["ubicacion"].unique())
unique_2010_2014 = list(missing_2010_2014["ubicacion"].unique())
unique_add = list(missing_add["ubicacion"].unique())


def add_cleaning_2(df, column_name, column_name_replace):
    '''
    Convierte bogota d.c. en bogota y casa de nariño en bogota.
    Se encuentra que esto se repite en la base
    '''
    internacional = ["nueva york", "brasilia", "kingston", "santiago de chile", "merida", 
                 "mar del plata", "paris","pinalito", "lima", "berlin", "providence", 
                 "washington", "ciudad de guatemala", "saint kitts and nevis",
                 "ciudad de mexico", "seul", "tokio", "londres", "paracas" 
                 "caracas", "ankara", "la habana", "shanghai", "beijing", "singapur",
                 "rio de janeiro", "los cabos", "los cabos mexico", "antofagasta",
                 "ashintukua",  "la haya", "hurdal", "cadiz", "lisboa", "tulcan", 
                 "ciudad del vaticano", "roma","israel", "tel aviv", "oxford", 
                 "puerto ayacucho", "lausana", "new york", "ciudad de panama", "miami", 
                 "tegucigalpa", "oporto", "davos", "punta mita", "estrasburgo",
                 "baru", "budapest", "munster", "viena", "toronto", "lawrence", 
                 "naciones unidas", "quito", "charlottesville", "asuncion", 
                 "san jose de costa rica","guayaquil", "belfast", "nicanor", "islas galapagos",
                 "puerto ordaz", "frutillar", "el salvador", "airlington", 
                 "estocolmo","oslo", "bruselas", "iquitos", "caracas", "puerto vallarta"]
    for i in internacional:
        df.loc[df[column_name] == i, column_name_replace] = "internacional"
    return df

def split_nan(df, column_name):
    '''
    Separa los datasets entre los que tienen asignado departamento
    y los que no 
    '''
    df_1 = df[df[column_name].notnull()]
    df_2 = df[~df[column_name].notnull()]
    return df_1, df_2

df_miss_2015_2018 = add_cleaning_2(missing_2015_2018, "ubicacion", "department")
df_miss_2010_2014 = add_cleaning_2(missing_2010_2014, "ubicacion", "department")
df_miss_add = add_cleaning_2(missing_add, "ubicacion", "department")

#Dividir nuevos datasets
df_miss_2015_2018, missing_2015_2018 = split_nan(df_miss_2015_2018, "department")
df_miss_2010_2014, missing_2010_2014 = split_nan(df_miss_2010_2014, "department")
df_miss_add, missing_add = split_nan(df_miss_add, "department")

with open("speeches.pkl", "rb") as f:  
    speeches = pickle.load(f)

speeches = speeches.append(df_miss_2015_2018, sort = False)
speeches = speeches.append(df_miss_2010_2014, sort = False)
speeches = speeches.append(df_miss_add, sort = False)

with open("speeches.pkl", "wb") as f:
    pickle.dump(speeches, f)

with open("missing.pkl", "wb") as f:
    pickle.dump([missing_2015_2018, missing_2010_2014, missing_add], f)


