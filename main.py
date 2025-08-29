from machine import SoftI2C, Pin
import time

import vars_g as payload

from ble import BLEManager
from mpu6050 import MPU6050
from sparkfun import SPARKFUN

from fonctions import *

# Initialisation de l'I2C ---
i2c = SoftI2C(scl=Pin('D15'), sda=Pin('D14'), freq=100000)

# ---------------------------

# Initialisation de la communication avec le chargeur de batterie ---
sparkfun = SPARKFUN(i2c, "D12")

# -------------------------------------------------------------------

# Initialisation de la communication avec les MPU6050 ---
capteur_haut = MPU6050(i2c, 0x69, "D13", "haut")
capteur_bas = MPU6050(i2c, 0x68, "A5", "bas")

# -------------------------------------------------------

# Initialisation des variables du payload ---
payload.capteurs["dt"] = 5

payload.machineEtat = "non_connecte"

payload.batterie.pourcentage = sparkfun.read_soc()
payload.batterie.tension = sparkfun.read_voltage()
payload.batterie.temperature = sparkfun.read_temperature()
payload.batterie.capaciteeMaximale = sparkfun.read_FullChargeCapacity()
# ----------------------------------------------

# Initialisation du BLE ---
ble = BLEManager(name="STM32Test")

# -------------------------

while True :
    
    print(payload.capteurs["bas"].connecte)
    
    # tant que non connecte, retour visuel avec un chenillard
    if (payload.machineEtat == "non_connecte") :
        
        chenillard()
    
    elif (payload.machineEtat == "connecte") :
        
        LEDs_blink()
        ble.send_battery_info()
        
        payload.machineEtat = "actif"
    
    if (payload.machineEtat == "actif") :
        
        if (payload.batterie.changement) :
            ble.send_battery_info()
            payload.batterie.changement = False
        
        if (capteur_haut.actif) :
            ble.send_imu_data(capteur_haut.read(), "haut")
        
        if (capteur_bas.actif) :
            ble.send_imu_data(capteur_bas.read(), "bas")
        
        # sleep entre chaque mesure ---
        time.sleep(payload.capteurs["dt"])
        
        # -----------------------------

    elif (payload.machineEtat == "non_actif") :
        
        LED3.high()
        time.sleep(0.1)
        LED3.low()
        time.sleep(0.5)
        
        if (payload.batterie.changement) :
            ble.send_battery_info()
            payload.batterie.changement = False


