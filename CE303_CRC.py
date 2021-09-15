import binascii


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
        for i in map(lambda x: int(x, 16), code_string.split()):
            if bin(i).count('1') % 2 == 0:
                _CRC += i
            else:
                _CRC += i + bit
        return format(_CRC & 0xFF, '02X')

    @staticmethod
    def bin_encode(arg, mode):
        if mode == 'int':
            return format(int(format(int(arg), '02X'), 16), 'b')
        elif mode == 'ord':
            return format(int(format(ord(arg), '02X'), 16), 'b')

    @staticmethod
    def hex_encode(arg, mode):
        if mode:
            return format(int(arg, 2) + 0x80, '02X')
        else:
            return format(int(arg, 2), '02X')

    """
    Закодировать пакет
    """

    def CE303HexPackage(self, mode, arg_string):
        """

        :param mode: R1 или W1
        :param arg_string: Параметры
        :return:
        """
        concat_string = f'{mode}2{arg_string}3'
        hex_array = list()
        for i in concat_string:
            if i == '2' or i == '3':
                bin_string = self.bin_encode(i, 'int')
            else:
                bin_string = self.bin_encode(i, 'ord')
            if self.event:
                if bin_string.count('1') % 2 != 0:
                    hex_array.append(self.hex_encode(bin_string, True))
                else:
                    hex_array.append(self.hex_encode(bin_string, False))
            else:
                hex_array.append(self.hex_encode(bin_string, False))
        return ' '.join(hex_array)

    """
    Раскодировать пакет
    """

    def CE303ASCIIPackage(self, package):
        """

        :param package: Параметры
        :return:
        """
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


if __name__ == "__main__":

    ce = CE30X(True)

    encode_package = ce.CE303HexPackage('R1', 'TIME_()')  # D2 B1 82 D4 C9 4D C5 5F 28 A9 03
    decode_package = ce.CE303ASCIIPackage(encode_package)  # R1TIME_()
    crc_byte = ce.CE303CRC(encode_package)  # E7

    print("Закодированный пакет : ", encode_package)
    print("CRC : ", crc_byte)
    print("Раскодированный пакет : ", decode_package)
