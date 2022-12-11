import debug
COLORS = {"red": "\033[91m", "green": "\n\033[92m",
          "yellow": "\033[93m", "blue": "\033[94m", "purple": "\033[95m", "white": "\033[97m"}

class pythonCli:
    def __init__(self):
        self.connected = False
        debug.disconnectPIN()
        self.myMainLoop()
    
    def myInput(self):
        return (input("\n%s$ "% COLORS["white"]).split())
    
    def myMainLoop(self):
        print("\n%sCmd: 'help' for more informations" % COLORS["blue"])
        key = ""
        signature = ""
        while(True):                
            cmd = self.myInput()
            if cmd[0] == "login":
                self.pinConnection()
            elif cmd[0] == "changepin":
                self.changePin(cmd)
            elif cmd[0] == "help":
                self.help()
            elif cmd[0] == "logout":
                debug.disconnectPIN()
                self.connected = False
            elif cmd[0] == "key":
                key = debug.getPublicKey()
                print("\n%skey has been generated"% COLORS["green"])
            elif cmd[0] == "sign":
                signature = self.sign(cmd)
            elif cmd[0] == "info":
                self.info()
            elif cmd[0] == "verify":
                self.verify(cmd, key, signature)
            elif cmd[0] == "exit":
                return
            else:
                print("\n%sUnknown command"% COLORS["red"])

    def changePin(self, cmd):
        if len(cmd) >= 2 and debug.changePIN(cmd[1]) and self.connected:
            print("\n%spin has changed"% COLORS["green"])
        else :
            print("\n%soops something went wrong"% COLORS["red"])

    def sign(self, cmd):
        if len(cmd) < 2 and not self.connected:
            print("\n%sWrong number of arguments or not connected to the card"% COLORS["red"])
            return
        msg = (" ".join(cmd)).split('"')[1]
        return debug.signMessage(msg)
    
    def verify(self, cmd , key, signature):
        if key == "" or signature == "":
            print("\n%sSignature or key missing"% COLORS["red"])
        elif len(cmd) <2:
            print("\n%sWrong number of arguments"% COLORS["red"])
        elif not self.connected:
            print("\n%sNot connected to the card"% COLORS["red"])
        else:
            msg = (" ".join(cmd)).split('"')[1]
            debug.verifyMessage(msg, signature, key)

    def pinConnection(self):
        print("\n%sPlease enter your pin :"% COLORS["blue"])
        if debug.connectPIN(self.myInput()[0]):
            print("\n%sConnected" % COLORS["green"])
            self.connected = True
        else:
            print("\n%sNot connected" % COLORS["red"])

    def info(self):
        debug.getDATA(0xCA, 0x05)

    def help(self):
        print("%sCommand List :" % COLORS["green"])
        print("%s\t- login -> connect with a pin to the card" % COLORS["blue"])
        print("%s\t- logout  -> disconnect the card" % COLORS["blue"])
        print("%s\t- info  -> get card infos" % COLORS["blue"])
        print("%s\t- changepin \"...\"  -> change the pin (need to be connected to the card) " % COLORS["blue"])
        print("%s\t- key  -> generate a public key" % COLORS["blue"])
        print("%s\t- sign \"...\"  -> get the signature of a message (need to be connected to the card) " % COLORS["blue"])
        print("%s\t- verify \"...\"  -> check if the message in argument is matching (need to be connected to the card) " % COLORS["blue"])




print(COLORS["white"])
pythonCli()