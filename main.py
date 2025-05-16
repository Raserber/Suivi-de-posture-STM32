from machine import SoftI2C, Pin
import time

from mpu6050 import MPU6050

# Initialisation de l'I2C
i2c = SoftI2C(scl=Pin('D15'), sda=Pin('D14'), freq=100000)

capteur_haut = MPU6050(i2c, 0x69, "D13")
capteur_bas = MPU6050(i2c, 0x68, "A5")

devices = i2c.scan()
print("Liste devices dispos :", devices)

while True:
    print(capteur_haut.read())
    print(capteur_bas.read())
    time.sleep(2)