
import serial
import serial.tools.list_ports
import threading

class SerialReader:
    def __init__(self):
        self.serial_port = None
        self.running = False
        self.time_data = []
        self.power_percent_data = []
        self.thrust_data = []
        self.electrical_power_data = []

    def list_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self, port):
        self.serial_port = serial.Serial(port, 9600, timeout=1)

    def start(self):
        if self.serial_port and self.serial_port.is_open:
            self.running = True
            threading.Thread(target=self.read_serial, daemon=True).start()

    def stop(self):
        self.running = False

    def read_serial(self):
        while self.running:
            try:
                line = self.serial_port.readline().decode('utf-8').strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 4:
                        t, p, thrust, e_power = map(float, parts)
                        self.time_data.append(t)
                        self.power_percent_data.append(p)
                        self.thrust_data.append(thrust)
                        self.electrical_power_data.append(e_power)
            except:
                pass

    def get_data(self):
        return {
            'time': self.time_data,
            'power_percent': self.power_percent_data,
            'thrust': self.thrust_data,
            'electrical_power': self.electrical_power_data
        }
