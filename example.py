from CE303_CRC import CE30X
from collections import namedtuple
from time import sleep


ce = CE30X(True)  # False - без проверки четности, True - проверяем четность
PASSWD = '777777'
ID = ''
auth = ['/?{0}!\r\n', '\x06051\r\n']  # /?! CRLF ; \x06 051 CRLF
end = '01 42 30 03 75'  # \x01 B0 \x03

# "Р" – команда пароля
# "W" – команда записи
# "R" – команда чтения
# "В" – команда выхода (прерывания)

stat_param = ('P0', 'P1', 'R1', 'W1', 'B0')

device_param = (
    'MODEL', 'COMPL', 'CPU_A', 'CPU_B', 'CPU_C',
    'CPI_A', 'CPI_B', 'CPI_C', 'CER_A', 'CER_B',
    'CER_C', 'VFEEA', 'VFEEB', 'VFEEC', 'QUANT',
    'TEMPN', 'TEMPR', 'SNUMB', 'CONDI', 'TIME_'
)


def COMMAND(param='', value=''):
    return '{}({})'.format(param, value)


if __name__ == "__main__":
    marks = namedtuple('MARKS', device_param)(*device_param)
    stat = namedtuple('STAT', stat_param)(*stat_param)

    command_line = COMMAND(param=marks.CPI_A, value='')

    encode_package = ce.CE303HexPackage(True,  # True-считаем CRC, False-не считаем
                                        # auth[0].format('')
                                        '\x01',
                                        stat.R1,
                                        '\x02',
                                        command_line,
                                        '\x03'
                                        )
    encode_package_2 = ce.CE303HexPackage(False, auth[1])  # True-считаем CRC, False-не считаем

    decode_package = ce.CE303ASCIIPackage(encode_package[:-3])  #
    crc_byte = ce.CE303CRC(encode_package[:-3])  #

    print("Закодированный пакет : ", encode_package)
    print("CRC : ", crc_byte)
    print("Раскодированный пакет : ", decode_package)
    print('\n')

    ce.exchange(encode_package, 15)
    sleep(1)
    ce.exchange(encode_package_2, 3)
