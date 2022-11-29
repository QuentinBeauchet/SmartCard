from smartcard import *
from smartcard.util import toHexString
from smartcard.System import readers
from smartcard.CardConnection import CardConnection

r = readers()
print(r[0])
connection = r[0].createConnection()
connection.connect()
AID = [0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]
SELECT = [0x00, 0xA4, 0x04, 0x00]


def listToString(list):
    return "".join([chr(x) for x in list])


def select():
    apdu = SELECT + [len(AID)] + AID
    print("Sending APDU: %s" % toHexString(apdu).replace(" ", ""))
    data, sw1, sw2 = connection.transmit(apdu)
    print("%x %x" % (sw1, sw2))
    print('data:', data)


def getDATA(ins):
    apdu = [0x80, 0xCA, 0x00, ins, 0x0C]
    print("Sending APDU: %s" % toHexString(apdu).replace(" ", ""))
    data, sw1, sw2 = connection.transmit(apdu)
    print("status: %x %x" % (sw1, sw2))
    print('data:', data, listToString(data))


def sendCMD(cmd):
    print("Sending APDU: %s" % toHexString(cmd).replace(" ", ""))
    data, sw1, sw2 = connection.transmit(cmd)
    print("status: %x %x" % (sw1, sw2))
    print('data:', data, listToString(data))


select()
getDATA(0x40)
