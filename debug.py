import rsa
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
          "yellow": "\033[93m", "blue": "\033[94m", "purple": "\033[95m", "white": "\033[97m"}


def listToString(list):
    return "".join([chr(x) for x in list])


def sendAPDU(apdu, code=False):
    print("\nSending APDU: %s" % toHexString(apdu).replace(" ", ""))
    data, sw1, sw2 = connection.transmit(apdu)
    print("%x %x" % (sw1, sw2))
    return (data, sw1, sw2) if code else data


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


def getPublicKey():
    data = getDATA(0xB0, 0x00)

    data = getDATA(0xB1, 0x47)

    len_exp = int.from_bytes(data[:2], "big")
    offset = 2
    exp = int.from_bytes(data[offset:offset + len_exp], "big")
    offset += len_exp
    len_mod = int.from_bytes(data[offset:offset + 2], "big")
    offset += 2
    mod = int.from_bytes(data[offset:offset + len_mod], "big")

    return rsa.PublicKey(mod, exp)


def signMessage(message):
    hex_msg = [ord(x) for x in message]
    sendAPDU([0x80, 0xB2, 0x00, 0x00] + [len(hex_msg)] + hex_msg)
    return getDATA(0xB3, 0x40)


def verifyMessage(message, signature, publicKey):
    try:
        rsa.verify(bytes(message, "utf-8").ljust(127,
                   b'\x00'), signature, publicKey)
        print("Signature is valid.")
    except:
        print("Signature is invalid.")


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

print("\n%s----------- Running INS CA -----------" % COLORS["blue"])
getDATA(0xCA, 0x05)

print("\n%s----------- Disconnecting PIN -----------" % COLORS["red"])
disconnectPIN()

print("\n%s----------- Connecting with PIN -----------" % COLORS["green"])
connectPIN("secret")

print("\n%s----------- Connecting with PIN -----------" % COLORS["green"])
connectPIN("salut!")

print("\n%s----------- Fetching RSA PubKey -----------" % COLORS["purple"])
publicKey = getPublicKey()

print("\n%s----------- Sign Message -----------" % COLORS["purple"])
signature = signMessage("salut")

print("\n%s----------- Verify signature -----------" % COLORS["purple"])
verifyMessage("salut", signature, publicKey)

print("\n%s----------- Verify signature -----------" % COLORS["purple"])
verifyMessage("marchera pas", signature, publicKey)
