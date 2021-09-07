import codecs
import config as cfg
from prettytable import PrettyTable
import json


x = PrettyTable()
_PWD = codecs.encode(cfg.PASSWORD.encode(), 'hex')
_APN = codecs.encode(cfg.APN.encode(), 'hex')
_IP = codecs.encode(cfg.IP.encode(), 'hex')
_PORT = format(cfg.PORT, 'X')
_MODE = format(cfg.MODE, '02X')
if _MODE == '01' or _MODE == '03':
    SMS = '01%s0228012C1723%s001726%s001727%s1722%s1703001A' % \
          (_PWD.decode(), _APN.decode(), _IP.decode(), _PORT, _MODE)
else:
    SMS = '01%s0228012C1723%s001727%s1722%s1703001A' % \
          (_PWD.decode(), _APN.decode(), _PORT, _MODE)


_CREATE_TMP = json.loads(cfg.create_sms_mode())
_CREATE_TMP.append(SMS)


x.field_names = ['Mode', 'Password', 'APN', 'IP', 'Port', 'SMS']
x.add_row(_CREATE_TMP)
print(x)
