"""
ETL_DAGSTER
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse
from dagster import MetadataValue, Output, asset, op, AssetIn
from dagster import AssetKey, ConfigurableIOManager
from pandas import DataFrame


@asset
def obteniendo_pagina():
    url = "https://www.howlanders.com/blog/latam/lagos-mas-grandes-de-sudamerica/amp/"
    respuesta = requests.get(url)
    pagina = BeautifulSoup(respuesta.text,"html.parser")
    return pagina
    
@asset
def extrayendo_nombre_y_pais(obteniendo_pagina): 
    pagina=obteniendo_pagina
    Datos = pd.DataFrame() 
    Nombre = []
    Pais = []
    nombre_pais = pagina.find_all("h2")
    for i in range (1,9):
        Nombre.append(nombre_pais[i].span.text.split(",")[0])
        Pais.append(nombre_pais[i].span.text.split(",")[1].strip())
    Datos["Pais"]= Pais
    Datos["Nombre"]=Nombre  
    return Datos
    
@asset
def extrayendo_superficie(extrayendo_nombre_y_pais,obteniendo_pagina):   
    Datos=extrayendo_nombre_y_pais
    pagina=obteniendo_pagina
    superficie=[]
    superficie_temporal= pagina.find_all("b")

    for i in range(1,13):
        a=superficie_temporal[i].text.strip().replace(".","").split(" ")
        if "kilómetros" in a :
            for j in range(len(a)):
                if a[j].isdigit():
                    superficie.append(a[j])
        elif "km²" in a :
            for k in range(len(a)):
                if a[k].isdigit():
                    superficie.append(a[k])
        else:
            pass


    Datos['Superficie']=superficie
    return Datos

@asset
def extrayendo_lat_long(extrayendo_superficie):
    Datos=extrayendo_superficie
    Latitud = []
    Longitud = []
    Lagos_Nombre =Datos['Nombre']
    Lagos_Pais= [str(nombre).split(" ")[0] for nombre in Datos['Pais']] 
    for i in range(len(Lagos_Nombre)):
        direccion ='https://geocode.maps.co/search?q='+Lagos_Nombre[i]+'&'+Lagos_Pais[i]
        respuesta = requests.get(direccion).json()
        jsonpath_expr_Lat = parse('$.[*].lat')
        Latitud.append([match.value for match in jsonpath_expr_Lat.find(respuesta)][0])
        jsonpath_expr_Lon = parse('$.[*].lon')
        Longitud.append([match.value for match in jsonpath_expr_Lon.find(respuesta)][0])
    Datos['Latitud']=Latitud
    Datos['Longitud']=Longitud
    return Datos

@asset
def Cargando(extrayendo_lat_long):
    Datos=extrayendo_lat_long
    Datos.to_csv("C:/Users/HP/Desktop/DIPLOMADO MACHINE LEARNING/Modulo 1/DATOS_CSV/Tarea.csv")
    return Datos


if __name__ == "__main__":
    pass
