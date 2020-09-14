# -*- coding: utf-8 -*-
"""
@author: Juan Felipe Ladino
"""
##############################################################################
#
#Funciones para web scrapping
#
#Discursos presidente Santos agosto 2014 - diciembre 2015
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


def extract_h1_add():
    '''
    Obtiene el codigo HTML con los links
    y titulos de cada discurso entre agosto 2014 y diciembre 2015
    '''
    url_prefix = "http://wp.presidencia.gov.co/Discursos/"
    browser = webdriver.Chrome(executable_path=r"C:\Users\juanf\Desktop\UR 2018 - 2\MCPP\chromedriver_win32\chromedriver.exe")
    Mes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", 
           "Agosto","Septiembre", "Octubre", "Noviembre", "Diciembre"]
    Year = ["2014", "2015"]

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


def extract_links_add(html):
    '''
    Extrae del codigo HTML el link de los discursos 2014-2015 adicionales
    '''
    lista_links = []
    
    for h1 in html:
        #Busca links
        links1 = re.findall("\<a href=\"(http://wp.presidencia.gov.co/Noticias/.+/Paginas/.+?)\"", str(h1)) 
        lista_links += links1
    return lista_links

def extract_titles_add(lista_links):
    '''
    De la lista de links procesa el título de los discursos
    entre agosto 2014 y diciembre 2015
    '''
    lista_titulos = []
    
    for link in lista_links:
        #BUsca títulos
        tit = re.findall("[0-9]-(.+?)\.aspx", str(link))
        #Procesa título
        tit = tit[0].split("-")
        title = " ".join(tit)
        lista_titulos += [title]
    return lista_titulos

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

def get_speeches_add():
    '''
    Obtiene lista de discursos entre agosto 2014 a diciembre 2018
    '''
    #Función principal para extraer discursos
    html = extract_h1_add()
    lista_links_add = extract_links_add(html)
    discursos_add = extract_discursos(lista_links_add)
    return discursos_add

def get_numcodes_add(lista_links):
    '''
    Obtiene de los links los codigos de fecha
    '''
    expresiones = []
    
    for link in lista_links:
        expresion = re.findall("http://wp.presidencia.gov.co/Noticias/.+?/Paginas/([0-9]+)", str(link))
        expresiones += expresion
    return expresiones

def get_dates_add(lista_links):
    '''
    Obtiene del html las fechas de los discursos adicionales
    ''' 
    days = []
    months = []
    years = []
    dates = []
    
    nums = get_numcodes_add(lista_links)
    for num in nums:
        day = num[6:8]
        days += [day]
        month = num[4:6]
        months += [month]
        year = num[0:4]
        years += [year]
        date = day + "/" + month + "/" + year
        date = datetime.datetime.strptime(date, "%d/%m/%Y")
        dates += [date]
    return days, months, years, dates

def get_places_html_add():
    '''
    Obtiene html con lugares de discursos adicionales
    '''
    url_prefix = "http://wp.presidencia.gov.co/Discursos/"
    browser = webdriver.Chrome(executable_path=r"C:\Users\juanf\Desktop\UR 2018 - 2\MCPP\chromedriver_win32\chromedriver.exe")
    Mes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", 
           "Agosto","Septiembre", "Octubre", "Noviembre", "Diciembre"]
    Year = ["2014", "2015"]

    html = []    
    for year in Year:
        for mes in Mes:
            url = url_prefix + year + "/Paginas/" + mes + ".aspx"
            browser.get(url)
            time.sleep(10)
            html_discursos = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            soup_discursos = BeautifulSoup(html_discursos, "html.parser")
            text_html = soup_discursos.findAll(name ="div", class_= "description")
            html += text_html
    return html

def get_places_add(html):
    '''
    Obtiene lugares de discursos adicionales
    '''
    
    lugar = []
    for h1 in html:
        lugares = re.findall("\"description\">(.*?)[,.\(\)\<]", str(h1), re.DOTALL)
        lugar += lugares        
    return lugar   

#Aplicaciión de funciones 

discursos_add = get_speeches_add()
html_add = extract_h1_add()
lista_links_add = extract_links_add(html_add)
lista_titulos_add = extract_titles_add(lista_links_add)
dia_add, mes_add, año_add, fecha_add = get_dates_add(lista_links_add)
html_places = get_places_html_add()
lugar_add = get_places_add(html_places)

dataframe_add = pd.DataFrame({"link discurso": lista_links_add, "titulo": lista_titulos_add,
                               "ubicacion": lugar_add, "dia": dia_add, "mes": mes_add, "año": año_add,
                               "fecha": fecha_add, "discurso": discursos_add})

#Saving objects

with open('variables_add.pkl', 'wb') as f:
    pickle.dump([lista_links_add, lista_titulos_add, lugar_add,
                 dia_add, mes_add, año_add, fecha_add, discursos_add], f)
    
with open("data_frame_add.pkl", "wb") as f:
    pickle.dump(dataframe_add, f)


