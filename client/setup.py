import os

caches_route = "/home/pi/caches"

location_route = "/home/pi/location.json"

try:
    os.makedirs(caches_route)    
    print("Directorio " , caches_route ,  " creado ")
except FileExistsError:
    print("Directorio " , caches_route ,  " ya existe")

with open(location_route, 'x') as f:
    f.write('{"location": "Wamba"}')
    print("Fichero de localización creado. Localidad por defecto: Wamba.")