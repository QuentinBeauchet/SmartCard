from APDU import CustomAPDU
from Colors import *


class JavaCardCLI:
    def __init__(self, log=False):
        self.APDU = CustomAPDU(log)
        self.myMainLoop()

    def myInput(self):
        return (input("\n%s$ " % white).split())

    def myMainLoop(self):
        print("\n%sCmd: 'help' for more informations" % blue)
        try:
            while (True):
                cmd = self.myInput()
                if (cmd == []):
                    pass
                elif cmd[0] == "login":
                    self.validateCmd(cmd, self.APDU.connectPIN)
                elif cmd[0] == "changepin":
                    self.validateCmd(cmd, self.APDU.changePIN)
                elif cmd[0] == "logout":
                    self.APDU.disconnectPIN()
                elif cmd[0] == "genkeys":
                    self.APDU.generateRSAKeyPair()
                elif cmd[0] == "pubkey":
                    self.APDU.getRSAPublicKey()
                elif cmd[0] == "sign":
                    self.validateCmd(cmd, self.APDU.signMessageUsingRSA)
                elif cmd[0] == "verify":
                    self.validateCmd(cmd, self.APDU.verifyRSASignature)
                elif cmd[0] == "info":
                    self.APDU.getInfos()
                elif cmd[0] == "help":
                    self.help()
                elif cmd[0] == "exit":
                    print()
                    return
                else:
                    print("\n%sUnknown command" % red)
        except KeyboardInterrupt:
            print()
            return

    def validateCmd(self, cmd, callback):
        if len(cmd) != 2:
            print("\n%sWrong number of arguments" % red)
            return
        callback(cmd[1])

    def info(self):
        self.APDU.getInfos()

    def help(self):
        print("%sCommand List :" % white)
        print("%s- login \"...\"%s -> connect with a PIN to the card" %
              (green, light_grey))
        print("%s- logout%s  -> disconnect the card" %
              (red, light_grey))
        print("%s- changepin \"...\"%s  -> change the PIN" %
              (yellow, light_grey))
        print("%s- genkeys%s  -> generate a RSA key pair" %
              (green, light_grey))
        print("%s- pubkey%s  -> get the public key from the card" %
              (cyan, light_grey))
        print("%s- sign \"...\"%s  -> get the signature of a message" %
              (purple, light_grey))
        print("%s- verify \"...\"%s  -> check if the message in argument is matching" %
              (grey, light_grey))
        print("%s- info%s  -> get card infos" %
              (blue, light_grey))


if __name__ == '__main__':
    JavaCardCLI()
