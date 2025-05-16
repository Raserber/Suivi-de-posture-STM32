import bluetooth
import time
import struct

# Initialisation du Bluetooth LE
ble = bluetooth.BLE()
ble.active(True)

# UUIDs du service et de la caractéristique
UUID_SERVICE = bluetooth.UUID(0x180C)
UUID_CHARACTERISTIC = bluetooth.UUID(0x2A56)

# Enregistrement du service
SERVICE = (UUID_SERVICE, ((UUID_CHARACTERISTIC, bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY),))
SERVICES = (SERVICE,)
handles = ble.gatts_register_services(SERVICES)
handle = handles[0][0]  # Récupération correcte du handle

# Fonction d'annonce BLE
def ble_advertise():
    name = b"STM32_BLE"
    adv_data = b"\x02\x01\x06" + bytes([len(name) + 1, 0x09]) + name
    ble.gap_advertise(50, adv_data)  # Intervalle de publicité réduit à 50 ms
    print("Annonce BLE en cours...")

# Fonction pour envoyer les données BLE
def send_ble_data():
    #ax, ay, az, gx, gy, gz = get_sensor_data()
    data = struct.pack("hhhhhh", ax, ay, az, gx, gy, gz)
    ble.gatts_write(handle, data)
    print(f"Accel: {ax}, {ay}, {az} | Gyro: {gx}, {gy}, {gz}")

# Fonction de rappel pour les événements BLE
def on_connect(event, data):
    if event == bluetooth.EVENT_CONNECT:
        print("Périphérique connecté.")
        ble.gap_advertise(None)  # Arrêter la publicité lorsque connecté
    elif event == bluetooth.EVENT_DISCONNECT:
        print("Périphérique déconnecté.")
        ble_advertise()  # Redémarrer la publicité lorsque déconnecté

# Enregistrement des rappels
ble.irq(on_connect)
ble_advertise()

while True:
    send_ble_data()
    time.sleep(0.5)
    
    # TODO : Implémenter le BLE pour utilisation finale