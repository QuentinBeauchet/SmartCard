import rsa
from smartcard import *
from smartcard.util import toHexString
from smartcard.System import readers

from Colors import *


class APDU:
    def __init__(self):
        r = readers()
        print("%sConnected to %s\n" % (white, r[0]))
        self.connection = r[0].createConnection()
        self.connection.connect()

    def sendAPDU(self, apdu, log=False):
        hex_string = toHexString(apdu).replace(" ", "")
        msg = f"Sending APDU: {hex_string}"
        delimiter = "-" * min(len(msg), 100)

        data, sw1, sw2 = self.connection.transmit(apdu)

        if log:
            print("%s%s%s\n%s\nResponse: %x %x\nData: %s\n%s%s" %
                  (dim, light_grey, delimiter, msg, sw1, sw2, data, delimiter, reset))

        return (data, sw1, sw2)

    def selectAID(self, AID=[0xA0, 0x00, 0x00, 0x00, 0x62, 0x03, 0x01, 0x0C, 0x06, 0x01, 0x02]):
        apdu = [0x00, 0xA4, 0x04, 0x00] + [len(AID)] + AID
        _, sw1, sw2 = self.sendAPDU(apdu)
        if self.checkResultCode(sw1, sw2) == 0:
            print("Successfully selected AID")
        else:
            print("Something went wrong when selecting AID")

    def checkResultCode(self, sw1, sw2):
        if sw1 == 0x90 and sw2 == 0x00:  # Success
            return 0
        if sw1 == 0x61:  # sw2 bytes are avalaible to receive
            return sw2
        if sw1 == 0x69 and sw2 == 0x82:  # Not connected with PIN
            return -1
        if sw1 == 0x69 and sw2 == 0x83:  # Succesfully changed the PIN
            return -2
        if sw1 == 0x6f and sw2 == 0x00:  # Error system on the card.
            return -3

    def sendData(self, ins, data, log=False):
        hex_data = [ord(x) for x in data]
        apdu = [0x80, ins, 0x00, 0x00] + [len(hex_data)] + hex_data
        return self.sendAPDU(apdu, log)

    def sendEmptyInstruction(self, ins, log=False):
        return self.sendData(ins, "", log)

    def receiveData(self, ins, len, log=False):
        apdu = [0x80, ins, 0x00, 0x00, len]
        return self.sendAPDU(apdu, log)

    def dataToString(self, data):
        return "".join([chr(x) for x in data])


class CustomAPDU(APDU):
    def __init__(self, log=False):
        super().__init__()
        self.log = log
        self.selectAID()
        self.disconnectPIN()

    def getInfos(self):
        data, sw1, sw2 = self.receiveData(0x00, 0x2B, self.log)
        if self.checkResultCode(sw1, sw2) == -1:
            print("%sNot connected with PIN" % red)
        else:
            print("%s%s" % (blue, self.dataToString(data)))

    def connectPIN(self, pin):
        _, sw1, sw2 = self.sendData(0XA0, pin, self.log)
        if self.checkResultCode(sw1, sw2) == 0:
            print("%sSuccessfully connected using PIN" % green)
        elif self.checkResultCode(sw1, sw2) == -1:
            print("%sWrong PIN" % red)
        else:
            print("%sThe PIN needs to be 6 characters long" % red)

    def disconnectPIN(self):
        _, sw1, sw2 = self.sendEmptyInstruction(0XA1, self.log)
        if self.checkResultCode(sw1, sw2) == -1:
            print("%sSuccessfully disconnected the PIN" % green)
        else:
            print("%sSomething went wrong while trying to disconnect the PIN" % red)

    def changePIN(self, pin):
        if len(pin) != 6:
            print("%sThe PIN needs to be 6 characters long" % red)
        else:
            _, sw1, sw2 = self.sendData(0XA2, pin, self.log)
            if self.checkResultCode(sw1, sw2) == -1:
                print("%sNot connected with PIN" % red)
            elif self.checkResultCode(sw1, sw2) == -2:
                print("%sSuccessfully changed the PIN and disconnected" % green)
            else:
                print("%sSomething went wrong while trying to change the PIN" % red)

    def generateRSAKeyPair(self):
        _, sw1, sw2 = self.sendEmptyInstruction(0xB0, self.log)
        if self.checkResultCode(sw1, sw2) == 0:
            print("%sSuccessfully generated a new RSA KeyPair" % green)
        elif self.checkResultCode(sw1, sw2) == -1:
            print("%sNot connected with PIN" % red)
        else:
            print(
                "%sSomething went wrong while trying to generated a new RSA KeyPair" % red)

    def getRSAPublicKey(self):
        data, sw1, sw2 = self.receiveData(0xB1, 0x47, self.log)
        if self.checkResultCode(sw1, sw2) == 0:
            len_exp = int.from_bytes(data[:2], "big")
            offset = 2
            exp = int.from_bytes(data[offset:offset + len_exp], "big")
            offset += len_exp
            len_mod = int.from_bytes(data[offset:offset + 2], "big")
            offset += 2
            mod = int.from_bytes(data[offset:offset + len_mod], "big")

            self.publicKey = rsa.PublicKey(mod, exp)

            print("%s%s" %
                  (green, self.publicKey.save_pkcs1().decode("utf-8")), end="")
        elif self.checkResultCode(sw1, sw2) == -1:
            print("%sNot connected with PIN" % red)
        else:
            print(
                "%sSomething went wrong while trying to receive the RSA Public Key" % red)

    def signMessageUsingRSA(self, message):
        _, sw1, sw2 = self.sendData(0xB2, message, self.log)
        if self.checkResultCode(sw1, sw2) == -1:
            print("%sNot connected with PIN" % red)
        elif self.checkResultCode(sw1, sw2) == -3:
            print("%sThe message needs to be under 127 characters" % red)
        else:
            data, sw1_2, sw2_2 = self.receiveData(0xB3, sw2, self.log)
            if self.checkResultCode(sw1_2, sw2_2) != 0:
                print(
                    "%sSomething went wrong while trying to receive the RSA Signature" % red)
                return
            self.signature = data
            print("%sReceived signature: %s\n" %
                  (green, self.dataToString(self.signature)))

    def verifyRSASignature(self, message):
        try:
            rsa.verify(bytes(message, "utf-8").ljust(127, b'\x00'),
                       self.signature, self.publicKey)
            print("%sSignature is valid" % green)
        except:
            print("%sSignature is invalid." % red)

    def testAPDU(self):
        self.connectPIN("secret")

        self.getInfos()

        self.disconnectPIN()

        self.getInfos()

        self.connectPIN("secret")

        self.changePIN("coucou")

        self.getInfos()

        self.connectPIN("coucou")

        self.getInfos()

        self.generateRSAKeyPair()

        self.getRSAPublicKey()

        self.signMessageUsingRSA("salut")

        self.verifyRSASignature("salut45")

        self.verifyRSASignature("salut")


#app = CustomAPDU()
# app.testAPDU()
