# -*- coding: utf-8 -*-
"""
@author: Juan Felipe Ladino
"""
###############################################################################
#
#Revisión de últimos lugares missing 
#
###############################################################################

import os
import pickle
import pandas as pd


os.chdir("C:\\Users\\juanf\\Desktop\\UR 2018 - 2\\MCPP\\Proyecto Final")

def split_nan(df, column_name):
    '''
    Separa los datasets entre los que tienen asignado departamento
    y los que no 
    '''
    df_1 = df[df[column_name].notnull()]
    df_2 = df[~df[column_name].notnull()]
    return df_1, df_2

with open("speeches.pkl", "rb") as f:  
    speeches = pickle.load(f)

speeches, speeches_nan = split_nan(speeches, "department")

depto = list(speeches_nan.department)

for i in range(len(depto)):
    depto[i] = "internacional"    
depto[0] = "No identificado"
depto[2] = "valle del cauca"
depto[7] = "No identificado"
depto[20] = "No identificado"
depto[21] = "No identificado"
depto[26] = "No identificado"

speeches_nan.department = depto

speeches = speeches.append(speeches_nan, sort = False)

#Reset index: ya está la versión final
speeches.reset_index(drop = True, inplace = True)

with open("speeches.pkl", "wb") as f:
    pickle.dump(speeches, f)

