import binascii


class CE30X:

    def __init__(self, event):

        self.event = event

        if self.event:
            self.ascii = ['82', '03']
        else:
            self.ascii = ['02', '03']

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
        return format(_CRC & 0xFF, '02X')

    # @staticmethod
    # def bin_encode(arg, mode):
    #     if mode == 'int':
    #         return format(int(format(int(arg), '02X'), 16), 'b')
    #     elif mode == 'ord':
    #         return format(int(format(ord(arg), '02X'), 16), 'b')

    # @staticmethod
    # def hex_encode(arg, mode):
    #     if mode:
    #         return format(int(arg, 2) + 0x80, '02X')
    #     else:
    #         return format(int(arg, 2), '02X')

    """
    Закодировать пакет
    """

    def CE303HexPackage(self, *args):
        hex_array = list()
        for num, item in enumerate(args):
            for i in item:
                binary = format(int(format(ord(i), '02X'), 16), 'b')
                if self.event:
                    if binary.count('1') % 2 != 0:
                        hex_array.append(format(int(binary, 2) + 0x80, '02X'))
                    else:
                        hex_array.append(format(int(binary, 2), '02X'))
                else:
                    hex_array.append(format(int(binary, 2), '02X'))

            hex_array.append(self.ascii[num])

        hex_array.insert(0, '01')
        tmp_package = ' '.join(hex_array)
        crc = self.CE303CRC(tmp_package)
        return f'{tmp_package} {crc}'

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


if __name__ == "__main__":

    ce = CE30X(True)

    encode_package = ce.CE303HexPackage('R1', 'TIME_()')  # D2 B1 82 D4 C9 4D C5 5F 28 A9 03
    decode_package = ce.CE303ASCIIPackage(encode_package[:-3])  # R1TIME_()
    crc_byte = ce.CE303CRC(encode_package[:-3])  # E7

    print("Закодированный пакет : ", encode_package)
    print("CRC : ", crc_byte)
    print("Раскодированный пакет : ", decode_package)
