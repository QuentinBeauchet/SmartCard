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
    print("\nSending APDU: %s" % toHexString(apdu).replace(" ", ""))
    data, sw1, sw2 = connection.transmit(apdu)
    print("%x %x" % (sw1, sw2))
    return data


def select():
    apdu = SELECT + [len(AID)] + AID
    data = sendAPDU(apdu)
    print('data:', data)


def getDATA(ins, length):
    apdu = [0x80, ins, 0x00, 0x00, length]
    data = sendAPDU(apdu)
    print("data:", [hex(x) for x in data], " -> ", listToString(data))
    return data


def connectPIN(pin):
    hex_pin = [ord(x) for x in pin]
    apdu = [0x80, 0xA0, 0x00, 0x00] + [len(hex_pin)] + hex_pin
    sendAPDU(apdu)
    data = getDATA(0xA1, 0x01)
    if (data == [0]):
        print("Connected using the PIN")
    else:
        print("Wrong PIN")


print("\n----------- Selecting AID -----------")
select()

print("\n----------- Running INS 00 -----------")
getDATA(0x00, 0x0C)

print("\n----------- Running INS CA -----------")
getDATA(0xCA, 0x05)

print("\n----------- Connecting with PIN -----------")
connectPIN("secret")
