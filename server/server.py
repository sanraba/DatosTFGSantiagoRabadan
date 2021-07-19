from flask import Flask, request
import requests
import json
import make_cache
import municipios
import datetime

app = Flask(__name__)

@app.route("/test", methods=["POST"])
def test():
    data = request.json
    print(data.get("json_payload"))
    print(data.get("apikey"))

    return{"status": "test"}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    credentials_send = data.get("json_payload")
    user = credentials_send['user']
    password = credentials_send['password']

    print(user)
    print(password)

    with open ("credentials.json", "r") as credentials_file:
        credentials = json.load(credentials_file)

    password_data = credentials.get(user)
    if password_data:
        if password_data == password:
            return {"status": "Logged in"}
        return {"status": "Wrong password"}
        
    return {"status": "Wrong username"}

@app.route("/cache", methods=["POST"])
def place():
    data = request.json
    place = data.get("json_payload")

    place_aux = place.lower()
    sitio_sin_espacios = place_aux.replace(" ", "")
    url = "https://" + sitio_sin_espacios + ".ayuntamientosdevalladolid.es/contacto"

    try:
        check_url = requests.get(url)
        if check_url.status_code == 200:
            available = True
    except:
        available = False

    if municipios.buscaMunicipio(place) == None and available == False:
        return{"status": "poblacion no existe o no disponible"}
    else:
        cache = make_cache.create_caches(place)
        return cache 

@app.route("/date", methods=["POST"])
def date():
    data = request.json
    speaker_cache_date = data.get("json_payload")
    current_date = str(datetime.datetime.now())[0:10] + " " + str(datetime.datetime.now())[11:19]

    current_date_datetime = datetime.datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S')
    speaker_cache_date_datetime = datetime.datetime.strptime(speaker_cache_date, '%Y-%m-%d %H:%M:%S')

    print(speaker_cache_date_datetime)
    print(current_date_datetime)

    tiempo_para_actualizar = 12 #En horas

    if (current_date_datetime - speaker_cache_date_datetime) < datetime.timedelta(hours=tiempo_para_actualizar):
        return{"status": "cache updated"}
    else:
        return{"status": "actualiza cache"}

app.run(host="0.0.0.0", port=8080, debug=True)