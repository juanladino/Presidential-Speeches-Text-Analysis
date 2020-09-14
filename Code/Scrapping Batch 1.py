# -*- coding: utf-8 -*-
"""
@author: Juan Felipe Ladino
"""
##############################################################################
#
#Funciones para web scrapping
#
#Discursos presidente Santos septiembre 2015 - agosto 2018
#
##############################################################################

import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import datetime
import pandas as pd
import pickle

os.chdir("C:\\Users\\juanf\\Desktop\\UR 2018 - 2\\MCPP\\Proyecto Final")

def extract_h1_2015_2018():
    '''
    Obtiene el codigo HTML con los links
    y titulos de cada discurso entre septiembre 2015 y agosto 2018
    '''    
    html= []
    browser = webdriver.Chrome(executable_path=r"C:\Users\juanf\Desktop\UR 2018 - 2\MCPP\chromedriver_win32\chromedriver.exe")
    
    for i in range(1, 1242, 20):
        url_discursos = "http://es.presidencia.gov.co/discursos#k=#s="+str(i)
        browser.get(url_discursos) 
        time.sleep(10)
        html_discursos = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup_discursos = BeautifulSoup(html_discursos, "html.parser")
        #Extrae los elementos que contienen la información de los discursos
        text_html = soup_discursos.findAll(name = "h1", class_ = "mtmL-Titulo")
        html += text_html
    return html
    
def extract_links_2015_2018(html):
    '''
    Extrae del codigo HTML el link 
    y titulo de los discursos entre septiembre 2015 y agosto 2018
    '''     
    lista_links = []
    lista_titulos = []
    
    for h1 in html:
        #Busca links
        links = re.findall("\<a href=\"(http://es.presidencia.gov.co/discursos/.+?)\">", str(h1)) 
        #Busca títulos
        titulos = re.findall("\<br/>(.+)\</span>" , str(h1))
        lista_links += links
        lista_titulos += titulos    
    return lista_links, lista_titulos

def paste_paragraphs(parrafos):
    '''
    Pega parrafos para armar discurso
    '''
    #Al extraer el texto se extraen los párrafos por separado
    #Se procesan para que queden como un solo texto
    parrafos = [parrafos[i].text for i in range(len(parrafos))]
    discurso = [" ".join(parrafos)]
    return discurso
    
def extract_discursos(lista_links):
    '''
    Obtiene lista de discursos
    '''
    discursos = []
    browser = webdriver.Chrome(executable_path=r"C:\Users\juanf\Desktop\UR 2018 - 2\MCPP\chromedriver_win32\chromedriver.exe")

    for i in range(len(lista_links)):
        url_discurso = lista_links[i]
        #Obtiene información de cada link
        browser.get(url_discurso)
        #Extrae los tag que contienen los párrafos
        parrafos = browser.find_elements_by_tag_name("p")
        disc = paste_paragraphs(parrafos)
        discursos = discursos + disc
    return discursos

def get_speeches_2015_2018():
    '''
    Obtiene lista de discursos entre septiembre de 2015 a agosto del 2018
    '''
    #Función principal para extraer discursos
    html = extract_h1_2015_2018()
    lista_links, lista_titulos = extract_links_2015_2018(html)
    discursos = extract_discursos(lista_links)
    return discursos


def get_html_date_place_1518():
    '''
    Obtiene elementos que contienen lugares y fechas 
    de los discursos entre septiembre 2015 y agosto 2018
    '''
    html= []
    browser = webdriver.Chrome(executable_path=r"C:\Users\juanf\Desktop\UR 2018 - 2\MCPP\chromedriver_win32\chromedriver.exe")

    for i in range(1, 1242, 20):
        url_discursos = "http://es.presidencia.gov.co/discursos#k=#s="+str(i)
        browser.get(url_discursos) 
        time.sleep(10)
        html_discursos = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup_discursos = BeautifulSoup(html_discursos, "html.parser")
        #Extrae los elementos que contienen la información de fecha y lugar 
        text_html = soup_discursos.findAll(name = "span", class_ = "mtmL-fecha")
        html += text_html
    return html 

def get_dates_1518(html):
     '''
     Obtiene del html las fechas de 
     los discursos entre septiembre 2015 y agosto 2018
     '''
     days = []
     months = []
     years = []
     dates = []
     for h1 in html:
         #Encuentra día
         day = re.findall("(\d+) ", str(h1))
         days += day
         #Encuentra mes
         month = re.findall("[0-9]+ de (.+) de", str(h1))
         month = define_month(month[0])
         months += [month]
         #Encuentra año
         year = re.findall("de (\d+)", str(h1))
         years += year
         #Procesa fecha
         date = str(day[0]) + "/" + month + "/" + str(year[0])
         date = datetime.datetime.strptime(date, "%d/%m/%Y")
         dates += [date]
     return days, months, years, dates

def define_month(month):
    '''
    Función para convertir 
    nombre de mes en número
    '''
    m = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    for mes in range(len(m)):
        if month == m[mes]:
            month = str(mes + 1)
    return month

def get_places(html):
    '''
    Obtiene lugares de discursos 
    entre septiembre 2015 y agosto 2018
    '''
    lugar = []
    for h1 in html:
        #Extrae lugares
        lugares = re.findall("> (.+?)[,.\(\)]", str(h1))
        lugar += lugares
    return lugar

def places_dates():
    '''
    Obtiene fechas y lugares
    '''
    #Función principal para obtener fecha y lugar
    html = get_html_date_place_1518()
    dia, mes, año, fecha = get_dates_1518(html)
    lugar = get_places(html)
    return dia, mes, año, fecha, lugar

#Aplicación de funciones

discursos = get_speeches_2015_2018()
html = get_html_date_place_1518()
lista_links, lista_titulos = extract_links_2015_2018(html)
dia, mes, año, fecha, lugar = places_dates()

dataframe_1518 = pd.DataFrame({"link discurso": lista_links, "titulo": lista_titulos,
                               "ubicacion": lugar, "dia": dia, "mes": mes, "año": año,
                               "fecha": fecha, "discurso": discursos})   
  
#Saving objects
    
with open('variables_2015_2018.pkl', 'wb') as f:
    pickle.dump([url_discurso, lista_links, lista_titulos, lugar,
                 dia, mes, año, fecha, discursos], f)

with open("data_frame_2015_2018.pkl", "wb") as f:
    pickle.dump(dataframe_1518, f)
      
