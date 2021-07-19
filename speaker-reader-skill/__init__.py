from mycroft import MycroftSkill, intent_file_handler, intent_handler
import json


class SpeakerReader(MycroftSkill):
    def initialize(self):
        self.register_entity_file('/opt/mycroft/skills/speaker-reader-skill/locale/es-es/type.entity')

    @intent_file_handler('speaker.reader.intent')
    def handle_reader(self, message):
        with open('/home/pi/caches/cache.json') as json_file:
        #with open('/home/pi/caches/cache.json') as json_file:
            petition_type = message.data.get('type')
            data = json.load(json_file)
            location = data["cache_location"]
            fecha = data['cache_date']
            datos_abiertos = data['datos_abiertos']
            tiempo = data['tiempo']

            articulo = ""
            
            '''
            if(petition_type == 'lluvia' or petition_type == 'temperatura_maxima' or petition_type == 'temperatura_minima' or petition_type == 'nieve'):
                articulo = "la"
            elif(petition_type == 'temperaturas'):
                articulo = "las"
            else:
                articulo = "el"

            intro = articulo + petition_type + " es:"
            '''
            intro = ""

            if petition_type == 'ayuntamiento':
                dat_ayuntamiento = datos_abiertos['address']
                output = intro + dat_ayuntamiento
                self.speak(output)
            elif petition_type == 'email':
                dat_email = datos_abiertos['email']
                output = intro + dat_email
                self.speak(output)
            elif petition_type == 'correo':
                dat_email = datos_abiertos['email']
                output = intro + dat_email
                self.speak(output)
            elif petition_type == 'correo electrónico':
                dat_email = datos_abiertos['email']
                output = intro + dat_email
                self.speak(output)
            elif petition_type == 'teléfono':
                dat_telefono = datos_abiertos['telephone']
                dat_telefono = dat_telefono.replace(", ","")
                self.speak(intro)
                for digit in dat_telefono:
                    self.speak(str(digit))
            elif petition_type == 'fax':
                dat_fax = datos_abiertos['fax']
                dat_fax = dat_fax.replace(", ","")
                self.speak(intro)
                for digit in dat_fax:
                    self.speak(str(digit))
            elif petition_type == 'pueblo':
                dat_pueblo = location
                output = "Estamos en " + dat_pueblo
                self.speak(output)
            elif petition_type == 'tiempo':
                dat_pueblo = tiempo['location']
                dat_cielo = tiempo['sky']
                dat_temperatura_max = tiempo['max_temp']
                dat_temperatura_min = tiempo['min_temp']
                dat_lluvia = tiempo['precipitation']
                output = ""
                if(dat_lluvia == ""):
                    output = "la previsión para hoy en " + dat_pueblo + " es de " + dat_cielo + " con una temperatura maxima de " + dat_temperatura_max + " grados y una minima de " + dat_temperatura_min + " grados. No se esperan lluvias"
                else:
                    output = "la previsión para hoy en " + dat_pueblo + " es de " + dat_cielo + " con una temperatura maxima de " + dat_temperatura_max + " y una minima de " + dat_temperatura_min + ". Se esperan lluvias"
                self.speak(output)
            elif petition_type == 'cielo':
                dat_cielo = tiempo['sky']
                output = "Estamos en " + dat_pueblo
                self.speak(output)
            elif petition_type == 'temperaturas':
                dat_temperatura_max = tiempo['max_temp']
                dat_temperatura_min = tiempo['min_temp']
                output = "hoy se espera una temperatura máxima de " + dat_temperatura_max + " grados y una mínima de " + dat_temperatura_min + " grados"
                self.speak(output)
            elif petition_type == 'temperatura máxima':
                dat_temperatura_max = tiempo['max_temp']
                output = "hoy se espera una temperatura máxima de " + dat_temperatura_max + " grados"
                self.speak(output)
            elif petition_type == 'temperatura mínima':
                dat_temperatura_min = tiempo['min_temp']
                output = "hoy se espera una temperatura mínima de " + dat_temperatura_min + " grados"
                self.speak(output)
            elif petition_type == 'viento':
                dat_direccion_viento = tiempo['wind_direction']
                dat_velocidad_viento = tiempo['wind_speed']
                direccion = ""
                if(dat_direccion_viento==""):
                    direccion="hoy no se prevee viento"
                elif(dat_direccion_viento=="N"):
                    direccion="la dirección del viento es norte, con una velocidad de " + dat_velocidad_viento + " kilómetros por hora"
                elif(dat_direccion_viento=="NE"):
                    direccion="la dirección del viento es noreste, con una velocidad de " + dat_velocidad_viento + " kilómetros por hora"
                elif(dat_direccion_viento=="E"):
                    direccion="la dirección del viento es este, con una velocidad de " + dat_velocidad_viento + " kilómetros por hora"
                elif(dat_direccion_viento=="SE"):
                    direccion="la dirección del viento es sureste, con una velocidad de " + dat_velocidad_viento + " kilómetros por hora"
                elif(dat_direccion_viento=="S"):
                    direccion="la dirección del viento es sur, con una velocidad de " + dat_velocidad_viento + " kilómetros por hora"
                elif(dat_direccion_viento=="SO"):
                    direccion="la dirección del viento es suroeste, con una velocidad de " + dat_velocidad_viento + " kilómetros por hora"
                elif(dat_direccion_viento=="O"):
                    direccion="la dirección del viento es oeste, con una velocidad de " + dat_velocidad_viento + " kilómetros por hora"
                elif(dat_direccion_viento=="NO"):
                    direccion="la dirección del viento es noroeste, con una velocidad de " + dat_velocidad_viento + " kilómetros por hora"
                output = direccion
                self.speak(output)
            elif petition_type == 'nieve':
                dat_nieve = tiempo['snow_height']
                if(dat_nieve == ""):
                    output = "hoy no se espera nieve"
                else:
                    output = "la cota de nieve esta en " + dat_nieve + " metros"
                self.speak(output)
            elif(petition_type == 'día' or petition_type == 'fecha' or petition_type == 'cuándo'):
                dat_fecha = fecha

                date, time = dat_fecha.split(" ")

                year, month, day = date.split("-")

                hour, minutes, seconds = time.split(":")

                month_word = ""

                if month == "01":
                    month_word = "Enero"
                elif month == "02":
                    month_word = "Febrero"
                elif month == "03":
                    month_word = "Marzo"
                elif month == "04":
                    month_word = "Abril"
                elif month == "05":
                    month_word = "Mayo"
                elif month == "06":
                    month_word = "Junio"
                elif month == "07":
                    month_word = "Julio"
                elif month == "08":
                    month_word = "Agosto"
                elif month == "09":
                    month_word = "Septiembre"
                elif month == "10":
                    month_word = "Octubre"
                elif month == "11":
                    month_word = "Noviembre"
                elif month == "12":
                    month_word = "Diciembre"

                output = "La información que tengo es del " + day + " de " + month_word + " del " + year + " a las " + hour + " y " + minutes
                self.speak(output)

def create_skill():
    return SpeakerReader()

