from machine import Pin, I2C, RTC
import time
from dht import DHT11
from sh1106 import SH1106_I2C
import framebuf
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

# Configuración del reloj en tiempo real (RTC)
rtc = RTC()

# Configuración del sensor DHT11
DHT_PIN = 12  # Cambia al pin que estás utilizando para el sensor DHT
dht_sensor = DHT11(Pin(DHT_PIN))

# Configuración del display OLED SH1106
ancho = 128
alto = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SH1106_I2C(ancho, alto, i2c)
print(i2c.scan())

def get_formatted_time():
    time_tuple = rtc.datetime()
    hour = time_tuple[4]
    minute = time_tuple[5]
    
    am_pm = "AM"
    if hour >= 12:
        am_pm = "PM"
        if hour > 12:
            hour -= 12

    return "{:02d}:{:02d} {}".format(hour, minute, am_pm)

while True:
    # Limpiar la pantalla
    oled.fill(0)

    # Muestra el título "PlumaCod" con un icono de pollo
    oled.text("<PlumaCod>", 5, 0)
    def buscar_icono(ruta):
        dibujo = open(ruta, "rb")  # Abrir en modo lectura de bist
        dibujo.readline() # metodo para ubicarse en la primera linea de los bist
        xy = dibujo.readline() # ubicarnos en la segunda linea
        x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
        y = int(xy.split()[1])
        icono = bytearray(dibujo.read())  # guardar en matriz de bites
        dibujo.close()
        return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)

    oled.blit(buscar_icono("plumacod/codo.pbm"), 97, 0) # ruta y sitio de ubicación
 
    
    # Lee la temperatura y la humedad
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()

    # Muestra la temperatura y humedad
    oled.text("Temp:{:.2f} C".format(temperature), 0, 14)
    oled.text("Hum:{:.2f} %".format(humidity), 0, 25)
    
    print("")
    print("Temp:{:.2f} °C".format(temperature))
    print("Hum:{:.2f} %".format(humidity))
    

    # Muestra el título "Hora Actual" con un icono de reloj
    oled.text("Hora Actual:", 0, 43)

    # Muestra la hora actual en formato de 12 horas con AM y PM
    current_time = get_formatted_time()
    oled.text(current_time, 0, 54)
    
        # Actualiza la pantalla
    oled.show()
    time.sleep(2)