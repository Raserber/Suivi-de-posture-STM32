from machine import Pin

class MPU6050:
    PWR_MGMT_1 = 0x6B
    SMPLRT_DIV = 0x19
    CONFIG = 0x1A
    GYRO_CONFIG = 0x1B
    ACCEL_CONFIG = 0x1C
    ACCEL_XOUT_H = 0x3B
    GYRO_XOUT_H = 0x43

    # Configuration des plages
    DLFP_CFG_FILTER_4 = 0x04
    GYRO_CONFIG_500 = 0x08  # +/- 500dps
    ACCEL_CONFIG_4G = 0x08  # +/- 4G

    def __init__(self, i2cHandler, MPU6050_ADDR, pin_temoin_connexion):
        
        self.i2c = i2cHandler
        self.adresse = MPU6050_ADDR
        
        self.temoin_connexion = Pin(pin_temoin_connexion, Pin.IN, Pin.PULL_NONE)
        self.temoin_connexion.irq(trigger=self.temoin_connexion.IRQ_FALLING | self.temoin_connexion.IRQ_RISING, handler=self.irq)

        self.actif = self.temoin_connexion.value()
        
        self.ax, self.ay, self.az = 0, 0, 0
        self.gx, self.gy, self.gz = 0, 0, 0

        if self.actif:
            self.initialisationI2C()

    def initialisationI2C(self):
        try:
            self.i2c.writeto_mem(self.adresse, self.PWR_MGMT_1, bytes([0x00]))
            self.i2c.writeto_mem(self.adresse, self.SMPLRT_DIV, bytes([0x04]))
            self.i2c.writeto_mem(self.adresse, self.CONFIG, bytes([self.DLFP_CFG_FILTER_4]))
            self.i2c.writeto_mem(self.adresse, self.GYRO_CONFIG, bytes([self.GYRO_CONFIG_500]))
            self.i2c.writeto_mem(self.adresse, self.ACCEL_CONFIG, bytes([self.ACCEL_CONFIG_4G]))
        except Exception as e:
            return -1

    def get_raw_data(self, addr):
        if not self.actif:
            return 0

        try:
            high, low = self.i2c.readfrom_mem(self.adresse, addr, 2)
            value = (high << 8) | low
            if value > 32767:
                value -= 65536
            return value
        except Exception as e:
            return -1

    def get_accelerometre(self):
        self.ax = self.get_raw_data(self.ACCEL_XOUT_H)
        self.ay = self.get_raw_data(self.ACCEL_XOUT_H + 2)
        self.az = self.get_raw_data(self.ACCEL_XOUT_H + 4)

    def get_gyroscope(self):
        self.gx = self.get_raw_data(self.GYRO_XOUT_H)
        self.gy = self.get_raw_data(self.GYRO_XOUT_H + 2)
        self.gz = self.get_raw_data(self.GYRO_XOUT_H + 4)

    def read(self):
        self.get_accelerometre()
        self.get_gyroscope()
        
        return self.ax, self.ay, self.az, self.gx, self.gy, self.gz

    def irq(self, pin):
        
        if (self.actif == self.temoin_connexion.value()) :
            return 0;
        
        self.actif = self.temoin_connexion.value()
        
        print("Capteur", self.adresse, ":", "Actif" if self.actif else "Inactif")
        
        if self.actif:
            self.initialisationI2C()
