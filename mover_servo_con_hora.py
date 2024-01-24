from machine import Pin, PWM, RTC
import utime
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

# Configuración de los pines
servo_pin = 13  # Puedes cambiar este número dependiendo del pin que uses
pwm = PWM(Pin(servo_pin))
pwm.freq(50)  # Establece la frecuencia en 50 Hz para el servo

# Función para mover el servo a un ángulo específico
def move_servo(angle):
    duty = int(((angle / 180) * 95) + 40)  # Calcula el ciclo de trabajo para el ángulo dado
    pwm.duty(duty)
    utime.sleep(0)  # Espera un segundo para que el servo se mueva

# Instancia del reloj RTC (Real-Time Clock)
rtc = RTC()

# Bucle principal para darle comida a las codornices
while True:
    # Obtener la fecha y hora actual del RTC
    hora_actual = rtc.datetime()[4]  # Índice 4 corresponde a la hora
    min_actual = rtc.datetime()[5]  # Índice 5 corresponde a los minutos
    
    # Verificar si son las 7:30 AM o las 7:30 PM
    if (hora_actual == 7 and min_actual == 30) or (hora_actual == 17 and min_actual == 50):
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