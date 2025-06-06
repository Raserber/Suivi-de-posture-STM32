from machine import Pin, I2C
import time

class SPARKFUN:
    
    adresse_lecture = 0x55  # 7-bit address
    adresse_ecriture = 0x55
    
    # Lecture seule
    Voltage = 0x04
    StateOfCharge = 0x1C
    InternalTemperature = 0x1E
    StateOfHealth = 0x20
    Flags = 0x06
    TrueRemainingCapacity = 0x6A
    FullChargeCapacity = 0x0A

    # Lecture/écriture
    Control = 0x00

    def __init__(self, i2cHandler, pin_interuption):
        self.i2c = i2cHandler

        # Test de présence
        if self.adresse_lecture not in self.i2c.scan():
            raise Exception("bq27441 non détecté sur le bus I2C")

        # Configuration du GPIO d'interruption si précisé
        self.gpout = Pin(pin_interuption, Pin.IN, Pin.PULL_DOWN)
        self.gpout.irq(trigger=Pin.IRQ_RISING, handler=self.irq)

    def read16(self, reg):
        """Lit un registre 16 bits (LSB + MSB)."""
        self.i2c.writeto(self.adresse_ecriture, bytes([reg]))
        time.sleep_us(70)  # tBUF ≥ 66µs
        data = self.i2c.readfrom(self.adresse_lecture, 2)
        return data[0] | (data[1] << 8)

    def read_voltage(self):
        return self.read16(self.Voltage)

    def read_soc(self):
        return self.read16(self.StateOfCharge)

    def read_temperature(self):
        raw = self.read16(self.InternalTemperature)
        return (raw / 10.0) - 273.15  # Conversion 0.1 K → °C
    
    def read_trueRemainingCapacity(self):
        return self.read16(self.TrueRemainingCapacity)
    
    
    def read_FullChargeCapacity(self):
        return self.read16(self.FullChargeCapacity)
    

    def read_soh(self):
        raw = self.read16(self.StateOfHealth)
        percentage = raw & 0xFF
        status = (raw >> 8) & 0xFF
        return (percentage, status)

    def control_command(self, subcommand):
        """Envoie une sous-commande Control()"""
        cmd = bytes([self.Control, subcommand & 0xFF, (subcommand >> 8) & 0xFF])
        self.i2c.writeto(self.adresse_ecriture, cmd)
        time.sleep_us(70)

    def irq(self, pin):
        """Callback appelée sur front descendant de GPOUT."""
        
        payload.batterie.pourcentage = sparkfun.read_soc()
        payload.batterie.tension = sparkfun.read_voltage()
        payload.batterie.temperature = sparkfun.read_temperature()
        payload.batterie.capaciteeMaximale = sparkfun.read_FullChargeCapacity()
        
        payload.batterie.changement = True

    
    # TODO : instrumenter StateOfHealth pour pourcentage réel de charge
    # TODO : Configurer le pin GPOUT en pull-down et avertissement à chaque changement de pourcentage
    # TODO : réflechir à aller chercher informations supplementaires quand batterie basse (tension, capacité restante ...)
    # TODO : aller chercher capacité réelle que lors du démarrage et autres informations non changeantes rapidement
    

