import pyb
import time

# Initialisation des LEDs ---

LED1 = pyb.LED(1)
LED2 = pyb.LED(2)
LED3 = pyb.LED(3)
# ---------------------------

def chenillard () :

    LED1.on()
    LED2.off()
    LED3.off()
    time.sleep(0.4)
    
    LED1.off()
    LED2.on()
    LED3.off()
    time.sleep(0.4)
    
    LED1.off()
    LED2.off()
    LED3.on()
    time.sleep(0.4)
    
    LED3.off()

def LEDs_blink() :
    
    # extinction de toutes les LEDs ---
    LED1.off()
    LED2.off()
    LED3.off()
    time.sleep(0.1)
    # ---------------------------------
    
    # premiere allumage ---
    LED1.on()
    LED2.on()
    LED3.on()
    time.sleep(0.25)
    LED1.off()
    LED2.off()
    LED3.off()
    time.sleep(0.1)
    # --------------------
    
    # second allumage ---
    LED1.on()
    LED2.on()
    LED3.on()
    time.sleep(0.25)
    LED1.off()
    LED2.off()
    LED3.off()
    time.sleep(0.1)
    # --------------------
    
    # troisieme allumage ---
    LED1.on()
    LED2.on()
    LED3.on()
    time.sleep(0.25)
    LED1.off()
    LED2.off()
    LED3.off()
    # --------------------
