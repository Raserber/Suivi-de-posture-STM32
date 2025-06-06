import pyb

def chenillard () :

    LED1.high()
    LED2.low()
    LED3.low()
    time.sleep(0.2)
    
    LED1.low()
    LED2.high()
    LED3.low()
    time.sleep(0.2)
    
    LED1.low()
    LED2.low()
    LED3.high()
    time.sleep(0.2)
    
    LED3.low()

def LEDs_blink() :
    
    # extinction de toutes les LEDs ---
    LED1.low()
    LED2.low()
    LED3.low()
    time.sleep(0.1)
    # ---------------------------------
    
    # premiere allumage ---
    LED1.high()
    LED2.high()
    LED3.high()
    time.sleep(0.25)
    LED1.low()
    LED2.low()
    LED3.low()
    time.sleep(0.1)
    # --------------------
    
    # second allumage ---
    LED1.high()
    LED2.high()
    LED3.high()
    time.sleep(0.25)
    LED1.low()
    LED2.low()
    LED3.low()
    time.sleep(0.1)
    # --------------------
    
    # troisieme allumage ---
    LED1.high()
    LED2.high()
    LED3.high()
    time.sleep(0.25)
    LED1.low()
    LED2.low()
    LED3.low()
    # --------------------