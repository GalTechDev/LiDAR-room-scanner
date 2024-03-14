from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo
from serial import Serial
import time

def get_connected_port():
    result: list[ListPortInfo] = []
    ports = list_ports.comports()
    for p in ports:
        if "SERIAL" in p[1]:
            result.append(p[0])
    return result

class Arduino:
    def __init__(self, port, baudrate=115200) -> None:
        self.port = port
        self.baudrate = baudrate
        self.arduino = Serial(self.port, baudrate=self.baudrate, timeout=1)

    def get_data(self):
        while True:
            raw_data = self.arduino.readline().decode().strip()
            if raw_data == "END":
                break 
            elif raw_data:
                data = raw_data.split(';')
                if len(data) == 3:
                    try:
                        for value in data:
                            yield float(value)
                    except ValueError:
                        print("Erreur lors de la conversion des valeurs en float")
                else:
                    print("Les données reçues ne sont pas au bon format")
            else:
                print("Pas de données reçues de l'Arduino")

    def start(self, min_h:float, max_h: float, min_v:float, max_v:float, res: int):
        while True:
            commande_a_envoyer = f"{chr(0)}START;{min_h};{max_h};{min_v};{max_v};{res}{chr(10)}"
            self.arduino.write(commande_a_envoyer.encode())
            while True:
                try:
                    reponse = self.arduino.readline().decode().strip()
                    if reponse == "capture":
                        return self.read_data(self.arduino)
                    if reponse == "erreur":
                        break
                    print(reponse)
                except ValueError:
                        print("Erreur lors de la communication")

    def stop(self):
        pass

if __name__ == "__main__":
    while True:
        print(get_connected_port())
        time.sleep(1)