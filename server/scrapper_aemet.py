#!/usr/bin/env python3
# coding=utf-8

from typing import MutableMapping
import requests
from bs4 import BeautifulSoup #pip3 install beautifulsoup4
import json
import datetime
import urllib3
import municipios
from pathlib import Path


urllib3.disable_warnings()

def scrapper(place):

    if municipios.buscaMunicipio(place) == None:
        print ("El municipio no existe.")
    else:
        url = municipios.buscaMunicipio(place)

        place = place.lower()
        place = place.replace(" ", "_")

        response = requests.get(url, verify=False)    # make a get http request    
        # print(">>>> ",response.status_code)       # the status can be handled, in case of error
        text_response = response.text   # obtaint the html response 
        soup = BeautifulSoup(text_response, 'lxml')      # parse the response as HTML code
        # print(soup.prettify()) 

        cache_file = "cache_aemet_" + place + ".json"
        fecha_web = soup.find('elaborado').text.strip()[0:10] + " " + soup.find('elaborado').text.strip()[11:]

        try:
            with open(cache_file, 'r') as cache_antigua:
                data = json.load(cache_antigua)
                fecha_prediccion = data["prediction_date"][0:10] + " " + data["prediction_date"][11:]
                fecha_cache = data["cache_datetime"]
                print(fecha_cache)
                print(fecha_web)
                print(fecha_prediccion)
                if fecha_web == fecha_prediccion:
                    print("La cache está actualizada. Actualiza hora de acceso.") 
                    data["cache_datetime"] = str(datetime.datetime.now())[0:10] + " " + str(datetime.datetime.now())[11:19]
                    with open(cache_file, 'w') as cache_antigua:
                        json.dump(data, cache_antigua) 
                else:
                    ("Hay una nueva version. Actualizando.")
                    construir_cache(place, response)
        except:
            print('Caché no encontrada. Se crea una nueva.')
            construir_cache(place, response)

def construir_cache(place, response):

    text_response = response.text 
    soup = BeautifulSoup(text_response, 'lxml')  
    cache_file = "cache_aemet_" + place + ".json"

    #jsonpath = Path('caches')
   
    cache = {}  
    cache["location"] = soup.find('nombre').text.strip()
    cache["cache_datetime"] = str(datetime.datetime.now())[0:10] + " " + str(datetime.datetime.now())[11:19]  
    cache["prediction_date"] = soup.find('elaborado').text.strip()[0:10] + " " + soup.find('elaborado').text.strip()[11:]
    cache["precipitation"] = soup.find('prob_precipitacion').text.strip()
    cache["snow_height"] = soup.find('cota_nieve_prov').text.strip()
    cache["sky"] = soup.find('estado_cielo').text.strip()
    cache["wind_direction"] = soup.find('direccion').text.strip()
    cache["wind_speed"] = soup.find('velocidad').text.strip()
    cache["max_temp"] = soup.find('maxima').text.strip()
    cache["min_temp"] = soup.find('minima').text.strip()


    with open (cache_file, "w") as write_file:
        #jsonpath.write_text(json.dump(cache, write_file))
        json.dump(cache, write_file)