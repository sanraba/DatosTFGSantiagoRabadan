#!/usr/bin/env python3
# coding=utf-8

import scrapper_datos_abiertos
import scrapper_aemet
import cache_maker
import json
import os

def create_caches(place):

    print(place)

    scrapper_datos_abiertos.scrapper(place.lower())
    scrapper_aemet.scrapper(place)
    cache_maker.montar_cache(place)

    place = place.lower()
    place = place.replace(" ", "_")

    #caches_path = "/home/pi/caches/" #LINUX
    #caches_path = ".//caches//"
    '''
    caches_path = r".\\caches\\" #WINDOWS

    if not os.path.exists(caches_path):
        os.makedirs(caches_path)
    '''

    #file_name = "cache_" + place + ".json"
    file_name = "cache_" + place + ".json"

    with open(file_name) as cache:
        data = json.load(cache)

    return data



