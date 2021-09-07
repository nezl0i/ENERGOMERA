
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


array2 = '52 31 02 54 49 4D 45 5F 28 29 03'
print(CE303CRC(array2, False))
