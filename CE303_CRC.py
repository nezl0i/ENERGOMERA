def CE303CRC(string, check=False) -> str:
    """

    :param string: as '52 31 02 54 49 4D 45 5F 28 29 03'
    :param check: True - if parity check; else False
    :return: _CRC
    """
    _CRC = 0
    bit = 0x80 if check else 0
    for i in map(lambda x: int(x, 16), string.split()):
        if bin(i).count('1') % 2 == 0:
            _CRC += i
        else:
            _CRC += i + bit
    return format(_CRC & 0xFF, '02X')


# array2 = '52 31 02 54 49 4D 45 5F 28 29 03'
# print(CE303CRC(array2, False))


def bin_encode(arg, mode):
    if mode == 'int':
        return format(int(format(int(arg), '02X'), 16), 'b')
    elif mode == 'ord':
        return format(int(format(ord(arg), '02X'), 16), 'b')


def hex_encode(arg, mode):
    if mode:
        return format(int(arg, 2) + 0x80, '02X')
    else:
        return format(int(arg, 2), '02X')


"""
Закодировать пакет
"""


def CE303HexPackage(mode, arg_string,  checkeven=False):
    concat_string = f'{mode}2{arg_string}3'
    hex_array = list()
    for i in concat_string:
        if i == '2' or i == '3':
            bin_string = bin_encode(i, 'int')
        else:
            bin_string = bin_encode(i, 'ord')
        if checkeven:
            if bin_string.count('1') % 2 != 0:
                hex_array.append(hex_encode(bin_string, True))
            else:
                hex_array.append(hex_encode(bin_string, False))
        else:
            hex_array.append(hex_encode(bin_string, False))
    return ' '.join(hex_array)


"""
Раскодировать пакет
"""


def CE303ASCIIPackage(package, mode):
    ascii_string = str()
    for i in list(package.split()):
        if mode:
            if int(i, 16) > 0x7F:
                tmp = chr(int(i, 16) - 0x80)
            else:
                tmp = chr(int(i, 16))
        else:
            tmp = chr(int(i, 16))
        ascii_string += tmp
    return ascii_string


print("Закодированный пакет : ", CE303HexPackage('R1', 'TIME_()', True))
print("CRC : ", CE303CRC(CE303HexPackage('R1', 'TIME_()', True), True))
print("Раскодированный пакет : ", CE303ASCIIPackage(CE303HexPackage('R1', 'TIME_()', True), True))
