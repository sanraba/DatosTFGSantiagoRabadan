#!/usr/bin/env python3
# coding=utf-8

import requests
from bs4 import BeautifulSoup #pip3 install beautifulsoup4

import json
import datetime
import urllib3
from pathlib import Path

urllib3.disable_warnings()

def scrapper(place):
    
    #with open('urls_to_crawl.json') as json_file:
        #data = json.load(json_file)

    sitio_sin_espacios = place.replace(" ", "")
    sitio_con_barrabaja = place.replace(" ", "_")

    #jsonpath = Path('caches')
 
    url = "https://" + sitio_sin_espacios + ".ayuntamientosdevalladolid.es/contacto"

        # url = data['locales'][place]['ayto']['contacto']

    response = requests.get(url, verify=False)    # make a get http request    
    # print(">>>> ",response.status_code)       # the status can be handled, in case of error
    text_response = response.text   # obtaint the html response 
    soup = BeautifulSoup(text_response, 'html.parser')      # parse the response as HTML code
    # print(soup.prettify()) 

    cache = {}  
    cache["cache_datetime"] = str(datetime.datetime.now())[0:10] + " " + str(datetime.datetime.now())[11:19]    # set the date of the cache data
    cache["address"]= soup.find("div", "address").text.strip()  # no whitespaces 
    the_telephone_number= soup.find("div", "phone local").text[5:]   # without " +34 "
    cache["telephone"] = the_telephone_number.replace(" ",", ",2) # prepare to better speech 
    the_fax_number = soup.find("div", "phone fax").text[5:]   # without " +34 "
    cache["fax"] = the_fax_number.replace(" ",", ",2)
    cache["email"] = soup.find("div", "email").text.strip()
    cache["URL"] = soup.find("div", "urlExterna").text.strip()

    cache_file = "cache_datos_abiertos_" + sitio_con_barrabaja + ".json"

    with open (cache_file, "w") as write_file:
        #jsonpath.write_text(json.dump(cache, write_file))
        json.dump(cache, write_file)
