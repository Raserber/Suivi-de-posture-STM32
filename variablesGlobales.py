
# Variables globales à partagees entre tous les fichiers pour simplifier leur utilisation

class Batterie:
    def __init__(self):
        self.pourcentage = None        # state of charge
        self.sante = None             # state of health
        self.tension = None
        self.temperature = None
        self.capaciteeActuelle = None
        self.capaciteeMaximale = None

class Capteur:
    def __init__(self):
        self.connecte = None
        self.ax = None
        self.ay = None
        self.az = None
        self.gx = None
        self.gy = None
        self.gz = None

class Capteurs:
    def __init__(self):
        self.haut = Capteur()
        self.bas = Capteur()
        self.dt = None
        self.conversion_acc = None
        self.conversion_gyr = None

class BLEStatus:
    def __init__(self):
        self.connecte = False

class Payload:
    def __init__(self):
        self.machineEtat = ""  # ex: "non_connecte", "connecte", "actif", "non_actif"
        self.batterie = Batterie()
        self.capteurs = Capteurs()
        self.BLE = BLEStatus()


payload = Payload()