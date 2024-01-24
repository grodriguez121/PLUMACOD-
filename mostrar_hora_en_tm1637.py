from machine import Pin
import tm1637
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

# Definir los pines CLK y DIO
pin_clk = Pin(23, Pin.OUT)
pin_dio = Pin(19, Pin.OUT)

# Crear un objeto TM1637 con los pines CLK y DIO
display = tm1637.TM1637(clk=pin_clk, dio=pin_dio)

# Función para mostrar la hora en el display
def mostrar_hora(hora, minutos):
    # Formatear la hora y los minutos
    hora_str = "{:02d}".format(hora)
    minutos_str = "{:02d}".format(minutos)

    # Crear un string con la hora y minutos
    hora_completa = hora_str + minutos_str

    # Mostrar en el display
    display.show(hora_completa)

# Bucle principal
while True:
    # Simulación de obtener la hora actual
    hora_actual = time.localtime()
    hora, minutos = hora_actual[3], hora_actual[4]

    mostrar_hora(hora, minutos)
    print("hora:", hora,"minutos:", minutos)
    time.sleep(1)