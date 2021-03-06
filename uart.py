import sys
import serial
from serial.serialutil import SerialException
import serial.tools.list_ports

# sudo nano /etc/udev/rules.d/50-myusb.rules
# KERNEL=="ttyUSB[0-9]*",MODE="0666"
# KERNEL=="ttyACM[0-9]*",MODE="0666"


class UartSerialPort:
    __slots__ = ('port_name', 'port_timeout', 'sp', 'data')

    def __init__(self, port_name, port_timeout):
        self.list_port()
        try:
            self.sp = serial.Serial(
                port=port_name,
                baudrate=300,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=port_timeout
            )
        except SerialException as e:
            print(e)
            self.sp = None
            sys.exit()

        self.data = ''

    def __str__(self):
        return f'Port {self.sp.port} open' if self.sp else 'Port not opened or port no available'

    def write(self, data):
        try:
            return self.sp.write(data)
        except AttributeError:
            return False

    def inWait(self):
        return self.sp.inWaiting()

    def read(self, count):
        try:
            if count:
                return self.sp.read(count)
            else:
                return self.sp.read()
        except AttributeError:
            return False

    def readall(self):
        try:
            return self.sp.readall()
        except AttributeError:
            return False

    @staticmethod
    def list_port():
        ports = [port for port in serial.tools.list_ports.comports()]
        print(f'{" Default ports ":=^72}')
        for port in ports:
            print(f'{port}')
        print(f'{"":=^72}', '\n')

#   =========== From CSD terminal settings ================

    def CSD_send(self, string):
        send_string = bytearray(string, encoding='ascii')
        self.sp.write(send_string)
        print(f'Send command: {send_string.decode()}')
        self.data = self.CSD_read()
        return self.data

    def CSD_read(self):
        self.data = self.sp.readall()
        if 'OK' in self.data.decode():
            return 'OK'
        elif 'CONNECT' in self.data.decode():
            return 'Connect OK (9600)\n'
        elif 'BUSY' in self.data.decode():
            return 'BUSY\n'
        return 'ERROR\n'

    def set_time(self, val):
        self.sp.timeout = val
        return

    def clear(self):
        self.sp.flushInput()
        self.sp.flushOutput()
