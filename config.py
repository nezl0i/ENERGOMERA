import json


PASSWORD = '12345678'
APN = 'kuben93.ug.kvk'
IP = '10.168.24.146'  # Если настройка на клиента
PORT = 9100
MODE = 2  # 1 client, 2 server, 3 client + CSD, 4 server + CSD


def create_sms_mode():
    _TMP_MODE = None
    _TMP_IP = None
    if MODE == 1:
        _TMP_MODE = 'CLIENT'
        _TMP_IP = IP
    elif MODE == 2:
        _TMP_MODE = 'SERVER'
    elif MODE == 3:
        _TMP_MODE = 'CLIENT (With CSD)'
        _TMP_IP = IP
    elif MODE == 4:
        _TMP_MODE = 'SEVER (With CSD)'

    _TMP = [_TMP_MODE, PASSWORD, APN, _TMP_IP, PORT]

    return json.dumps(_TMP)
