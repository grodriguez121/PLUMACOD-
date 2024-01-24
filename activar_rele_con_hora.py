from machine import Pin, RTC
import utime
import network
import time
import urequests

urlProcess = 'https://cmqj71x633.execute-api.us-east-1.amazonaws.com/pro/process'
rtc = RTC()

# Nombre y contraseña de la red Wi-Fi
SSID = "TIGO_WIFI"
PASSWORD = "WF7KR662*@"

# Configurar la conexión Wi-Fi
sta_if = network.WLAN(network.STA_IF)

# Verificar si la conexión está activada
if not sta_if.isconnected():
    print('Conectando a la red Wi-Fi...')
    sta_if.active(True)  # Activar la interfaz de red
    
    # Conectar a la red Wi-Fi
    sta_if.connect(SSID, PASSWORD)
    
    # Esperar hasta que se conecte
    while not sta_if.isconnected():
        time.sleep(1)

print('Conexión exitosa a la red Wi-Fi')
print('Dirección IP:', sta_if.ifconfig()[0])


# Configuración del pin del relé
pin_rele = Pin(14, Pin.OUT)  # Puedes cambiar este número según tu configuración

# Función para activar el relé
def activate_relay():
    pin_rele.value(1)  # Activa el relé

# Función para desactivar el relé
def deactivate_relay():
    pin_rele.value(0)  # Desactiva el relé

# Bucle principal
while True:
    hora_actual = utime.localtime()[3]  # Obtener la hora actual (0-23)
    min_actual = utime.localtime()[4]   # Obtener el minuto actual
    
    # Verificar si son las 6:15 PM
    if hora_actual == 17 and min_actual == 50:
        activate_relay()  # Activa el relé
        print("\nSE PRENDE BOMBILLO")
        
        id_proceso = 'A3656_' + "{}{:02d}{:02d}".format(RTC().datetime()[0], RTC().datetime()[1], RTC().datetime()[2]) + "{:02d}{:02d}{:02d}".format(RTC().datetime()[4], RTC().datetime()[5], RTC().datetime()[6])
        fecha_actual = "{}/{:02d}/{:02d}".format(RTC().datetime()[0], RTC().datetime()[1], RTC().datetime()[2]) + ' ' + "{:02d}:{:02d}:{:02d}".format(RTC().datetime()[4], RTC().datetime()[5], RTC().datetime()[6])
        payloadon = {'id_process': id_proceso ,'dat_datetime_ini': fecha_actual,'dat_datetime_fin': '','str_estado': 'Prendido', 'str_evento': 'Control iluminacion Automatico','str_gramos': '','str_temperatura': ''}
        responseon = urequests.post(urlProcess, json=payloadon)
        gc.collect()
        responseon.close()
        
    # Verificar si son las 6:40 AM
    if hora_actual == 17 and min_actual == 55:
        deactivate_relay()  # Desactiva el relé
        print("SE APAGA BOMBILLO")
        
        id_proceso = 'A3656_' + "{}{:02d}{:02d}".format(RTC().datetime()[0], RTC().datetime()[1], RTC().datetime()[2]) + "{:02d}{:02d}{:02d}".format(RTC().datetime()[4], RTC().datetime()[5], RTC().datetime()[6])
        fecha_actual = "{}/{:02d}/{:02d}".format(RTC().datetime()[0], RTC().datetime()[1], RTC().datetime()[2]) + ' ' + "{:02d}:{:02d}:{:02d}".format(RTC().datetime()[4], RTC().datetime()[5], RTC().datetime()[6])
        payloadon = {'id_process': id_proceso ,'dat_datetime_ini': fecha_actual,'dat_datetime_fin': '','str_estado': 'Apagado', 'str_evento': 'Control iluminacion Automatico','str_gramos': '','str_temperatura': ''}
        responseon = urequests.post(urlProcess, json=payloadon)
        gc.collect()
        responseon.close()    
    utime.sleep(60)  # Espera 1 minuto antes de verificar nuevamente+