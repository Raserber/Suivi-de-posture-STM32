from machine import SoftI2C, Pin
import time

from variablesGlobales import payload

from ble import BLEManager
from mpu6050 import MPU6050
from sparkfun import SPARKFUN

from fonctions import *

# Initialisation des LEDs ---

LED1 = pyb.LED(1)
LED2 = pyb.LED(2)
LED3 = pyb.LED(3)
# ---------------------------

# Initialisation de l'I2C ---
i2c = SoftI2C(scl=Pin('D15'), sda=Pin('D14'), freq=100000)

# ---------------------------

# Initialisation de la communication avec le chargeur de batterie ---
sparkfun = SPARKFUN(i2c, "D12")

# -------------------------------------------------------------------

# Initialisation de la communication avec les MPU6050 ---
capteur_haut = MPU6050(i2c, 0x69, "D13", position="haut")
capteur_bas = MPU6050(i2c, 0x68, "A5", position="bas")

# -------------------------------------------------------

# Initialisation des variables du payload ---
payload.capteurs.dt = 500

payload.machineEtat = "non_connecte"

payload.batterie.pourcentage = sparkfun.read_soc()
payload.batterie.tension = sparkfun.read_voltage()
payload.batterie.temperature = sparkfun.read_temperature()
payload.batterie.capaciteeMaximale = sparkfun.read_FullChargeCapacity()
# ----------------------------------------------

# Initialisation du BLE ---
ble = BLEManager(name="FAME_IUT1Test")

# -------------------------

while True :
    
    # tant que non connecte, retour visuel avec un chenillard
    if (payload.machineEtat == "non_connecte") :
        
        chenillard()
    
    else if (payload.machineEtat == "connecte") :
        
        LEDs_blink()
        ble.send_battery_info()
        
        payload.machineEtat = "actif"
    
    if (payload.machineEtat == "actif") :
        
        if (capteur_haut.actif) :
            ble.send_imu_data(capteur_haut.read())
        
        if (capteur_bas.actif) :
            ble.send_imu_data(capteur_bas.read())
        
        # sleep entre chaque mesure ---
        time.sleep(payload.capteurs.dt)
        
        # -----------------------------

    else if (payload.machineEtat == "non_actif") :
        
        LED3.high()
        time.sleep(0.1)
        LED3.low()
        time.sleep(0.5)
        
    if (payload.batterie.changement) :
        ble.send_battery_info()
        payload.batterie.changement = False
