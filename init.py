from smartcard import *
from smartcard.util import toHexString
from smartcard.System import readers

r = readers()
print(r[0])
connection = r[0].createConnection()
connection.connect()
AID = [0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]
SELECT = [0x00, 0xA4, 0x04, 0x00]

COLORS = {"red": "\033[91m", "green": "\n\033[92m",
          "yellow": "\033[93m", "blue": "\033[94m", "white": "\033[97m"}


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


def disconnectPIN():
    data = getDATA(0xA2, 0x01)
    if (data == [0]):
        print("Something went wrong: still connected with PIN")
    else:
        print("PIN disconnected")


def changePIN(pin):
    hex_pin = [ord(x) for x in pin]
    apdu = [0x80, 0xA3, 0x00, 0x00] + [len(hex_pin)] + hex_pin
    sendAPDU(apdu)
    connectPIN(pin)


print("\n%s----------- Selecting AID -----------" % COLORS["white"])
select()

print("\n%s------------ Disconnecting PIN -----------" % COLORS["red"])
disconnectPIN()

print("\n%s------------ Running INS 00 -----------" % COLORS["blue"])
getDATA(0x00, 0x0C)

print("\n%s----------- Running INS CA -----------" % COLORS["blue"])
getDATA(0xCA, 0x05)

print("\n%s----------- Connecting with PIN -----------" % COLORS["green"])
connectPIN("secret")

print("\n%s----------- Running INS CA -----------" % COLORS["blue"])
getDATA(0xCA, 0x05)

print("\n%s----------- Disconnecting PIN -----------" % COLORS["red"])
disconnectPIN()

print("\n%s----------- Running INS CA -----------" % COLORS["blue"])
getDATA(0xCA, 0x05)

print("\n%s----------- Changing PIN -----------" % COLORS["yellow"])
changePIN("salut!")

print("\n%s----------- Disconnecting PIN -----------" % COLORS["red"])
disconnectPIN()

print("\n%s----------- Connecting with PIN -----------" % COLORS["green"])
connectPIN("secret")

print("\n%s----------- Connecting with PIN -----------" % COLORS["green"])
connectPIN("salut!")
