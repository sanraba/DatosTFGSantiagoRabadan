import http.client
import requests
import sys
import json
from pathlib import Path
import os
import time

contador = 0

while 1:

    if contador == 1:
        break

    error = "Caché recibida"

    
    with open ("urls.json", "r") as urls_file:
        urls = json.load(urls_file)
    
    '''
    url_login = "http://157.88.123.226:8080/login"
    '''

    login_url = urls["URL_LOGIN"]
    cache_url = urls["URL_CACHE"]
    date_url = urls["URL_DATE"]

    
    # retrieve MAC of device
    macfile = "./caches/macfile.txt"
    comando = "sudo ifconfig | grep ether > " + macfile
    os.system(comando)
    # wait to do more safe
    time.sleep(2) 
    # extract MAC
    with open(macfile, "r") as file: 
        data = file.readline().replace('ether', '').replace("\t", '').replace("\n", '').replace(" ", '')[:17]
    with open(macfile, "w") as file:
        file.write(data)
    # Generate credentials to sign in.
    tmp = data

    c = "K" + tmp[9:11] + "U" + tmp[15:17] + "i" + tmp[3:5] + "l" + tmp[12:14] + "p" + tmp[0:2] + "P" + tmp[6:8] + "j" 
    x = '{"user": "' + data + '", "password": "' + c + '"}'

    credentials = json.loads(x)

    payload = {"json_payload": credentials}

    r = requests.post(login_url, json=payload)
    response = r.text
    response_json = json.loads(response)
    status = response_json["status"]
    
    if status == "Wrong password":
        error = "Las credenciales no son correctas: password error"
        break
    elif status == "Wrong username":
        error = "Las credenciales no son correctas: user error"
        break
    else:


        with open("/home/pi/location.json", "r") as location_file:
            data = json.load(location_file) 

        print(status)
        municipio = data['location'] # Extraer de archivo de configuración

        place = municipio.lower()
        place = place.replace(" ", "_")

        caches_path = "/home/pi/caches/" #LINUX
        #caches_path = r".\\caches\\ #WINDOWS

        if not os.path.exists(caches_path):
            os.makedirs(caches_path)

        nombre_cache = caches_path + "cache.json"
        
        my_file = Path(nombre_cache)
        
        if my_file.is_file():

            with open (nombre_cache, "r") as cache_descargada:
                cache = json.load(cache_descargada)

            cache_datetime = cache['cache_date']
            cache_location = cache['cache_location']
            payload_date = {"json_payload": cache_datetime}
            payload_place = {"json_payload": municipio}

            r_date = requests.post(date_url, json=payload_date)
            cache_date_status = r_date.text
            cache_date_json = json.loads(cache_date_status)
            status_date = cache_date_json["status"]

            r_place = requests.post(cache_url, json=payload_place)
            cache_place_status = r_place.text
            cache_place_json = json.loads(cache_place_status)

            try:
                status_place = cache_place_json["status"]
                
                if(status_place == "poblacion no existe o no disponible"):
                    error = "El municipio no existe o no está disponible para hacer la caché."
                    break
                
            except:

                if(status_date == "cache updated"):
                    error = "Cache reciente. No se descarga una nueva."
                    break
                else:
                    downloaded_cache = cache_place_status
                    downloaded_cache_json = json.loads(downloaded_cache)

                    with open(nombre_cache, "w") as cache:
                        json.dump(downloaded_cache_json, cache)

        else:  
            
            payload = {"json_payload": municipio}
            r = requests.post(cache_url, json=payload)

            cache_status = r.text

            try:
                cache_json = json.loads(cache_status)
                status = cache_json["status"]

                if(status == "poblacion no existe o no disponible"):
                    error = "Municipio no existe o no está disponible."
                    break
                
            except:
                downloaded_cache = cache_status
                downloaded_cache_json = json.loads(downloaded_cache)

                with open(nombre_cache, "w") as cache:
                    json.dump(downloaded_cache_json, cache)

            '''
            if(cache_status == "poblacion no existe o no disponible"):
                error = "Municipio no existe o no está disponible."
                break
            else:
                downloaded_cache = cache_status
                downloaded_cache_json = json.loads(downloaded_cache)

                with open(nombre_cache, "w") as cache:
                    json.dump(downloaded_cache_json, cache)
            '''


    contador = contador + 1

print(error)

'''
def signin(self):
        all_urls = "./cache/urls.json"
        with open (all_urls, "r") as read_file:
            urls = json.load(read_file)
        url = urls["URL_LOGIN"]
        try:
            # sign in the system
            response = requests.post(url, data = self.credentials)
            if (response.status_code == 200):
                # save tokens
                tokens = './cache/token.json'
                with open(tokens, "w") as file:
                    file.write(response.content)
                    self.tokens = response.content
                return True
            else:
                print("[login] Cannot sign in: " + str(response.content))
                return False
        except Exception as err:
            print("[login] Cannot connect to the host: " + str(err))
            return False
'''
