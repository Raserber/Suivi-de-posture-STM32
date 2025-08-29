
# Variables globales à partagees entre tous les fichiers pour simplifier leur utilisation

class Batterie:
    def __init__(self):
        self.pourcentage = 0       # state of charge
        self.sante = 0             # state of health
        self.tension = 0
        self.temperature = 0
        self.capaciteeActuelle = 0
        self.capaciteeMaximale = 0
        
        self.changement = False

class Capteur:
    def __init__(self):
        self.connecte = False
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


machineEtat = ""  # ex: "non_connecte", "connecte", "actif", "non_actif"
batterie = Batterie()
capteurs = {
    "haut" : Capteur(),
    "bas" : Capteur(),
    "dt" : None,
    "conversion_acc" : None,
    "conversion_gyr" : None
    }
