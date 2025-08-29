from bluetooth import BLE, UUID, FLAG_READ, FLAG_NOTIFY, FLAG_WRITE
import struct
import pyb
import time

import vars_g as payload

LED1 = pyb.LED(1)

class BLEManager:
    def __init__(self, name="SensorNode"):
        self.ble = BLE()
        self.ble.active(True)
        self.ble.irq(self._irq)

        self.name = name
        self._connections = set()
        self._pourcentageBatterie_last_sent = None

        # UUIDs mis à jour
        self._uuid_batt_svc = UUID(0x180F)
        self._uuid_batt_level = UUID(0x2A19)

        self._uuid_custom_svc = UUID("04dbe0ce-7da7-4629-b2c1-7b6389fd5290")
        self._uuid_imu_char = UUID("150b83fc-1440-4104-b232-4e61ebc94322")
        self._uuid_batt_details_char = UUID("775b6cf8-f951-41ff-9eb1-b37469b4ed64")
        self._uuid_cmd_char = UUID("c6183eb2-ce58-46c1-82de-c96e5033d7a4")

        self._batt_handle = None
        self._imu_handle = None
        self._batt_details_handle = None
        self._cmd_handle = None

        self._register_services()
        self._advertise(self.name)

    def _register_services(self):
        # Service batterie (standard)
        batt_service = (
            self._uuid_batt_svc,
            ((self._uuid_batt_level, FLAG_READ | FLAG_NOTIFY),)
        )

        # Service custom : IMU (notify), batterie détails (notify), commande (write)
        custom_service = (
            self._uuid_custom_svc,
            (
                (self._uuid_imu_char, FLAG_NOTIFY),
                (self._uuid_batt_details_char, FLAG_NOTIFY),
                (self._uuid_cmd_char, FLAG_WRITE),
            )
        )

        services = (batt_service, custom_service)
        handles = self.ble.gatts_register_services(services)

        ((self._batt_handle,), (self._imu_handle, self._batt_details_handle, self._cmd_handle)) = handles

    def _advertise(self, name):
        payload_BLE = self._advertising_payload(name=name)
        self.ble.gap_advertise(100_000, payload_BLE)

    def _advertising_payload(self, name):
        return bytearray(
            b'\x02\x01\x06' +                     # Flags
            bytes([len(name) + 1, 0x09]) +        # Complete name
            name.encode('utf-8')
        )

    def _irq(self, event, data):
        if event == 1:  # _IRQ_CENTRAL_CONNECT
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("BLE connecté")
            
            payload.machine["etat"] = "connecte"
            
        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT
            conn_handle, _, _ = data
            self._connections.discard(conn_handle)
            self._advertise(self.name)
            print("BLE déconnecté")
            
            payload.machine["etat"] = "non_connecte"
            
        elif event == 3:  # _IRQ_GATTS_WRITE
            conn_handle, attr_handle = data
            if attr_handle == self._cmd_handle:
                cmd = self.ble.gatts_read(attr_handle)
                print("Commande reçue :", cmd)
                
                if (cmd == 0) :
                    
                    payload.machine["etat"] = "non_connecte"

    def send_imu_data(self, data, origine="haut"):
        """
        data = tuple/list of 6 valeurs : ax, ay, az, gx, gy, gz
        origine = "haut" ou "bas"
        """
    
        if not self._connections:
            return
        
        LED1.on()
        # Ajout d’un champ d’origine (0 = haut, 1 = bas) dans le payload
        if (origine == "haut") :
            origine_code = 1
        elif (origine == "bas") :
            origine_code = 0
            
        payload = struct.pack("<Bhhhhhh",
                              origine_code,
                              int(data[0]), int(data[1]), int(data[2]),
                              int(data[3]), int(data[4]), int(data[5]))

        for conn in self._connections:
            self.ble.gatts_notify(conn, self._imu_handle, payload)

        
        LED1.off()
        
    def send_battery_info(self) :
        
        if not self._connections:
            return

        LED1.on()
        
        # Envoi pourcentage (standard)
        if payload.batterie["pourcentage"] != self._pourcentageBatterie_last_sent:
            for conn in self._connections:
                self.ble.gatts_notify(conn, self._batt_handle, bytes([payload.batterie["pourcentage"]]))
            self._pourcentageBatterie_last_sent = payload.batterie["pourcentage"]

        # Envoi détails (custom)
        payload_BLE = struct.pack("<HhHHHH",
                              int(payload.batterie["tension"]),                 # mV
                              int(payload.batterie["temperature"] * 100),       # centièmes °C
                              int(payload.batterie["capaciteeMaximale"]),               # mAh
                              int(payload.capteurs["dt"]*1000),        # ms
                              int(payload.capteurs["conversion_acc"]),
                              int(payload.capteurs["conversion_gyr"]))
                            

        for conn in self._connections:
            self.ble.gatts_notify(conn, self._batt_details_handle, payload_BLE)

        LED1.off()
