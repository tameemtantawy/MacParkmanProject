import math
import serial

class Sensor:
    def __init__(self, port):
        self.port = port
        self.ser = None
        self.connected = False
        self.active = False
        self.x = 0
        self.y = 0
        self.z = 0
        self.column = "neutral"

    def connect(self):
        try:
            self.ser = serial.Serial(f"COM{self.port}", 115200, timeout=1)
            self.connected = True
        except serial.SerialException:
            self.connected = False

    def read_data(self):
        if self.connected and self.ser:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 5:
                        self.x = float(parts[2])
                        self.y = float(parts[3])
                        self.z = float(parts[4])
                        return True
            except (ValueError, TypeError, serial.SerialException):
                pass
        return False

    def close(self):
        if self.ser:
            self.ser.close()

class SensorManager:
    def __init__(self):
        self.sensors = [Sensor(i) for i in range(1, 9)]
        self.total_x_external = 0
        self.total_y_external = 0
        self.total_z_external = 0
        self.total_x_internal = 0
        self.total_y_internal = 0
        self.total_z_internal = 0

    def connect_sensors(self):
        for sensor in self.sensors:
            sensor.connect()

    def update_sensors(self):
        self.total_x_external = 0
        self.total_y_external = 0
        self.total_z_external = 0
        self.total_x_internal = 0
        self.total_y_internal = 0
        self.total_z_internal = 0

        for sensor in self.sensors:
            if sensor.active and sensor.read_data():
                if sensor.column == "external":
                    self.total_x_external += sensor.x
                    self.total_y_external += sensor.y
                    self.total_z_external += sensor.z
                elif sensor.column == "internal":
                    self.total_x_internal += sensor.x
                    self.total_y_internal += sensor.y
                    self.total_z_internal += sensor.z

    def close_sensors(self):
        for sensor in self.sensors:
            sensor.close()

class LogicHandler:
    def __init__(self):
        self.sensor_manager = SensorManager()

    def connect_to_sensors(self):
        self.sensor_manager.connect_sensors()

    def read_xyz_data(self):
        print(self.sensor_manager.total_x_external)
        self.sensor_manager.update_sensors()
        external_xyz = (self.sensor_manager.total_x_external, self.sensor_manager.total_y_external, self.sensor_manager.total_z_external)
        internal_xyz = (self.sensor_manager.total_x_internal, self.sensor_manager.total_y_internal, self.sensor_manager.total_z_internal)
        return external_xyz, internal_xyz

    def calculate_magnitude(self, xyz):
        return math.sqrt(xyz[0]**2 + xyz[1]**2 + xyz[2]**2)

    def close_sensors(self):
        self.sensor_manager.close_sensors()