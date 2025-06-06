from bluetooth import BLE, UUID, FLAG_READ, FLAG_NOTIFY, FLAG_WRITE
import struct

from variablesGlobales import payload

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
        payload = self._advertising_payload(name=name)
        self.ble.gap_advertise(100_000, payload)

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
        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT
            conn_handle, _, _ = data
            self._connections.discard(conn_handle)
            self._advertise(self.name)
            print("BLE déconnecté")
        elif event == 3:  # _IRQ_GATTS_WRITE
            conn_handle, attr_handle = data
            if attr_handle == self._cmd_handle:
                cmd = self.ble.gatts_read(attr_handle)
                print("Commande reçue :", cmd)
                # Tu peux traiter ici (ex: changer un mode, déclencher un reset, etc.)

    def send_imu_data(self, data, origine="haut"):
        """
        data = tuple/list of 6 valeurs : ax, ay, az, gx, gy, gz
        origine = "haut" ou "bas"
        """
        if not self._connections:
            return

        # Ajout d’un champ d’origine (0 = haut, 1 = bas) dans le payload
        origine_code = 0 if origine == "haut" else 1

        payload = struct.pack("<Bhhhhhh",
                              origine_code,
                              int(data[0]), int(data[1]), int(data[2]),
                              int(data[3]), int(data[4]), int(data[5]))

        for conn in self._connections:
            self.ble.gatts_notify(conn, self._imu_handle, payload)

    def send_battery_info(self, pourcentageBatterie=payload.batterie.pourcentage,
                          tensionBatterie=payload.batterie.tension,
                          temperatureBatterie=payload.batterie.temperature,
                          capaciteeMaximale=payload.batterie.capaciteeMaximale):
        if not self._connections:
            return

        # Envoi pourcentage (standard)
        if pourcentageBatterie != self._pourcentageBatterie_last_sent:
            for conn in self._connections:
                self.ble.gatts_notify(conn, self._batt_handle, bytes([pourcentageBatterie]))
            self._pourcentageBatterie_last_sent = pourcentageBatterie

        # Envoi détails (custom)
        payload = struct.pack("<HhH",
                              int(tensionBatterie),           # mV
                              int(temperatureBatterie * 100),         # centièmes °C
                              int(capaciteeMaximale))         # mAh

        for conn in self._connections:
            self.ble.gatts_notify(conn, self._batt_details_handle, payload)