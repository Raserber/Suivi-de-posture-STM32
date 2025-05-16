from machine import Pin

class MPU6050:
    
    PWR_MGMT_1 = 0x6B
    SMPLRT_DIV = 0x19
    CONFIG = 0x1A
    GYRO_CONFIG = 0x1B
    ACCEL_CONFIG = 0x1C
    ACCEL_XOUT_H = 0x3B
    GYRO_XOUT_H = 0x43

    #Configuration des plages
    DLFP_CFG_FILTER_4 = 0x04
    GYRO_CONFIG_500 = 0x08  # +/- 500dps
    ACCEL_CONFIG_4G = 0x08  # +/- 4G
    
    def __init__(self, i2cHandler, MPU6050_ADDR, pin_temoin_connexion) :

        self.i2c = i2cHandler

        self.adresse = MPU6050_ADDR

        self.temoin_connexion = Pin(pin_temoin_connexion, Pin.IN, Pin.PULL_DOWN)
        self.temoin_connexion.irq(trigger=self.temoin_connexion.IRQ_FALLING|self.temoin_connexion.IRQ_RISING, handler=self.irq)

        self.actif = self.temoin_connexion.value()

        self.ax = 0
        self.ay = 0
        self.az = 0
        self.gx = 0
        self.gy = 0
        self.gz = 0


        if (self.actif) :

            self.initialisationI2C()

    def initialisationI2C(self) :

        self.i2c.writeto_mem(self.adresse, self.PWR_MGMT_1, bytes([0x00]))
        self.i2c.writeto_mem(self.adresse, self.SMPLRT_DIV, bytes([0x04]))
        self.i2c.writeto_mem(self.adresse, self.CONFIG, bytes([self.DLFP_CFG_FILTER_4]))
        self.i2c.writeto_mem(self.adresse, self.GYRO_CONFIG, bytes([self.GYRO_CONFIG_500]))
        self.i2c.writeto_mem(self.adresse, self.ACCEL_CONFIG, bytes([self.ACCEL_CONFIG_4G]))

    # Lecture des données brutes
    def get_raw_data(self, addr) :

        if (self.actif == 0) :

            return 0

        high, low = self.i2c.readfrom_mem(self.adresse, addr, 2)
        value = (high << 8) | low
        if value > 32767:
            value -= 65536
        return value

    # Récupération des valeurs de l'accéléromètre
    def get_accelerometre(self):
        self.ax = self.get_raw_data(self.ACCEL_XOUT_H)
        self.ay = self.get_raw_data(self.ACCEL_XOUT_H + 2)
        self.az = self.get_raw_data(self.ACCEL_XOUT_H + 4)

    # Récupération des valeurs du gyroscope
    def get_gyroscope(self) :
        self.gx = self.get_raw_data(self.GYRO_XOUT_H)
        self.gy = self.get_raw_data(self.GYRO_XOUT_H + 2)
        self.gz = self.get_raw_data(self.GYRO_XOUT_H + 4)

    # variable publique pour la lecture
    def read(self) :

        self.get_accelerometre()
        self.get_gyroscope()

        return self.ax, self.ay, self.az, self.gx, self.gy, self.gz

    def irq(self, pin) :
        
        if (self.actif != self.temoin_connexion.value()) :
            
            self.actif = self.temoin_connexion.value()
            print("capteur ", self.adresse, " : ", self.actif)

            if (self.actif) :

                self.initialisationI2C()
