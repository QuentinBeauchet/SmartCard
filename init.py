from smartcard import *
from smartcard.util import toHexString
from smartcard.System import readers

r = readers()
print(r[0])
connection = r[0].createConnection()
connection.connect()
AID = [0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]
SELECT = [0x00, 0xA4, 0x04, 0x00]


def listToString(list):
    return "".join([chr(x) for x in list])


def sendAPDU(apdu):
    print("Sending APDU: %s" % toHexString(apdu).replace(" ", ""))
    data, sw1, sw2 = connection.transmit(apdu)
    print("%x %x" % (sw1, sw2))
    print('data:', data)
    return data


def select():
    apdu = SELECT + [len(AID)] + AID
    sendAPDU(apdu)


def getDATA(ins):
    apdu = [0x80, 0xCA, 0x00, ins, 0x0C]
    data = sendAPDU(apdu)
    print(listToString(data))


select()
getDATA(0x40)
