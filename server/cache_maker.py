from datetime import datetime
import json
from pathlib import Path
import datetime

def montar_cache(place):

    aux = place

    place = place.lower()
    place = place.replace(" ", "_")

    #jsonpath = Path('caches')

    cache_aemet = "cache_aemet_" + place + ".json"
    cache_datos_abiertos= "cache_datos_abiertos_" + place + ".json"

    with open(cache_aemet) as json_file_aemet:
        tiempo = json.load(json_file_aemet)

    with open(cache_datos_abiertos) as json_file_datos_abiertos:
        datos_abiertos = json.load(json_file_datos_abiertos)

    cache_file = "cache_" + place + ".json"

    with open (cache_file, "w") as write_file:

        write_file.write('{\n\t"cache_location": \"' + aux + "\",\n" + "\t\t")

        write_file.write('\n\t"cache_date": \"' + str(datetime.datetime.now())[0:10] + " " + str(datetime.datetime.now())[11:19] + "\",\n" + "\t\t")
        
        write_file.write('\n\t"tiempo": ' + "\n" + "\t\t")
        json.dump(tiempo, write_file)
        write_file.write(",\n")

        # Copiar y pegar este bloque, y cambiar el nombre cada vez que se añada una nueva web a la cache
        write_file.write('\n\t"datos_abiertos": ' + "\n" + "\t\t")
        json.dump(datos_abiertos, write_file)
        # write_file.write(",\n")

        write_file.write("\n}")