from machine import Pin, PWM, RTC
from utime import sleep, sleep_ms
from _thread import start_new_thread
import network
import time


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

# Configuración del buzzer
buzzer = PWM(Pin(5))

tones = {
"B0": 31,"C1": 33,"CS1": 35,"D1": 37,"DS1": 39,"E1": 41,"F1": 44,"FS1": 46,
"G1": 49,"GS1": 52,"A1": 55,"AS1": 58,"B1": 62,"C2": 65,
"CS2": 69,"D2": 73,"DS2": 78,"E2": 82,"F2": 87,"FS2": 93,"G2": 98,
"GS2": 104,"A2": 110,"AS2": 117,"B2": 123,"C3": 131,"CS3": 139,
"D3": 147,"DS3": 156,"E3": 165,"F3": 175,"FS3": 185,
"G3": 196,"GS3": 208,"A3": 220,"AS3": 233,"B3": 247,"C4": 262,"CS4": 277,"D4": 294,"DS4": 311,
"E4": 330,"F4": 349,"FS4": 370,"G4": 392,"GS4": 415,"A4": 440,"AS4": 466,"B4": 494,"C5": 523,"CS5": 554,"D5": 587,"DS5": 622,"E5": 659,"F5": 698,
"FS5": 740,"G5": 784,"GS5": 831,"A5": 880,"AS5": 932,"B5": 988,"C6": 1047,"CS6": 1109,"D6": 1175,"DS6": 1245,"E6": 1319,"F6": 1397,"FS6": 1480,"G6": 1568,"GS6": 1661,
"A6": 1760,"AS6": 1865,"B6": 1976,"C7": 2093,"CS7": 2217,"D7": 2349,"DS7": 2489,"E7": 2637,"F7": 2794,"FS7": 2960,"G7": 3136,"GS7": 3322,"A7": 3520,
"AS7": 3729,"B7": 3951,"C8": 4186,"CS8": 4435,"D8": 4699,"DS8": 4978
}

mario = ["E7", "E7", 0, "E7", 0, "C7", "E7", 0, "G7", 0, 0, 0, "G6", 0, 0, 0, "C7", 0, 0, "G6",
         0, 0, "E6", 0, 0, "A6", 0, "B6", 0, "AS6", "A6", 0, "G6", "E7", 0, "G7", "A7", 0, "F7", "G7",
         0, "E7", 0,"C7", "D7", "B6", 0, 0, "C7", 0, 0, "G6", 0, 0, "E6", 0, 0, "A6", 0, "B6", 0,
         "AS6", "A6", 0, "G6", "E7", 0, "G7", "A7", 0, "F7", "G7", 0, "E7", 0,"C7", "D7", "B6", 0, 0]

# Configuración del RTC (Real-Time Clock)
rtc = RTC()

def is_7_30_pm_or_7_30_am():
    # Obtener la hora actual del RTC
    current_time = rtc.datetime()
    # Verificar si es 7:30 PM o 7:30 AM
    return (
        (current_time[4] == 22 and current_time[5] == 33) or
        (current_time[4] == 17 and current_time[5] == 50)
    )

def play_tone(frequency):
    buzzer.duty_u16(9000)
    buzzer.freq(frequency)

def be_quiet():
    buzzer.duty_u16(0)

def play_song(mysong):
    for i in range(len(mysong)):
        if mysong[i] == "P" or mysong[i] == 0:
            be_quiet()
        else:
            play_tone(tones[mysong[i]])
        sleep_ms(200)
    be_quiet()

# Bucle principal
while True:
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
        sleep(10)

