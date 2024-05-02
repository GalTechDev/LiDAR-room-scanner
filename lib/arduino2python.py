from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo
from serial import Serial
import time
from threading import Thread

WAITING = 1
SCANNING = 2


def get_connected_port():
    ports = list_ports.comports()
    return [port.device for port in ports]
   

class Arduino:
    gen_parameter = {
        "res":None,
        "min_h":None,
        "max_h":None,
        "min_v":None,
        "max_v":None,
    }
    def __init__(self, port, baudrate=115200) -> None:
        self.port = port
        self.baudrate = baudrate
        self.arduino = Serial(self.port, baudrate=self.baudrate, timeout=1) if self.port != None else None

        self.data_x = []
        self.data_y = []
        self.data_z = []

        self.status = WAITING
        self.thread = None

    def set_gen_parameter(self, h_value, v_value, res):
        self.gen_parameter["res"]=res 
        self.gen_parameter["min_h"]=h_value[0] 
        self.gen_parameter["max_h"]=h_value[1]
        self.gen_parameter["min_v"]=v_value[0] 
        self.gen_parameter["max_v"]=v_value[1]

    def get_data(self):
        return (self.data_x, self.data_y, self.data_z)
    
    def get_data_thread(self):
        while True:
            raw_data = self.arduino.readline().decode().strip()
            if raw_data == "END":
                break 
            elif raw_data:
                data = raw_data.split(';')
                if len(data) == 3:
                    try:
                        self.data_x.append(float(data[0]))
                        self.data_y.append(float(data[1]))
                        self.data_z.append(float(data[2]))
                    except ValueError:
                        print("Erreur lors de la conversion des valeurs en float")
                else:
                    print("Les données reçues ne sont pas au bon format")
            else:
                print("Pas de données reçues de l'Arduino")
        self.status = WAITING

    def start(self, min_h: float, max_h: float, min_v: float, max_v: float, res: int):
        if None in [min_h, max_h, min_v, max_v, res]:
            print("Error on parametters")
            print(min_h, max_h, min_v, max_v, res)
            return
        if self.status == WAITING:
            commande_a_envoyer = f"START;{min_h};{max_h};{min_v};{max_v};{res}"
            self.arduino.write(commande_a_envoyer.encode())
            while True:
                try:
                    b_reponse = self.arduino.readline()
                    reponse = b_reponse.decode().strip()
                    if reponse == "CAPTURE":
                        self.status = SCANNING
                        self.thread = Thread(target=Arduino.get_data_thread, args=[self])
                        self.thread.start()
                        return
                    else:
                        self.arduino.write(commande_a_envoyer.encode())

                except ValueError as e:
                    print("Erreur lors de la communication")
                    print(e)
        else:
            return

    def stop(self):
        if self.status == SCANNING:
            commande_a_envoyer = f"STOP"
            self.arduino.write(commande_a_envoyer.encode())


class FakeArduino(Arduino):
    def __init__(self) -> None:
        super().__init__(None)

if __name__ == "__main__":
    while True:
        print(get_connected_port())
        arduino = Arduino(get_connected_port()[int(input())])
        arduino.start(0.0, 360.0,0.0,90.0,5.0)
        while True:
            print("\nnew get")
            print(arduino.get_data())
            time.sleep(1)