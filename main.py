from machine import SoftI2C, Pin
import time

from ble import BLEManager
from mpu6050 import MPU6050
from sparkfun import SPARKFUN


# Initialisation de l'I2C
i2c = SoftI2C(scl=Pin('D15'), sda=Pin('D14'), freq=100000)

sparkfun = SPARKFUN(i2c, "D12")
capteur_haut = MPU6050(i2c, 0x69, "D13", position="haut")
capteur_bas = MPU6050(i2c, 0x68, "A5", position="bas")

print(capteur_haut.read())
ble = BLEManager(name="STM32TestLounes")

while True :
    time.sleep(0.1)
    
    ble.send_imu_data(capteur_bas.read())
    



ble.send_imu_data(capteur_bas.read())
ble.send_battery_info(soc, voltage, temperature, capacity)

soc = sparkfun.read_soc()
voltage = sparkfun.read_voltage()
temperature = sparkfun.read_temperature()
capacity = sparkfun.read_FullChargeCapacity()

print("scan I2C :", i2c.scan())
print("voltage :", sparkfun.read_voltage()/1000, "V")
print("state of charge :", sparkfun.read_soc(), "%")
print("temp :", sparkfun.read_temperature(), "°C")
print("capacite :", sparkfun.read_trueRemainingCapacity(), "mAh")
print("capacite max :", sparkfun.read_FullChargeCapacity(), "mAh")
print("state of health :", sparkfun.read_soh()[0], "%, code ", sparkfun.read_soh()[1])
