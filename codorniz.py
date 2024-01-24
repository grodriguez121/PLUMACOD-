# Modulos o librerias
from machine import Pin, PWM, RTC
import network, time, utime
from utime import sleep, sleep_ms
from _thread import start_new_thread
from mario import play_tone, be_quiet, play_song, is_7_30_pm_or_7_30_am  # Obtener la hora act
import urequests

# objetos

# Configuración de los pines
buzzer = PWM(Pin(5))
servo_pin = 13  # Puedes cambiar este número dependiendo del pin que uses
pwm = PWM(Pin(servo_pin))
pwm.freq(50)  # Establece la frecuencia en 50 Hz para el servo
# Instancia del reloj RTC (Real-Time Clock)
rtc = RTC()
pin_rele = Pin(14, Pin.OUT)



urlProcess = 'https://cmqj71x633.execute-api.us-east-1.amazonaws.com/pro/process'

# Funciones
# Función para mover el servo a un ángulo específico
def move_servo(angle):
    duty = int(((angle / 180) * 95) + 40)  # Calcula el ciclo de trabajo para el ángulo dado
    pwm.duty(duty)
    utime.sleep(0)  # Espera un segundo para que el servo se mueva

# Función para activar el relé
def activate_relay():
    pin_rele.value(1)  # Activa el relé

# Función para desactivar el relé
def deactivate_relay():
    pin_rele.value(0)  # Desactiva el relé



def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True



if conectaWifi ("TIGO_WIFI", "WF7KR662*@"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
      
    while True:
    # Obtener la fecha y hora actual del RTC
        hora_actual = rtc.datetime()[4]  # Índice 4 corresponde a la hora
        min_actual = rtc.datetime()[5]  # Índice 5 corresponde a los minutos
    
        # Verificar si son las 7:30 AM o las 7:30 PM
        if (hora_actual == 7 and min_actual == 30) or (hora_actual == 19 and min_actual == 12):
            # Mueve el servo a 90 grados
            move_servo(90)
            utime.sleep(0)  # Espera 0 segundos
            
            # Vuelve el servo a 0 grados
            move_servo(0)
            utime.sleep(0.5)  # Espera medio segundo para dar 25 gramos de cuido
            print("\n SE DA EL CUIDO A LAS CODORNICES \n")
     
            
            # Mueve el servo a 90 grados
            move_servo(90)
            print(" SE TERMINA DE DAR EL CUIDO A LAS CODORNICES")
                   
            
            utime.sleep(60)  # Espera un minuto antes de verificar la hora nuevamente
        else:
            utime.sleep(10)  # Espera 10 segundos antes de verificar la hora nuevamente
        
        
        # Verificar si es 7:30 PM o 7:30 AM
        if is_7_30_pm_or_7_30_am():
            # Reproducir la canción completa
            play_song(mario)
            # Esperar hasta que sea 7:31 PM o 7:31 AM antes de volver a verificar
            while is_7_30_pm_or_7_30_am():
                sleep(1)
        else:
            # Si no es la hora específica, mantener el buzzer apagado
            be_quiet()
            # Esperar un tiempo antes de verificar nuevamente
            sleep(1)  # Puedes ajustar este tiempo según tus preferencias
        
        # Verificar si son las 6:15 PM
        if hora_actual == 19 and min_actual == 16:
            activate_relay()  # Activa el relé
            print("\nSE PRENDE BOMBILLO")
        
            id_proceso = 'A3656_' + "{}{:02d}{:02d}".format(RTC().datetime()[0], RTC().datetime()[1], RTC().datetime()[2]) + "{:02d}{:02d}{:02d}".format(RTC().datetime()[4], RTC().datetime()[5], RTC().datetime()[6])
            fecha_actual = "{}/{:02d}/{:02d}".format(RTC().datetime()[0], RTC().datetime()[1], RTC().datetime()[2]) + ' ' + "{:02d}:{:02d}:{:02d}".format(RTC().datetime()[4], RTC().datetime()[5], RTC().datetime()[6])
            payloadon = {'id_process': id_proceso ,'dat_datetime_ini': fecha_actual,'dat_datetime_fin': '','str_estado': 'Prendido', 'str_evento': 'Control iluminacion Automatico','str_gramos': '','str_temperatura': ''}
            responseon = urequests.post(urlProcess, json=payloadon)
            gc.collect()
            responseon.close()
        
        # Verificar si son las 6:40 AM
        if hora_actual == 19 and min_actual == 18:
            deactivate_relay()  # Desactiva el relé
            print("SE APAGA BOMBILLO")
        
            id_proceso = 'A3656_' + "{}{:02d}{:02d}".format(RTC().datetime()[0], RTC().datetime()[1], RTC().datetime()[2]) + "{:02d}{:02d}{:02d}".format(RTC().datetime()[4], RTC().datetime()[5], RTC().datetime()[6])
            fecha_actual = "{}/{:02d}/{:02d}".format(RTC().datetime()[0], RTC().datetime()[1], RTC().datetime()[2]) + ' ' + "{:02d}:{:02d}:{:02d}".format(RTC().datetime()[4], RTC().datetime()[5], RTC().datetime()[6])
            payloadon = {'id_process': id_proceso ,'dat_datetime_ini': fecha_actual,'dat_datetime_fin': '','str_estado': 'Apagado', 'str_evento': 'Control iluminacion Automatico','str_gramos': '','str_temperatura': ''}
            responseon = urequests.post(urlProcess, json=payloadon)
            gc.collect()
            responseon.close()    
        utime.sleep(10)  # Espera 10 seg antes de verificar nuevamente
      
    
 
else:
       print ("Imposible conectar")
       miRed.active (False)
