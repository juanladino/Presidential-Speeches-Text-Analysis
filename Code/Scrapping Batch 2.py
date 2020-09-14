# -*- coding: utf-8 -*-
"""
@author: Juan Felipe Ladino
"""
##############################################################################
#
#Funciones para web scrapping 
#
#Discursos presidente Santos agosto 2010 - agosto 2014
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


def extract_h1_2010_2014():
    '''
    Obtiene el codigo HTML con los links
    y titulos de cada discurso entre agosto 2010 y agosto 2014
    '''
    url_prefix = "http://wsp.presidencia.gov.co/Discursos/"
    browser = webdriver.Chrome(executable_path=r"C:\Users\juanf\Desktop\UR 2018 - 2\MCPP\chromedriver_win32\chromedriver.exe")
    Mes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", 
           "Agosto","Septiembre", "Octubre", "Noviembre", "Diciembre"]
    Year = ["2010", "2011", "2012", "2013", "2014"]

    html = []       
    for year in Year:
        for mes in Mes:
            url = url_prefix + year + "/Paginas/" + mes + ".aspx"
            browser.get(url)
            time.sleep(10)
            html_discursos = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            soup_discursos = BeautifulSoup(html_discursos, "html.parser")
            #Extrae los elementos que contienen la información de los discursos
            text_html = soup_discursos.findAll(name ="a")           
            html += text_html
    return html

def extract_links_2010_2014(html):
    '''
    Extrae del codigo HTML el link y titulo del discursos
    entre agosto 2010 y agosto 2014
    '''
    lista_links = []
    lista_titulos = []
    
    for h1 in html:
        #Busca links
        links1 = re.findall("\<a href=\"(http://wsp.presidencia.gov.co/Prensa/.+?)\"", str(h1)) 
        #Busca títullos
        titulos1 = re.findall("title=\"\">(.+?)\</a>" , str(h1))
        lista_links += links1
        lista_titulos += titulos1
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

def get_speeches_2010_2014():
    '''
    Obtiene lista de discursos entre agosto de 2010 a agosto del 2014
    '''
    #Función principal para extraer discursos
    html1 = extract_h1_2010_2014()
    lista_links1014, lista_titulos1014 = extract_links_2010_2014(html1)
    discursos1014 = extract_discursos(lista_links1014)
    return discursos1014

def get_numcodes_1014(lista_links):
    '''
    Obtiene de los links los codigos de fecha
    '''
    #Los links contienen series de números que representan la fecha
    #Se extrae esta serie de números
    expresiones = []
    numbers = []
    
    for link in lista_links:
        #Obtiene la serie de números para codificar la fecha
        expresion = re.findall("http://wsp.presidencia.gov.co/Prensa/.*/([0-9]+)", str(link))
        expresiones += expresion
        
        #Procesar series de números incompletas
    for exp in expresiones:
        if len(exp) == 7:
            exp = "2" + exp
        elif len(exp) == 2:
            exp = "201308" + exp
        numbers += [exp]
    return numbers    

def get_dates_1014(lista_links):
    '''
    Obtiene del html las fechas de los discursos entre 
    agosto 2010 y agosto 2014
    ''' 
    days = []
    months = []
    years = []
    dates = []
    
    nums = get_numcodes_1014(lista_links)
    for num in nums:
        #Encuentra día
        day = num[6:8]
        days += [day]
        #Encuentra mes
        month = num[4:6]
        months += [month]
        #Encuentra año
        year = num[0:4]
        years += [year]
        #Procesa fecha
        date = day + "/" + month + "/" + year
        date = datetime.datetime.strptime(date, "%d/%m/%Y")
        dates += [date]
    return days, months, years, dates

def get_placeshtml_2010_2014():
    '''
    Obtiene elementos que contienen lugares
    de discursos entre agosto 2010 y agosto 2014

    '''
    url_prefix = "http://wsp.presidencia.gov.co/Discursos/"
    browser = webdriver.Chrome(executable_path=r"C:\Users\juanf\Desktop\UR 2018 - 2\MCPP\chromedriver_win32\chromedriver.exe")
    Mes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", 
           "Agosto","Septiembre", "Octubre", "Noviembre", "Diciembre"]
    Year = ["2010", "2011", "2012", "2013", "2014"]

    html = []    
    for year in Year:
        for mes in Mes:
            url = url_prefix + year + "/Paginas/" + mes + ".aspx"
            browser.get(url)
            time.sleep(10)
            html_discursos = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            soup_discursos = BeautifulSoup(html_discursos, "html.parser")
            #Extrae los elementos que contienen la información de lugar 
            text_html = soup_discursos.findAll(name ="div", class_= "description")
            html += text_html
    return html

def get_places_2010_2014(html):
    '''
    Obtiene lugares de discursos 2010 - 2014
    '''
    
    lugar = []
    for h1 in html:
        #Extrae lugares
        lugares = re.findall("\"description\">(.*?)[,.\(\)\<]", str(h1), re.DOTALL)
        lugar += lugares
    return lugar    

#Aplicación de funciones

discursos1014 = get_speeches_2010_2014()
html1014 = extract_h1_2010_2014()
lista_links1014, lista_titulos1014 = extract_links_2010_2014(html1014)
dia1014, mes1014, año1014, fecha1014 = get_dates_1014(lista_links1014)
html_lugar = get_placeshtml_2010_2014()
lugar1014 = get_places_2010_2014(html_lugar)
    
dataframe_1014 = pd.DataFrame({"link discurso": lista_links1014, "titulo": lista_titulos1014,
                               "ubicacion": lugar1014, "dia": dia1014, "mes": mes1014, "año": año1014,
                               "fecha": fecha1014, "discurso": discursos1014})


#Saving objects
    
with open('variables_2010_2014.pkl', 'wb') as f:
    pickle.dump([url, lista_links1014, lista_titulos1014, lugar1014,
                 dia1014, mes1014, año1014, fecha1014, discursos1014], f)
    
with open("data_frame_2010_2014.pkl", "wb") as f:
    pickle.dump(dataframe_1014, f)
