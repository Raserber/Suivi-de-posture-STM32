
# Variables globales à partagees entre tous les fichiers pour simplifier leur utilisation
# Pour qu'elles se partagent dynamiquement entre les fichiers il faut que les variables soient des dictionnaires


class Capteur:
    def __init__(self):
        self.connecte = False
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.gx = 0
        self.gy = 0
        self.gz = 0


machine = {"etat": "non_connecte"}  # ex: "non_connecte", "connecte", "actif", "non_actif"

batterie = {
    "pourcentage" : 0, #state of charge
    "sante" : 0, # state of health
    "tension" : 0,
    "temperature" : 0,
    "capaciteeActuelle" : 0,
    "capaciteeMaximale" : 0,
    "changement" : False
    }
capteurs = {
    "haut" : Capteur(),
    "bas" : Capteur(),
    "dt" : 200,
    "conversion_acc" : 16384,
    "conversion_gyr" : 131
    }
