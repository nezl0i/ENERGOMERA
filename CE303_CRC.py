import binascii
import sys
from sys import platform
from datetime import datetime
from time import sleep
from uart import UartSerialPort

serial = UartSerialPort('COM12', 1.7)

if platform.startswith('win'):
    from colors import WinColors
    c = WinColors()
else:
    from colors import Colors
    c = Colors()


def repeat(func):
    def wrapper_repeat(*args, **kwargs):
        for _ in range(3):
            current_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S.%f')
            check, get_hex, tmp = func(*args, **kwargs)
            print(f'[{current_time}] :{c.BLUE} >>', get_hex, c.END)
            if check:
                print(f'[{current_time}] :{c.FAIL} <<', tmp, c.END)
                return check, get_hex, tmp
            sleep(1)
        print(f'{c.WARNING}Нет ответа от устройства.{c.END}')
        sys.exit()
    return wrapper_repeat


class CE30X:

    def __init__(self, event):
        self.event = event

    def CE303CRC(self, code_string):
        """
        :param code_string: as '52 31 02 54 49 4D 45 5F 28 29 03'
        :return: _CRC
        """
        _CRC = 0
        bit = 0x80 if self.event else 0
        for i in map(lambda x: int(x, 16), code_string.split()[1:]):
            if bin(i).count('1') % 2 == 0:
                _CRC += i
            else:
                _CRC += i + bit
        return format(_CRC & 0x7F, '02X')

    @repeat
    def exchange(self, command, count):
        transfer = bytearray.fromhex(command)
        print_line = ' '.join(map(lambda x: format(x, '02x'), transfer))
        serial.write(transfer)
        buffer = serial.read(count)
        while buffer:
            if len(buffer) == count:
                return True, print_line, buffer.hex(' ', -1)
            break
        return False, print_line, buffer.hex(' ', -1)

    """
    Закодировать пакет
    
     - '\x01'
     - '\x02'
     - '\x03'
     - '\x06'

    """

    def CE303HexPackage(self, crc_byte=True, *args):
        hex_array = list()
        for item in args:
            for i in item:
                binary = format(int(format(ord(i), '02X'), 16), 'b')
                if self.event:
                    if binary.count('1') % 2 != 0:
                        hex_array.append(format(int(binary, 2) + 0x80, '02X'))
                        continue
                hex_array.append(format(int(binary, 2), '02X'))
        tmp_package = ' '.join(hex_array)
        crc = self.CE303CRC(tmp_package)
        if crc_byte:
            return f'{tmp_package} {crc}'
        return f'{tmp_package}'

    """
    Раскодировать пакет
    R1TIME_()
    """

    def CE303ASCIIPackage(self, package):
        ascii_string = str()
        if self.event:
            for i in list(package.split()):
                if int(i, 16) > 0x7F:
                    tmp = chr(int(i, 16) - 0x80)
                else:
                    tmp = chr(int(i, 16))
                ascii_string += tmp
        else:
            try:
                ascii_string = binascii.unhexlify(package.replace(' ', '')).decode()
            except UnicodeDecodeError:
                return "Ошибка в режиме проверки контроля четности"
        return ascii_string
